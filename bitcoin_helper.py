import re
from hashlib import sha256
import traceback

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
            addr_found = False
            # print(traceback.print_exc())

        if addr_found:
            valid_addresses.append(str_item)

    return valid_addresses