#!/usr/bin/env python
import sys
import os.path
import logging
from urlparse import urlparse, urljoin
import feedparser
from downloader import DownloadURLOpener

logging.basicConfig(level=logging.DEBUG, 
        format='%(asctime)s %(levelname)s %(message)s')

valid_chars = '-_/ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

class BaseFeedExtractor(object):
    """
    A Video Downloader that knows how to extract and download videos from a 
    MRSS feed.
    """

    def __init__(self):
        pass
    
    def get_page_url(self, baseurl, pagenum):
        """
        Generates a url of a feed from a baseurl and  page number
        (override this in your service BaseFeedExtractor if you want)
        A baseurl is a feed's url without the pagination part. 
        """
        return "%s/%s" % (baseurl.rstrip('/'), str(pagenum))

    def flv_url_locate(self, entry):
        """
        Where is the actual FLV in the parsed entry?
        (override this in your service BaseFeedExtractor if you want)
        """
        return entry['media_content'][1]['url']

    def flv_url_transform(self, flvurl):
        """
        if the flv in the mediarss feed isn't actually what we needed to
        download, transform it (implement this in your service
        BaseFeedExtractor) to tell the downloader which flv url to download.
        """
        return flvurl
    
    def title_to_filename(self, title):
        """Generates a good filename for a given video title"""
        new_title = ''.join(c for c in title if c in valid_chars)
        return '%s.flv' % new_title.replace(' ', '_').\
                replace('/', '_').replace('__', '_')

    def extract_videos(self, url):
        """
        Extracts videos flv urls and titles from a feed   
        and fills a dict
        """
        d = feedparser.parse(url)
        videos = [ {
                    'title': self.title_to_filename(e['title']), 
                    'url': self.flv_url_transform(self.flv_url_locate(e))
                    }
                    for e in d['entries']
                ]
        return videos

class PlayListDownloader(object):
    """
    Mass downloader for a playlist of feeds that are paginated.
    i.e. the feeds urls follow the same pattern which include a page parameter.
    Example:
    url1 = 'http://dailymotion.com/rss/playlist/[code]/1'
    url2 = 'http://dailymotion.com/rss/playlist/[code]/2'
    ...
    urln = 'http://dailymotion.com/rss/playlist/[code]/n'
    """

    def __init__(self, url, pages, worker):
        """
        A PlayListDownloader will fetch a playlist of feeds that are paginated
        given a base feed url, the number of pages, and a BaseFeedExtractor 
        class to be used to extract the vids.
        """
        self.play_list_url = url
        self.pages = pages
        self.worker = worker()

    def get_page_url(self, pagenum):
        return self.worker.get_page_url(self.play_list_url, pagenum)

    def _reporthook(self, blocks_read, block_size, total_size):
        if not blocks_read:
            print 'Connection opened'
            return
        if total_size < 0:
            # Unknown size
            print 'Read %d blocks' % blocks_read
        else:
            amount_read = blocks_read * block_size
            print 'Read %d blocks, or in bytes: %d/%d\033[A' % (blocks_read, 
                    amount_read, total_size)
        return

    def _download_flv(self, flv_url, local_filename):
        downloader = DownloadURLOpener()
        downloader.retrieve_resume(flv_url, local_filename, 
                reporthook=self._reporthook)

    def download(self, destination_dir):
        """
        Download with resume ability all the videos.
        """
        for p in range(1, self.pages):
            url = self.get_page_url(p)
            videos = self.worker.extract_videos(url)
            for video in videos:
                flv_url = video['url']
                filename = os.path.join(destination_dir, video['title'])
                logging.info('Downloading %s' % video['title'])
                self._download_flv(flv_url, filename)

    def genbash(self, destination_dir):
        """
        Generates a bash script using wget to download the videos. 
        Redirect this output to a file and use it.
        """
        print "#!/usr/bin/env sh"
        print ""
        for p in range(1, self.pages+1):
            url = self.get_page_url(p)
            print """# -- Videos in %s";""" % url
            videos = self.worker.extract_videos(url)
            for video in videos:
                flv_url = video['url']
                filename = os.path.join(destination_dir, video['title'])
                print """wget -c "%s" -O "%s";""" % (flv_url, filename)



