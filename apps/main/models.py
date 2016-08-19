from __future__ import unicode_literals

from django.db import models
from ..loginandreg.models import User
# Create your models here.

class MrManager(models.Manager):
	def plan(self, new_trip):
		# creates dictionary of error messages to send back after return
		messages={}
		if len(new_trip['destination'])<1:
			messages['destination'] = 'Please provide a destination'
		if len(new_trip['description'])<1:
			messages['description'] = 'Please provide a description'
		# checks to make sure that date to is after date from
		if new_trip['travel_date_to']< new_trip['travel_date_from']:
			messages['date'] = 'Please ensure date to is after date from'
		# checks to make sure that date from is after today
		if new_trip['travel_date_from']<=new_trip['today']:
			messages['date_future'] = 'Please ensure date is in the future...future...future'
		# if any error messages exist, DOES NOT CREATE
		if messages:
			return False, messages
		else:
			trip = Trip.objects.create(destination = new_trip['destination'], description = new_trip['description'], travel_date_from = new_trip['travel_date_from'], travel_date_to = new_trip['travel_date_to'], user = new_trip['user'])
			return True

class Trip(models.Model):
	destination = models.CharField(max_length=45)
	description = models.CharField(max_length=1000)
	travel_date_from = models.CharField(max_length=45)
	travel_date_to = models.CharField(max_length=45)
	user = models.ForeignKey(User, related_name='usertrip')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	mrManager = MrManager()
	objects = models.Manager()
	
