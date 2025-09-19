from db import db

class EquipmentModel(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False)
    equipment_type_id = db.Column(db.Integer, db.ForeignKey('equipment_type.id'), nullable=False)
    equipment_condition_id = db.Column(db.Integer, db.ForeignKey('equipment_condition.id'), nullable=False)
    
    equipment_type = db.relationship('EquipmentTypeModel', backref='equipment', lazy=True)
    equipment_condition = db.relationship('EquipmentConditionModel', backref='equipment', lazy=True)
