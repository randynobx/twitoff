"""Flask Models"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """User Table"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    username = DB.Column(DB.String, nullable=False)
    
    def __repr__(self) -> str:
        return f'<User: {self.username}>'


class Tweet(DB.Model):
    """Tweet Table"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vector = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(
        DB.BigInteger,
        DB.ForeignKey('user.id')
    )
    user = DB.relationship(
        'User',
        backref=DB.backref('tweets', lazy=True)
    )
    
    def __repr__(self) -> str:
        return f'<Tweet: {self.text}>'
