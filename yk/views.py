import requests
from urllib.parse import urlparse
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, AnonymousUser
import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from datetime import datetime
from yk.webpusher import send_notification, send_notification_to_user

from django.core.mail.message import EmailMessage

def send_email(request):
    subject = "message"
    to = ["hhncn4471@gmail.com"]
    from_email = "yonkoring21@gmail.com"
    message = "메지시 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()

@login_required(login_url='../')
def join_done(request):
    user = request.user
    if Self_info.objects.filter(user=user):
        my_school_auth = School_img.objects.filter(user=user)
        auth_count = my_school_auth.count()
        my_profile = Profile.objects.filter(user=user)
        if request.method == 'POST':
            my_profile.update(
                want_gender=request.POST['gender']
            )
            ctx ={
                'my_school_auth': auth_count,
                'want_gender': request.POST['gender'],
            }
            
            return render(request, 'join_done.html', ctx)
        
        if my_profile[0].want_gender:
            ctx ={
                'my_school_auth': auth_count,
                'want_gender': my_profile[0].want_gender
            }
        else:
            my_profile.update(
                want_gender='both'
            )
            ctx ={
                'my_school_auth': auth_count,
                'want_gender': 'both'
            }
        return render(request, 'join_done.html', ctx)
        
    else:
        return redirect('registrations:join1')
    


# def social_login(request):
#     user = request.user
#     ctx = {
#         'user': user
#     }
#     return render(request, 'login.html', ctx)

# # 로그인 require 추가하기


def profile(request):
    # 친구 요청
    user = request.user
    random_profile = Profile.objects.all().order_by('?')[0]
    random_pk = random_profile.user.pk
    self_info = Self_info.objects.get(user=random_pk)
    my_request = Friend_request.objects.filter(
        requestor=user, responsor=random_pk)

    ctx = {
        'profile': random_profile,
        'my_request': my_request.count(),
        'random_pk': random_pk,
        'self_info': self_info,
    }

    return render(request, 'profile.html', ctx)

@login_required(login_url='../')
def call_end(request):
    # 친구 요청
    user = request.user
    random_profile = Profile.objects.all().order_by('?')[0]
    random_pk = random_profile.user.pk
    self_info = Self_info.objects.get(user=random_pk)
    my_request = Friend_request.objects.filter(
        requestor=user, responsor=random_pk)
    ctx = {
        'profile': random_profile,
        'my_request': my_request.count(),
        'random_pk': random_pk,
        'self_info': self_info,
    }

    return render(request, 'call_end.html', ctx)

@login_required(login_url='../')
def my_page(request):
    user = request.user
    my_profile = Profile.objects.filter(user=user)[0]
    if request.method == 'POST':
        # request_body라는 dict에서 user_pk의 value를 가져옴
        soon_friend = User.objects.get(pk=request.POST['user_pk'])

        # 내가 보낸 친구 수락 객체 생성
        Friend_response.objects.create(
            requestor=user,
            responsor=soon_friend,
        )
        # 내가 받은 친구 요청 객체 삭제
        try:
            Friend_request.objects.get(
                requestor=soon_friend,
                responsor=user,
            ).delete()
        except:
            return redirect('yk:my_page')

        friend_pk = request.POST['user_pk']
        # 둘의 쪽지 네트워크가 이미 있는 경우(이 경우는 사실 이미 친구인데 다시 만나서 친구 수락을 한 거임 >> 이상한 경우)
        if Letter_network.objects.filter(users=user).filter(users=User.objects.get(pk=friend_pk)):
            pass
        # 새롭게 쪽지 네트워크 생성
        else:
            new_network = Letter_network.objects.create(
            )
            new_network.users.add(User.objects.get(pk=friend_pk))
            new_network.users.add(user)
            # 쪽지 푸쉬 알림 켜는 것을 기본값으로
            new_network.push_on.add(User.objects.get(pk=friend_pk))
            new_network.push_on.add(user)

        # 내가 이 친구에게 보냈던 요청이 있을 경우 삭제 [내가 요청 받아줘서 친구 됐으니까 이제 불필요]
        try:
            needless_request = Friend_request.objects.filter(
                requestor=user).filter(responsor=soon_friend)
            if needless_request:
                needless_request.delete()
            return redirect('yk:my_page')
        except:
            return redirect('yk:my_page')

    # 친구 목록 구성[내가 포함되어 있는 Friend_response 객체 탐색]

    # resquestor가 유저인 경우
    friend_queryset1 = Friend_response.objects.filter(requestor=user)
    friend_list1 = []
    for query in friend_queryset1:
        friend_list1.append(query.responsor)

    # responsor가 사용자인 경우
    friend_queryset2 = Friend_response.objects.filter(responsor=user)
    friend_list2 = []
    for query in friend_queryset2:
        friend_list2.append(query.requestor)

    # 리스트 합산 [중복 제외, 사실 한 명이 수락하면 나머지 request는 자동 삭제되므로 중복되는 경우는 없을 것임]
    final_list = list(set(friend_list1) | set(friend_list2))

    friend_requests = Friend_request.objects.filter(
        responsor=request.user
    )

    ctx = {
        'friend_requests': friend_requests,
        'final_list': final_list,
        'my_profile': my_profile,
    }

    return render(request, 'my_page.html', ctx)


