from pyexpat import model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Urls
from django.contrib import auth

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15,min_length=9)
    password = serializers.CharField(max_length=60, min_length = 6, write_only = True)
    tokens = serializers.CharField(max_length = 68, min_length = 6, read_only=True)

    class Meta:
        model = User
        fields = ('phone', 'password', 'tokens',)


    def validate(self, attrs):
        phone = attrs.get('phone','')
        password = attrs.get('password','')

        user = auth.authenticate(phone= phone, password=password)

        if not user:
            raise AuthenticationFailed("Invalid Credentials")

        return {
            'phone': user.phone,
            'tokens': user.tokens
        }



class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Urls
        fields = ('id', 'url','created_at','tag')
        extra_kwargs = {'id': {'read_only': True},'created_at':{'read_only': True}}