from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'ykboard'

urlpatterns = [
    path('home/', home, name='home'),
    path('new/', new, name='new'),
    path('detail/<int:post_pk>', detail, name='detail'),
    path('like/', like, name='like'),
    path('edit/<int:post_pk>', edit, name='edit'),
    path('delete/<int:post_pk>', delete, name='delete'),
    path('comment/delete/<int:post_pk>/<int:comment_pk>', comment_delete, name='comment_delete'),
    path('my_post/', my_post, name='my_post'),
    path('my_comment/', my_comment, name='my_comment'),
    path('yk_update/', yk_update, name='yk_update'),
]