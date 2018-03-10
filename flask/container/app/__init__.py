# -*- encoding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)

# app.config.from_object('configuration.ProductionConfig')
app.config.from_object('app.config')
# app.config.from_object('configuration.TestingConfig')

db = SQLAlchemy(app)  # flask-sqlalchemy

socketio = SocketIO(app, message_queue=app.config['REDIS_URI'])

from app import views, models
