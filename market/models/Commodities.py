from flask_sqlalchemy import SQLAlchemy
from market import db

class Commodities(db.Model):
    __tablename__ = 'market'  # Must match MySQL table name

    id = db.Column(db.Integer, primary_key=True)
    commodity_type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), unique=True, nullable=False)

