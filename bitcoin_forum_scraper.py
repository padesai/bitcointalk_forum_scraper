from scrapy.linkextractors import LinkExtractor
import scrapy
import re
from hashlib import sha256
import traceback


# takes in a string and returns all potential bitcoin addresses in a list
def find_bitcoin_addr(text):
    # Below regular expression should do the trick. Modified from the Bitcoin Transaction Analysis Graph Paper.
    # (https://arxiv.org/pdf/1502.01657.pdf)
    # We need to support multisig bitcoin addresses that have a 3 in front of them. https://en.bitcoin.it/wiki/Address
    match = re.findall(b"[13].[a-km-zA-HJ-NP-Z1-9]{26,33}", text)

    if match:
        return match
    else:
        return False


digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


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
    print("Should be True, actually is "+str(check_bc('18vaZ4K62WiL6W2Qoj9AE1cerfCHRaUW4x')))


test_bitcoin_validity_func()

class BitcoinSpider(scrapy.Spider):
    name = "bitcoin_forum"
    start_urls = [
        # 'http://bitcointalk.org',
        'http://bitcointalk.org/index.php?topic=20333.0'
        #'http://bitcointalk.org/index.php'
        # 'file:///home/brian/network_security/dev/tuturial/bitcointalk-0.html'
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
        #filename = 'found_addresses.txt'
        print ("LENGTH OF POTENTIAL MATCHES: " + str(len(potential_matches)))

        # with open(filename, 'w') as f:
        #     for item in potential_matches:
        #         addr_found = False
        #         str_item = item.decode("utf-8")
        #         # f.write("this is the str_item: "+str_item)
        #         try:
        #             addr_found = check_bc(str_item)
        #         except AttributeError:
        #             print("Please run with Python3!")
        #             exit()
        #         except ValueError:
        #             f.write('Value Error encountered on :'+str(str_item)+' and that is a '+str(type(str_item))+'\n')
        #             addr_found = False
        #         except TypeError:
        #             print(traceback.print_exc())
        #         if addr_found:
        #             f.write(str(item)+'\n')

        valid_addresses = []
        unique_matches = set(potential_matches)
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
            if addr_found:
                valid_addresses.append(str_item)

        yield {"url" : response.url,
               "bitcoin_addresses" : list(valid_addresses)}
