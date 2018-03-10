# -*- encoding: utf-8 -*-

from flask import render_template

from app import app, socketio
from app.forms import ExampleForm, LoginForm
from app.models import User
from flask_socketio import emit
import sys


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logview')
def log_view():
    return render_template('logview.html')


@app.route('/test')
def test():
    return render_template('test.html')


@socketio.on('connect')
def socket_connect():
    print('Connected!', file=sys.stderr)
    emit('message', '<Monitoring log file>\n')

@socketio.on('message')
def socket_message(message):
    print(message, file=sys.stderr)
