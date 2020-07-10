from digifluxMonitor import db
from datetime import datetime

#Website Model
class Website(db.Model):
    __tablename__ = 'website'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    hostname = db.Column(db.String(100))
    env = db.Column(db.String(100))
    history = db.relationship('Pinghistory', backref = 'website', lazy=True)

    def __init__(self, name, hostname, env):
        self.name = name
        self.env = env
        self.hostname = hostname

# Ping History Model
class Pinghistory(db.Model):
    __tablename__ = 'pinghistory'
    id = db.Column(db.Integer, primary_key = True)
    batch_no = db.Column(db.Integer)
    date_time = db.Column(db.DateTime, default = datetime.utcnow)
    status = db.Column(db.String(100))
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'), nullable=False)

    def __init__(self, batch_no, date_time, status, website_id):
        self.batch_no = batch_no
        self.date_time = date_time
        self.status = status
        self.website_id = website_id