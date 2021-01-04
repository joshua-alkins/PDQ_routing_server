from flask import Blueprint
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

from flask import jsonify, request

import datetime, json, random

from ..Database import DB as DB


utilities_api = Blueprint('utilies_api', __name__)

@utilities_api.route('/populate-drivers')
def populate_drivers():

    firstnames = ['Joshua', 'Jason', 'Antonio', 'Michael', 'William', 'Jack']
    lastnames = ['Smith', 'Turner', 'Taylor', 'Jackson', 'Sparrow', 'Swan']

    drivers = []

    for i in range(10):
        
        firstname = random.choice(firstnames)
        lastname = random.choice(lastnames)
        name = firstname + ' ' + lastname

        
        password = generate_password_hash('password')

        plate = ''

        for j in range(2):
            plate += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        
        for j in range(2):
            plate += random.choice('0123456789')

        factory = random.choice(['F1','F2','F3','F4'])

        email = firstname + '_' + lastname + plate + '@pdq.com' 

        driver = {'name': name, 'email': email, 'license': plate, 'factory_id':factory,'password': password}
        drivers += [driver]

    DB.add_many_drivers(drivers)
    return 'success'

@utilities_api.route('/populate-deliveries')
def populate_deliveries():

    deliveries = []

    for i in range(20):

        #random order id
        id_extention = ''
        for j in range(7):
            id_extention += random.choice('0123456789')

        order_id = 'O' + id_extention
        factory_id = random.choice(['F1','F1','F1','F1'])
        factory_location = {"lat":31.339018926934187, "lon":120.41726838280294}
        delivery_location =  random.choice([{"lat":31.32756756669994, "lon":120.41071042984981},{"lat":31.32365879731752, "lon":120.43023074941391}])
        driver_id = None
        status = 'open'

        #now with random offset
        seconds = random.choice(range(150)) #* random.choice([-1,1])
        order_time = datetime.datetime.utcnow() + datetime.timedelta(0,seconds)
        delivery_time = None

        delivery={'order_id': order_id, 'factory_id': factory_id, 'factory_location': factory_location, 'delivery_location': delivery_location, 'driver_id': driver_id, 'status': status, 'order_time': order_time, 'delivery_time': delivery_time}
        deliveries += [delivery]

    DB.add_many_deliveries(deliveries)
    return 'success'