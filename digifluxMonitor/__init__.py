from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Shivam@06@localhost/digiflux_monitor'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://krmjdikkogzcwk:65901849017fc8bc49d71872bc18613f901b5ec11131be8ede39e9b454f5985d@ec2-54-159-138-67.compute-1.amazonaws.com:5432/ddae6r1uom1ndp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# basedir = os.path.abspath(os.path.dirname(__file__))
# #Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')


#Initial db
db = SQLAlchemy(app)

#Init ma
ma = Marshmallow(app)

# from flasktree import models
from digifluxMonitor import routes