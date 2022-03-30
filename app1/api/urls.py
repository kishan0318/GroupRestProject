from django.urls import path
from .views import *


app_name = 'app1'

urlpatterns = [
    path('resetpassword',Resetpassword.as_view(),name='resetpassword'),
    path('login',LoginAPIView.as_view(),name='login'),
    path('signupeadmin',SignupAPIView.as_view(),name='signupeadmin'),
    path('create',AdminUserCreateView.as_view(),name='create'),
    path('create1',TeacherCreateView.as_view(),name='create1'),
    path('profile',StudentProfileView.as_view(),name='create3'),
]
