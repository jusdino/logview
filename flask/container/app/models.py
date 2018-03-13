# -*- encoding: utf-8 -*-

from app import db, app
from app.forms import LoginForm
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Integer, DateTime
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime


class User(db.Model):
    '''
    Self explanatory, I should think
    '''

    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True, nullable=False)
    email = Column(String(120), index=True, unique=True)
    failed_attempts = Column(Integer, nullable=False, default=0)
    password_hash = Column(String(255), nullable=False)
    password_expires = Column(DateTime)

    @property
    def password(self) -> str:
        '''
        For getting purposes, we'll consider password
        and password_hash to be synonymous.
        '''
        return self.password_hash

    @password.setter
    def password(self, password: str):
        '''
        Automatically hash passwords before storage
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self) -> bool:
        ''' So long as the password isn't expired
        '''
        if self.password_expires:
            return self.password_expires > datetime.datetime.utcnow()
        else:
            return True

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    @classmethod
    def from_form(cls, form: LoginForm):
        '''
        Find user described in form and check password
        '''
        user = cls.by_name(form.name.data)
        if user:
            if user.failed_attempts < app.config['MAX_LOGIN_ATTEMPTS'] \
                    and user.check_password(form.password.data):
                return user
            user.failed_attempts += 1
        return None

    @classmethod
    def by_name(cls, name: str):
        return cls.query.filter(User.name.ilike(name)).first()

    def get_id(self) -> str:
        return str(self.id)

    def __repr__(self):
        return "<User(id='{id}', name='{name}')>".format(
            id=self.id, name=self.name)
