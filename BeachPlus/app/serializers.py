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
        model=BusinessWeekHours
        fields=('Business','Day','StartTime','CloseTime')
    def create(self,validated_data):
        RA=BusinessWeekHours.objects.create(**validated_data)
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
        fields=('User','Title','Date','Time','Location','SelectMode','latitude','longitude','player_counts')
        
    def create(self,validated_data):
        RA=HostMatches.objects.create(**validated_data)
        return RA    
        
class MatchRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model=MatchRounds
        fields=('HostMatch','Team1Score','Team2Score','Round')
        
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

class Team1Serializer(serializers.ModelSerializer):
    class Meta:
        model=Team1Players
        fields=('HostMatch','Player')
        
    def create(self,validated_data):
        RA=Team1Players.objects.create(**validated_data)
        return RA      

class Team2Serializer(serializers.ModelSerializer):
    class Meta:
        model=Team2Players
        fields=('HostMatch','Player')
        
    def create(self,validated_data):
        RA=Team2Players.objects.create(**validated_data)
        return RA        
        
class FriendRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model=FriendRequests
        fields=('id','Sender','Receiver')
        
    def create(self,validated_data):
        RA=FriendRequests.objects.create(**validated_data)
        return RA                
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=('User','HostMatch','Text','UserSending')
        
    def create(self,validated_data):
        RA=Notification.objects.create(**validated_data)
        return RA

class OnlinePlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model=OnlineUsers
        fields=('Business','Player','SelectMode','StartTime','CloseTime','Day')
    def create(self,validated_data):
        RA=OnlineUsers.objects.create(**validated_data)
        return RA
        
class MatchSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model=MatchSummary
        fields=('HostMatch','Team1','Team2')
        
    def create(self,validated_data):
        RA=MatchSummary.objects.create(**validated_data)
        return RA        

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChatRoom
        fields=('roomname','Users')
        
    def create(self,validated_data):
        RA=ChatRoom.objects.create(**validated_data)
        return RA    
        
class RoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=RoomMessage
        fields=('User','Room','Content')
        
    def create(self,validated_data):
        RA=RoomMessage.objects.create(**validated_data)
        return RA            

# from .models import *
# from rest_framework import serializers
# from django.contrib.auth.models import User
# from rest_framework.exceptions import APIException
# from rest_framework import status
# from django.utils.encoding import force_str
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from rest_framework.serializers import ModelSerializer, CharField

#     # user = ForeignKey(User, on_delete=CASCADE, verbose_name='user',related_name='from_user', db_index=True)
#     # recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='recipient',related_name='to_user', db_index=True)
# class MessageModelSerializer(serializers.ModelSerializer):
#     user = CharField(source='user.username', read_only=True)
#     recipient = CharField(source='recipient.username')
#     user_id=ForeignKey(User, on_delete=CASCADE, verbose_name='user',related_name='from_user', db_index=True)
#     # recipient_id=ForeignKey(User, on_delete=CASCADE, verbose_name='recipient',related_name='to_user', db_index=True)

#     def create(self, validated_data):
#         user = self.context['request'].user
#         user_id=self.context['request']
#         recipient = get_object_or_404(
#             User, username=validated_data['recipient']['username'])
#         # recipient_id=get_object_or_404(User,username=validated_data['recipient_id']['username'])
#         msg = MessageModel(recipient=recipient,
#                           body=validated_data['body'],
#                           user=user.id)
#         msg.save()
#         return msg

#     class Meta:
#         model = MessageModel
#         fields = ('id', 'user', 'user_id','recipient', 'recipient_id','timestamp', 'body')


# class UserModelSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username',)

# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from app.models import MessageModel
# from rest_framework.serializers import ModelSerializer, CharField

# class MessageModelSerializer(ModelSerializer):
#     user = CharField(source='user.username')
#     recipient = CharField(source='recipient.username')

#     def create(self, validated_data):
#         user = self.context['request'].user
#         recipient = get_object_or_404(
#             User, username=validated_data['recipient']['username'])
#         msg = MessageModel(recipient=recipient,
#                           body=validated_data['body'],
#                           user=user.id)
#         msg.save()
#         return msg

#     class Meta:
#         model = MessageModel
#         fields = ('id', 'user','user_id', 'recipient','recipient_id', 'timestamp', 'body')


# class UserModelSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username',)





    
        