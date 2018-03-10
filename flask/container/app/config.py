# -*- encoding: utf-8 -*-
import os

DEBUG = os.environ.get('DEBUG') == 'true'
TESTING = os.environ.get('TESTING') == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY')
REDIS_URI = os.environ.get('REDIS_URI')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') == 'true'
CSRF_ENABLED = True
