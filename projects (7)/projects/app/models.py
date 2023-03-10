from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import datetime
import django
from six import python_2_unicode_compatible

class PrimaryGunType(models.Model):
    GunName=models.CharField(max_length=250)

    def __str__(self):
        return self.GunName

class PrimaryHolsterType(models.Model):
    HolsterName=models.CharField(max_length=250)

    def __str__(self):
        return self.HolsterName

class Amount(models.Model):
    data=models.CharField(max_length=20)
    
class Plans(models.Model):
    PlanId=models.CharField(max_length=255,primary_key=True,default='com.gi')
    PlanName=models.CharField(max_length=500)
    PlanCost=models.IntegerField()
    text=models.TextField()
    Descritption=models.CharField(max_length=500)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

class UserProfiles(models.Model):
    User_id=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    ProfileImage=models.ImageField(upload_to='media',blank=True,null=True)
    FirstName=models.CharField(max_length=100,blank=True,null=True)
    LastName=models.CharField(max_length=200,blank=True,null=True)
    username=models.CharField(max_length=200,blank=True,null=True)
    Email=models.EmailField()
    Country=models.CharField(max_length=300,blank=True,null=True)
    State=models.CharField(max_length=400,blank=True,null=True)
    Gun=models.ForeignKey(PrimaryGunType,on_delete=models.CASCADE,blank=True,null=True)
    IsSuspended=models.BooleanField(default=False)
    Holster=models.ForeignKey(PrimaryHolsterType,on_delete=models.CASCADE,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    CurrentPlanId=models.ForeignKey(Plans,on_delete=models.CASCADE,default='com.mtdryfire.free')

class SuspendReason(models.Model):
    Name=models.CharField(max_length=500)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
class SuspendHistory(models.Model):
    User=models.ForeignKey(UserProfiles,on_delete=models.CASCADE)
    Reason=models.ForeignKey(SuspendReason,on_delete=models.CASCADE)
    OtherReasonText=models.CharField(max_length=1000,blank=True,null=True)
    DateSuspended=models.DateTimeField(default=django.utils.timezone.now)

class Contact(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE)
    Email=models.EmailField()
    Message=models.TextField()
    Subject=models.CharField(max_length=200)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

class Devices(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE)
    iOS='iOS'
    Android='Android'
    CategoryChoices=[
        (iOS,'iOS'),
        (Android,'Android'),
    ]
    DeviceToken=models.CharField(max_length=250,unique=True)
    DeviceType=models.CharField(max_length=500,choices=CategoryChoices)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.User_id


class TermAndPolicy(models.Model):
    Policy=models.CharField(max_length=300)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.Policy



class AboutUs(models.Model):
    about=models.TextField(max_length=400)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.about


class GunInstruction(models.Model):
    Instruction=models.TextField(max_length=400)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.Instruction

class AppStoreNotifications(models.Model):
    request_body=models.TextField(blank = True, null = True)
    DateTimeAdded=models.DateTimeField(default=django.utils.timezone.now)

class Invite(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user7')
    email=models.EmailField()
    message=models.TextField()
    InviteDate=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.email

class SubscribedUser(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE)
    Subscription_id=models.ForeignKey(Plans,on_delete=models.CASCADE)
    Transaction_id=models.CharField(max_length=500,blank=True,null=True)
    # Amount_id=models.ForeignKey(Amount,on_delete=models.CASCADE,related_name='users56')
    SubscribedDate=models.DateTimeField(default=django.utils.timezone.now)
    Month=models.CharField(max_length=500)
    subscriptionEndDate=models.CharField(max_length=500)
    

class UserRecords(models.Model):
    User_id=models.ForeignKey(UserProfiles,on_delete=models.CASCADE,related_name='user99hgho')
    Gun=models.ForeignKey(PrimaryGunType,on_delete=models.CASCADE,related_name='user110')
    Holster=models.ForeignKey(PrimaryHolsterType,on_delete=models.CASCADE,related_name='user111')
    ParTime=models.FloatField(blank = True, null = True,default=0)
    FirstBeep=models.FloatField(blank = True, null = True,default=0)
    DrawTime=models.FloatField(blank = True, null = True,default=0)
    ShotTime=models.FloatField(blank = True, null = True,default=0)
    DateOfRecord=models.DateTimeField(default=django.utils.timezone.now) 
    HolsterName=models.CharField(max_length=250)

    def __str__(self):
        return self.HolsterName
