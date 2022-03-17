import re
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from ..models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *


class SignupAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = SignupSer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'Success': 'user created successfully', 'data': data}, status=HTTP_200_OK)
        return Response({'Error': 'Something went wrong'}, status=HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSer(data=request.data)
        if serializer.is_valid():
            return Response({'Success': 'login successfully', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'Error': 'Login failed'}, status=HTTP_400_BAD_REQUEST)

TITLE_CHOICES = [
    ('1', 'Superuser_user'),
    ('2', 'Teacher'),
    ('3', 'Student')
]

class AdminUserCreateView(APIView):
    permission_classes = [IsAdminUser, ]
    def post(self, request):
        try:
            User.objects.get(username=request.data.get('username')).exist()
            return Response({'error': 'User already exists'}, status=HTTP_400_BAD_REQUEST)
        except:
            if request.data.get('user_type')=='2':
                obj=User.objects.create(username=request.data.get('username'),email=request.data.get('email'),mobile=request.data.get('mobile'), user_type='3',is_staff=True,is_superuser=False,gender=request.data.get('gender'),image=request.data.get('image'),branch=request.data.get('branch'))
                obj.set_password(request.data.get('password')) 
                obj.save()
                return Response({'Done': 'profile added succesfully', 'data': True}, status=HTTP_200_OK)
            else:
                obj=User.objects.create(username=request.data.get('username'),email=request.data.get('email'),mobile=request.data.get('mobile'), user_type='3',is_staff=False,is_superuser=False,gender=request.data.get('gender'),image=request.data.get('image'),branch=request.data.get('branch'))
                obj.set_password(request.data.get('password')) 
                obj.save()
                return Response({'Done': 'profile added succesfully', 'data': True}, status=HTTP_200_OK)
    
    def get(self, request):
        queryset = User.objects.all()
        serializer=ProfileSer(queryset,many=True)
        return Response(serializer.data,status=HTTP_200_OK)
        
class TeacherCreateView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        if request.user.is_staff==True:
            try:
                User.objects.get(username=request.data.get('username')).exist()
                return Response({'error': 'User already exists'}, status=HTTP_400_BAD_REQUEST)
            except:
                obj=User.objects.create(username=request.data.get('username'),is_active=True,is_staff=False,is_superuser=False,email=request.data.get('email'),mobile=request.data.get('mobile'),gender=request.data.get('gender'),image=request.data.get('image'),branch=request.data.get('branch'),user_type='3')
                obj.set_password(request.data.get('password'))
                return Response({'Done': 'profile added succesfully', 'data': True}, status=HTTP_200_OK)
        else:
            return Response({'Not Done': 'You are not authorised to do'}, status=HTTP_400_BAD_REQUEST)
    def get(self,request):
        queryset = User.objects.filter(is_active=True,is_staff=False,is_superuser=False)
        serializer=ProfileSer(queryset,many=True)
        return Response(serializer.data,status=HTTP_200_OK)

class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        queryset = User.objects.filter(username=request.user)
        serializer= ProfileSer(queryset,many=True)
        return Response(serializer.data,status=HTTP_200_OK)

class resetpassword(APIView):
    def post(self, request):

        serializer = resetpasswordSerializer(data=request.data)
        alldatas = {}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            alldatas['data'] ='successfully registered'
            print(alldatas)
            return Response(alldatas)
        return Response('failed retry after some time')



