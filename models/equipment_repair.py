from db import db

class EquipmentRepairModel(db.Model):
    __tablename__ = 'equipment_repair'
    id = db.Column(db.Integer, primary_key=True)
    date_of_repair = db.Column(db.Date, nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    
    worker = db.relationship('WorkerModel', backref='equipment_repair', lazy=True)
    equipment = db.relationship('EquipmentModel', backref='equipment_repair', lazy=True)