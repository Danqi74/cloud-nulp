from db import db

class UserOrderModel(db.Model):
    __tablename__ = 'user_order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    time_of_order = db.Column(db.DateTime, nullable=False)
    
    user = db.relationship("UserModel", backref="user_order")
    equipment = db.relationship("EquipmentModel", backref="user_order")