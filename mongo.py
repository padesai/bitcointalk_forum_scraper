from flask import Flask, jsonify, request, abort
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'bitcoin_rest'

mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def flask_get_all_users():
    return jsonify(get_all_users())


@app.route('/users/name/<name>', methods=['GET'])
def flask_get_user_from_name(name):
    return jsonify(get_user_from_name(name))


@app.route('/users/bitcoin/<address>', methods=['GET'])
def flask_get_users_from_bitcoin(address):
    return jsonify(get_users_from_bitcoin(address))


@app.route('/comments', methods=['GET'])
def flask_defaul_get_comments():
    return jsonify(get_comments(10))


@app.route('/comments/<int:amount>', methods=['GET'])
def flask_get_comments(amount=10):
    return jsonify(get_comments(amount))


@app.route('/comments/name/<name>', methods=['GET'])
def flask_get_comments_from_name(name):
    return jsonify(get_comments_from_name(name))


@app.route('/comments/bitcoin/<address>', methods=['GET'])
def flask_get_comments_from_bitcoin(address):
    return jsonify(get_comments_from_bitcoin(address))


@app.route('/all/name/<name>', methods=['GET'])
def flask_get_all_from_name(name):
    return jsonify(get_all_from_name(name))


@app.route('/all/bitcoin/<address>', methods=['GET'])
def flask_get_all_from_bitcoin(address):
    return jsonify(get_all_from_bitcoin(address))


@app.route('/users/insert', methods=['POST'])
def flask_add_user():
    try:
        username = request.json['username']
        profile_url = request.json['profile_url']
        bitcoin_addresses = request.json['bitcoin_addresses']
    except KeyError:
        abort(400)
    except:
        abort(400)

    return jsonify(add_user(username, profile_url, bitcoin_addresses))


@app.route('/users/overwrite', methods=['POST'])
def flask_overwrite_user():
    try:
        username = request.json['username']
        profile_url = request.json['profile_url']
        bitcoin_addresses = request.json['bitcoin_addresses']
    except KeyError:
        abort(400)
    except:
        abort(400)

    return jsonify(overwrite_user(username, profile_url, bitcoin_addresses))


def get_all_users():
    # Return all users and their information in the database
    users = mongo.db.users

    output = []

    for q in users.find():
        output.append(
            {'profile_url': q['profile_url'], 'username': q['username'], 'bitcoin_addresses': q['bitcoin_addresses']})

    return {'result': output}


def get_user_from_name(name):
    # Return all related information of a given username
    users = mongo.db.users

    q = users.find_one({'username': name})
    output = {}
    if q:
        output = {'profile_url': q['profile_url'], 'username': q['username'],
                  'bitcoin_addresses': q['bitcoin_addresses']}

    return {'result': output}


def get_users_from_bitcoin(address):
    # Return all users and related information of users given a bitcoin address
    users = mongo.db.users

    q = users.find({'bitcoin_addresses': address})
    output = []
    for user in q:
        output.append({'profile_url': user['profile_url'], 'username': user['username'],
                       'bitcoin_addresses': user['bitcoin_addresses']})

    return {'result': output}


def get_comments(amount):
    # Return all comments in the database
    comments = mongo.db.comments

    output = []

    for q in comments.aggregate([{"$sample": {'size': amount}}]):
        output.append(
            {'username': q['username'], 'profile_url': q['profile_url'], 'comment': q['comment'],
             'comment_url': q['comment_url'],
             'bitcoin_addresses': q['bitcoin_addresses'], 'date': q['date']})

    return {'result': output}


def get_comments_from_name(name):
    # Return all comments of a given username
    comments = mongo.db.comments

    q = comments.find({'username': name})
    output = []
    for comment in q:
        output.append(
            {'username': comment['username'], 'profile_url': comment['profile_url'], 'comment': comment['comment'],
             'comment_url': comment['comment_url'],
             'bitcoin_addresses': comment['bitcoin_addresses'], 'date': comment['date']})

    return {'result': output}


