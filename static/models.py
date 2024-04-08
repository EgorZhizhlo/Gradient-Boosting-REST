from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class MODELS(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    totsp = db.Column(db.String(300), unique=False, nullable=False)
    dist = db.Column(db.String(300), unique=False, nullable=False)
    metrdist = db.Column(db.String(300), unique=False, nullable=False)
    walk = db.Column(db.String(300), unique=False, nullable=False)
    price = db.Column(db.String(300), unique=False, nullable=False)
    pred = db.Column(db.String(300), unique=False, nullable=False)
    error = db.Column(db.String(300), unique=False, nullable=False)


with app.app_context():
    db.create_all()
