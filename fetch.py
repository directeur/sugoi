#!/usr/bin/env python
import os.path
from optparse import OptionParser
import services
from extractor import PlayListDownloader

def main():
    usage = "usage: %prog [params] arg1 arg2 %prog 1.0"
    oparser = OptionParser(usage=usage)
    oparser.add_option("-b", "--bash", action="store_true", dest="bash", 
            default=False)
    oparser.add_option("-d", "--dest", dest="dest", type="string", 
            help="the distination directory")

    oparser.add_option('-n', '--pages', dest='pages', type='int',
                      help="Number of RSS pages")
    oparser.set_default('dest', os.path.dirname(__file__))
    oparser.set_default('pages', 1)

    (options, args) = oparser.parse_args()

    url = args[0]
    service = services.get_service_from_url(url)

    PLD = PlayListDownloader(url, options.pages, services.map[service])

    if options.bash:
        PLD.genbash(options.dest)
    else:
        PLD.download(options.dest)


if __name__ == '__main__':
    main()
