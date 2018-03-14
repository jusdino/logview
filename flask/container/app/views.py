# -*- encoding: utf-8 -*-

from flask import render_template

from app import app, socketio, lm, db
from app.forms import LoginForm, PasswordForm
from app.models import User
from flask_socketio import emit, disconnect
from flask.globals import request, session
from flask_login.utils import login_user, login_required, logout_user,\
    current_user
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
import sys
from functools import wraps


def sio_login_required(f):
    ''' Convenient login_required-like
    decorator that is SocketIO-friendly'''
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.from_form(form)
            if user:
                login_user(user)
                session['user_id'] = user.id
                if user.is_authenticated:
                    flash('Welcome back, {uname}!'.format(
                        uname=user.name))
                    return redirect(url_for('log_view'))
                flash('Please change your password!')
                return redirect(url_for('change_password'))
        flash('Invalid login')
    return render_template('login.html',
                           title='Log In',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/change', methods=['GET', 'POST'])
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            if form.password1.data == form.password2.data:
                current_user.password = form.password1.data
                current_user.password_expires = None
                db.session.commit()
                flash('Password changed!')
                return redirect(url_for('index'))
            else:
                flash("Passwords don't match!")
        else:
            flash('Incorrect password.')
    return render_template('change_password.html',
                           form=form)


@app.route('/logview')
@login_required
def log_view():
    return render_template('logview.html')


@socketio.on('connect')
@sio_login_required
def socket_connect():
    print('Connected!', file=sys.stderr)
    emit('message', '<Monitoring log file>\n')


@socketio.on('message')
@sio_login_required
def socket_message(message):
    print(message, file=sys.stderr)


@lm.user_loader
def load_user(uid) -> User:
    return User.query.get(int(uid))
