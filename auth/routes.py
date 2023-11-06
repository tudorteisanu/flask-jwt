from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)
from models import User, TokenBlocklist
from .schemas import CurrentUserSchema, LoginFormSchema, RegisterFormSchema

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register_user():
    data = request.get_json()
    errors = RegisterFormSchema().validate(data)
    
    if errors:
        return (
            jsonify(
                {"errors": errors})
        )

    user = User.get_user_by_username(username=data.get("username"))

    if user is not None:
        return jsonify({"error": "User already exists"}), 409

    new_user = User(username=data.get("username"), email=data.get("email"))

    new_user.set_password(password=data.get("password"))

    new_user.save()

    return jsonify({"message": "User created"}), 201


@auth_bp.post("/login")
def login_user():
    data = request.get_json()
    errors = LoginFormSchema().validate(data)

    if errors:
        print(errors, '------')
        return (
            jsonify(
                {"errors": errors})
        )
    user = User.get_user_by_username(username=data.get("username"))

    if user and (user.check_password(password=data.get("password"))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return (
            jsonify(
                {
                    "message": "Logged In ",
                    "tokens": {"access": access_token, "refresh": refresh_token},
                    "user": CurrentUserSchema().dump(user)
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid username or password"}), 400


@auth_bp.get("/check")
@jwt_required()
def whoami():
    return jsonify(
        {
            "user": CurrentUserSchema().dump(current_user),
        }
    )


@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"accessToken": new_access_token})


@auth_bp.get('/logout')
@jwt_required(verify_type=False) 
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']
    token_b = TokenBlocklist.query.filter_by(jti=jti)

    if token_b is not None: 
        return jsonify({"message": f"Token was already revoked"}) , 400
    
    token_b = TokenBlocklist(jti=jti)

    token_b.save()

    return jsonify({"message": f"{token_type} token revoked successfully"}) , 200

