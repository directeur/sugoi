# -*- coding: utf-8 -*-
#inspired from http://repo.or.cz/w/gpodder.git?a=blob;f=src/gpodder/download.py

import urllib
import os.path
import os

class DownloadCancelledException(Exception): pass

class DownloadHTTPError(Exception):
    def __init__(self, url, error_code, error_message):
        self.url = url
        self.error_code = error_code
        self.error_message = error_message

class DownloadURLOpener(urllib.FancyURLopener):

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        """
        FancyURLopener by default does not raise an exception when
        there is some unknown HTTP error code. We want to override
        this and provide a function to log the error and raise an
        exception, so we don't download the HTTP error page here.
        """
        # The following two lines are copied from urllib.URLopener's
        # implementation of http_error_default
        void = fp.read()
        fp.close()
        raise DownloadHTTPError(url, errcode, errmsg)

    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        # The next line is taken from urllib's URLopener.open_http
        # method, at the end after the line "if errcode == 200:"
        return urllib.addinfourl(fp, headers, 'http:' + url)

    def retrieve_resume(self, url, filename, reporthook=None, data=None):
        """retrieve_resume(url) returns (filename, headers) for a local object
        or (tempfilename, headers) for a remote object.
        The filename argument is REQUIRED (no tempfile creation code here!)
        Additionally resumes a download if the local filename exists"""

        current_size = 0
        tfp = None
        if os.path.exists(filename):
            try:
                current_size = os.path.getsize(filename)
                tfp = open(filename, 'ab')
                #If the file exists, then only download the remainder
                self.addheader('Range', 'bytes=%s-' % (current_size))
            except:
                log('Cannot open file for resuming: %s', filename, sender=self, traceback=True)
                tfp = None
                current_size = 0

        if tfp is None:
            tfp = open(filename, 'wb')

        url = urllib.unwrap(urllib.toBytes(url))
        fp = self.open(url, data)
        headers = fp.info()
        result = filename, headers
        bs = 1024*8
        size = -1
        read = current_size
        blocknum = int(current_size/bs)
        if reporthook:
            if "content-length" in headers:
                size = int(headers["Content-Length"]) + current_size
            reporthook(blocknum, bs, size)
        while 1:
            block = fp.read(bs)
            if block == "":
                break
            read += len(block)
            tfp.write(block)
            blocknum += 1
            if reporthook:
                reporthook(blocknum, bs, size)
        fp.close()
        tfp.close()
        del fp
        del tfp

        # raise exception if actual size does not match content-length header
        if size >= 0 and read < size:
            raise urllib.ContentTooShortError("retrieval incomplete: got only %i out "
                                       "of %i bytes" % (read, size), result)

        return result


