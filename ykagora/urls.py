from django.urls import path
from . import views

app_name = 'ykagora'

urlpatterns = [
    path('call/', views.index, name='agora-index'),
    path('pusher/auth/', views.pusher_auth, name='agora-pusher-auth'),
    path('token/', views.generate_agora_token, name='agora-token'),
    path('call-user/', views.call_user, name='agora-call-user'),
    path('check-callable-state/', views.check_callable_state, name='agora-check-callable-state'),
    path('send-accept-message/', views.send_accept_message, name='agora-send-accept-message'),
    path('add-callable-users/', views.add_callable_users, name='agora-add-callable-users'),
    path('game/', views.game, name='agora-game'),
]