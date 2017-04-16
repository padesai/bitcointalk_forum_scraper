from scrapy.linkextractors import LinkExtractor
import scrapy
import re
from hashlib import sha256
import traceback
import bitcoin_helper

class UserProfileSpider(scrapy.Spider):
    name = "user_profile_spider"
    start_urls = [
        # "https://bitcointalk.org/index.php?action=profile;u=10197",
        "https://bitcointalk.org/index.php?topic=1783218.0;all",
        #"https://bitcointalk.org/index.php?topic=1074337.380"
    ]
    allowed_domains = ["bitcointalk.org"]
    page = 0
    PRINT_LOGS = True

    def parse_user_profile(self, response):
        # Used to find Threads on a Board Page. Will navigate to next Board Page
        bitcoins = bitcoin_helper.collect_bitcoins(response.body)
        # print("LENGTH OF LIST: "+str(len(bitcoins)))
        if len(bitcoins)>0:
            user_id = response.css('.windowbg tr:nth-child(1) td:nth-child(2)::text').extract_first()
            yield {"user_id": user_id, "Profile URL": response.url, "bitcoin_addresses": bitcoins}

    def parse(self, response):
        list_users = response.css('.poster_info b a::attr(href)').extract()
        for href in list_users:
            yield scrapy.Request(href, callback=self.parse_user_profile)
