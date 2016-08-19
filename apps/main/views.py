#check migration file to make sure there are no dependencies!

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count
from .models import User, Trip
# Create your views here.
def index(request):
	return render(request, 'loginandreg/index.html')

def logout(request):
	request.session.clear()
	return redirect(reverse('loginandreg'))

def dashboard(request):
	user = User.objects.get(id=request.session['user'])
	trips = Trip.objects.all()
	context={
		'user':user,
		'trips':trips
	}
	return render(request, 'main/dashboard.html', context)

def add(request):
	user = User.objects.get(id=request.session['user'])
	return render(request, 'main/add_trip.html')

def create(request):
	date_from = request.POST['travel_date_from']
	date_to = request.POST['travel_date_to']
	import time
	# grabs time as string
	today = time.strftime('%b %d %Y')
	from datetime import datetime
	import re
	# regex ensures date matches format to convert properly for comparison
	DATE = re.compile(r'^[a-zA-Z][a-zA-Z][a-zA-Z] \d\d \d\d\d\d$')
	if not DATE.match(request.POST['travel_date_from']) or not DATE.match(request.POST['travel_date_to']):
		messages.add_message(request, messages.ERROR, 'Date must be in format Mmm DD YYYY')
	elif len(request.POST['travel_date_from'])<1 or len(request.POST['travel_date_to'])<1:
		messages.add_message(request, messages.ERROR, 'Date from and Date to fields cannot be blank')
		return redirect(reverse('add'))
	# if date has been provided correctly, converts into comparable datetime date.  Also adds today as datetime date so that date_from can be checked against current day.  
	else:
		date_from = datetime.strptime(request.POST['travel_date_from'], '%b %d %Y').date()
		date_to = datetime.strptime(request.POST['travel_date_to'], '%b %d %Y').date()
		today = datetime.strptime(today, '%b %d %Y').date()
	# packages everything in dict for Mr.Manager to perform the final validation
	new_trip = {
		'user': User.objects.get(id=request.session['user']),
		'destination': request.POST['destination'],
		'description': request.POST['description'],
		'travel_date_from': date_from,
		'travel_date_to': date_to,
		'today':today
	}
	trip = Trip.mrManager.plan(new_trip)
	# if mr.Manager's validation works out, we return true and go on our merry way.  Otherwise, prints all of the errors that were collected.  
	if trip == True:
		return redirect(reverse('dashboard'))
	if trip[0] == False:
		errors = trip[1]
		print trip[1]
		for key in trip[1]:
			messages.add_message(request, messages.ERROR, trip[1][key])
		return redirect(reverse('add'))

def destination(request, id):
	destination = Trip.objects.get(id=id)
	# filter is used to narrow our query to trips that match our destination - used to provide other users.  
	trips = Trip.objects.filter(destination=destination.destination)
	context={
		'destination':destination,
		'trips':trips
	}
	return render(request, 'main/destination.html', context)

def join(request, id):
	#grabs trip and user ids so that a new trip can be created for the current user with the same info.  
	trip = Trip.objects.get(id=id)
	user = User.objects.get(id=request.session['user'])
	newtrip = Trip.objects.create(destination=trip.destination, description=trip.description, travel_date_from=trip.travel_date_from, travel_date_to=trip.travel_date_to, user=user) 
	return redirect(reverse('dashboard'))

