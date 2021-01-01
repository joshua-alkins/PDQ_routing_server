from flask import Flask
from .extensions import mongo

from .API.DriverAPI import driver_api
from .API.DeliveryAPI import delivery_api
from .API.UtilitiesAPI import utilities_api

def create_app(config_object = 'routing_server.settings'):
    app = Flask(__name__)

    app.config.from_object(config_object)
    mongo.init_app(app)

    app.register_blueprint(driver_api, url_prefix='/driver')
    app.register_blueprint(delivery_api, url_prefix='/delivery')
    app.register_blueprint(utilities_api, url_prefix='/util')

    return app
