from hashlib import sha256
import re
import codecs
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
 
def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')
def check_bc(bc):
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]


def read_bitcoin_html(filename):
	ret_string = ''

	with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as fdata:
		ret_string = fdata.read()
	return ret_string

def find_bitcoin_addr(text):
	#Below regular expression should do the trick. Modified from the Bitcoin Transaction Analysis Graph Paper. 
	#(https://arxiv.org/pdf/1502.01657.pdf)
	#We need to support multisig bitcoin addresses that have a 3 in front of them. https://en.bitcoin.it/wiki/Address
	match = re.findall(r"[13].{26,33}", text)
	if match:
		print ("Potential bitcoin address(es) found!")
		return match
	else: 
		return False



def test_bitcoin_regex_matching():
	print("Looking for bitcoin addresses in strings")
	print(find_bitcoin_addr('blah'))
	print(find_bitcoin_addr('\n<html>blalh<body><18vaZ4K62WiL6W2Qoj9AE1cerfCHRaUW4x>,17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j'))
	print(find_bitcoin_addr("3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8"))

def test_bitcoin_validity_func():
	print("Checking validity of some test bitcoin addresses...")
	print(check_bc('1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i'))
	print(check_bc("17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j"))
	print(check_bc("18vaZ4K62WiL6W2Qoj9AE1cerfCHRaUW4x"))
	print(check_bc("3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8"))

# test_bitcoin_regex_matching()
test_bitcoin_validity_func()
test_bitcoin_regex_matching()
# potential_matches = find_bitcoin_addr(read_bitcoin_html(
# 	'/home/brian/network_security/dev/bitcoin-analysis/bitcoin_forum_scraper/bitcointalk-testing.html'))

for item in potential_matches:
	try:
		addr_found = check_bc(item)
	except:
		addr_found = False
	if addr_found:
		print(item)