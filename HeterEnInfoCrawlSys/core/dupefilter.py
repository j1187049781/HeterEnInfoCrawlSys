import logging

from scrapy.utils.request import request_fingerprint
from scrapy_redis.dupefilter import RFPDupeFilter

from HeterEnInfoCrawlSys import settings
from HeterEnInfoCrawlSys.core.bloomFilterOnRedis import BloomFilter
from HeterEnInfoCrawlSys.settings import CLR_KEY

logger = logging.getLogger(__name__)


# TODO: Rename class to RedisDupeFilter.
class BloomDupeFilter(RFPDupeFilter):
    """Redis-based request duplicates filter.

    This class can also be used with default Scrapy's scheduler.

    """

    logger = logger

    def __init__(self, server, key, debug=False):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.

        """
        if (settings.SAME_KEY):
            key='allSpider:dupefiltter'
        self.bloomFilter = BloomFilter(server=server,key=key)
        self.debug = debug
        self.logdupes = True


    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)
        # This returns  true if already exists.
        if self.bloomFilter.isContains(fp):
            return True
        else:
            self.bloomFilter.insert(fp)

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        if CLR_KEY:
            self.clear()

    def clear(self):
        """Clears fingerprints data."""
        self.bloomFilter.clear()

