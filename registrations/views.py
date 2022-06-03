from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from yk.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def main(request):
    if request.method == 'POST':
        username = request.POST['username']
        found_user = auth.authenticate(
            username=username,
            password=request.POST['password']
        )
        if found_user == None:
            error = '아이디 혹은 비밀번호가 틀렸습니다'
            return render(request, 'main.html', {'error': error, 'username': username})
        else:
            auth.login(request, found_user)
            # 로그인 했는데 프로필이 없을 때
            if len(request.user.profile.all()) == 0:
                return redirect('registrations:join1')
            # 로그인 했는데 프로필이 있을 때
            else:
                return redirect('yk:join_done')
    
    if request.user.is_authenticated:
        # 로그인 되어있는데 프로필이 있을 때
        if len(request.user.profile.all()) > 0:
            return redirect('yk:join_done')
        # 로그인 되어있는데 프로필이 없을 때
        else:
            return redirect('registrations:join1')
    else:
        return render(request, 'main.html')


@login_required(login_url='../')
@csrf_exempt
def join1(request):
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
                    school=request.POST['school'],
                    age=request.POST['age'],
                    mbti=request.POST['mbti'],
                    gender=request.POST['gender'],
                    bio=request.POST['introduce'],
                )
            if request.POST['address'] == '서울':
                my_profile.update(address=request.POST['address']+ ' ' +request.POST['address_more'])
            else:
                my_profile.update(address=request.POST['address'])
                
            return redirect('registrations:join2')

        # 유저 프로필이 없다면 새로 create
        else:
            if request.POST['address'] == '서울':
                new_profile = Profile.objects.create(
                    user=user,
                    nickname=request.POST['name'],
                    school=request.POST['school'],
                    age=request.POST['age'],
                    mbti=request.POST['mbti'],
                    gender=request.POST['gender'],
                    bio=request.POST['introduce'],
                    address=request.POST['address']+ ' ' +request.POST['address_more'],
                    want_gender='both'
                )
                username = request.user.username
                request.FILES['image'].name = username
                new_profile.profile_image = request.FILES['image']
                new_profile.save()

            else:
                new_profile = Profile.objects.create(
                    user=user,
                    nickname=request.POST['name'],
                    school=request.POST['school'],
                    age=request.POST['age'],
                    mbti=request.POST['mbti'],
                    gender=request.POST['gender'],
                    bio=request.POST['introduce'],
                    address=request.POST['address'],
                    want_gender='both'
                )

                username = request.user.username
                request.FILES['image'].name = username
                new_profile.profile_image = request.FILES['image']
                new_profile.save()

            return redirect('registrations:join2')

    if my_profile:
        ctx = {
            'user': user,
            'my_profile': my_profile[0],
            'address_more':address_more
        }
        return render(request, 'join1.html', ctx)
    else:
        ctx = {
            'address_more':address_more
        }
        return render(request, 'join1.html', ctx)

@login_required(login_url='../')
def join2(request):
    user = request.user
    my_self = Self_info.objects.filter(user=user)
    # post일때
    if request.method == 'POST':
        # join2를 처음 작성하는 경우
        if not my_self:
            my_profile = Profile.objects.filter(user=user)[0]
            my_profile.goal = request.POST['introduce']
            my_profile.save()
            Self_info.objects.create(
                user=user,
                text=request.POST['self_info'],
            )
            return redirect('registrations:join3')
        # join2를 이미 작성했고, 수정하는 경우
        else:
            my_profile = Profile.objects.filter(user=user)[0]
            my_profile.goal = request.POST['introduce']
            my_profile.save()
            Self_info.objects.filter(user=user).update(
                user=user,
                text=request.POST['self_info'],
            )
            return redirect('registrations:join3')
    # get일때
    # join2를 처음 작성하는 경우
    if not my_self:
        return render(request, 'join2.html')
    # join2를 이미 작성했고, 수정하는 경우
    else:

        ctx = {
            'user': user,
            'self_info': my_self[0].text,
            'goal': Profile.objects.filter(user=user)[0].goal
        }
        return render(request, 'join2.html', ctx)

@login_required(login_url='../')
def join3(request):
    user = request.user
    if request.method == 'GET':
        ctx = {
            'user': user
        }
        return render(request, 'join3.html', ctx)
    elif request.method == 'POST':
        my_profile = Profile.objects.filter(user=user)[0]
        my_profile.club = request.POST['introduce']
        my_profile.interest = request.POST['interest']
        my_profile.save()
        return redirect('yk:join_done')



def signup(request):
    if request.method == "POST":
        found_user = User.objects.filter(username=request.POST['username'])
        if len(found_user) > 0:
            error = '이미 존재하는 아이디입니다'
            return render(request, 'signup.html', {'error': error})
        new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email = request.POST['username']
            )
        agree_items = request.POST.getlist('agree_items[]')
        if agree_items[-1] == 'mkAgree':
            Agree.objects.create(
                user=new_user,
                agree=True,
            )
            
        Phone.objects.create(
            user=new_user,
            phone=request.POST['phone_number']

        )
        
        auth.login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('registrations:join1')
        
    return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('registrations:main')

@login_required(login_url='../')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('registrations:main')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
    