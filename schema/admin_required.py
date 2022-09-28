from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from graphql import GraphQLError

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                raise GraphQLError("Admins Only!")
        return decorator
    return wrapper