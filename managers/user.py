from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models.user import ComplainerModel


class UserManager:
    @staticmethod
    def register(user_data):
        # валидация
        user_data["password"] = generate_password_hash(user_data["password"])
        user = ComplainerModel(**user_data)
        db.session.add(user)  # добавяме user
        try:
            db.session.commit()  # запазваме
        except Exception as ex:
            if ex.orig.pgcode == UNIQUE_VIOLATION:
                raise BadRequest("Please login")
            else:
                InternalServerError("Server is unavailable. Please try again later")
        return user

    @staticmethod
    def login(user_data):
        # проверяваме дали има такъв user по email-a му
        user = ComplainerModel.query.filter_by(email=user_data["email"]).first()
        if not user:
            raise BadRequest("Wrong email or password")
        # сравнява паролата
        if not check_password_hash(user.password, user_data["password"]):
            raise BadRequest("Wrong email or password")

        return user
