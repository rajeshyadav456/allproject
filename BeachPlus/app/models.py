from django.db import models
from django.contrib.auth.models import User
import django
from datetime import datetime

class Devices(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    iOS='iOS'
    Android='Android'
    CategoryChoices=[
        (iOS,'iOS'),
        (Android,'Android'),
    ]
    DeviceToken=models.CharField(max_length=250,blank=True,null=True)
    DeviceType=models.CharField(max_length=500,choices=CategoryChoices)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
class Profiles(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    ProfileImage=models.ImageField(upload_to='UserProfileImages',blank=True,null=True)
    FirstName=models.CharField(max_length=200,blank=True,null=True)
    LastName=models.CharField(max_length=200,blank=True,null=True)
    Country=models.CharField(max_length=200,blank=True,null=True)
    City=models.CharField(max_length=200,blank=True,null=True)
    State=models.CharField(max_length=200,blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    ZipCode=models.CharField(max_length=10,blank=True,null=True)
    CPFNumber=models.CharField(max_length=14,blank=True,null=True)
    MatchesHosted=models.IntegerField(blank=True,null=True,default=0)
    MatchesWon=models.IntegerField(blank=True,null=True,default=0)
    MatchesPlayed=models.IntegerField(blank=True,null=True,default=0)
    Feedback=models.TextField()
    IsSuspended=models.BooleanField(default=False,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    def __str__(self):
        return str(self.FirstName)

class Contact(models.Model):
    User=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    Name=models.CharField(max_length=200)
    Email=models.CharField(max_length=200)
    Subject=models.CharField(max_length=200)
    Message=models.CharField(max_length=200,blank=True,null=True)

class BusinessModel(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    ProfileImage=models.ImageField(upload_to='BusineesProfileImages',blank=True,null=True)
    Name=models.CharField(max_length=200,blank=True,null=True)
    Address=models.CharField(max_length=200,blank=True,null=True)
    BusinessImages=models.FileField(upload_to='BusinessImages',blank=True,null=True,max_length=500)
    Location=models.CharField(max_length=200,blank=True,null=True)
    latitude = models.FloatField(max_length = 500,blank=True,null=True)
    longitude = models.FloatField(max_length = 500,blank=True,null=True)
    Contact=models.BigIntegerField(blank=True,null=True)
    CPFNumber=models.CharField(max_length=14,blank=True,null=True)
    Description=models.CharField(max_length=1000,blank=True,null=True)
    TennisCourts=models.IntegerField(default=0)

class OnlineUsers(models.Model):
    Business=models.ForeignKey(BusinessModel,on_delete=models.CASCADE,blank=True,null=True)
    DateOfRecord=models.DateTimeField(default=django.utils.timezone.now,blank=True,null=True) 
    Player=models.ForeignKey(Profiles,on_delete=models.CASCADE,blank=True,null=True)
    Open='Open'
    Close='Close'
    CategoryChoices=[
        (Open,'Open'),
        (Close,'Close')
        
    ]
    SelectMode=models.CharField(max_length=200,choices=CategoryChoices,default='Open',blank=True,null=True)
    Monday='Monday'
    Tuesday='Tuesday'
    Wednesday='Wednesday'
    Thursday='Thursday'
    Friday='Friday'
    Saturday='Saturday'
    Sunday='Sunday'
    CategoryChoices=[
        (Monday,'Monday'),
        (Tuesday,'Tuesday'),
        (Wednesday,'Wednesday'),
        (Thursday,'Thursday'),
        (Friday,'Friday'),
        (Saturday,'Saturday'),
        (Sunday,'Sunday')
    ]
    Day=models.CharField(max_length=200,blank=True,null=True,choices=CategoryChoices)
    StartTime=models.TimeField(blank=True,null=True)
    CloseTime=models.TimeField(blank=True,null=True)
    
    # @property
    # def is_open(self):
    #     return True if self.opening_time <= datetime.now().time() < self.closing_time else False
        
class ContactFromBusiness(models.Model):
    User=models.ForeignKey(BusinessModel,on_delete=models.CASCADE)
    Name=models.CharField(max_length=200)
    Email=models.CharField(max_length=200)
    Subject=models.CharField(max_length=200)
    Message=models.CharField(max_length=200,blank=True,null=True)
    
class BusinessServices(models.Model):
    Business=models.ForeignKey(BusinessModel,on_delete=models.CASCADE)
    Service=models.CharField(max_length=200,blank=True,null=True)
    
class BusinessWeekHours(models.Model):
    Business=models.ForeignKey(BusinessModel,on_delete=models.CASCADE)
    Monday='Monday'
    Tuesday='Tuesday'
    Wednesday='Wednesday'
    Thursday='Thursday'
    Friday='Friday'
    Saturday='Saturday'
    Sunday='Sunday'
    CategoryChoices=[
        (Monday,'Monday'),
        (Tuesday,'Tuesday'),
        (Wednesday,'Wednesday'),
        (Thursday,'Thursday'),
        (Friday,'Friday'),
        (Saturday,'Saturday'),
        (Sunday,'Sunday')
    ]
    Day=models.CharField(max_length=200,blank=True,null=True,choices=CategoryChoices)
    StartTime=models.TimeField(blank=True,null=True)
    CloseTime=models.TimeField(blank=True,null=True)
    

        
class HostMatches(models.Model):
    User=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    Title=models.CharField(max_length=200,blank=True,null=True)
    Date=models.DateField(blank=True,null=True)
    Time=models.TimeField(blank=True,null=True)
    Location=models.CharField(max_length=200,blank=True,null=True)
    latitude=models.FloatField(blank=True,null=True)
    longitude=models.FloatField(blank=True,null=True)
    player_counts=models.IntegerField(blank=True,null=True)
    Public='Public'
    Private='Private'
    CategoryChoices=[
        (Public,'Public'),
        (Private,'Private')
    ]
    SelectMode=models.CharField(max_length=200,choices=CategoryChoices,default='Private')
    Initiated='Initiated'
    Cancelled='Cancelled'
    Completed='Completed'
    StatusChoices=[
        (Initiated,'Initiated'),
        (1,'1'),
        (2,'2'),
        (3,'3')
    ]
    Status=models.CharField(max_length=200,choices=StatusChoices,default='Initiated')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
class HostInvitations(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    UserInvited=models.ForeignKey(Profiles,on_delete=models.CASCADE,blank=True,null=True)
    NumberInvited=models.BigIntegerField(blank=True,null=True)
    Sent='Sent'
    Attend='Attend'
    Decline='Decline'
    CategoryChoices=[
        (Sent,'Sent'),
        (Attend,'Attend'),
        (Decline,'Decline')
    ]
    Status=models.CharField(max_length=200,choices=CategoryChoices,default='Sent')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)  
    
class Team1Players(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    Player=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    Result=models.CharField(max_length=5,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)    

class Team2Players(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    Player=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    Result=models.CharField(max_length=5,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)  

class MatchRounds(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    Team1Score=models.IntegerField(blank=True,null=True,default=0)
    Team2Score=models.IntegerField(blank=True,null=True,default=0)
    Round=models.IntegerField(blank=True,null=True,default=0)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)    
    
class PlayerRatings(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    PlayerRating=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='PlayerRating',blank=True,null=True,)
    PlayerRated=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='PlayerRated',blank=True,null=True,)
    Rating=models.FloatField(blank=True,null=True,default=0)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)       

class FriendRequests(models.Model):
    Sender=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='Sender')
    Receiver=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='Receiver')
    Sent='Sent'
    Accept='Accept'
    Reject='Reject'
    CategoryChoices=[
        (Sent,'Sent'),
        (Accept,'Accept'),
        (Reject,'Reject')
    ]
    Status=models.CharField(max_length=200,choices=CategoryChoices,default='Sent')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)       
    
    
class Notification(models.Model):
    User=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='user1',blank=True,null=True)
    UserSending=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='UserSending',blank=True,null=True)
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE,related_name='user2',blank=True,null=True)
    Text=models.CharField(max_length=500,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

class MatchSummary(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    Team1=models.IntegerField(blank=True,null=True,default=0)
    Team2=models.IntegerField(blank=True,null=True,default=0)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)   

class ChatRoom(models.Model):
    roomname=models.CharField(max_length=255,blank=False)
    Users=models.ManyToManyField(Profiles,related_name='UsersInRoom')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)    
    
    def __str__(self):
        return str(self.title)
    
