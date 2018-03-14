import multiprocessing

from scrapy import cmdline
import sys
reload(sys)
sys.setdefaultencoding('utf8')


cmdline.execute('scrapy crawl cnChinaCn'.split())
# cmdline.execute('scrapy crawl sbgg'.split())
# cmdline.execute('scrapy crawl zhaopin'.split())