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


parsed_username = "YOYOYo"
parsed_url = "NLBLBL"

# Create table as per requirement
sql = "INSERT INTO user_profiles (username, profile_url) VALUES ('%s','%s')"%(parsed_username, parsed_url)
print sql
cursor = cnx.cursor()
cursor.execute(sql)	

cnx.commit()

#open the JSON file
with open('user_profile.json') as data_file:    
    data = json.load(data_file)

cnx.close()

# pprint(data)




