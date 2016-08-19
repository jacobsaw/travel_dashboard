from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='loginandreg'),
    url(r'^registration$', views.register, name='registration'),
    url(r'^login$', views.login, name='login'),
]