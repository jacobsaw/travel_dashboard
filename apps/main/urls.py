from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='loginandreg'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^dashboard/logout$', views.logout, name='logout'),
    url(r'^dashboard/add$', views.add, name='add'),
    url(r'^dashboard/create$', views.create, name='create'),
    url(r'^dashboard/destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^dashboard/join/(?P<id>\d+)$', views.join, name='join'),
]