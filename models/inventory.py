from unicodedata import category
from sqlalchemy.orm import backref
from main import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),  nullable=False)
    category=db.Column(db.String(80), nullable=False)
    selling_price = db.Column(db.Integer, nullable=False)
    rel = db.relationship('Charges', backref='inventory', lazy=True)  
    