"""yonkoring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from yk import views
from django.conf.urls import handler400, handler403, handler404, handler500
from django.contrib.auth import views as auth_views
# 오류 페이지 설정
handler400 = 'yonkoring.views.error_handle'
handler403 = 'yonkoring.views.error_handle'
handler404 = 'yonkoring.views.error_handle'
handler500 = 'yonkoring.views.error_handle_500'

urlpatterns = [
    # 카카오 로그인
    path('admin/', admin.site.urls),
    path('', include('yk.urls')),
    path('accounts/', include('allauth.urls')),
    path('friend_request', views.friend_request, name='friend_request'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('send_email/', views.send_email, name='send_email'),

    # Agora Route
    path('', include('ykagora.urls')),
    path('', include('registrations.urls')),
    path('', include('ykboard.urls')),
    path('friend_nono/', views.friend_nono, name='friend_nono'),
    # pwa
    path('', include('pwa.urls')),
    re_path(r'^webpush/', include('webpush.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
