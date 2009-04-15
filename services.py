import os.path
from urlparse import urlparse
from optparse import OptionParser
from extractor import BaseFeedExtractor, PlayListDownloader

class DailymotionExtractor(BaseFeedExtractor):
    """FLV extractor from a dailymotion Feed"""

    def flv_url_transform(self, flvurl):
        """Replace 80x60 with 320x240"""
        return flvurl.replace('80x60', '320x240')


class YoutubeExtractor(BaseFeedExtractor):
    """FLV extractor from a youtube Feed"""
    pass

# -- Services Mapper
# A service's name is actually the domain name 
# in lowercase minus the TLD, minus any subdomain 
# part.

def get_service_from_url(url):
    o = urlparse(url)
    hostname = o.hostname
    service = hostname.split('.')[-2]
    return service

map = {
        'dailymotion': DailymotionExtractor,        
        'youtube': YoutubeExtractor,        
}
