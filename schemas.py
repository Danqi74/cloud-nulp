from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime
from models import WorkerPositionModel
from db import db


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True)
    team = fields.Nested('TeamSchema', dump_only=True)

class EquipmentSchema(Schema):
    id = fields.Int(dump_only=True)
    model = fields.Str(required=True)
    serial_number = fields.Str(required=True)
    # equipment_type_id = fields.Int(required=True)
    # equipment_condition_id = fields.Int(required=True)
    equipment_type = fields.Nested('EquipmentTypeSchema', dump_only=True)
    equipment_condition = fields.Nested('EquipmentConditionSchema', dump_only=True)

class UserOrderSchema(Schema):
    id = fields.Int(dump_only=True)
    # user_id = fields.Int(required=True)
    # equipment_id = fields.Int(required=True)
    time_of_order = fields.DateTime(required=True, default=datetime.utcnow)
    user = fields.Nested('UserSchema', dump_only=True)
    equipment = fields.Nested('EquipmentSchema', dump_only=True)

class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class EquipmentConditionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class EquipmentRepairSchema(Schema):
    id = fields.Int(dump_only=True)
    date_of_repair = fields.Date(required=True)
    # worker_id = fields.Int(required=True)
    # equipment_id = fields.Int(required=True)
    worker = fields.Nested('WorkerSchema', dump_only=True)
    equipment = fields.Nested('EquipmentSchema', dump_only=True)

class EquipmentTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class LaserCutterOrderSchema(Schema):
    id = fields.Int(dump_only=True)
    time_of_start = fields.DateTime(required=True)
    time_of_end = fields.DateTime(required=True)
    # user_id = fields.Int(required=True)
    # laser_cutter_id = fields.Int(required=True)
    user = fields.Nested('UserSchema', dump_only=True)
    laser_cutter = fields.Nested('LaserCutterSchema', dump_only=True)

class LaserCutterRepairSchema(Schema):
    id = fields.Int(dump_only=True)
    date_of_repair = fields.Date(required=True)
    # worker_id = fields.Int(required=True)
    # laser_cutter_id = fields.Int(required=True)
    worker = fields.Nested('WorkerSchema', dump_only=True)
    laser_cutter = fields.Nested('LaserCutterSchema', dump_only=True)

class LaserCutterSchema(Schema):
    id = fields.Int(dump_only=True)
    model = fields.Str(required=True)
    serial_number = fields.Str(required=True)
    # equipment_condition_id = fields.Int(required=True)
    equipment_condition = fields.Nested('EquipmentConditionSchema', dump_only=True)

class WorkerPositionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class WorkerSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    phone_number = fields.Str()
    address = fields.Str()
    worker_position = fields.Nested('WorkerPositionSchema', dump_only=True)

class WorkerRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    phone_number = fields.Str(required=True)
    address = fields.Str(required=True)
    worker_position_id = fields.Int(required=True)

    @validates("worker_position_id")
    def validate_worker_position_id(self, value):
        exists = db.session.query(
            db.session.query(WorkerPositionModel).filter_by(id=value).exists()
        ).scalar()

        if not exists:
            raise ValidationError(f"Worker position with id={value} does not exist.")

class LaserCutterOrderEvaluationSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int()
    quality_score = fields.Int()

class LoginSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)