from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
import time
from datetime import date

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)
    #timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    timestamp = db.Column(db.TIMESTAMP, default=func.now())

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words
        self.timestamp = func.timezone('UTC', func.now())
        #self.timestamp = date.fromtimestamp(time.time()) no time        
        #self.timestamp = func.timezone('UTC', func.current_timestamp())
        #self.timestamp = func.timezone('UTC', func.localtimestamp())
        #https://www.postgresql.org/docs/9.2/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT

    def __repr__(self):
        return '<id {}>'.format(self.id)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    userpassword = db.Column(db.String())    
    createdtime = db.Column(db.TIMESTAMP, default=func.now())

    def __init__(self, username, userpassword):
        self.username = username
        self.userpassword = userpassword        
        self.createdtime = func.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)
