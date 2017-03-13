import json
from pprint import pprint
import mysql.connector
import traceback


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


def add_user_profiles():
	#open the JSON file
	with open('user_profiles.json','r') as data_file:    
	    data = json.load(data_file)
	    for line_item in data:
		    parsed_username = line_item['user_id']
		    parsed_url = line_item['Profile URL']
		    #SQL query that will add a username and profile url for the parsed data
		    sql = "INSERT IGNORE INTO user_profiles (username, profile_url) VALUES ('%s','%s')"%(parsed_username, parsed_url)
		    cursor = cnx.cursor(buffered=True)
		    try:
		    	cursor.execute(sql)
		    	# print sql
		    	cnx.commit()
		    except:
		    	print "failed on "+parsed_username


def add_user_bitcoins():
	with open('user_profiles.json','r') as data_file:
		data = json.load(data_file)
		for line_item in data:
			parsed_username = line_item['user_id']
			parsed_url = line_item['Profile URL']
		    #Get the bitcoin addresses found for the scraped data
			bitcoin_addresses = line_item['bitcoin_addresses']
			cursor = cnx.cursor(buffered=True)
			try:
				#get the foreign key for the user that is an owner of the bitcoin address
				sql = "Select id from user_profiles where username = '%s'"%(parsed_username)
				cursor.execute(sql)
				user_id = cursor.fetchone()[0]
				for addr in bitcoin_addresses:
					sql = "INSERT INTO user_bitcoins (user_profile_id,bitcoin_address) VALUES ('%s','%s')"%(user_id,addr)
					cursor.execute(sql)
					cnx.commit()
			except:
				traceback.print_exc()
				print "failed! on "+str(line_item)
				with open('failed.json','a') as failed:
					failed.write(str(line_item)+"\n")

	      	
def add_user_comments():
	with open('out.json', 'r') as user_comments:
		data = json.load(user_comments)
		for line in data:
			data = json.load(line)
		print data
# add_user_profiles()	  
# add_user_bitcoins() 
add_user_comments()
cnx.close()


	      	#Get the bitcoin addresses found for the scraped data
	      	# bitcoin_addresses = line_item['bitcoin_addresses']
	      	# user_id = get_db_id_of_user(parsed_username)
	      	# for addr in bitcoin_addresses:
	      	# 	sql = "INSERT INTO user_bitcoins (user_profile_id,bitcoin_address) VALUES ('%s','%s')"%(user_id,addr)
	      	# 	cursor.execute(sql)
	      	# 	cnx.commit()



# pprint(data)


def separate_json():
	with open('out.json','r') as my_json_file:
		with open('user_profiles.json', 'a') as write_file:
			for line_item in my_json_file:
				if 'comment_text' not in line_item:
					write_file.write(line_item)



def separate_user_comments():
	with open('out.json','r') as my_json_file:
		with open('user_comments.json', 'w') as write_file:
			for line_item in my_json_file:
				if 'comment_text' in line_item:
					write_file.write(line_item)

