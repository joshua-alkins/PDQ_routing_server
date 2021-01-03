from flask import Blueprint
from flask import jsonify, request, make_response
from werkzeug.security import check_password_hash

from ..Database import DB as DB
from ..Security.Security import create_token

security_api = Blueprint('security_api', __name__)

@security_api.route('/driver-login')
def driver_login():
    _json = request.json
    try:
        _email = _json['email']
        _password = _json['password']
    except:
        return make_response('Missing credentials.', 401)

    if _email and _password:
        result = DB.get_driver_password(_email)
        if check_password_hash(result['password'],_password):
            token = create_token(_email)
            return token
        else:  
            return make_response('Could not verify!', 401)

    else:
        return make_response('Missing credentials.', 401)