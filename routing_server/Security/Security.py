from flask import request, jsonify
from ..settings import SECRET_KEY

import datetime

from functools import wraps

import jwt


def token_required(f):
    # Creates wrapper to verify tokens for API routes
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            pass
            token = request.json['token']
            try:
                data = jwt.decode(token, SECRET_KEY,algorithms="HS256")
            except :
                return jsonify({'message': 'token is invalid.'})
        except:
            return jsonify({'message': 'token is missing.'})
        

        return f(*args, **kwargs)
    return decorated


def create_token(email):
    return jwt.encode({'user':email},SECRET_KEY)
