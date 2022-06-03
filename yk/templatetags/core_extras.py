from django.template.defaulttags import register
from ..models import Letter_network
from django.contrib.auth.models import User

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.inclusion_tag('check_letter.html')
def check_letter(username):
    user = User.objects.get(username=username)
    my_networks = Letter_network.objects.filter(users=user)
    # 이 친구와 나의 네트워크의 편지 중에서 내가 읽지 않은 편지가 있나 확인
    for my_network in my_networks:
        try:
            if my_network.letters.filter(reader=user).filter(check_read=False).count() > 0:
                return {'unread': 'o'}
        except:
            pass
    
