from scrapy.linkextractors import LinkExtractor
import scrapy
import re
import itertools
from bitcoin_helper import collect_bitcoins


# Run Program with 'scrapy runspider bitcoin_forum_scraper.py -o out.json -s DOWNLOAD_DELAY=1 --nolog'

class BitcoinSpider(scrapy.Spider):
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
        # Used to find Threads on a Board Page. Will navigate to next Board Page
        PRINT_LOGS = True

        # Navigate to each Thread on the Board Page
        for href in response.css('.leftimg+ td span a ::attr(href)').extract():
            if PRINT_LOGS: print("On Board {}, yielding thread {}".format(response.url, href))
            yield scrapy.Request(href, callback=self.parse_thread)

        # Navigate to the next Board Page
        next_page = response.css('.prevnext .navPages ::attr(href)').extract()
        if len(next_page) > 0:
            if PRINT_LOGS: print("On Board {}, yielding Board {}".format(response.url, next_page[-1]))
            yield scrapy.Request(next_page[-1], callback=self.parse)

    def parse_thread(self, response):
        # Used to search for Bitcoins on a Thread Page. Will navigate to next Thread Page
        PRINT_LOGS = True

        addresses = []
        for comment in itertools.chain(response.css('.windowbg').extract(), response.css('windowbg2').extract()):
            valid_addresses = collect_bitcoins(str.encode(comment))
            if len(valid_addresses) > 0:
                match = re.search(r'href=[\'"]?([^\'" >]+)', comment)
                if match:
                    addresses.append({"user_page": match.group(0)[6:], "posted_addresses": valid_addresses})

        if len(addresses) > 0:
            yield {"url": response.url, "addresses": addresses}

        # Outputs to the output file for each Thread Page with valid Bitcoins
        # valid_addresses = collect_bitcoins(response.body)
        # if len(valid_addresses) > 0:
        #    print("parse_thread: found {} on {}.".format(valid_addresses, response.url))
        #    yield {"url": response.url, "bitcoin_addresses": valid_addresses}

        # Navigate to the next page in the Thread
        next_page = response.css('.prevnext .navPages ::attr(href)').extract()
        if len(next_page) > 0:
            if PRINT_LOGS: print("On P {}, yielding P {}".format(response.url, next_page[-1]))
            yield scrapy.Request(next_page[-1], callback=self.parse_thread)

            # '.poster_info b a' is the css selector for a url to the poster's profile
