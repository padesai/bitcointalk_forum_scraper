import json
from pprint import pprint

total_urls = 0

list_addr = []
with open('out.json') as data_file:    
    data = json.load(data_file)
    for url in data:
    	total_urls = total_urls+1
    	for bitcoin_addr in url['bitcoin_addresses']:
    		list_addr.append(bitcoin_addr)

unique_addr = set(list_addr)
print("Total instances of addresses found: "+str(len(list_addr)))
print("Total unique addresses found: "+ str(len(unique_addr)))

print("TOTAL URLS: "+str(total_urls))