class RoomMessage(models.Model):
    User=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='UserSendingMessage')
    Room=models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name='Room')
    timestamp=models.DateTimeField(auto_now_add=True)
    content=models.TextField(unique=False,blank=False)
    
    def __str__(self):
        return str(self.content)          

class SingleChatRoom(models.Model):
    roomname=models.CharField(max_length=255,blank=False)
    user1=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='User1InRoom')
    user2=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='User2InRoom')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)    
    
    def __str__(self):
        return str(self.roomname)
    
class SingleRoomMessage(models.Model):
    User=models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='SingleUserMessage')
    Room=models.ForeignKey(SingleChatRoom,on_delete=models.CASCADE,related_name='SingleRoom')
    timestamp=models.DateTimeField(auto_now_add=True)
    content=models.TextField(unique=False,blank=False)
    text='text'
    media='media'
    messageTypeChoices=[
        (text,'text'),
        (media,'media')
    ]
    messageType=models.CharField(max_length=255,choices=messageTypeChoices,default='text')
    message_read=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.content)    

# from django.contrib.auth.models import User
# from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
#                               CASCADE)

# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer


# class MessageModel(Model):
#     """
#     This class represents a chat message. It has a owner (user), timestamp and
#     the message body.
#     """
#     user = ForeignKey(User, on_delete=CASCADE, verbose_name='user',
#                       related_name='from_user', db_index=True)
#     recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='recipient',
#                           related_name='to_user', db_index=True)
#     timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
#                               db_index=True)
#     body = TextField('body')

#     def __str__(self):
#         return str(self.id)

#     def characters(self):
#         """
#         Toy function to count body characters.
#         :return: body's char number
#         """
#         return len(self.body)

#     def notify_ws_clients(self):
#         """
#         Inform client there is a new message.
#         """
#         notification = {
#             'type': 'recieve_group_message',
#             'message': '{}'.format(self.id)
#         }

#         channel_layer = get_channel_layer()
#         print("user.id {}".format(self.user.id))
#         print("user.id {}".format(self.recipient.id))

#         async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
#         async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

#     def save(self, *args, **kwargs):
#         """
#         Trims white spaces, saves the message and notifies the recipient via WS
#         if the message is new.
#         """
#         new = self.id
#         self.body = self.body.strip()  # Trimming whitespaces from the body
#         super(MessageModel, self).save(*args, **kwargs)
#         if new is None:
#             self.notify_ws_clients()

#     # Meta
#     class Meta:
#         app_label = 'app'
#         verbose_name = 'message'
#         verbose_name_plural = 'messages'
#         ordering = ('-timestamp',)
