'''
Created on Mar 12, 2018

@author: jusdino
'''

from getpass import getpass
from app import db, models


# Get first user data, make them an admin
user = models.User.query.get(1)
if not user:
    name = input("Enter username:")
    email = input("Enter user email:")
    user = models.User(name=name,
                       email=email)
    db.session.add(user)
pwd = getpass("Enter user password:")
if pwd == getpass("Confirm password:"):
    user.password = pwd
    db.session.commit()
    print('Your user has been generated! The app is ready to start!')
else:
    print('Password match failed. Try again.')
