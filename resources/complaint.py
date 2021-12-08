from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.complaint import ComplaintManager
from models.enums import RoleType
from schemas.request.complaint import ComplaintCreateRequestSchema
from schemas.response.complaint import ComplaintCreateResponseSchema
from util.decorators import validate_schema, permission_required


class ListCreateComplaint(Resource):
    @auth.login_required
    def get(self):
        # ще взема всичктие complaints които имаме
        # TODO add logic for different roles
        complaints = ComplaintManager.get_all()
        schema = ComplaintCreateResponseSchema()
        return schema.dump(
            complaints, many=True
        )  # many=True, защото връщаме лист от complaints
        pass

    # искаме да е логнат user-a, но и да валидираме permission-a
    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(ComplaintCreateRequestSchema)
    def post(self):
        current_user = auth.current_user()
        # вземаме json от request и го подаваме на create
        complaint = ComplaintManager.create(request.get_json(), current_user.id)
        schema = ComplaintCreateResponseSchema()
        return schema.dump(complaint)  # прави го на речник с всички полета


class ComplaintDetail(Resource):
    def get(self, id_):
        pass

    # само user-a ще може да си ъпдейтва complain-a, ако е в статус Pending
    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(ComplaintCreateRequestSchema)
    def put(self, id_):
        updated_complaint = ComplaintManager.update(request.get_json(), id_)
        schema = ComplaintCreateResponseSchema()
        return schema.dump(updated_complaint)  # прави го на речник с всички полета

    @auth.login_required
    # @permission_required(RoleType.admin)
    def delete(self, id_):
        ComplaintManager.delete(id_)
        return {"message": "Successfully deleted"}, 204


class ApproveComplaint(Resource):
    @auth.login_required
    # @permission_required(RoleType.approver)
    def get(self, id_):
        complaint = ComplaintManager.approve(id_)
        schema = ComplaintCreateResponseSchema()
        return schema.dump(complaint)


class RejectComplaint(Resource):
    @auth.login_required
    # @permission_required(RoleType.approver)
    def get(self, id_):
        complaint = ComplaintManager.reject(id_)
        schema = ComplaintCreateResponseSchema()
        return schema.dump(complaint)
