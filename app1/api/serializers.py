
from rest_framework.serializers import *
from ..models import User
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.serializers import *

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class SignupSer(Serializer):
    password=CharField(write_only=True,error_messages={'required':'password key is required','blank':'password  is required'})
    email=CharField(error_messages={'required':'email key is required','blank':'email is required'})
    username=CharField(error_messages={'required':'username key is required','blank':'username is required'})
    
    def validate(self,data):
        username=data.get('username')
        qs=User.objects.filter(username=data.get('username'))
        if qs.exists():
            raise ValidationError("Username already exists")
        qs=User.objects.filter(email=data.get('email'))
        if qs.exists():
            raise ValidationError("Email already exists")
        return data

    def create(self,validated_data):
        obj=User.objects.create(username=validated_data.get('username'),email=validated_data.get('email'),is_superuser=True)
        obj.set_password(validated_data.get('password'))
        obj.save()
        return validated_data


class LoginSer(Serializer):
    email=EmailField(error_messages={'required':'Email key is required','blank':'Email is required'})
    password=CharField(error_messages={'required':'Password key is required','blank':'Password is required'})
    token=CharField(read_only=True, required=False)

    def validate(self,data):
        qs=User.objects.filter(email=data.get('email'))
        if not qs.exists():
            raise ValidationError('No account with this email')
        user=qs.first()
        if user.check_password(data.get('password'))==False:
            raise ValidationError('Invalid Password')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        data['token']='JWT'+str(token)
        return data

class ProfileSer(ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class resetpasswordSerializer(ModelSerializer):
    username=CharField(max_length=100)
    password=CharField(max_length=100)
    email=CharField(max_length=100)
    class Meta:
        model=User
        fields='__all__'
    def save(self):
        username=self.validated_data['username']
        password=self.validated_data['password']
        email=self.validated_data['email']
        #filtering out whethere username is existing or not, if your username is existing then if condition will allow your username
        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists:
            #if your username is existing get the query of your specific username 
            user=User.objects.get(username=username)
            #then set the new password for your username
            user.set_password(password)
            user.save()
            return user
        else:
            raise ValidationError({'error':'please enter valid crendentials'})
