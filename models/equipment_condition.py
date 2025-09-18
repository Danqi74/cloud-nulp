from db import db

class EquipmentConditionModel(db.Model):
    __tablename__ = 'equipment_condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
