from db import db

class LaserCutterOrderModel(db.Model):
    __tablename__ = 'laser_cutter_order'
    id = db.Column(db.Integer, primary_key=True)
    time_of_start = db.Column(db.DateTime, nullable=False)
    time_of_end = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    laser_cutter_id = db.Column(db.Integer, db.ForeignKey('laser_cutter.id'), nullable=False)
    
    user = db.relationship("UserModel", backref="laser_cutter_order")
    laser_cutter = db.relationship("LaserCutterModel", backref="laser_cutter_order")
