import secrets
import os

class Base:
    FLASK_APP = os.environ.get("FLASK_APP")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16)

class Development(Base):
    FLASK_ENV = os.environ.get("FLASK_ENV")
    DATABASE = os.environ.get("DATABASE")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

class Staging(Base):
    DATABASE = "d5pjjee5639vdt"
    POSTGRES_USER = "lwkpjzajnzxfbi"
    POSTGRES_PASSWORD = "a00b3c6741edc36ddf796ea948f820a58a90cf07104be13f7e0781034cb2d572"
    SQLALCHEMY_DATABASE_URI= "postgresql://lwkpjzajnzxfbi:a00b3c6741edc36ddf796ea948f820a58a90cf07104be13f7e0781034cb2d572@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/d5pjjee5639vdt"

class Production(Base):
    pass