def webpush(request): # 테스트용 html, 작업 완료후엔 삭제 예정
    send_notification()
    print("Hello")
    return render(request, 'webpush.html')

@login_required(login_url='../')
@csrf_exempt
def friend_request(request):
    # 비동기 처리를 위한  과정
    # request.body(string, detail.html에서 stringify해서 보냈잖아)를 dict로 변환
    request_body = json.loads(request.body)
    # request_body라는 dict에서 user_pk의 value를 가져옴
    user_pk = request_body['user_pk']
    existing_request = Friend_request.objects.filter(
        requestor=request.user,
        responsor=User.objects.get(pk=user_pk)
    )
    # 친구 요청 이미 누른 경우[기존의 친구요청을 취소]
    if existing_request.count() > 0:
        existing_request.delete()

    # 친구 요청 새로 누르는 경우
    else:
        Friend_request.objects.create(
            requestor=request.user,
            responsor=User.objects.get(pk=user_pk),
        )

    my_request = Friend_request.objects.filter(
        requestor=request.user,
        responsor=User.objects.get(pk=user_pk)
    )

    response = {
        'my_request': my_request.count(),
    }  # dict형태

    return HttpResponse(json.dumps(response))  # dict를 string으로 바꿔서 보내줌

@login_required(login_url='../')
def friend_list(request):
    user = request.user
    # requestor가 사용자인 경우
    friend_queryset1 = Friend_response.objects.filter(requestor=user)
    friend_list1 = []
    for query in friend_queryset1:
        friend_list1.append(query.responsor)

    # responsor가 사용자인 경우
    friend_queryset2 = Friend_response.objects.filter(responsor=user)
    friend_list2 = []
    for query in friend_queryset2:
        friend_list2.append(query.requestor)

    # 리스트 합산 [중복 제외]
    final_list = list(set(friend_list1) | set(friend_list2))
    ctx = {
        'final_list': final_list
    }

    return render(request, 'friend_list.html', ctx)


