import re
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from ..models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *

#This view is for registration of Admin user but only Superuser(django admin ) have privilages to add:
class SignupAPIView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = SignupSer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'Success': 'user created successfully', 'data': data}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#This view is for login:
class LoginAPIView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = LoginSer(data=request.data)
        if serializer.is_valid():
            return Response({'Success': 'login successfully', 'data': serializer.data}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

TITLE_CHOICES = [
    ('1', 'Superuser_user'),
    ('2', 'Teacher'),
    ('3', 'Student')
]

#This Function is used to check if any field is blank or None if any case:
def check_blank_or_null(data):
	status=True
	for x in data:
		if x=="" or x==None:
			status=False
			break
		else:
			pass					
	return status   

#In this view the Admin(User=='1') can add both the user student or teacher(user=="1" or '2') and can view('GET') all the users.
class AdminUserCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        if request.user.user_type=='1': 
            qs=User.objects.filter(username=request.data.get('username'))
            if qs.exists():
                raise ValidationError("Username already exists")
            qs=User.objects.filter(email=request.data.get('email'))
            if qs.exists():
                raise ValidationError("Email already exists")
            else:
                username=request.data.get('username')
                first_name=request.data.get('first_name')
                email=request.data.get('email')
                mobile=request.data.get('mobile')
                user_type=request.data.get('user_type')
                gender=request.data.get('gender')
                image=request.data.get('image')
                branch=request.data.get('branch')
                password=request.data.get('password')
                if request.data.get('user_type')=='2' and check_blank_or_null([username,email,password,first_name,mobile,image,branch,gender]):
                    obj=User.objects.create(username=username,first_name=first_name,email=email,mobile=mobile, user_type=user_type,is_staff=True,is_superuser=False,gender=gender,image=image,branch=branch)
                    obj.set_password(password)
                    obj.save()
                    return Response({'Done': 'profile added succesfully', 'data': True}, status=HTTP_200_OK)
                elif request.data.get('user_type')=='3' and check_blank_or_null([username,email,password,first_name,mobile,image,branch,gender]):
                    obj=User.objects.create(username=username,email=email,first_name=first_name,mobile=mobile, user_type='3',is_staff=False,is_superuser=False,gender=gender,image=image,branch=branch)
                    obj.set_password(password) 
                    obj.save()
                    return Response({'Done': 'profile added succesfully', 'data': True}, status=HTTP_200_OK)
                else:
                    return Response({'Error':'Plz fill all fields'},status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Error':'You are not authorised register any user'},status=HTTP_401_UNAUTHORIZED)
    
    def get(self, request):
        if request.user.user_type=='1':
            queryset = User.objects.all()
            serializer=ProfileSer(queryset,many=True)
            return Response(serializer.data,status=HTTP_200_OK)
        else:
            return Response({'Error':'You are not authorised to see any user.'},status=HTTP_400_BAD_REQUEST)

#In this View the Teacher user(user=='2') can only add(POST) the only user student user(user=='3') and can also see(GET) all the Student user(user=='3')
class TeacherCreateView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def post(self, request):
        if request.user.user_type=='2':
            try:
                qs=User.objects.filter(username=request.data.get('username'))
                if qs.exists():
                    raise ValidationError("Username already exists")
                qs=User.objects.filter(email=request.data.get('email'))
                if qs.exists():
                    raise ValidationError("Email already exists")
            except:
                username=request.data.get('username')
                first_name=request.data.get('first_name')
                email=request.data.get('email')
                mobile=request.data.get('mobile')
                gender=request.data.get('gender')
                image=request.data.get('image')
                branch=request.data.get('branch')
                password=request.data.get('password')
                if check_blank_or_null([username,email,password,first_name,mobile,image,branch,gender]):
                    obj=User.objects.create(username=username,email=email,first_name=first_name,mobile=mobile, user_type='3',is_staff=False,is_superuser=False,gender=gender,image=image,branch=branch)
                    obj.set_password(password) 
                    obj.save()
                    return Response({'Done': 'profile added succesfully', 'data': True}, status=HTTP_200_OK)
                else:
                    return Response({'Error':'Something went wrong'},status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({'Not Done': 'You are not authorised to do'}, status=HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        if request.user.user_type=='2':
            queryset = User.objects.filter(is_active=True,is_staff=False,is_superuser=False)
            serializer=ProfileSer(queryset,many=True)
            return Response(serializer.data,status=HTTP_200_OK)
        else:
            return Response({'Error':'You are not authorised to see any user'},status=HTTP_200_OK)



#Here we can use [if request.user.user_type=='3': ... else:
# return Response(...) But in this case everyuser can see their profile.]
class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        queryset = User.objects.filter(username=request.user)
        serializer= ProfileSer(queryset,many=True)
        return Response(serializer.data,status=HTTP_200_OK)

#this view is for resetting password just by entering emil , username, password(newpasssword only)
class Resetpassword(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = ResetpasswordSerializer(data=request.data)
        alldatas = {}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            alldatas['data'] ='Successfully Changed'
            print(alldatas)
            return Response(alldatas)
        return Response('failed retry after some time')



