from django.db import models
from django.contrib.auth.models import User
import django
# Create your models here.

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
    CPFNumber=models.CharField(max_length=14,unique = True,blank=True,null=True)
    MatchesHosted=models.IntegerField(blank=True,null=True,default=0)
    MatchesWon=models.IntegerField(blank=True,null=True,default=0)
    MatchesPlayed=models.IntegerField(blank=True,null=True,default=0)
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
    CPFNumber=models.CharField(max_length=14,unique = True,blank=True,null=True)
    Description=models.CharField(max_length=1000,blank=True,null=True)
    TennisCourts=models.IntegerField(default=0)

class ContactFromBusiness(models.Model):
    User=models.ForeignKey(BusinessModel,on_delete=models.CASCADE)
    Name=models.CharField(max_length=200)
    Email=models.CharField(max_length=200)
    Subject=models.CharField(max_length=200)
    Message=models.CharField(max_length=200,blank=True,null=True)
    
class BusinessServices(models.Model):
    Business=models.ForeignKey(BusinessModel,on_delete=models.CASCADE)
    Service=models.CharField(max_length=200,blank=True,null=True)
    
class BusinessHours(models.Model):
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
    StartTime=models.CharField(max_length=200,blank=True,null=True)
    CloseTime=models.CharField(max_length=200,blank=True,null=True)
        
class HostMatches(models.Model):
    User=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    Title=models.CharField(max_length=200,blank=True,null=True)
    Date=models.DateField(blank=True,null=True)
    Time=models.TimeField(blank=True,null=True)
    Location=models.CharField(max_length=200,blank=True,null=True)
    latitude=models.FloatField(blank=True,null=True)
    longitude=models.FloatField(blank=True,null=True)
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
        (Cancelled,'Cancelled'),
        (Completed,'Completed')
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
    
# class Teams(models.Model):
#     HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    # DateAdded=models.DateTimeField(default=django.utils.timezone.now)    
    
class Team1Players(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    Player=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)    

class Team2Players(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    Player=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)  

class MatchRounds(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    # Team=models.ForeignKey(Teams,on_delete=models.CASCADE,related_name='teamround')
    Team1Score=models.IntegerField(blank=True,null=True,default=0)
    Team2Score=models.IntegerField(blank=True,null=True,default=0)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)    
    
class PlayerRatings(models.Model):
    HostMatch=models.ForeignKey(HostMatches,on_delete=models.CASCADE)
    Player=models.ForeignKey(Profiles,on_delete=models.CASCADE)
    Rating=models.IntegerField(blank=True,null=True,default=0)
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
    
    
    # class Meta:
    #     unique_together = (('Sender', 'Receiver',))
    #     ordering = ["-DateAdded"]