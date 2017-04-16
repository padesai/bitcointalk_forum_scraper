import pymongo
import sys
import json
from comment_parser import parse_comment


def import_json(filename):
    """Reads a JSON file and inserts each element into the database
    """
    mongo = pymongo.MongoClient()
    database = mongo["bitcoin_rest"]
    users = database.users
    comments = database.comments

    with open(filename) as f:
        data = json.load(f)

    # User keys: {"bitcoin_addresses": [], "profile_url": "", "user_id": ""}
    # Comment keys: {"bitcoin_addresses": [], "comment_text": "", "comment_url": ""}
    parsed_users = []
    parsed_comments = []
    for elem in data:
        if elem.has_key('user_id'):
            # Is a user profile JSON element
            user = {"username": elem["user_id"], "bitcoin_addresses": elem["bitcoin_addresses"],
                    "profile_url": elem["profile_url"]}
            parsed_users.append(user)

        elif elem.has_key('comment'):
            # Is a comment JSON element

            # No longer needed since scraper handles this
            # p = parse_comment(elem['comment_text'])
            # comment = {"username": p["username"], "bitcoin_addresses": elem["bitcoin_addresses"],
            #            "profile_url": p["profile_url"], "date": p["date"], "comment": p["comment"],
            #            "comment_url": elem["comment_url"]}
            # parsed_comments.append(comment)

            parsed_comments.append(elem)

    # Add everything into the mongo db
    users.insert_many(parsed_users)
    comments.insert_many(parsed_comments)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Must pass filename as first and only argument"
        quit()

    import_json(sys.argv[1])
