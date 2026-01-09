from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user=get_jwt_identity()
            if user["role"] not in roles:
                return jsonify({"message":"Access Forbidden."}),403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

