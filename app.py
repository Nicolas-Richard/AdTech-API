from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
api = Api(app)



