README FOR WEB SCRAPER
Project for network security - CS6262
======================================
out.json --> get these data from running bitcoin_forum_scraper.py; json file containing relevant
             data scraped from the bitcointalk.org forum. File contains a list of records that
             are in either of the following two formats:
             User Profile Page: {"profile_url": "", "user_id": "", "bitcoin_addresses": ["", "", ...]}
             Comment: {"profile_url": "", "date": "", "username": "", "comment_url": "",
                       "bitcoin_addresses": ["", "", ...], "comment": {"post": "", "signature": ""}}

bitcoin_forum_scraper.py --> script that, when run, will scrape all user profile pages and thread
                             pages present on bitcointalk.org. Requires Python 3.
        RUN: scrapy runspider bitcoin_forum_scraper.py -o out.json -s DOWNLOAD_DELAY=1 --nolog
        OUTPUT FILE: out.json

bitcoin_helper.py --> helper file that contains functions to validate Bitcoin addresses. This is
                      imported into bitcoin_forum_scraper.py. Also requires Python3
        RUN: N/A

comment_parser.py --> helper file that contains the function to parse a comment for the scraper. Will
                      return a parsed comment when given a valid string.  Imported into
                      bitcoin_forum_scraper.py to parse any valid comment. Also requires Python3
        RUN: N/A

import_json.py --> script that, when run, will open a connection to the running mongodb service and
                   create the database from the output file of bitcoin_forum_scraper. Creates two
                   collections, "users" and "comments", in the database titled "bitcoin_rest". Requires
                   Python2.7
        RUN: python import_json.py out.json

web_app.py --> script used to create a RESTful API using Flask which connects to the "bitcoin_rest"
               mongodb database. Various GET and POST requests can be made to the API to retrieve
               information from the database. Requires Python2.7
        RUN: python web_app.py

old_code/ --> folder containing any old/depricated code we had. Including: how we scraped the website
              originally, parsing the JSON file with old formatting, and creating a mysql database.
              Note: no guarantee any of this will work successfully