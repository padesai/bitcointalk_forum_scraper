import json
from pprint import pprint
import mysql.connector


def readConfigFile(config_file):
#reads the config file and returns an array of relevant values
#array[0] = username, array[1] = password
	values = []
	with open(config_file,'r') as cfg_file:
		username = cfg_file.readline()
		password = cfg_file.readline()
	values.append(username)
	values.append(password)
	return values

#get the configuration information for the mysql database
configValues = readConfigFile('mysqlconfig.txt')
username = configValues[0]
user_pass = configValues[1]



#connect to the mysql database
cnx = mysql.connector.connect(user=username, password=user_pass,
                              host='127.0.0.1',
                              database='bitcoin_forum_scraping')



#open the JSON file
with open('user_profile.json') as data_file:    
    data = json.load(data_file)
    for line_item in data:
    	parsed_username = line_item['user_id']
    	parsed_url = line_item['Profile URL']
      	sql = "INSERT INTO user_profiles (username, profile_url) VALUES ('%s','%s')"%(parsed_username, parsed_url)
      	cursor = cnx.cursor(buffered=True)
      	cursor.execute(sql)	
      	cnx.commit()
      	#Get the primary key of the last inserted user ID
      	sql = "SELECT LAST_INSERT_ID();"
      	cursor.execute(sql)
      	user_id = cursor.fetchone()[0]

      	#Get the bitcoin addresses found for the scraped data
      	bitcoin_addresses = line_item['bitcoin_addresses']
      	for addr in bitcoin_addresses:
      		sql = "INSERT INTO user_bitcoins (user_profile_id,bitcoin_address) VALUES ('%s','%s')"%(user_id,addr)
      		cursor.execute(sql)
      		cnx.commit()


cnx.close()

# pprint(data)




