from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
NAME = re.compile(r'^[a-zA-Z]+ [a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
	def register(self, new_user):
		messages={}
		if not NAME.match(new_user['name']):
			messages['name_match'] = 'Please enter a valid name (first and last)'
		if len(new_user['name'])<3:
			messages['name_length'] = 'Please enter your entire first and last name'
		if len(new_user['username'])<3:
			messages['username'] = 'Username must be longer than 3 characters'
		if len(new_user['password'])<8:
			messages['password_length'] = 'Password must be at least 8 characters'
		if new_user['password'] != new_user['confirm_password']:
			messages['password_match'] = 'Password and confirm password do not match'
		if messages:
			return False, messages
		else:
			password = new_user['password'].encode()
			hashed = bcrypt.hashpw(password, bcrypt.gensalt())
			user = User.objects.create(name = new_user['name'], username = new_user['username'], password = hashed)
			return True
	def login(self, user):
		messages = {}
		if User.objects.filter(username=user['username']):
			me=User.objects.get(username=user['username'])
			if bcrypt.hashpw(user['password'].encode(), me.password.encode())== me.password:
				return True
			else:
				messages['failure'] = 'Failed!'
				return False, messages
		else:
			messages['failure'] = 'Failed!'
			return False, messages

class User(models.Model):
	name = models.CharField(max_length=45)
	username = models.CharField(max_length=45)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	userManager = UserManager()
	objects = models.Manager()