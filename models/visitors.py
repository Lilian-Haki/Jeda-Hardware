from sqlalchemy.orm import backref
from sqlalchemy.sql import func
from main import db
class Visitors(db.Model):
    __tablename__='visitors'
    id = db.Column(db.Integer, primary_key=True)
    patient_id=db.Column(db.Integer,db.ForeignKey('patients.id'))
    name=db.Column(db.String(80),  nullable=True)
    gender=db.Column(db.String(80),  nullable=True)
    visitor_pnone=db.Column(db.String(80),  nullable=True)
    visiting_time=db.Column(db.DateTime(timezone=True),server_default=func.now())
