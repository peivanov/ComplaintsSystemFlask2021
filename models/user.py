from db import db
from models.enums import RoleType


class BaseUserModel(db.Model):  # db.Model за да ползваме SQLAlchemy
    __abstract__ = True  # abstract table

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    # nullable=False - задължително да попълнем име
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    # unique=True - уникални emails
    phone = db.Column(db.String(13), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class ComplainerModel(BaseUserModel):
    __tablename__ = "complainers"

    iban = db.Column(db.String(22))
    role = db.Column(db.Enum(RoleType), default=RoleType.complainer, nullable=False)


class ApproverModel(BaseUserModel):
    __tablename__ = "approvers"

    certificate = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleType), default=RoleType.approver, nullable=False)


class AdministatorModel(BaseUserModel):
    __tablename__ = "administrators"

    role = db.Column(db.Enum(RoleType), default=RoleType.admin, nullable=False)
