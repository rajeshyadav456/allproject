from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import django
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
User = settings.AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Cfrom django.conf import settings

class Profile(models.Model):
    User_id=models.OneToOneField(User,on_delete=models.CASCADE,related_name='users')
    ProfileImage=models.ImageField(upload_to='UserProfileImages',blank=True,null=True)
    FirstName=models.CharField(max_length=100,blank=True,null=True)
    LastName=models.CharField(max_length=100,blank=True,null=True)
    PhoneNumber=models.CharField(max_length=100,blank=True,null=True)
    email=models.CharField(max_length=100,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.User_id_id

class Notifications(models.Model):
    User_id=models.OneToOneField(User,on_delete=models.CASCADE,related_name='Nuser')
    Status=models.BooleanField(default=True)
    ReferalCode=models.CharField(max_length=100,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.Status

class UserNotifications(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user99')
    OtherUser_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user98')
    Name=models.CharField(max_length=500,blank=True,null=True)
    text=models.CharField(max_length=500,blank=True,null=True)
    DateAdded=models.DateTimeField(default=datetime.utcnow().strftime('%Y %M %D - %H:%M:%S'))
    
    def __str__(self):
        return self.Name

class Transactions(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user76')
    Transaction_id=models.CharField(max_length=500,blank=True,null=True)
    Amount=models.CharField(max_length=50,blank=True,null=True)
    Timeframe=models.CharField(max_length=500,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

class Guests(models.Model):
    id=models.AutoField(primary_key=True)
    iOS='iOS'
    Android='Android'
    CategoryChoices=[
        (iOS,'iOS'),
        (Android,'Android'),
    ]
    DeviceType=models.CharField(max_length=500,choices=CategoryChoices)
    DeviceToken=models.CharField(max_length=255,unique=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.DeviceType

class Devices(models.Model):
    User_id=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user1')
    iOS='iOS'
    Android='Android'
    CategoryChoices=[
        (iOS,'iOS'),
        (Android,'Android'),
    ]
    DeviceType=models.CharField(max_length=500,choices=CategoryChoices)
    DeviceToken=models.CharField(max_length=255,unique=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.DeviceType

class Categories(models.Model):
    id=models.AutoField(primary_key=True)
    Name=models.CharField(max_length=500)
    PosterImage=models.ImageField(upload_to='CategoryImages',blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.Name

class Items(models.Model):
    id=models.AutoField(primary_key=True)
    Category_id=models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='category1')
    Name=models.CharField(max_length=500,blank=True,null=True)
    Description=models.CharField(max_length=5000,blank=True,null=True)
    File=models.FileField(upload_to='ItemFiles',blank=True,null=True)
    Duration=models.CharField(max_length=500,blank=True,null=True)
    PosterImage=models.ImageField(upload_to='ItemImages',blank=True,null=True)
    Likes=models.BigIntegerField(default=0)
    TimesPlayed=models.BigIntegerField(default=0)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    ArtistName=models.CharField(max_length=500,blank=True,null=True)
    Views=models.BigIntegerField(default=0)
    Comments=models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.Name
        
class Trending(models.Model):
    Item_id=models.OneToOneField(Items,on_delete=models.CASCADE,primary_key=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.Item_id

class ForYou(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user2')
    item_id=models.ForeignKey(Items,on_delete=models.CASCADE,related_name='items')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    def __str__(self):
        return self.User_id

class LikedItems(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user3')
    Item_id=models.ForeignKey(Items,on_delete=models.CASCADE,related_name='item1')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.User_id

class Favourites(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user321')
    Item_id=models.ForeignKey(Items,on_delete=models.CASCADE,related_name='item121')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.User_id

class GuestPreviouslyPlayed(models.Model):
    Guest_id=models.ForeignKey(Guests,on_delete=models.CASCADE,related_name='user45')
    Item_id=models.ForeignKey(Items,on_delete=models.CASCADE,related_name='item85')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.Guest_id

class UserPreviouslyPlayed(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user35')
    Item_id=models.ForeignKey(Items,on_delete=models.CASCADE,related_name='item55')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.User_id

class Friends(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user4')
    OtherUser_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user5')
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.User_id

class TermsAndPolicyText(models.Model):
    policy=models.CharField(max_length=5000,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    

    def __str__(self):
        return self.policy

class RequestedAudio(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user6')
    SongName=models.CharField(max_length=500,blank=True,null=True)
    #Category_id=models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='category2')
    CategoryName=models.CharField(max_length=500,blank=True,null=True)
    Message=models.CharField(max_length=500,blank=True,null=True)
    image=models.CharField(max_length=1000,blank=True,null=True)#models.ImageField(upload_to='UserProfileImages',blank=True,null=True)
    FirstName=models.CharField(max_length=100,blank=True,null=True)
    LastName=models.CharField(max_length=100,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    

    def __str__(self):
        return self.SongName

class Contacts(models.Model):
    User_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user7')
    Email=models.EmailField(blank=True,null=True)
    Subject=models.CharField(max_length=500,blank=True,null=True)
    Message=models.CharField(max_length=500,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.Email


class Reports(models.Model):
    User_id=models.ForeignKey(User, on_delete=models.CASCADE,related_name='user9')
    Item_id=models.ForeignKey(Items,on_delete=models.CASCADE)
    Title=models.CharField(max_length=500,blank=True,null=True)
    Message=models.TextField(blank=True,null=True)
    image=models.CharField(max_length=1000,blank=True,null=True)
    FirstName=models.CharField(max_length=100,blank=True,null=True)
    LastName=models.CharField(max_length=100,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.Title

class Seasons(models.Model):
    id=models.AutoField(primary_key=True)
    Item_id=models.ForeignKey(Items,on_delete=models.CASCADE,related_name='item4')
    SeasonName=models.CharField(max_length=500,blank=True,null=True)
    PosterImage=models.ImageField(upload_to='SeasonImages',blank=True,null=True)
    Description=models.CharField(max_length=5000,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.SeasonName


class Episodes(models.Model):
    id=models.AutoField(primary_key=True)
    Item_id=models.ForeignKey(Items,on_delete=models.CASCADE,related_name='item5')
    Season_id=models.ForeignKey(Seasons,on_delete=models.CASCADE,related_name='season')
    Name=models.CharField(max_length=500,blank=True,null=True)
    Description=models.CharField(max_length=5000,blank=True,null=True)
    File=models.FileField(upload_to='upload',blank=True,null=True)
    Duration=models.CharField(max_length=500,blank=True,null=True)
    PosterImage=models.ImageField(upload_to='EpisodeImages',blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)
    
    def __str__(self):
        return self.Name

class Comments(models.Model):
    id=models.AutoField(primary_key=True)
    User_id=models.ForeignKey(User, on_delete=models.CASCADE,related_name='user0')
    Item_id=models.ForeignKey(Items,on_delete=models.CASCADE,related_name='item7')
    Comment=models.CharField(max_length=500,blank=True,null=True)
    DateAdded=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.Comment
        
class PodcastManagement(models.Model):
    name=models.CharField(max_length=100)
    title=models.CharField(max_length=500)
    description=models.TextField(max_length=500)
    action=models.CharField(max_length=100)
    image=models.ImageField(upload_to='ram')

    def __str__(self):
        return self.name

class Podcast(models.Model):
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    audiofile=models.FileField(upload_to='None')
    descritption=models.TextField(max_length=500)
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title

    