from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.encoding import force_str


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, detail2,field2,status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail),field2: int(force_str(detail2))}
        else: self.detail = {'detail': force_str(self.default_detail)}


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=('id','username','email')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfiles
        fields=('User_id','ProfileImage','FirstName','LastName','username','Email','Country','Gun','Holster','State')

    def create(self,validated_data):
        RA=UserProfiles.objects.create(**validated_data)
        return RA

class SubscribedSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubscribedUser
        fields=('User_id','Subscription_id','Transaction_id','SubscribedDate','subscriptionEndDate')
        
    def create(self,validated_data):
        RA=SubscribedUser.objects.create(**validated_data)
        return RA

class AppStoreNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=AppStoreNotifications
        fields=('request_body',)
        
    def create(self,validated_data):
        RA=AppStoreNotifications.objects.create(**validated_data)
        return RA

# class EditProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Profile
#         fields=('User_id','ProfileImage','FirstName','LastName','Email','Country','Gun','Holster')
    
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=('User_id','Email','Message','Subject')
    def create(self,validated_data):
        RA=Contact.objects.create(**validated_data)
        return  RA



class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Devices
        fields=('User_id','DeviceType','DeviceToken')

    def create(self,validated_data):
        RA=Devices.objects.create(**validated_data)
        return RA



# class NotificationsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Notifications
#         fields=('User_id','refferal_code')
        
#     def create(self,validated_data):
#         RA=Notifications.objects.create(**validated_data)
#         return RA



# class FriendsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Friends
#         fields=('User_id','OtherUser_id','DateAdded')

#     def create(self,validated_data):
#         RA=Friends.objects.create(**validated_data)
#         return RA


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Invite
        fields=('User_id','email','message')
        
    def create(self,validated_data):
        RA=Invite.objects.create(**validated_data)
        return RA

class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserRecords
        fields=('User_id','Gun','Holster','ParTime')
        
    def create(self,validated_data):
        RA=UserRecords.objects.create(**validated_data)
        return RA        

class SignupSerializer(serializers.ModelSerializer):
    def validate(self, value):
        if User.objects.filter(email=value['email']):
            raise CustomValidation('Email already exists.','msg',400,'status', status_code=status.HTTP_200_OK)
        return value
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password':{'write_only':True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['email'], validated_data['password'])
        return user 
        
        

# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Devices
#         fields=('User_id','DeviceType','DeviceToken')
#     def update(self,instance,validated_data):
#         instance.DeviceType=validated_data['DeviceType']
#         instance.DeviceToken=validated_data['DeviceToken']

#         instance.save()
#         return instance





