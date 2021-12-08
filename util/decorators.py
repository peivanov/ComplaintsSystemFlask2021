from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth


def validate_schema(schema_name):
    def wrapper(func):
        def decorated_func(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if errors:
                raise BadRequest(errors)
            return func(*args, **kwargs)

        return decorated_func

    return wrapper


def permission_required(permission):
    def wrapper(func):  # вземаме функцията която сме декорирали
        def decorated_func(*args, **kwargs):
            user = auth.current_user()
            # имаме аутентикиран user, но той няма permissions
            if not user.role == permission:
                raise Forbidden("You do not have access to this resource")  # 403
            return func(*args, **kwargs)

        return decorated_func

    return wrapper
