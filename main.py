from os import environ, path

from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from db import db

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

app = Flask(__name__)
CORS(app)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "DB REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

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