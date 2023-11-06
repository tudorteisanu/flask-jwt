from flask import Flask, jsonify
from extensions import db, jwt
from auth import auth_bp
from users import user_bp
from models import User, TokenBlocklist
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask2:flask2@db:3306/flask2'
    app.config['JWT_SECRET_KEY'] = 'some_secret'
    app.config['PORT'] = 5001
    app.config['DEBUG'] = True
    
    # initialize exts
    db.init_app(app)
    jwt.init_app(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})


    # register bluepints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    
    @app.before_request
    def create_all():
        db.create_all()

    # load user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        identity = jwt_data["sub"]

        return User.query.filter_by(username=identity).one_or_none()

    # jwt error handlers

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request doesnt contain valid token",
                    "error": "authorization_header",
                }
            ),
            401,
        )
    
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header,jwt_data):
        jti = jwt_data['jti']

        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

        return token is not None

    return app
