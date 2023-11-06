
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import User
from .schemas import UserSchema, CreateUserFormSchema, UpdateUserFormSchema
from sqlalchemy import or_


user_bp = Blueprint("users", __name__)


@user_bp.get("")
# @jwt_required()
def get_all_users():
    page = request.args.get("page", default=1, type=int)

    per_page = request.args.get("size", default=10, type=int)

    users = User.query.paginate(page=page, per_page=per_page)

    result = UserSchema().dump(users, many=True)

    return (
        jsonify(
            {
                "items": result,
                "size": per_page,
                "page": page,
                "total": users.total
            }
        ),
        200,
    )

@user_bp.delete("<id>")
# @jwt_required()
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return (
        jsonify(
            {
                "message": "User not found!",
            }
        ),
        404,
    )

    user.delete()

    return (
        jsonify(
            {
                "message": "Deleted",
            }
        ),
        200,
    )


@user_bp.get("<id>")
# @jwt_required()
def get_user_by_id(id):
    user = User.query.get(id)

    if not user:
        return (
        jsonify(
            {
                "message": "User not found!",
            }
        ),
        404,
    )

    user_data = UserSchema().dump(user)

    return (
        jsonify(user_data),
        200,
    )


@user_bp.post("")
# @jwt_required()
def add_user():
    payload = request.json
    errors = CreateUserFormSchema().validate(payload)
    if errors:
        return (
        jsonify({
            "message": "Validation failed",
            "errors": errors
        }),
        400,
    )
    newUser = User.query.filter(or_(User.email == payload['email'], User.username == payload['username'])).first()
    
    if newUser is not None:
        return (
        jsonify({
            "message": "User with this email or username exists"
        }),
        400,
    )

    newUser = User()
    newUser.add(payload)

    return (
        jsonify(UserSchema().dump(newUser)),
        200,
    )

@user_bp.patch("<id>")
# @jwt_required()
def update_user_by_id(id):
    payload = request.json
    errors = UpdateUserFormSchema().validate(payload)
    
    if errors:
        return (
        jsonify({
            "message": "Validation failed",
            "errors": errors
        }),
        400,
    )

    user = User.query.get(id)
    
    if not user:
        return (
        jsonify(
            {
                "message": "User not found!",
            }
        ),
        404,
    )

    payload = request.json
    user.update(payload)
    user_data = UserSchema().dump(user)

    return (
        jsonify(user_data),
        200,
    )