@login_required(login_url='../')
def my_profile(request):
    user = request.user
    my_profile = Profile.objects.filter(user=user)
    address_more = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']

    if request.method == 'POST':
        # 유저 프로필이 이미 있는 경우 create이 불가하므로 업데이트로 하기
        if my_profile:
            try:
                # 중복 및 중복 등록 방지를 위해 파일명에 유저명 부여
                username = request.user.username
                request.FILES['image'].name = username
                my_profile[0].profile_image = request.FILES['image']
                my_profile[0].save()
            except:
                pass
            
            my_profile.update(
                    nickname=request.POST['name'],
                    phone_number=request.POST.get('onlyNumber'),
                    school=request.POST['school'],
                    age=request.POST['age'],
                    mbti=request.POST['mbti'],
                    gender=request.POST['gender'],
                    bio=request.POST['introduce1'],
                    interest=request.POST['interest'],
                    goal=request.POST['introduce2'],
                    club=request.POST['introduce3'],

                )
            if request.POST['address'] == '서울':
                my_profile.update(address=request.POST['address']+ ' ' +request.POST['address_more'])
            else:
                my_profile.update(address=request.POST['address'])
                
            my_selfInfo = Self_info.objects.get(user=user)
            my_selfInfo.text = request.POST['self_info']
            my_selfInfo.save()

        return redirect('yk:my_page')
        
    my_profile1 = Profile.objects.filter(user=user)[0]
    my_info = Self_info.objects.get(user=user)
    ctx = {
        'user': user,
        'my_profile': my_profile1,
        'my_info': my_info,
        'address_more':address_more,
    }

    return render(request, 'my_profile.html', ctx)

@login_required(login_url='../')
def letter_main(request):
    user = request.user
    
    result = {}
    letter_networks = Letter_network.objects.filter(users=user)
    letter_networks = letter_networks.order_by('-update_at')
    for letter_network in letter_networks:
        try:
            friend = letter_network.users.all().exclude(username=user.username)[0]
            seen_letters = letter_network.letters.exclude(unseen_to=user).order_by('created_at')
            letter_content = seen_letters.last().content
            result[friend] = letter_content
        except:
            result[friend] = None

    friend_queryset1 = Friend_response.objects.filter(requestor=user)
    friend_list = []
    for query in friend_queryset1:
        friend_list.append(query.responsor)

    # responsor가 사용자인 경우
    friend_queryset2 = Friend_response.objects.filter(responsor=user)
    for query in friend_queryset2:
        friend_list.append(query.requestor)

    # 내가 읽지 않은 메시지를 확인하기 위한 딕셔너리 만들기
    result2 = {}
    for friend in friend_list:
        try:
            this_network_query = Letter_network.objects.filter(
                users=user).filter(users=friend)
            recent_network = this_network_query[len(this_network_query)-1]
            # 이 친구와 나의 네트워크의 편지 중에서 내가 읽지 않은 편지가 있나 확인
            unread = recent_network.letters.filter(
                reader=user).filter(check_read=False).count()
            result2[friend] = unread
        except:
            result2[friend] = 0

    # 친구가 없는 경우를 예외 처리하기 위함
    friend_count = len(friend_list)
    return render(request, 'letter_main.html', {'friend_count': friend_count, 'result': result, 'result2': result2})

@login_required(login_url='../')
def letter_detail(request, friend_pk):
    friend = User.objects.get(pk=friend_pk)
    user = request.user
    # 친구와 내가 속해 있는 쪽지 네트워크 필터링
    this_network = Letter_network.objects.filter(
        users=friend).filter(users=user)
    recent_network = this_network[len(this_network)-1]
    if request.method == 'POST':
        if user in recent_network.push_on.all():
            recent_network.push_on.remove(user)
            return redirect('yk:letter_detail', friend_pk)
        recent_network.push_on.add(user)
        return redirect('yk:letter_detail', friend_pk)
    # 그중 가장 최신 네트워크의 쪽지들[사실 네트워크가 두개면 안 됨]
    this_letters = recent_network.letters.exclude(unseen_to=user).order_by('-created_at')
    # 현재 메시지중 나에게 온 메시지 모두 읽음 처리
    letters_to_me = this_letters.filter(reader=user)
    for letter in letters_to_me:
        letter.check_read = True
        letter.save()
    current_time = datetime.now()

    if user in recent_network.push_on.all():
        on = 'o'
    else:
        on = ''

    return render(request, 'letter_detail.html', {'friend': friend, 'letters': this_letters, 
    'current_time': current_time, 'on': on})

