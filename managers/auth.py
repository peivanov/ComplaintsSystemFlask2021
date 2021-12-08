from datetime import timedelta, datetime

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import BadRequest


# алтернативен начин с lambda
# mapper = {
#     ComplainerModel: lambda x: ComplainerModel.query.filter_by(id=x),
#     ApproverModel: lambda x: ApproverModel.query.filter_by(id=x),
#     AdministatorModel: lambda x: AdministatorModel.query.filter_by(id=x)
# }


class AuthManager:
    @staticmethod
    # кодираме токен
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=100),
            "role": user.__class__.__name__,
        }
        return jwt.encode(payload, key=config("JWT_KEY"), algorithm="HS256")

    @staticmethod
    # декодираме токен
    def decode_token(token):
        try:
            # algoritms трябва да е в масив (List)
            data = jwt.decode(token, key=config("JWT_KEY"), algorithms=["HS256"])
            return data["sub"], data["role"]  # data["sub"] = user.id
        except jwt.ExpiredSignatureError:
            raise BadRequest("Token has expired")
        except jwt.InvalidTokenError:
            raise BadRequest("Token is invalid")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    user_id, role = AuthManager.decode_token(token)
    # подпъхва ролята на user (ComlpModel, ApprModel, AdminModel);
    # ще филтърне по id и ще вземе first
    # user = mapper[role](user_id)  # алтернативен начин с lambda
    user = eval(f"{role}.query.filter_by(id={user_id}).first()")
    return user
