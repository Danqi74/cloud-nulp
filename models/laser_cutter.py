from db import db

class LaserCutterModel(db.Model):
    __tablename__ = 'laser_cutter'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    equipment_condition_id = db.Column(db.Integer, db.ForeignKey('equipment_condition.id'), nullable=False)
    
    equipment_condition = db.relationship('EquipmentConditionModel', backref='laser_cutter', lazy=True)
