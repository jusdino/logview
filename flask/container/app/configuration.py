# -*- encoding: utf-8 -*-
import os
from uuid import uuid4

# Required config variables
REDIS_URI = os.environ.get('REDIS_URI')

# Optional config variables
DEBUG = os.environ.get('DEBUG') == 'true'
TESTING = os.environ.get('TESTING') == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY') \
        or uuid4().hex
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') \
        or 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS') == 'true'
MAX_LOGIN_ATTEMPTS = os.environ.get('MAX_LOGIN_ATTEMPTS') \
        or 5

# Not really configurable
CSRF_ENABLED = True
