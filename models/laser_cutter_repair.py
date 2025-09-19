from db import db

class LaserCutterRepairModel(db.Model):
    __tablename__ = 'laser_cutter_repair'
    id = db.Column(db.Integer, primary_key=True)
    date_of_repair = db.Column(db.Date, nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    laser_cutter_id = db.Column(db.Integer, db.ForeignKey('laser_cutter.id'), nullable=False)
    
    worker = db.relationship('WorkerModel', backref='laser_cutter_repair', lazy=True)
    laser_cutter = db.relationship('LaserCutterModel', backref='laser_cutter_repair', lazy=True)
