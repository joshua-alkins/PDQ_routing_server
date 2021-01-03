from flask import request, jsonify
from ..settings import SECRET_KEY

from functools import wraps

import jwt

def token_required(f):
    # Creates wrapper to verify tokens for API routes
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'token is missing.'})
        try:
            data = jwt.decode(token,SECRET_KEY)
        except:
            return jsonify({'message': 'token is invalid.'})

        return f(*args, **kwargs)
    return decorated


def create_token(email):
    return jwt.encode({'user':email},SECRET_KEY)
