from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    nick = db.Column(db.String(100), unique=True)
    mvs = db.relationship('Movies')
    # usr = db.relationship('Movies')
    wmvs = db.relationship('WannaSee')
    # ratings = db.relationship('Rating')


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # added by?
    # nick = db.Column(db.String(100), db.ForeignKey('user.nick'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    picture = db.Column(db.String(256))
    rating = db.Column(db.Integer)
    # avg_rating = db.relationship('Rating')
    # ratings = db.relationship('Rating')


class WannaSee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    streamings = db.Column(db.String)  # multiselect (Netflix, HBO Max, Amazon Prime)
    picture = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # added by?
    date = db.Column(db.DateTime(timezone=True), default=func.now())
