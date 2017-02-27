from scrapy.linkextractors import LinkExtractor
import scrapy
import re
from hashlib import sha256
import traceback

# Run Program with 'scrapy runspider bitcoin_forum_scraper.py -o out.json -s DOWNLOAD_DELAY=1 --nolog'

digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


# takes in a string and returns all potential bitcoin addresses in a list
def find_bitcoin_addr(text):
    # Below regular expression should do the trick. Modified from the Bitcoin Transaction Analysis Graph Paper.
    # (https://arxiv.org/pdf/1502.01657.pdf)
    # We need to support multisig bitcoin addresses that have a 3 in front of them. https://en.bitcoin.it/wiki/Address
    match = re.findall(b"[13].[a-km-zA-HJ-NP-Z1-9]{26,33}", text)

    if match:
        return match
    else:
        return []


def decode_base58(bc, length):
    #print(bc)
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(str(char))
        # n = n * 58 + 10
    return n.to_bytes(length, 'big')


def check_bc(bc):
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]


def test_bitcoin_validity_func():
    print("Checking validity of some test bitcoin addresses...")
    print("Should be True, actually is " + str(check_bc('18vaZ4K62WiL6W2Qoj9AE1cerfCHRaUW4x')))


test_bitcoin_validity_func()


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

        # Outputs to the output file for each Thread Page with valid Bitcoins
        valid_addresses = collect_bitcoins(response.body)
        if len(valid_addresses) > 0:
            print("parse_thread: found {} on {}.".format(valid_addresses, response.url))
            yield {"url": response.url, "bitcoin_addresses": valid_addresses}

        # Navigate to the next page in the Thread
        next_page = response.css('.prevnext .navPages ::attr(href)').extract()
        if len(next_page) > 0:
            if PRINT_LOGS: print("On P {}, yielding P {}".format(response.url, next_page[-1]))
            yield scrapy.Request(next_page[-1], callback=self.parse_thread)

            # '.poster_info b a' is the css selector for a url to the poster's profile


def collect_bitcoins(body):
    # Given an HTML page, returns a list of all unique, valid bitcoins on that page
    potential_matches = find_bitcoin_addr(body)
    valid_addresses = []
    unique_matches = set(potential_matches)

    # Try to validate each regex matched address
    for item in unique_matches:
        addr_found = False
        str_item = item.decode("utf-8")
        try:
            addr_found = check_bc(str_item)

        except AttributeError:
            print("Please run with Python3!")
            exit()

        except ValueError:
            addr_found = False

        except TypeError:
            print(traceback.print_exc())

        except OverflowError:
            print(traceback.print_exc())

        if addr_found:
            valid_addresses.append(str_item)

    return valid_addresses