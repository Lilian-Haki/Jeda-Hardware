from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from main import db

class Staff(db.Model):
    __tablename__ = 'staff'    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    department = db.Column(db.String(80), unique=False, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    telephone = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable = False)

    appointments = db.relationship('Appointment', backref='staff', lazy=True)
    # patients = db.relationship('Patient', backref='staff', lazy=True)

    def insert(self):
        db.add(self)
        db.commit()

        return self

    # @classmethod
    # def find_user_byId(cls, user_id):
    #     return cls.query.filter_by(id = user_id).first()

    # authenticate password
    @classmethod
    def check_password(cls,email,password):
        record = cls.query.filter_by(email=email).first()

        if record and check_password_hash(record.password, password):
            return True
        else:
            return False

    @classmethod
    def check_email_exists(cls, email):
        record = cls.query.filter_by(email = email).first()

        if record:
            return True
        else:
            return False

    # fetch by email
    @classmethod
    def fetch_by_email(cls,email):
        return cls.query.filter_by(email = email).first()