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
    """Used to scrape all comments and the profile page of each user that commented
    """

    name = "bitcoin_forum"
    start_urls = [
        # 'http://bitcointalk.org',
        # 'https://bitcointalk.org/index.php?topic=423995.0'
        # 'https://bitcointalk.org/index.php?topic=20333.0',
        # 'https://bitcointalk.org/index.php?topic=1791378.0'
        'https://bitcointalk.org/index.php?board=1.0'
    ]
    allowed_domains = ["bitcointalk.org"]
    page = 0

    def parse(self, response):
        """Root funtion to scrape Comments and User Profiles containing valid Bitcoins from the bitcointalk.org forum.
        Navigates from a Board page to the next Board page, yielding each Thread in the board.
        """

        # Navigate to each Thread on the Board page
        for href in response.css('.leftimg+ td span a ::attr(href)').extract():
            logging.debug("Board {}, going to Thread {}".format(response.url, href))
            yield scrapy.Request(href, callback=self.parse_thread)

        # Navigate to the next Board Page
        next_page = response.css('.prevnext .navPages ::attr(href)').extract()
        if len(next_page) > 0:
            logging.debug("Board {}, going to Board {}".format(response.url, next_page[-1]))
            yield scrapy.Request(next_page[-1], callback=self.parse)

    def parse_thread(self, response):
        """Navigates from a Page in a Thread to the next Page in that Thread.
        Navigates from a Page in a Thread to each User that commented on this Page.
        Searches and scrapes valid Bitcoins from this Page.
        """

        # Navigate to every Commenter's Profile page
        list_users = response.css('.poster_info b a::attr(href)').extract()
        for href in list_users:
            logging.debug("Page {}, going to User {}".format(response.url, href))
            yield scrapy.Request(href, callback=self.parse_user_profile)

        # Search each comment for a valid Bitcoin address
        for comment in itertools.chain(response.css('.windowbg').extract(), response.css('windowbg2').extract()):
            valid_addresses = collect_bitcoins(str.encode(comment))
            if len(valid_addresses) > 0:
                logging.debug("Page {}, yielding a Comment".format(response.url))
                yield {"comment_url": response.url, "bitcoin_addresses": valid_addresses, "comment_text": comment}

        # Navigate to the next Page in the Thread
        next_page = response.css('.prevnext .navPages ::attr(href)').extract()
        if len(next_page) > 0:
            logging.debug("Page {}, going to Page {}".format(response.url, next_page[-1]))
            yield scrapy.Request(next_page[-1], callback=self.parse_thread)

    def parse_user_profile(self, response):
        """Searches and scrapes valid Bitcoins from a User's Profile page.
        """

        # Search for valid bitcoins
        bitcoins = collect_bitcoins(response.body)
        if len(bitcoins) > 0:
            user_id = response.css('.windowbg tr:nth-child(1) td:nth-child(2)::text').extract_first()
            logging.debug("User {}, yielding Bitcoins".format(response.url))
            yield {"user_id": user_id, "profile_url": response.url, "bitcoin_addresses": bitcoins}
