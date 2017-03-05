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
        "https://bitcointalk.org/index.php?action=profile;u=648651"
    ]
    allowed_domains = ["bitcointalk.org"]
    page = 0

    def parse(self, response):
        # Used to find Threads on a Board Page. Will navigate to next Board Page
        bitcoins = bitcoin_helper.collect_bitcoins(response.body)
        # print("LENGTH OF LIST: "+str(len(bitcoins)))
        if len(bitcoins)>0:
            
            user_id = response.css('.windowbg tr:nth-child(1) td:nth-child(2)::text').extract_first()
            yield {"user_id": user_id, "bitcoin_addr":bitcoins[0]}

