# -*- encoding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login.login_manager import LoginManager

app = Flask(__name__)

app.config.from_object('app.configuration')

lm = LoginManager(app)
db = SQLAlchemy(app)  # flask-sqlalchemy

socketio = SocketIO(app, message_queue=app.config['REDIS_URI'])

from app import views, models

lm.login_view = 'login'
