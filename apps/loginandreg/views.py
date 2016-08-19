#check migration file to make sure there are no dependencies!

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	user = User.objects.all()
	return render(request, 'loginandreg/index.html')

def register(request):
	user=User.userManager.register(request.POST)
	if user == True:
		me = User.objects.get(username=request.POST['username'])
		request.session['user'] = me.id
		return redirect(reverse('dashboard'))
	if user[0] == False:
		errors = user[1]
		print user[1]
		for key in user[1]:
			messages.add_message(request, messages.ERROR, user[1][key])
		return redirect(reverse('loginandreg'))

def login(request):
	user = {
		'username':request.POST['username'],
		'password':request.POST['password']
	}
	user=User.userManager.login(user)
	if user == True:
		me = User.objects.get(username=request.POST['username'])
		request.session['user'] = me.id
		return redirect(reverse('dashboard'))
	if user[0] == False:
		messages.add_message(request, messages.ERROR, user[1]['failure'])
		return redirect(reverse('loginandreg'))