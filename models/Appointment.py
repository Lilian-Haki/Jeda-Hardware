from sqlalchemy.orm import backref
from main import db

class Appointment(db.Model):
    __tablename__ = 'appointments'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    patient = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor = db.Column(db.Integer, db.ForeignKey('staff.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    triage_report = db.Column(db.Text)
    symptoms_report = db.Column(db.Text)
    medication_report = db.Column(db.Text)
    other_remarks = db.Column(db.Text)
    lab_report = db.Column(db.Text)
    status = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())