from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Podcast
#optional
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
# from knox.models import AuthToken

#optional
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (ModelSerializer,CharField)


from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text

class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, detail2,field2,status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail),field2: int(force_text(detail2))}
        else: self.detail = {'detail': force_text(self.default_detail)}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ('User_id','DeviceType', 'DeviceToken')
        
    def create(self, validated_data):
        RA = Devices.objects.create(**validated_data)
        return RA 

class LoginSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Devices
        fields = ('User_id','DeviceType','DeviceToken')
        
    def update(self, instance,validated_data):
        instance.DeviceType = validated_data['DeviceType']
        instance.DeviceToken = validated_data['DeviceToken']
        
        instance.save()
        return instance 



class SignupSerializer(serializers.ModelSerializer):
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
        model = Profile
        fields = ('User_id','ProfileImage', 'FirstName', 'LastName','PhoneNumber','email')
        
    # def validate_User_id(self, value):
    #     a=1
    #     if a==1:
    #     #if Profile.objects.filter(User_id=value):
    #         #Profile.objects.filter(User_id=value['User_id']).update(ProfileImage=value['ProfileImage'],FirstName=value['FirstName'],LastName=value['LastName'],PhoneNumber=value['PhoneNumber'])
    #         raise CustomValidation('Profile Created successfully.','msg',200,'status', status_code=status.HTTP_409_CONFLICT)
    #     return value
        
    def update_or_create(self, validated_data):
        profile = Profile.objects.create(**validated_data)#User_id=validated_data['User_id'],ProfileImage=validated_data['ProfileImage'],FirstName=validated_data['FirstName'],LastName=validated_data['LastName'],PhoneNumber=validated_data['PhoneNumber'])
        
        return profile  

class EditProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Profile
        fields = ('User_id','ProfileImage', 'FirstName', 'LastName','PhoneNumber')
        
    # def update(self, instance,validated_data):
    #     instance.ProfileImage = validated_data.get('ProfileImage',instance.ProfileImage)
    #     instance.FirstName = validated_data.get('FirstName',instance.FirstName)
    #     instance.LastName = validated_data.get('LastName',instance.LastName)
    #     instance.PhoneNumber = validated_data.get('PhoneNumber',instance.PhoneNumber)
        
    #     instance.save()
    #     return instance         

class GuestLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guests
        fields = ('DeviceType', 'DeviceToken')
        
    def create(self, validated_data):
        RA = Guests.objects.create(**validated_data)
        return RA 
        
class RequestAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedAudio
        fields = ('User_id', 'CategoryName', 'SongName','Message','image','FirstName','LastName')
        
    def create(self, validated_data):
        RA = RequestedAudio.objects.create(**validated_data)
        return RA 
        
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('User_id', 'Email', 'Subject','Message')
        
    def create(self, validated_data):
        RA = Contacts.objects.create(**validated_data)
        return RA         
        
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ('User_id', 'Item_id', 'Title','Message','image','FirstName','LastName')
        
    def create(self, validated_data):
        RA = Reports.objects.create(**validated_data)
        return RA      
        
class LikedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedItems
        fields = ('User_id', 'Item_id')
        
    def create(self, validated_data):
        RA = LikedItems.objects.create(**validated_data)
        return RA          

class MarkFavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('User_id', 'Item_id')
        
    def create(self, validated_data):
        RA = Favourites.objects.create(**validated_data)
        return RA          
        
class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ('User_id', 'OtherUser_id')
        
    def create(self, validated_data):
        RA = Friends.objects.create(**validated_data)
        return RA                  
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id','User_id', 'Item_id','Comment')
        
    def create(self, validated_data):
        RA = Comments.objects.create(**validated_data)
        return RA                
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=('id','User_id','Item_id','Comment')

    def create(self,validated_data):
        RA=Comments.objects.create(**validated_data)
        return RA

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model=Podcast
        fields=('id','category','audiofile','description','title')

    def create(validated_data):
        RA=Podcast.objects.create(**validated_data)
        return RA

class PodcastManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model=PodcastManagement
        fields=('id','name','title','descritpion','action','image')

    def create(validated_data):
        RA=PodcastManagement.objects.create(**validated_data)
        return RA
                
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('Transaction_id','User_id', 'Amount','Timeframe')
        
    def create(self, validated_data):
        RA = Transactions.objects.create(**validated_data)
        return RA        
