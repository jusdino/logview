# -*- encoding: utf-8 -*-

from wtforms.fields.simple import TextField, PasswordField,\
    HiddenField
from wtforms.validators import Required
from flask_wtf.form import FlaskForm
from flask.globals import request
from urllib.parse import urlparse, urljoin
from werkzeug.utils import redirect
from flask.helpers import url_for


class RedirectForm(FlaskForm):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
#         super(RedirectForm, self).__init__(self, *args, **kwargs)
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class LoginForm(RedirectForm):
    name = TextField('User',
                     validators=[Required()])
    password = PasswordField('Password',
                             validators=[Required()])


class PasswordForm(FlaskForm):
    password = PasswordField('Enter old password',
                             validators=[Required()])
    password1 = PasswordField('Enter new password',
                              validators=[Required()])
    password2 = PasswordField('Repeat new password',
                              validators=[Required()])


def is_safe_url(target: 'url') -> bool:
    '''
    Returns true if url passes basic safety tests
    '''
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    '''
    Returns url encoded in 'next' argument if the url is safe
    '''
    target = request.args.get('next')
    if target and is_safe_url(target):
        return target
