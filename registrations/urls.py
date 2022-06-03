from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'registrations'

urlpatterns = [
    path('', main, name='main'),
    path('join/1', join1, name='join1'),
    path('join/2', join2, name='join2'),
    path('join/3', join3, name='join3'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    url(r'^change_password/$', change_password, name='change_password')
]