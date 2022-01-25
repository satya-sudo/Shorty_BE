from functools import partial
from django.shortcuts import render
from .models import User
from .serializers import RegistrationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter, SearchFilter


from rest_framework import generics

from api import serializers
from api.filters import IsOwnerFilterBackend





class RegisterUser(generics.GenericAPIView):
    
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response({'data':user_data,'status':True}, status=201)


class LoginAPIView(generics.GenericAPIView):
    
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({'data':serializer.data,'status':True}, status= 200)


class UrlList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UrlSerializer

    def get_queryset(self):
        return self.request.user.urls.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)