def get_comments_from_bitcoin(address):
    # Return all comments including a specific bitcoin address
    comments = mongo.db.comments

    q = comments.find({'bitcoin_addresses': address})
    output = []
    for comment in q:
        output.append(
            {'username': comment['username'], 'profile_url': comment['profile_url'], 'comment': comment['comment'],
             'comment_url': comment['comment_url'],
             'bitcoin_addresses': comment['bitcoin_addresses'], 'date': comment['date']})

    return {'result': output}


def get_all_from_name(name):
    # Return everything for a given username
    users_result = get_user_from_name(name)['result']
    comments_result = get_comments_from_name(name)['result']

    if len(users_result) == 0 and len(comments_result) == 0:
        return {'result': {}}

    if len(users_result) > 0:
        # There exists a stored user
        username = users_result['username']
        profile_url = users_result['profile_url']
        user_addresses = users_result['user_addresses']
    else:
        # No stored user, get info from comments
        username = comments_result[0]['username']
        profile_url = comments_result[0]['profile_url']
        user_addresses = []

    comment_addresses = []
    reduced_comments = []
    for c in comments_result:
        reduced_comments.append(
            {'comment': c['comment'], 'comment_url': c['comment_url'], 'bitcoin_addresses': c['bitcoin_addresses'],
             'date': c['date']})
        for adr in c['bitcoin_addresses']:
            comment_addresses.append(adr)

    address_set = list(set(user_addresses + comment_addresses))

    output = {'username': username, 'profile_url': profile_url,
              'bitcoin_addresses': address_set, 'comments': reduced_comments}

    return {'result': output}


def get_all_from_bitcoin(address):
    # Return everything for a given username
    users_result = get_users_from_bitcoin(address)['result']
    comments_result = get_comments_from_bitcoin(address)['result']

    if len(users_result) == 0 and len(comments_result) == 0:
        return {'result': {}}

    all_users_set = set()
    related_addresses_set = set()
    for user in users_result:
        all_users_set.add(user['username'])
        for adr in user['bitcoin_addresses']:
            related_addresses_set.add(adr)

    for comment in comments_result:
        all_users_set.add(comment['username'])
        for adr in comment['bitcoin_addresses']:
            related_addresses_set.add(adr)

    output = {'all_users': list(all_users_set), 'all_bitcoin_addresses': list(related_addresses_set),
              'comments': comments_result}

    return {'result': output}


def add_user(username, profile_url, bitcoin_addresses):
    # Insert a totally new user into the database
    users = mongo.db.users

    if users.find_one({'username': username}):
        return jsonify({'result': "User '{}' already exists".format(username)})

    user_id = users.insert({'profile_url': profile_url, 'username': username,
                            'bitcoin_addresses': bitcoin_addresses})
    new_user = users.find_one({'_id': user_id})

    output = {}
    if new_user:
        output = {'profile_url': new_user['profile_url'], 'username': new_user['username'],
                  'bitcoin_addresses': new_user['bitcoin_addresses']}

    return {'result': output}


def overwrite_user(username, profile_url, bitcoin_addresses):
    # Overwrites a user's data or creates a new one if doesn't exist
    users = mongo.db.users

    replacement_user = {'profile_url': profile_url, 'username': username,
                        'bitcoin_addresses': bitcoin_addresses}

    orig_user = users.find_one_and_replace({'username': username}, replacement_user, upsert=True)

    new_user = users.find_one({'username': username})

    if orig_user:
        out_orig = {'profile_url': orig_user['profile_url'], 'username': orig_user['username'],
                    'bitcoin_addresses': orig_user['bitcoin_addresses']}
    else:
        out_orig = {}

    if new_user:
        out_new = {'profile_url': new_user['profile_url'], 'username': new_user['username'],
                   'bitcoin_addresses': new_user['bitcoin_addresses']}
    else:
        out_new = {}

    output = {'old_user': out_orig, 'new_user': out_new}

    return {'result': output}


if __name__ == '__main__':
    app.run(debug=True)
