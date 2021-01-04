from routing_server.extensions import mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime, json


""" Deliveries Cluster"""

def add_new_delivery(order_id, factory_id, factory_location, delivery_location):
    driver_id = None
    status = "open"
    order_time = datetime.datetime.utcnow()
    delivery_time = None

    mongo.db.deliveries.insert_one({'order_id': order_id, 'factory_id': factory_id, 'factory_location': factory_location, 'delivery_location': delivery_location, 'driver_id': driver_id, 'status': status, 'order_time': order_time, "delivery_time": delivery_time})
    return True

def retrieve_deliveries(factory_id):
    query = {"factory_id": factory_id, "status": "open"}

    request_deliveries = mongo.db.deliveries.find(query).sort("order_time", 1)
    
    return dumps(request_deliveries)

def retrieve_delivery(factory_id):
    query = {"factory_id": factory_id, "status": "open"}

    delivery = mongo.db.deliveries.find(query).sort("order_time",1).limit(1)
    print(delivery)
    try:
        response = dumps(delivery[0])

        json_data = json.loads(response)

        order_id = json_data['order_id']

        query = {'order_id': order_id}
        values = {"$set": {'status': 'transit'}}
        mongo.db.deliveries.update_one(query, values)
    except:
        response = {}

    return response

def confirm_order(order_id, driver_id):
    query = {'order_id': order_id}
    values ={"$set":{'driver_id': driver_id, 'status': 'transit'}}

    mongo.db.deliveries.update_one(query,values)
    return True

def deliver_order(order_id):
    current_time = datetime.datetime.utcnow()
    query = {'order_id': order_id}
    values = {'$set': {'status': 'delivered','delivery_time':current_time}}

    mongo.db.deliveries.update_one(query, values)

    return True

def decline_order(order_id, driver_id):
    query = {'order_id': order_id}
    values ={"$set":{'driver_id': driver_id, 'status': 'open'}}

    mongo.db.deliveries.update_one(query,values)
    return True

""" Driver Cluster """
def add_driver(name, email, license_plate, password):
    mongo.db.drivers.insert({'name': name, 'email': email, 'license': license_plate, 'password': password})
    return True

def retrieve_all_drivers():
    drivers = mongo.db.drivers.find()
    return drivers

def retrieve_driver(driver_id):
    driver = mongo.db.drivers.find_one({'_id':ObjectId(driver_id)})
    return driver

def delete_driver(driver_id):
    mongo.db.drivers.delete_one({'_id': ObjectId(driver_id)})
    return True

def update_driver(driver_id, name, email, license_plate, password):
    mongo.db.drivers.update_one({'_id': ObjectId(driver_id['$oid']) if '$oid' in driver_id else ObjectId(driver_id)}, {'$set': {'name': name, 'email': email, 'license': license_plate,'password': password}})
    return True

def get_driver_password(email):
    query = {"email": email}
    driver = mongo.db.drivers.find_one(query)
    try:
        password = driver['password']
    except:
        password = None
    return password

""" Utilities """
def add_many_drivers(drivers):
    mongo.db.drivers.insert_many(drivers)
    return True

def add_many_deliveries(deliveries):
    mongo.db.deliveries.insert_many(deliveries)
    return True