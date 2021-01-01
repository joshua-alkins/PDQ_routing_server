from flask import Flask
from flask_pymongo import PyMongo
from flask_pymongo import MongoClient

app = Flask(__name__)

app.secret_key = "secretkey"

development_db_uri = "mongodb://127.0.0.1:2717/PDQ"
production_db_uri = "mongodb+srv://general_user:PDQ_password@cluster0.7rkon.mongodb.net/<dbname>?retryWrites=true&w=majority"

# app.config['MONGO_URI'] = development_db_uri

client = MongoClient(production_db_uri)

mongo = client.get_database('PDQ_routing_subsystem')
# PyMongo(app)

from DriverAPI import driver_api
from DeliveryAPI import delivery_api
from UtilitiesAPI import utilities_api

app.register_blueprint(driver_api, url_prefix='/driver')
app.register_blueprint(delivery_api, url_prefix='/delivery')
app.register_blueprint(utilities_api, url_prefix='/util')

if __name__ == "__main__":
    app.run(debug=True)
