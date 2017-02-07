from scrapy.linkextractors import LinkExtractor
import scrapy
import re
from hashlib import sha256

#takes in a string and returns all potential bitcoin addresses in a list
def find_bitcoin_addr(text):
    #Below regular expression should do the trick. Modified from the Bitcoin Transaction Analysis Graph Paper. 
    #(https://arxiv.org/pdf/1502.01657.pdf)
    #We need to support multisig bitcoin addresses that have a 3 in front of them. https://en.bitcoin.it/wiki/Address
    match = re.findall(r"[13].{26,33}", text)
    if match:
        return match
    else: 
        return False

digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
 
def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')
def check_bc(bc):
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]


class BitcoinSpider(scrapy.Spider):
    name = "bitcoin_forum"
    start_urls = [
            # 'http://bitcointalk.org',
            # 'http://bitcointalk.org/index.php?topic=20333.0'
            'file:///home/brian/network_security/dev/tuturial/bitcointalk-0.html'

        ]
    allowed_domains = ["bitcointalk.org"]
    page = 0

    #     for url in start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse_url)

    def parse(self, response):
        # filename = 'bitcointalk-%s.html' % "testing"
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        # self.page = self.page +1
        
        potential_matches = find_bitcoin_addr(response.body)
        print "LENGTH OF POTENTIAL MATCHES: "+str(len(potential_matches))
        filename = 'found_addresses.txt'
        with open(filename,'wb') as f:
            for item in potential_matches:
                try:
                    addr_found = check_bc(item)
                except AttributeError:
                    print "Please run with Python3!"
                    exit()
                except ValueError:
                    addr_found = False
                
                if addr_found:
                    f.write(item)
            




