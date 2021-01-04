from flask import Blueprint
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash

from ..Security.Security import token_required

from ..Database import DB as DB

from ..settings import SECRET_KEY

driver_api = Blueprint('driver_api', __name__)

@driver_api.route('/add', methods=['POST'])
def add():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _license = _json['license']
    _password = _json['password']
    _factory_id = _json['factory_id']

    if _name and _email and _license and _password and _factory_id and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        driver_id = DB.add_driver(_name, _email, _license, _factory_id,_hashed_password)

        response = jsonify("Driver added successfully")

        return response
    else:
        return not_found()

@driver_api.route('/list-all')
def drivers():
    drivers = DB.retrieve_all_drivers()
    response = dumps(drivers)
    return response

@driver_api.route('/<id>')
def driver(id):
    driver = DB.retrieve_driver(id)
    response = dumps(driver)
    return response

@driver_api.route('/delete/<id>', methods=['DELETE'])
def delete_driver(id):
    DB.delete_driver(id)
    response = jsonify("User successfully deleted")

    response.status_code = 200

    return response

@driver_api.route('/update/<driver_id>', methods = ['PUT'])
def update_driver(driver_id):
    _id = driver_id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _license = _json['license']
    _password = _json['password']

    if _name and _email and _id and _license and _password and request.method =='PUT':
        _hashed_password =  generate_password_hash(_password)

        DB.update_driver(_id,_name,_email,_license,_hashed_password)

        response = jsonify("User successfully added")
        response.status_code = 200

        return response

    else:
        return not_found()

@driver_api.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }

    response = jsonify(message)
    response.status_code = 404

    return response