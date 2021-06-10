from flask_jwt_extended import get_jwt


def admin_required(decorated_func):
    def decorator(*args, **kwargs):
        claims = get_jwt()
        if claims['admin']:
            return decorated_func(*args, **kwargs)
        return {'message': 'Admin privileges required'}, 401

    return decorator
