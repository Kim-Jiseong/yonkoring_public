from django.db import models
from django.contrib.auth.models import AbstractUser, User, BaseUserManager
from django.conf import settings
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Transpose
from datetime import datetime




class Interest(models.Model):
    interest = models.CharField(verbose_name='관심사', max_length=50)

    def __str__(self):
        return self.interest

class Profile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='profile')
    profile_image =  ProcessedImageField( blank=True, null=True,
                                        upload_to='profile_images',  
                                           format='JPEG',
                                            processors=[ Transpose()] , 
                                           options={'quality': 40})
    phone_number = models.IntegerField(
        verbose_name='전화번호', blank=True, null=True)
    nickname = models.CharField(
        verbose_name='닉네임', max_length=20, blank=True, null=True)
    school = models.CharField(
        verbose_name='학교', max_length=20, blank=True, null=True)
    block_school = models.BooleanField(
        verbose_name='학교 안보이기', default=False, blank=True, null=True)
    age = models.TextField(verbose_name='나이', blank=True, null=True)
    gender = models.CharField(
        verbose_name='성별', max_length=20, blank=True, null=True)
    goal = models.CharField(
        verbose_name='목표', max_length=100, blank=True, null=True)
    bio = models.TextField(verbose_name='자기 소개', blank=True, null=True)
    mbti = models.CharField(verbose_name='mbti',
                            max_length=50, blank=True, null=True)
    interest = models.TextField(verbose_name='관심사', blank=True, null=True)
    club = models.CharField(
        verbose_name='동아리', max_length=150, blank=True, null=True)
    user_report = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='user_report', blank=True)
    address = models.CharField(
        verbose_name='주소', max_length=100, null=True, blank=True)
    want_gender = models.CharField(
        verbose_name='성별', max_length=20, blank=True, null=True)
    def __str__(self):
        return self.user.username+'/'+self.gender+'('+self.want_gender+')/'+self.school

# join 2를 작성하지 않은 사람읊 구분하기 위해 self_info를 분리
class Self_info(models.Model):
    user = models.ForeignKey(
        User, related_name='self_info', on_delete=models.CASCADE, blank=True, null=True)
    text = TextField(verbose_name="자기소개", blank=True, null=True)


class Friend_request(models.Model):
    requestor = models.ForeignKey(
        User, related_name='request_sent', on_delete=models.CASCADE, blank=True, null=True)
    responsor = models.ForeignKey(
        User, related_name='request_got', on_delete=models.CASCADE, null=True, blank=True)


class Friend_response(models.Model):
    requestor = models.ForeignKey(
        User, related_name='response_sent', on_delete=models.CASCADE, null=True, blank=True)
    responsor = models.ForeignKey(
        User, related_name='response_got', on_delete=models.CASCADE, null=True, blank=True)


class Letter_network(models.Model):
    users = models.ManyToManyField(
        User, related_name='Letter_network', blank=True)
    push_on = models.ManyToManyField(
    User, related_name='push_on', blank=True, default=None)
    update_at = models.DateTimeField(default=datetime.now())


class Letter(models.Model):
    letter_network = models.ForeignKey(
        Letter_network, related_name='letters', on_delete=models.CASCADE, null=True, blank=True)
    writer = models.ForeignKey(
        User, related_name='written_letter', on_delete=models.CASCADE, null=True, blank=True,)
    reader = models.ForeignKey(
        User, related_name='given_letter', on_delete=models.CASCADE, null=True, blank=True,)
    content = models.TextField(
        verbose_name='letter_content', blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    check_read = models.BooleanField(default=False)
    unseen_to = models.ManyToManyField(
        User, related_name='my_unseen', blank=True)

    def __str__(self):
        return self.content

class School_img(models.Model):
    image = models.ImageField(upload_to='school_images/',blank=True, null=True)
    user = models.ForeignKey(
        User, related_name='school_img', on_delete=models.CASCADE, null=True, blank=True)
    confirm = models.BooleanField(default=False, blank=True, null=True)
    def __str__(self):
        if self.confirm:
            return self.user.username +'/확인완료'
        else:
            return '필요/'+self.user.username


class Agree(models.Model):
    user=models.ForeignKey(
        User, related_name='agree', on_delete=models.CASCADE, null=True, blank=True)
    agree= models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        if len(self.user.phone_number.filter()):
            if len(self.user.profile.filter()):
                return self.user.phone_number.filter()[0].phone +'/' + self.user.profile.filter()[0].gender
            else:
                return self.user.phone_number.filter()[0].phone
        else:
            return self.user.username


class Phone(models.Model):
    user=models.ForeignKey(
        User, related_name='phone_number', on_delete=models.CASCADE, null=True, blank=True
    )
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        if len(self.user.profile.filter()):
            return self.phone +'/' + self.user.profile.filter()[0].gender
        else:
            return self.phone