from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *#Usermodel,Reportmodel,Proadcastmodel,RequestAudiomodel,Profilemodel
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (ModelSerializer,CharField)
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text

User = get_user_model()

class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, detail2,field2,status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail),field2: int(force_text(detail2))}
        else: self.detail = {'detail': force_text(self.default_detail)}

class RegisterSerializer(serializers.ModelSerializer):
    
    def validate(self, value):
        if User.objects.filter(email=value['email']):
            raise CustomValidation('Email already exists.','msg',400,'status', status_code=status.HTTP_409_CONFLICT)
        return value
        
    
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['email'], validated_data['password'])

        return user 


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profilemodel
        fields = ('userid','profile_img', 'first_name', 'last_name','phonenumber')
    
    def validate_token(self, value):
        user = self.context['request'].user
        if validated_data['token']!=AuthToken.objects.create(user)[1]:
        #if not user.check_password(value):
            raise serializers.ValidationError({"token": "Token is expired."})
        return value
        
    def create(self, validated_data):
        user = Profilemodel.objects.create_user(validated_data['userid'],validated_data['profile_img'], validated_data['first_name'], validated_data['last_name'],validated_data['phonenumber'])

        return user 

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password','email')
        extra_kwargs = {
            'password': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.password = validated_data['password']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)
 
        
class InviteSerializer(serializers.ModelSerializer):
    emailid=serializers.EmailField()

class ContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    subject= serializers.CharField(write_only=True, required=True)
    message = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ( 'email','subject','message')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email']
        )

        
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profilemodel
        fields='__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reportmodel
        fields='__all__'
        
class  ProadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proadcastmodel
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RequestAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model=RequestAudiomodel
        fields='__all__'




# User Serializer

# Register Serializer




        
   


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class PasswordResetVerifiedSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=128)


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)


class EmailChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class EmailChangeVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

