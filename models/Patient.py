from sqlalchemy.orm import backref
from sqlalchemy.sql import func
from main import db

class Patient(db.Model):
    __tablename__ = 'patients'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(80), unique=False, nullable=False)
    telephone = db.Column(db.String(80), unique=False, nullable=False)
    guardian_name=db.Column(db.String(80), unique=False, nullable=True)
    guardian_phone_no=db.Column(db.String(80), unique=False, nullable=True)
    registering_time=db.Column(db.DateTime(timezone=True),server_default=func.now())
    appointments = db.relationship('Appointment', backref='patients', lazy=True)
    appointmen = db.relationship('Charges', backref='patients', lazy=True)
    appointme = db.relationship('Visitors', backref='patients', lazy=True)