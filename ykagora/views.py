import os
import time
import json

from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render

from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from pusher import Pusher
from django.views.decorators.csrf import csrf_exempt
from yk.models import *
from ykagora.models import *
from django.http import HttpResponse, response
import random



# Instantiate a Pusher Client
pusher_client = Pusher(app_id=os.environ.get('PUSHER_APP_ID'),
                       key=os.environ.get('PUSHER_KEY'),
                       secret=os.environ.get('PUSHER_SECRET'),
                       ssl=True,
                       cluster=os.environ.get('PUSHER_CLUSTER')
                       )

@login_required(login_url='/admin/')
@csrf_exempt
def index(request):
    my_school_auth = School_img.objects.filter(user=request.user)
    auth_count = my_school_auth.count()

    if request.method == "POST":
        request_body = json.loads(request.body)
        calleeID = request_body['calleeID']
        calleePRO = Profile.objects.filter(user=calleeID)[0]
        calleeSELFINFO = Self_info.objects.filter(user=calleeID)[0]
        my_request = Friend_request.objects.filter(requestor=request.user, responsor=User.objects.get(pk=calleeID))
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
        this_friend = User.objects.get(pk=calleeID)
        response = {
            'my_request': my_request.count(),
            'calleeIMG': calleePRO.profile_image.url,
            'calleeBIO': calleePRO.bio,
            'calleeNICKNAME': calleePRO.nickname,
            'calleeGENDER': calleePRO.gender,
            'calleeSELFINFO': calleeSELFINFO.text,
            'calleeGOAL': calleePRO.goal,
            'calleeAGE': calleePRO.age,
            'calleeSCHOOL': calleePRO.school,
            'calleeMBTI': calleePRO.mbti,
            'calleeADDRESS': calleePRO.address,
            'calleeCLUB': calleePRO.club,
            'calleeINTEREST': calleePRO.interest,
            'friend_pk': calleeID
        }
        if this_friend in final_list:
            response['check_friend'] = 'yes'
            
        
        return HttpResponse(json.dumps(response))

    else:
        ctx = {
            'callerId': request.user.id,   
            'auth_count': auth_count    
        }

    return render(request, 'ykagora/index.html', ctx)


def pusher_auth(request):
    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {
                'id': request.user.id,
                'name': request.user.username,
            }
        })
    return JsonResponse(payload)

# csrf_exempt는 일단 돌아가라고 해놓은 것...
# 아고라 동적 토큰 생성 함수
@csrf_exempt
def generate_agora_token(request):
    appID = os.environ.get('AGORA_APP_ID')
    appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
    channelName = json.loads(request.body.decode(
        'utf-8'))['channelName']
    userAccount = request.user.username
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithAccount(
        appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)

    return JsonResponse({'token': token, 'appID': appID})

def call_user(request):
    body = json.loads(request.body.decode('utf-8'))

    user_to_call = body['user_to_call']
    channel_name = body['channel_name']
    caller = User.objects.filter(id=request.user.id)[0]
    callee = User.objects.filter(id=user_to_call)[0]   
    callerGender = Profile.objects.filter(user=caller)[0].gender    #전화 건 사람의 성별
    calleeGender = Profile.objects.filter(user=callee)[0].gender  #전화 받는 사람의 성별
    callerWantGender = Profile.objects.filter(user=caller)[0].want_gender
    calleeWantGender = Profile.objects.filter(user=callee)[0].want_gender

    if (callerWantGender == calleeGender or callerWantGender == 'both') and (calleeWantGender == callerGender or calleeWantGender == 'both'):
        pusher_client.trigger(
            'presence-online-channel',
            'make-agora-call',
            {
                'userToCall': user_to_call,
                'channelName': channel_name,
                'from': request.user.id,
                'genderMatch': True
            },
        )
    else:
        pusher_client.trigger(
            'presence-online-channel',
            'make-agora-call',
            {
                'userToCall': user_to_call,
                'channelName': channel_name,
                'from': request.user.id,
                'genderMatch': False
            },
        )

    return JsonResponse({'message': 'call has been placed'})


def check_callable_state (request):
    body = json.loads(request.body.decode('utf-8'))
    caller_id = body['caller_id']
    is_unable_to_call = body['is_unable_to_call']
    pusher_client.trigger(
        'presence-online-channel',
        'get-callable-state-from-callee',
        {
            'caller_id': caller_id,
            'is_unable_to_call': is_unable_to_call,
        },
    )

    return JsonResponse({'message': 'call has been rejected'})


def add_callable_users (request):
    body = json.loads(request.body.decode('utf-8'))
    id = body['id']
    name = body['name']
    pusher_client.trigger(
        'presence-online-channel',
        'add-callable-users',
        {
            'id': id,
            'name': name,
        },
    )

    return JsonResponse({'message': 'add callableUsers list has been executed'})

def send_accept_message (request):
    body = json.loads(request.body.decode('utf-8'))
    opponent_id = body['opponent_id']
    pusher_client.trigger(
        'presence-online-channel',
        'get-accept-message-from-opponent',
        {
            'opponent_id': opponent_id,
        },
    )

    return JsonResponse({'message': 'Send accept message has been executed'})
@csrf_exempt
def game(request):
    game_list = Game.objects.all()
    game = random.choice(game_list)

    if request.method == "POST":
        response = {
            'game': game.content
        }
        return HttpResponse(json.dumps(response))