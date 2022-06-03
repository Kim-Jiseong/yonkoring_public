from django.contrib.auth import get_user_model
from webpush import send_user_notification
from .models import *
from django.templatetags.static import static

def send_notification():
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        payload = {"head": "연고링", "body": "테스트 메시지!"}
        send_user_notification(user=user, payload=payload, ttl=1000)

def send_notification_to_user(user, userfrom, message):
    my_nickname = Profile.objects.get(user=userfrom).nickname
    img_url = static('image 650.png')

    headMessage = "연고링 / " + my_nickname;
    payload = {"head": headMessage, "body": message, "icon": img_url, "url": "https://ykring.site/letter_rooms/"}
    send_user_notification(user=user, payload=payload, ttl=1000)