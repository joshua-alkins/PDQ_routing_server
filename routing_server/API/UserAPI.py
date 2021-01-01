from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

@app.route('/add-user', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        id = mongo.db.user.insert({'name': _name, 'email': _email, 'password': _hashed_password})

        response = jsonify("User added successfully")

        return response

    else:

        return not_found()

@app.route('/all-users')
def users():
    users = mongo.db.user.find()
    response = dumps(users)
    return response

@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id':ObjectId(id)})
    response = dumps(user)
    return response

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    response = jsonify("User successfully deleted")

    response.status_code = 200

    return response

@app.route('/update-user/<id>', methods = ['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _id and request.method =='PUT':
        _hashed_password =  generate_password_hash(_password)

        mongo.db.user.update_one({'_id': ObjectId(id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'email': _email, 'password': _hashed_password}})

        response = jsonify("User successfully added")
        response.status_code = 200

        return response

    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }

    response = jsonify(message)
    response.status_code = 404

    return response