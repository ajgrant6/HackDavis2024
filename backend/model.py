from __future__ import annotations

import bcrypt

from app import db

from flask_login import UserMixin
from typing import Union

class User(UserMixin, db.Model):

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)

	# userType: 0 => admin, 1 => user
	userType = db.Column(db.Integer    , unique=False, nullable=False)
	username = db.Column(db.String(256), unique=True , nullable=False)
	password = db.Column(db.String(256), unique=False, nullable=False)

	def __init__(self, username, password, userType=1):

		self.userType = userType

		# Username and password cannot be blank.
		assert username != None and password != None

		# Username must be unique.
		assert User.query.filter_by(username=username).first() == None

		self.username = username
		self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(4))

	def get_user(id: int) -> Union[User, None]:
		"""
		Get a user using their ID. 
		"""

		return User.query.filter_by(id=id).first()

	def login(username: str, password: str) -> Union[User, None]:
		"""
		Log into an account.
		"""

		try:
			assert (user:=User.query.filter_by(username=username).first()) != None
			assert bcrypt.checkpw(password.encode(), user.password)
			return user
		except:
			return None

