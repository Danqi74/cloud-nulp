from os import environ, path

from flask import Flask, jsonify
from flask_smorest import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from db import db
from blocklist import BLOCKLIST

from resources.user import blp as UserBlueprint
from resources.team import blp as TeamBlueprint
from resources.worker import blp as WorkerBlueprint
from resources.user_order import blp as UserOrderBlueprint
from resources.laser_cutter_order import blp as LaserCutterOrderBlueprint
from resources.laser_cutter import blp as LaserCutterBlueprint
from resources.laser_cutter_repair import blp as LaserCutterRepairBlueprint
from resources.worker_position import blp as WorkerPositionBlueprint
from resources.equipment_type import blp as EquipmentTypeBlueprint
from resources.equipment_condition import blp as EquipmentConditionBlueprint
from resources.equipment import blp as EquipmentBlueprint
from resources.equipment_repair import blp as EquipmentRepairBlueprint
from resources.laser_cutter_order_evaluation import blp as LaserCutterEvaluationBlueprint

from dotenv import load_dotenv

load_dotenv('.env')

DATABASE_URI = environ.get("DATABASE_URI")
PLAIN_DATABASE_URI = environ.get("PLAIN_DATABASE_URI")
SECRET_KEY = environ.get("SECRET_KEY")

app = Flask(__name__)
CORS(app)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Сloud REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.config["JWT_SECRET_KEY"] = SECRET_KEY
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )

@app.before_request
def crate_tables():
    db.create_all()

api = Api(app)

api.register_blueprint(UserBlueprint)
api.register_blueprint(TeamBlueprint)
api.register_blueprint(WorkerBlueprint)
api.register_blueprint(UserOrderBlueprint)
api.register_blueprint(LaserCutterOrderBlueprint)
api.register_blueprint(LaserCutterBlueprint)
api.register_blueprint(LaserCutterRepairBlueprint)
api.register_blueprint(WorkerPositionBlueprint)
api.register_blueprint(EquipmentTypeBlueprint)
api.register_blueprint(EquipmentConditionBlueprint)
api.register_blueprint(EquipmentBlueprint)
api.register_blueprint(EquipmentRepairBlueprint)
api.register_blueprint(LaserCutterEvaluationBlueprint)

if __name__ == "__main__":
    app.run()
