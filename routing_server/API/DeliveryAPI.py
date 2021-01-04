from flask import Blueprint

from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import jsonify, request, make_response

import datetime, json

from ..Database import DB as DB

delivery_api = Blueprint('delivery_api', __name__)

@delivery_api.route('/add', methods=['POST'])
def add():
    _json = request.json
    _order_id = _json['order_id']
    _factory_id = _json['factory_id']
    _factory_location = _json['factory_location']
    _delivery_location = _json['delivery_location']

    if _order_id and _factory_id and _factory_location and _delivery_location and request.method == 'POST':
        id = DB.add_new_delivery(_order_id,_factory_id,_factory_location,_delivery_location)

        response = jsonify('Delivery successfully added')
        return response
    else:
        return not_found()


@delivery_api.route('/request-list')
def request_list():
    _json = request.json
    _factory_id = _json['factory_id']

    
    if _factory_id:
        response = DB.retrieve_deliveries(_factory_id)
        return response
    else:
        not_found()

@delivery_api.route('/request', methods=['POST'])
def request_delivery():
    _json = request.json
    print("Request JSON:")
    print(_json)
    print("Request JSON:")
    print(request)
    _factory_id = _json['factory_id']
    
    if _factory_id:
        response = DB.retrieve_delivery(_factory_id)
        if response != {}:
            return response
        else:
            return {}, 204
    else:
        not_found()

@delivery_api.route('/accept', methods=['PUT'])
def accepted():
    _json = request.json
    _order_id = _json['order_id']
    _driver_id = _json['driver_id']

    if _order_id and _driver_id and request.method == 'PUT':
        DB.confirm_order(_order_id, _driver_id)

        response = jsonify('success')
        return response
    else:
        return not_found()

@delivery_api.route('/deliver', methods=['PUT'])
def delivered():
    _json = request.json
    _order_id = _json['order_id']

    if _order_id and request.method == 'PUT':
        DB.deliver_order(_order_id)

        response = jsonify("successfully updated")
        return response
    else:
        return not_found()

@delivery_api.route('/decline', methods=['PUT'])
def decline():
    _json = request.json
    _order_id = _json['order_id']

    if _order_id and request.method == 'PUT':
        DB.decline_order(_order_id)

        response = jsonify("successfully updated")
        return response
    else:
        return not_found()

@delivery_api.errorhandler(404)
def not_found(error=None):
    URL= request.url
    message = {
        'status': 404,
        'message': 'Unexpected error'
    }

    response = jsonify(message)
    response.status_code = 400

    return response