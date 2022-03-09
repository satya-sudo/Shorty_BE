from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
import  string
import random
import datetime

base_url =  "shty1.herokuapp.com/api/a/"

def GetPrefixId():
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))  # generate 4 length random string
    x = datetime.datetime.now()
    randomStr = base_url + f'{x.strftime("%M")}{res}' + "/"
    return randomStr

import uuid


class UserManage(BaseUserManager):
    def create_user(self,phone,password):
        if phone is None:
            raise ValueError("User must have a phone number")
        if password is None:
            raise ValueError("User must have a password")
        user = self.model(phone=phone)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,phone,password):
        user = self.create_user(phone,password)
        user.is_superuser = True
        user.save()
        return user
    

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone'

    objects = UserManage()

    def __str__(self):
        return self.phone

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return refresh.access_token


class Urls(models.Model):
    id  =  models.CharField(max_length=100, primary_key=True,unique=True,default=GetPrefixId)
    url = models.CharField(max_length=100,)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    created_at = models.DateTimeField(auto_now_add=True)
    visits  = models.IntegerField(default=0)
    tag = models.CharField(max_length=20, blank=True,default="Others")
