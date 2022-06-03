
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'yk'

urlpatterns = [
    path('main/', join_done, name='join_done'),
    
    path('profile/', profile, name='profile'),
    path('my_profile/', my_profile, name='my_profile'),
    path('friend_list/', friend_list, name='friend_list'),
    path('my_page/', my_page, name='my_page'),
    path('webpush/', webpush, name='webpush'),
    path('letter_rooms/', letter_main, name='letter_main'),
    path('<int:friend_pk>/letters', letter_detail, name='letter_detail'),
    path('letter_to/<int:friend_pk>', letter_write, name='letter_write'),
    path('<int:friend_pk>/stop_friend/', stop_friend, name='stop_friend'),
    path('<int:friend_pk>/hide_letter/', hide_letter, name='hide_letter'),
    path('school_auth/', school_auth, name='school_auth'),
    path('friend_profile/<int:friend_pk>', friend_profile, name='friend_profile'),
    path('user/goodbye', delete_user, name='delete_user'),
    path('rusure', rusure, name='rusure'),
    path('love/', love, name='love'),
    path('notice/', love, name='love'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
