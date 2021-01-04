from flask import Blueprint
from flask import jsonify, request, make_response
from werkzeug.security import check_password_hash

from ..Database import DB as DB
from ..Security.Security import create_token

security_api = Blueprint('security_api', __name__)

@security_api.route('/driver-login', methods=['POST'])
def driver_login():
    _json = request.json
    try:
        _email = _json['email']
        _password = _json['password']
    except:
        return make_response('Missing credentials.', 200)

    if _email and _password:
        result = DB.get_driver_by_email(_email)
        hashed_password = result['password']
        factory_id = result['factory_id']

        if result != None:
            if check_password_hash(hashed_password,_password):
                token = create_token(_email)
                print("valid credentials")
                return jsonify({"token":token, "factory_id": factory_id,"valid":"valid"})
            else:  
                print("credentials did not match")
                return make_response(jsonify({"valid":"invalid"}), 200)
        else:
            print("could not find user")
            return make_response(jsonify({"valid":"invalid"}), 200)

    else:
        return make_response(jsonify({"valid":"missing"}), 200)