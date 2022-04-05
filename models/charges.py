from sqlalchemy.orm import backref
from sqlalchemy.sql import func
from main import db

class Charges(db.Model):
    __tablename__='charges'
    id = db.Column(db.Integer, primary_key=True)
    patient_id=db.Column(db.Integer,db.ForeignKey('patients.id'))
    inventory_id=db.Column(db.Integer,db.ForeignKey('inventory.id'))
    service_offered=db.Column(db.String(80),  nullable=True)
    cost=db.Column(db.Integer, nullable=True)
    time_of_offering=db.Column(db.DateTime(timezone=True),server_default=func.now())