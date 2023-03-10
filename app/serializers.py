from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.encoding import force_text


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, detail2,field2,status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail),field2: int(force_text(detail2))}
        else: self.detail = {'detail': force_text(self.default_detail)}

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
        
class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Devices
        fields=('User','DeviceType','DeviceToken')

    def create(self,validated_data):
        RA=Devices.objects.create(**validated_data)
        return RA        
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profiles
        fields=('User','ProfileImage','FirstName','LastName','Country','City','State','ZipCode','CPFNumber','latitude','longitude')
    def create(self,validated_data):
        RA=Profiles.objects.create(**validated_data)
        return RA  

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model=BusinessModel
        fields=('User','ProfileImage','Name','Address','Contact','Location','TennisCourts','BusinessImages','CPFNumber','Description','latitude','longitude')
    def create(self,validated_data):
        RA=BusinessModel.objects.create(**validated_data)
        return RA  
   
class BusinessServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model=BusinessServices
        fields=('Business','Service')
    def create(self,validated_data):
        RA=BusinessServices.objects.create(**validated_data)
        return RA  

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model=BusinessHours
        fields=('Business','Day','StartTime','CloseTime')
    def create(self,validated_data):
        RA=BusinessHours.objects.create(**validated_data)
        return RA  
 
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=('User','Name','Email','Subject','Message')
    def create(self,validated_data):
        RA=Contact.objects.create(**validated_data)
        return RA          
        
class ContactFromBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactFromBusiness
        fields=('User','Name','Email','Subject','Message')
    def create(self,validated_data):
        RA=ContactFromBusiness.objects.create(**validated_data)
        return RA           
        
class HostMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model=HostMatches
        fields=('User','Title','Date','Time','Location','SelectMode','latitude','longitude')
        
    def create(self,validated_data):
        RA=HostMatches.objects.create(**validated_data)
        return RA    
        
class MatchRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model=MatchRounds
        fields=('HostMatch','Team1Score','Team2Score')
        
    def create(self,validated_data):
        RA=MatchRounds.objects.create(**validated_data)
        return RA  
        
class RatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=PlayerRatings
        fields=('HostMatch','PlayerRating','PlayerRated','Rating')
        
    def create(self,validated_data):
        RA=PlayerRatings.objects.create(**validated_data)
        return RA          
        
class InvitationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=HostInvitations
        fields=('HostMatch','UserInvited')
        
    def create(self,validated_data):
        RA=HostInvitations.objects.create(**validated_data)
        return RA        
        
class FriendRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model=FriendRequests
        fields=('id','Sender','Receiver')
        
    def create(self,validated_data):
        RA=FriendRequests.objects.create(**validated_data)
        return RA                
        
        