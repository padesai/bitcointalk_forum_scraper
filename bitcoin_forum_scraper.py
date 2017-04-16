from scrapy.linkextractors import LinkExtractor
import scrapy
from scrapy.spiders import SitemapSpider
import itertools
import logging
from bitcoin_helper import collect_bitcoins
from comment_parser import parse_comment

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Run Program with 'scrapy runspider bitcoin_forum_scraper.py -o out.json -s DOWNLOAD_DELAY=1 --nolog'

class BitcoinSpider(SitemapSpider):
    """Used to scrape the entire bitcointalk.org forum. Will look for Bitcoin addresses in comments and user profiles"""
    name = "bitcoin_forum"

    sitemap_urls = ['https://bitcointalk.org/sitemap.php']
    sitemap_rules = [
        ('topic=', 'parse_page'),
        ('action=profile', 'parse_user_profile')
    ]
    allowed_domains = ["bitcointalk.org"]
    page = 0

    def parse_user_profile(self, response):
        """Searches and scrapes valid Bitcoins from a User's Profile page.
        """
        # Search for valid bitcoins
        bitcoins = collect_bitcoins(response.body)
        if len(bitcoins) > 0:
            user_id = response.css('.windowbg tr:nth-child(1) td:nth-child(2)::text').extract_first()
            logging.debug("User {}, yielding Bitcoins".format(response.url))
            yield {"user_id": user_id, "profile_url": response.url, "bitcoin_addresses": bitcoins}

    def parse_page(self, response):
        """Searches and scrapes valid Bitcoins from this Page.
        """
        # Search each comment for a valid Bitcoin address
        for comment in itertools.chain(response.css('.windowbg').extract(), response.css('windowbg2').extract()):
            valid_addresses = collect_bitcoins(str.encode(comment))
            if len(valid_addresses) > 0:
                logging.debug("Page {}, yielding Bitcoins".format(response.url))
                p = parse_comment(comment)

                comment = {"username": p["username"], "bitcoin_addresses": valid_addresses,
                           "profile_url": p["profile_url"], "date": p["date"], "comment": p["comment"],
                           "comment_url": response.url}
                yield comment