@login_required(login_url='../')
def letter_write(request, friend_pk):
    friend = User.objects.get(pk=friend_pk)
    this_network = Letter_network.objects.filter(
        users=request.user).filter(users=friend)
    recent_network = this_network[len(this_network)-1]
    if request.method == 'POST':
        Letter.objects.create(
            writer=request.user,
            reader=friend,
            content=request.POST['letter_content'],
            letter_network=this_network[len(this_network)-1],
        )
        recent_network.update_at = datetime.now()
        recent_network.save()
        if friend in recent_network.push_on.all():
            send_notification_to_user(friend, request.user, request.POST['letter_content'])
        return redirect('yk:letter_detail', friend_pk)

    return render(request, 'letter_write.html', {'friend': friend})

@login_required(login_url='../')
def stop_friend(request, friend_pk):
    # 친구요청 객체(친구 리스트를 구성하는 객체) 삭제 1
    try:
        for bad_friend in Friend_response.objects.filter(requestor=request.user).filter(responsor=User.objects.get(pk=friend_pk)):
            bad_friend.delete()
    except:
        pass
    # 친구요청 객체(친구 리스트를 구성하는 객체) 삭제 2
    try:
        for bad_friend in Friend_response.objects.filter(requestor=User.objects.get(pk=friend_pk)).filter(responsor=request.user):
            bad_friend.delete()
    except:
        pass

    bad_networks = Letter_network.objects.filter(
        users=request.user).filter(users=User.objects.get(pk=friend_pk))
    for bad_network in bad_networks:
        bad_network.delete()

    return redirect('yk:letter_main')

@login_required(login_url='../')
def call_page(request):
    return render(request, 'call_main.html')

@login_required(login_url='../')
def lobby(request):
    return render(request, 'lobby.html')

@login_required(login_url='../')
def hide_letter(request, friend_pk):
    friend = User.objects.get(pk=friend_pk)
    # 선택한 친구와의 쪽지 네트워크 및 그 네트워크에 속한 쪽지들 선택
    this_network = Letter_network.objects.filter(
        users=request.user).filter(users=friend)
    recent_network = this_network[len(this_network)-1]
    good_bye_letters = recent_network.letters.all()
    # 그 네트워크에 속한 쪽지들 모두의 unseen_to 속성에 현재 유저 객체 부여
    for letter in good_bye_letters:
        letter.unseen_to.add(request.user)

    return redirect('yk:letter_detail', friend_pk)

@login_required(login_url='../')
def school_auth(request):
    if request.method == 'POST':
        # 파일명에 유저 이름 부여
        username = request.user.username
        request.FILES['image'].name = username+' school_auth'

        if School_img.objects.filter(user=request.user):
            School_img.objects.filter(user=request.user).update(
                user=request.user,
                image=request.FILES['image'],
            )
        else:
            School_img.objects.create(
                user=request.user,
                image=request.FILES['image'],
            )
        return redirect('yk:join_done')

    return render(request, 'school_auth.html')

@login_required(login_url='../')
def friend_nono(request):
    friend_requestor = User.objects.get(pk=request.POST['user_pk'])
    
    these_requests = Friend_request.objects.filter(requestor= friend_requestor, responsor=request.user)
    for this_request in these_requests:
        this_request.delete()
    return redirect('yk:my_page')

@login_required(login_url='../')
def friend_profile(request, friend_pk):
    friend = User.objects.get(pk=friend_pk)
    friend_profile = Profile.objects.get(user=friend)
    self_info = Self_info.objects.get(user=friend)

    ctx = {
        'profile': friend_profile,
        'friend_pk': friend_pk,
        'self_info': self_info,
    }

    return render(request, 'friend_profile.html', ctx)
@login_required(login_url='../')
def rusure(request):
    return render(request, 'delete_user.html')
@login_required(login_url='../')
def delete_user(request):
    try:
        user = request.user
        this_profile = Profile.objects.get(user=user)
        this_image = this_profile.profile_image
        this_image.delete()
        
    except:
        pass
    this_user = request.user
    this_user.delete()
    return redirect('yk:join_done')
    
def love(request):
    return redirect('yk:join_done')