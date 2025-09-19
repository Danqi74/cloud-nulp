from db import db

class EquipmentTypeModel(db.Model):
    __tablename__ = 'equipment_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # equipments = db.relationship('EquipmentModel', backref='equipment_type', lazy=True)