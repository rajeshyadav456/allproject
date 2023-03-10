from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from .helpers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import FileSystemStorage
import requests
from django.contrib.auth import authenticate,login,logout
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random, string
import json
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q,F,Case, Value, When, FloatField,OuterRef, Subquery,CharField,Count,Func
from django.urls import reverse
from datetime import datetime
import pandas as pd
User = get_user_model()

#admin pannel imports
from django.shortcuts import render , redirect , HttpResponseRedirect,HttpResponse    
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login

class SignupAPI(generics.GenericAPIView):
    serializer_class = SignupSerializer
        
    def post(self, request, *args, **kwargs):#,exception):
        data=request.data
        email=request.data['email']
        if request.data.get('UserType','User')=='Business':
            original_email=request.data['email']
            modified_email='business_'+original_email
            email=modified_email
            data=dict()
            data['email']=modified_email
            data['password']=request.data['password']
           
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        d=dict()
        d['User']=user.id
        d['DeviceToken']=request.data.get('DeviceToken','')
        d['DeviceType']=request.data.get('DeviceType','')
        Devices.objects.filter(DeviceToken=d['DeviceToken']).delete()
        serializer2 = DevicesSerializer(data=d)
        serializer2.is_valid(raise_exception=True)
        device=serializer2.save()
        if request.data.get('UserType','User')=='Business':
            d=dict()
            d['User']=user.id
            serializer3 = BusinessSerializer(data=d)
            serializer3.is_valid(raise_exception=True)
            profile=serializer3.save()
            profile=BusinessModel.objects.filter(User=user.id).values()[0]   
            profile['BusinessImages']=filter(None,str(profile['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
            profile['Email']=str(BusinessModel.objects.filter(User=user.id).values('User__email')[0]['User__email'])[9:]
            profile['Rating']=PlayerRatings.objects.filter(PlayerRating=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        else:
            
            up=Profiles.objects.filter(User=user.id)
            if len(up)==0:
                dat=dict()
                dat['User']=user.id
                serializer3 = ProfileSerializer(data=dat)
                serializer3.is_valid(raise_exception=True)
                profile=serializer3.save()
                profile=Profiles.objects.filter(User=user.id).values()[0]
                profile['Email']=User.objects.filter(id=user.id).values('email')[0]['email']
                profile['Rating']=PlayerRatings.objects.filter(PlayerRating=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
                device_exists=Devices.objects.filter(User=user.id).values()
                if device_exists:
                    device_exists.update(DeviceToken=request.data.get('DeviceToken',''))
                else:
                    d=dict()
                    d['User']=user.id
                    d['DeviceToken']=request.data.get('DeviceToken','')
                    d['DeviceType']=request.data.get('DeviceType','')
                    Devices.objects.filter(DeviceToken=d['DeviceToken']).delete()
                    serializer2 = DevicesSerializer(data=d)
                    serializer2.is_valid(raise_exception=True)
                    device=serializer2.save()
            else:
                profile=up.values()[0]
                profile['Email']=User.objects.filter(id=user.id).values('email')[0]['email']
                profile['Rating']=PlayerRatings.objects.filter(PlayerRating=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
        url='http://aashima.parastechnologies.in/BeachPlus/api/token/'
        payload={'username':email,'password':request.data['password']}
        
        response = requests.request("POST", url, data=payload)
        
        token=response.json()
        profile['UserType']=request.data.get('UserType','User')
        return Response({'data':{'Profile':profile,'token':token},
        'msg':'Signup Successfully',
        'status':200
        })        
        
      
class LoginAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email=request.data['email']
        if request.data.get('UserType','User')=='Business':
            original_email=request.data['email']
            email='business_'+original_email
        u=User.objects.filter(email__iexact=email)
        if len(u)>0:
            user = authenticate(request, username=email, password=request.data['password'])
            if user is not None:
                up=Profiles.objects.filter(User=user.id)
                if request.data.get('UserType','User')=='User':
                    if len(up)==0:
                        d=dict()
                        d['User']=user.id
                        serializer3 = ProfileSerializer(data=d)
                        serializer3.is_valid(raise_exception=True)
                        profile=serializer3.save()
                        profile=Profiles.objects.filter(User=user.id).values()[0]
                        profile['Email']=User.objects.filter(id=user.id).values('email')[0]['email']
                        profile['Rating']=PlayerRatings.objects.filter(PlayerRating=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
                        device_exists=Devices.objects.filter(User=user.id)
                        if device_exists:
                            device_exists.update(DeviceToken=request.data.get('DeviceToken',''))
                        else:
                           d=dict()
                           d['User']=user.id
                           d['DeviceToken']=request.data.get('DeviceToken','')
                           d['DeviceType']=request.data.get('DeviceType','')
                           Devices.objects.filter(DeviceToken=d['DeviceToken']).delete()
                           serializer2 = DevicesSerializer(data=d)
                           serializer2.is_valid(raise_exception=True)
                           device=serializer2.save()
                    else:
                        profile=up.values()[0]
                        profile['Email']=User.objects.filter(id=user.id).values('email')[0]['email']
                        profile['Rating']=PlayerRatings.objects.filter(PlayerRating=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
                        device_exists=Devices.objects.filter(User=user.id)
                        if device_exists:
                            device_exists.update(DeviceToken=request.data.get('DeviceToken',''))
                        else:
                            d=dict()
                            d['User']=user.id
                            d['DeviceToken']=request.data.get('DeviceToken','')
                            d['DeviceType']=request.data.get('DeviceType','')
                            Devices.objects.filter(DeviceToken=d['DeviceToken']).delete()
                            serializer2 = DevicesSerializer(data=d)
                            serializer2.is_valid(raise_exception=True)
                            device=serializer2.save()
                
                if request.data.get('UserType','User')=='Business':
                    up=BusinessModel.objects.filter(User=user.id)
                    
                    if len(up)==0:
                        d=dict()
                        d['User']=user.id
                        serializer3 = BusinessSerializer(data=d)
                        serializer3.is_valid(raise_exception=True)
                        profile=serializer3.save()
                        profile=BusinessModel.objects.filter(User=user.id).values()[0] 
                        profile['BusinessImages']=filter(None,str(profile['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
                        profile['Email']=str(BusinessModel.objects.filter(User=user.id).values('User__email')[0]['User__email'])[9:]
            
                    else:
                        profile=up.values()[0]    
                        profile['Email']=str(BusinessModel.objects.filter(User=user.id).values('User__email')[0]['User__email'])[9:]
                        profile['BusinessImages']=filter(None,str(profile['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
                url='http://aashima.parastechnologies.in/BeachPlus/api/token/'
                payload={'username':email,'password':request.data['password']}
                profile['UserType']=request.data.get('UserType','User')
                response = requests.request("POST", url, data=payload)
                token=response.json()
                return Response({"data":{"Profile":profile,'token':token},"status":200,"msg":'Login Successfully.'})
            else:
                return Response({"status":400,"msg":'Incorrect credentials.'})
        else:
            return Response({"status":400,"msg":'This email does not exist.'})        
            
class CreateProfileAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=ProfileSerializer
    def post(self,request,*args,**kwargs):
        profile=Profiles.objects.filter(User=request.POST['User']).values()
        if len(Profiles.objects.filter(User=request.data['User']))>0:
            Profiles.objects.filter(User=request.data['User']).delete()
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        profile=Profiles.objects.filter(User=request.POST['User']).values()[0]
        profile['Email']=User.objects.filter(id=request.POST['User']).values('email')[0]['email']
        profile['Rating']=PlayerRatings.objects.filter(PlayerRating=request.POST['User']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        return Response({
        'data':{'Profile':profile},
        'msg':'User Successfully',
        'status':200
        })      

class CreateBusiness(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=BusinessSerializer
    def post(self,request,*args,**kwargs):
        if len(BusinessModel.objects.filter(User=request.POST['User']))>0:
            BusinessModel.objects.filter(User=request.POST['User']).delete()
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        uids=str(request.data.get('Services','')).replace('[','').replace(']','').split(',')
        for i in uids:
            d=dict()
            d['Business']=RA.User
            d['Service']=i
            serializer2 = BusinessServicesSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
        files=[]
        if len(request.FILES.getlist('BusinessImages'))>0:
            files=request.FILES.getlist('BusinessImages')   
            Pstring=[]
            for i in range(len(files)):
                fs = FileSystemStorage()
                ppn=str(datetime.now())+'.jpg'
                filename = fs.save(ppn, files[i])
                uploaded_file_url = fs.url(filename)
                Pstring.append(uploaded_file_url)
            
            BusinessModel.objects.filter(User=request.POST['User']).update(BusinessImages=Pstring)
        profile=BusinessModel.objects.filter(User=request.POST['User']).values()[0]
        profile['BusinessImages']=filter(None,str(profile['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
        profile['Email']=str(BusinessModel.objects.filter(User=request.POST['User']).values('User__email')[0]['User__email'])[9:]
        s=BusinessServices.objects.filter(Business=request.POST['User']).values('Service')
        return Response({
        'data':{'Profile':profile,'Service':s},
        'msg':'Business saved Successfully',
        'status':200
        })

class AddBusinessHours(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=BusinessHoursSerializer
    def post(self,request,*args,**kwargs):
        data=BusinessWeekHours.objects.filter(Business=request.data['Business']).values()
        if len(BusinessWeekHours.objects.filter(Day=request.POST['Day'],Business=request.POST['Business']))>0:
            return Response({
                'msg':'You cannot add same day',
                'status':400
            })
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'data':data,'msg':'Business Hours saved Successfully','status':200})
        
class AddBusinessAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=BusinessSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({
            'msg':'Business saved Successfully',
            'status':200
        })

        
class BusinessRecordSerializer(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=OnlinePlayersSerializer
    def post(self,request,*args,**kwargs):
        bh=BusinessWeekHours.objects.filter(Business=request.POST['Business'])
        if len(OnlineUsers.objects.filter(Player=request.POST['Player']))>=1:
            return Response({'msg':'Player cannot access business More Than one','status':200 })
        bh_days=bh.values_list('Day',flat=True)
        days_list=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        today=days_list[datetime.today().weekday()]
        if today in bh_days:
            bh_hours=bh.filter(Day=today,StartTime__lte=datetime.strptime(str(request.POST['StartTime']), '%I:%M %p').time(),CloseTime__gte=datetime.strptime(str(request.POST['CloseTime']), '%I:%M %p').time())
            if bh_hours.count()>0:
                serializer=self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                RA=serializer.save()
                return Response({'msg':'CheckIn saved Successfully','status':200})
            else:
                return Response({'msg':'This business is not yet open.','status':400})
        else:
            return Response({'msg':'This business is not open today.','status':400})
                
                
class DeleteBusinessIMageAPI(generics.GenericAPIView):
    serializer_class=BusinessSerializer
    def post(self,request,*args,**kwargs):
        Business=request.POST['Business']
        ImageName=str(request.POST['ImageName'])#.replace('/BeachPlus/','').replace('%20',' ').replace('%3A',':')
        p=BusinessModel.objects.filter(User=Business)
        pp=str(p.values()[0]['BusinessImages']).replace(ImageName,'')
        pp=list(filter(None,str(pp).replace('[','').replace(']','').replace('\'','').replace(" ","").split(',')))
        p.update(BusinessImages=pp)
        
        import os 
        try:
            ImageName=ImageName.replace('/BeachPlus/','').replace('%20',' ').replace('%3A',':')
        
            os.remove('/home/aashima/BeachPlus/BeachPlus/static_'+str(str(ImageName)[1:]))
        except:
            a=1    
            
        profile=BusinessModel.objects.filter(User=request.POST['Business']).values()[0]
        profile['BusinessImages']=filter(None,str(profile['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
        profile['Email']=str(BusinessModel.objects.filter(User=request.POST['Business']).values('User__email')[0]['User__email'])[9:]
        s=BusinessServices.objects.filter(Business=request.POST['Business']).values('Service')
        return Response({'data':{'Profile':profile,'Service':s},'msg':'Business Image Delete Successfully','status':200})
        
class AddBusinessIMageAPI(generics.GenericAPIView):
    serializer_class=BusinessSerializer
    def post(self,request,*args,**kwargs):
        Business=request.POST['Business']
        files=[]
        if len(request.FILES.getlist('BusinessImages'))>0:
            files=request.FILES.getlist('BusinessImages')   
            profile=BusinessModel.objects.filter(User=request.POST['Business']).values()[0]
            Pstring=list(filter(None,str(profile['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(',')))
            newimages=[]
            for i in range(len(files)):
                fs = FileSystemStorage()
                ppn=str(datetime.now())+'.jpg'
                filename = fs.save(ppn, files[i])
                uploaded_file_url = fs.url(filename)
                Pstring.append(uploaded_file_url)
                newimages.append(uploaded_file_url)
            
            BusinessModel.objects.filter(User=request.POST['Business']).update(BusinessImages=Pstring)
        
        profile=BusinessModel.objects.filter(User=request.POST['Business']).values('BusinessImages')[0]
        profile['BusinessImages']=filter(None,str(profile['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
        profile['Email']=str(BusinessModel.objects.filter(User=request.POST['Business']).values('User__email')[0]['User__email'])[9:]
        s=BusinessServices.objects.filter(Business=request.POST['Business']).values('Service')
        return Response({'data':{'Profile':profile,"addedimage":newimages},'msg':'Business Image Added Successfully','status':200})


        
class EditBusinessHoursAPI(generics.GenericAPIView):
    queryset = BusinessWeekHours.objects.all()
    serializer_class=BusinessHoursSerializer
    def post(self, request, *args, **kwargs):
        p=BusinessWeekHours.objects.filter(Business=request.POST['Business'],id=request.data['id']).values()
        p.update(Day=request.POST.get('Day',p.values()[0]['Day']),       
        StartTime=request.POST.get('StartTime',p.values()[0]['StartTime']),
        CloseTime=request.POST.get('CloseTime',p.values()[0]['CloseTime']))
        return Response({
            "msg":'BusinessHours saved successfully',
            "status":200,
        })

class GetBusinessHours(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        data=BusinessWeekHours.objects.filter(Business=request.data['Business']).values()
        return Response({'data':data,'msg':'Business Hours.','status':200})        

class DeleteBusinessHours(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        data=BusinessWeekHours.objects.filter(Business=request.data['Business'],id=request.data['BusinessHour']).delete()
        data=BusinessWeekHours.objects.filter(Business=request.data['Business']).values()
        return Response({'data':data,'msg':'Business Hours.','status':200})   
        
class EditProfileAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        p=Profiles.objects.filter(User=request.data['User'])
        if len(p)>0:
            try:
                ProfileImage=request.FILES['ProfileImage']
                fs = FileSystemStorage()
                filename = fs.save('ProfileImage/'+ProfileImage.name, ProfileImage)
                uploaded_file_url = fs.url(filename).replace("/BeachPlus/media/",'')
                
                old_image = Profiles.objects.get(User=request.data['User'])
                try:
                    image_path = old_image.ProfileImage.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except:
                    a='leave it'
                p.update(ProfileImage=uploaded_file_url)
            except:
                a=1
        p.update(FirstName=request.POST.get('FirstName',p.values()[0]['FirstName']),
        LastName=request.POST.get('LastName',p.values()[0]['LastName']),
        Country=request.POST.get('Country',p.values()[0]['Country']),
        City=request.POST.get('City',p.values()[0]['City']),
        State=request.POST.get('State',p.values()[0]['State']),
        ZipCode=request.POST.get('ZipCode',p.values()[0]['ZipCode']),
        ProfileImage=request.POST.get('ProfileImage',p.values()[0]['ProfileImage']),
        latitude=request.POST.get('latitude',p.values()[0]['latitude']),
        longitude=request.POST.get('longitude',p.values()[0]['longitude']),
        CPFNumber=request.POST.get('CPFNumber',p.values()[0]['CPFNumber'])
        )
        u=User.objects.get(id=request.data['User'])
        if request.POST.get('password') is not None:
            u.set_password(request.data['password'])
            u.save()
        profile=p.values()[0]
        return Response({
            'data':{'Profile':profile},
            "msg":'Profile saved successfully',
            "status":200,
        })  
  
import json
class OnlinePlayerAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        
        # StartTime__lte=datetime.now().time(),CloseTime__gte=datetime.now().time()
        user=request.user
        d=OnlineUsers.objects.filter(Business=user.id,DateOfRecord__date=datetime.now().date()).values('Player_id','StartTime','CloseTime','Day',ProfileImage=F('Player__ProfileImage'),FirstName=F('Player__FirstName'),LastName=F('Player__LastName')).exclude(CloseTime__lte=datetime.now().time())
        
        return Response({
            'data':d,
            'msg':'Online Player',
            'status':200
        })
        
        
class EditBusiness(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        p=BusinessModel.objects.filter(User=request.data['Business'])
        if len(p)>0:
            try:
                ProfileImage=request.FILES['ProfileImage']
                fs = FileSystemStorage()
                filename = fs.save('ProfileImage/'+ProfileImage.name, ProfileImage)
                uploaded_file_url = fs.url(filename).replace("/BeachPlus/media/",'')
                
                old_image =BusinessModel.objects.get(User=request.data['Business'])
                try:
                    image_path = old_image.ProfileImage.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except:
                    a='leave it'
                p.update(ProfileImage=uploaded_file_url)
            except:
                a=1
        files=[]
        if len(request.FILES.getlist('BusinessImages'))>0:
            files=request.FILES.getlist('BusinessImages')   
            Pstring=[]
            for i in range(len(files)):
                fs = FileSystemStorage()
                ppn=str(datetime.now())+'.jpg'
                filename = fs.save(ppn, files[i])
                uploaded_file_url = fs.url(filename)
                Pstring.append(uploaded_file_url)
            
            BusinessModel.objects.filter(User=request.POST['Business']).update(BusinessImages=Pstring)
        p.update(Name=request.POST.get('Name',p.values()[0]['Name']),
        Address=request.POST.get('Address',p.values()[0]['Address']),
        Location=request.POST.get('Location',p.values()[0]['Location']),
        Contact=request.POST.get('Contact',p.values()[0]['Contact']),
        TennisCourts=request.POST.get('TennisCourts',p.values()[0]['TennisCourts']),
        CPFNumber=request.POST.get('CPFNumber',p.values()[0]['CPFNumber']),
        latitude=request.POST.get('latitude',p.values()[0]['latitude']),
        longitude=request.POST.get('longitude',p.values()[0]['longitude']),
        BusinessImages=request.POST.get('BusinessImages',p.values()[0]['BusinessImages']),
        Description=request.POST.get('Description',p.values()[0]['Description']),
        )
        uids=str(request.data.get('Services','')).replace('[','').replace(']','').split(',')
        if len(uids)>0:
            BusinessServices.objects.filter(Business=request.data['Business']).delete()
        for i in uids:
            d=dict()
            d['Business']=request.data['Business']
            d['Service']=i
            serializer2 = BusinessServicesSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
        p=BusinessModel.objects.filter(User=request.POST['Business']).values()[0]
        p['BusinessImages']=filter(None,str(p['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
        s=BusinessServices.objects.filter(Business=request.POST['Business']).values('Service')    
        return Response({
            "data":{'Profile':p,'Services':s},
            "msg":'Business saved successfully',
            "status":200,
        })  

from django.db.models import Avg
class MyProfileAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        MatchesPlayed1=Team1Players.objects.filter(Player=request.POST['User'])
        MatchesPlayed2=Team2Players.objects.filter(Player=request.POST['User'])
        MatchesPlayed=len(MatchesPlayed1)+len(MatchesPlayed2)
        
        MatchesHosted=len(HostMatches.objects.filter(User=request.POST['User']))
        
        MatchesWon1=Team1Players.objects.filter(Player=request.POST['User'],Result='Won')
        MatchesWon2=Team2Players.objects.filter(Player=request.POST['User'],Result='Won')
        MatchesWon=len(MatchesWon1)+len(MatchesWon2)
        
        Profiles.objects.filter(User=request.POST['User']).update(MatchesPlayed=MatchesPlayed,MatchesHosted=MatchesHosted,MatchesWon=MatchesWon)
        
        p=Profiles.objects.filter(User=request.POST['User']).values('FirstName','LastName','ProfileImage','Country','State','ZipCode','CPFNumber').values()[0]
        p['Email']=User.objects.filter(id=request.POST['User']).values('email')[0]['email']
        p['Rating']=PlayerRatings.objects.filter(PlayerRated=request.POST['User']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        return Response({
            'data':{'Profile':p},
            'msg':'MyProfile List',
            'status':200
        })        

class ForgotPasswordAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email=request.data['email']
        if request.data.get('UserType','User')=='Business':
            original_email=request.data['email']
            email='business_'+original_email
            
        u=User.objects.filter(email__iexact=email)
        if len(u)==0:
            return Response({"status":400,"msg":"Email does not exist.Please signup first."})
        else:
            x1 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(5))
            x2 = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(4))
            message = "Click on the below link to reset your password:\nhttp://aashima.parastechnologies.in/BeachPlus/ResetPwdTemplate/?code="+x1+str(u.values()[0]['id'])+x2
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId
            message = Mail(from_email='beachplusbr@gmail.com',to_emails=request.data['email'],subject="Reset Password Gun Instructor",html_content=message)
            sg = SendGridAPIClient('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')
            response = sg.send(message)

            return Response({"msg":'A Forgot Password link has been sent to your registered mail.',"status":200})

@api_view(['GET','POST'])
@csrf_exempt
def ResetPasswordAPI(request):
    code=request.GET['code']
    User_id=code[5:][:3]
    u=User.objects.get(id=User_id)
    dictValues={}
    dictValues['User_id']=User
    if u is not None:
        if request.method == 'POST':
            pwd=str(request.data['password'])
            ppwd=str(request.data['ppassword'])
        
            if pwd == ppwd and pwd != '' and ppwd != '':
                u.set_password(pwd)
                u.save()
                return HttpResponseRedirect('/BeachPlus/PwdResetSuccess/')
            else:
                dictValues['error']='Passwords do not match.'
                return render(request,'resetpassword.html',dictValues)
            
    return render(request,'resetpassword.html',dictValues)


class ResetPasswordAppAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        User_id=request.data['User_id']
        u=User.objects.get(id=User_id)
        pwd=str(request.data['password'])
        u.set_password(pwd)
        u.save()
        return Response({
            "msg":'Your password is changed successfully.',
            "status":200
        })  

class PwdResetSuccess(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        html = "<html><body>Your password has been reset.</body></html>" 
        return HttpResponse(html)


class ContactUs(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=ContactSerializer
    def post(self,request,*args,**kwargs):
        if request.data.get('UserType','User')=='Business':
            d=dict()
            d['User']=request.data['User']
            d['Name']=request.data.get('Name','')
            d['Email']=request.data.get('Email','')
            d['Subject']=request.data.get('Subject','')
            d['Message']=request.data.get('Message','')
            serializer3 = ContactFromBusinessSerializer(data=d)
            serializer3.is_valid(raise_exception=True)
            profile=serializer3.save()
        else:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            RA=serializer.save()
        
        return Response({'msg':'submitted.','status':200})

class InvitesFriendAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        match=HostInvitations.objects.filter(HostMatch=request.POST['HostMatch']).values()[0]
        h1=HostInvitations.objects.filter(HostMatch=request.POST['HostMatch']).delete()
        uids=str(request.data.get('UserInvited','')).replace("[", "").replace("]", "").split(",")
        for i in uids:
            d=dict()
            d['HostMatch']=match['HostMatch_id']
            d['UserInvited']=i
            serializer2 = InvitationsSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
            
            try:
                u_fn=HostMatches.objects.filter(id=request.POST['HostMatch']).values('User__FirstName','Title','User_id')[0]
                message_body=u_fn['User__FirstName']+' has invited you to the match '+u_fn['Title']+'.'
                User_id=int(u_fn['User_id'])
                device=Devices.objects.filter(User=i).values()[0]
                DeviceToken=device['DeviceToken']
                DT=device['DeviceType']
                Ntype='HostMatch'
                send_fcm(message_body,User_id,DeviceToken,DT,Ntype)
            except:
                print('notification not sent')
        h=dict()
        h["hostmatch"] = HostMatches.objects.filter(id=request.POST['HostMatch']).values()
        h["hostinvitaions"] = HostInvitations.objects.filter(HostMatch=request.POST['HostMatch']).values("UserInvited", ProfileImage=F("UserInvited__ProfileImage"))
        return Response({
            'data':h,
            'msg':'Invites List',
            'status':200
        }) 


class HostMatchAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=HostMatchSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        match=serializer.save()
        Profiles.objects.filter(User=request.POST['User']).update(MatchesHosted=len(HostMatches.objects.filter(User=request.POST['User'])))
        uids=str(request.data.get('UserInvited','')).replace('[','').replace(']','').split(',')
        for i in uids:
            d=dict()
            d['HostMatch']=match.id
            d['UserInvited']=i
            serializer2 = InvitationsSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
            try:
                d['User']=i
                message_body=Profiles.objects.filter(User=request.POST['User']).values()[0]['FirstName']+' has invited you to the match '+str(request.POST['Title'])+'.'
                User_id=int(request.POST['User'])
                d['Text']=message_body
                d['UserSending']=User_id
                serializer2 = NotificationSerializer(data=d)
                serializer2.is_valid(raise_exception=True)
                device=serializer2.save()
                
                device=Devices.objects.filter(User=i).values()[0]
                DeviceToken=device['DeviceToken']
                DT=device['DeviceType']
                Ntype='HostMatch'
                send_fcm(message_body,User_id,DeviceToken,DT,Ntype)
            except:
                do_nothing='do_nothing'
        return Response({'msg':'Host A Match','status':200})
    
        
class MyHostedOngoingMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        h=HostMatches.objects.filter(User=request.POST['User'],Status__in=['Initiated',1,2]).values('id','User','Title','Date','Time','Location','SelectMode','Status','DateAdded','player_counts',ProfileImage=F('User__ProfileImage')).order_by('-id')
        return Response({
            'data':h,
            'msg':'MyHostedOngoingMatches List',
            'status':200
            })  

class MyHostedCompletedMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        a_list=HostMatches.objects.filter(User=request.POST['User'],Status=3).values('id')
        total_detail=MatchSummary.objects.filter(HostMatch_id__in=a_list).values(Team1Score=F('Team1'),Team2Score=F('Team2'),Match_id=F('HostMatch_id'),Status=F('HostMatch__Status'),User=F('HostMatch__User'),Title=F('HostMatch__Title'),player_counts=F('HostMatch__player_counts'),ProfileImage=F('HostMatch__User__ProfileImage')).order_by('-HostMatch_id')
        return Response({
            'data':total_detail,
            'msg':'MyHostedCompletedMatches List',
            'status':200
        })

class MyAttendingOngoingMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        a_list=HostInvitations.objects.filter(UserInvited=request.POST['User'],Status='Attend').values('HostMatch_id')
        a=HostMatches.objects.filter(id__in=a_list,Status__in=[1,2,'Initiated']).order_by('-id').values()
        return Response({
            'data':a,
            'msg':'MyAttendingOngoingMatches List',
            'status':200
        })
        
class MyAttendingCompletedMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        a_list=HostInvitations.objects.filter(UserInvited=request.POST['User'],Status='Attend').values('HostMatch_id')
        a=HostMatches.objects.filter(id__in=a_list,Status=3).values('id','Status','User','Title','player_counts',ProfileImage=F('User__ProfileImage')).order_by('-id')
        total_detail=MatchSummary.objects.filter(HostMatch_id__in=a_list).values(Team1Score=F('Team1'),Team2Score=F('Team2'),Match_id=F('HostMatch_id'),Status=F('HostMatch__Status'),User=F('HostMatch__User'),Title=F('HostMatch__Title'),player_counts=F('HostMatch__player_counts'),ProfileImage=F('HostMatch__User__ProfileImage')).order_by('-HostMatch_id')
        for i in total_detail:
            team1=Team1Players.objects.filter(HostMatch=i['Match_id'])
            team1_players=team1.values_list('Player_id',flat=True)
            team2=Team2Players.objects.filter(HostMatch=i['Match_id'])
            team2_players=team2.values_list('Player_id',flat=True)
            
            if int(request.POST['User']) in team1_players and team1.values()[0]['Result']=='Won':
                i['Result']='You won.'
            if int(request.POST['User']) in team1_players and team1.values()[0]['Result']=='Lost':
                i['Result']='You lost.'
            if int(request.POST['User']) in team1_players and team1.values()[0]['Result']=='Draw':
                i['Result']='You draw.'
            if int(request.POST['User']) in team2_players and team2.values()[0]['Result']=='Won':
                i['Result']='You won.'
            if int(request.POST['User']) in team2_players and team2.values()[0]['Result']=='Lost':
                i['Result']='You lost.'
            if int(request.POST['User']) in team2_players and team2.values()[0]['Result']=='Draw':
                i['Result']='You draw.'
                
        return Response({
            'data':total_detail,
            'msg':'MyAttendingCompletedMatches List',
            'status':200
        })

class EndRound(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=MatchRoundSerializer
    def post(self,request,*args,**kwargs):
        if len(MatchRounds.objects.filter(HostMatch=request.POST['HostMatch']))>0:
            MatchRounds.objects.filter(HostMatch=request.POST['HostMatch'])
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'msg':'Ended Round.','status':200})


class CancelMatch(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        h=HostMatches.objects.filter(id=request.POST['Match_id']).delete()
        return Response({
            'msg':'Cancelled Match.',
            'status':200
        })  

class RatePlayer(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=RatePlayerSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'msg':'Ended Round.','status':200})
     
from django.core.exceptions import ObjectDoesNotExist        
class MatchDetailAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        player_counts=request.POST['player_counts']
        player_1=int(player_counts)/2
        
        m=HostMatches.objects.filter(id=request.POST['Match_id']).values('id','User','Title','Location','Date','Time',status=F('Status'))[0]
        n=HostInvitations.objects.filter(HostMatch=request.POST['Match_id']).values('UserInvited',FirstName=F('UserInvited__FirstName'),LastName=F('UserInvited__LastName'),ProfileImage=F('UserInvited__ProfileImage'))
        r=MatchRounds.objects.filter(HostMatch=request.POST['Match_id']).values('Team1Score','Team2Score','Round')
        team1player_list=Team1Players.objects.filter(HostMatch=request.POST['Match_id']).values(UserInvited_id=F('Player_id'),FirstName=F('Player__FirstName'),LastName=F('Player__LastName'),ProfileImage=F('Player__ProfileImage'))
        team2player_list=Team2Players.objects.filter(HostMatch=request.POST['Match_id']).values(UserInvited_id=F('Player_id'),FirstName=F('Player__FirstName'),LastName=F('Player__LastName'),ProfileImage=F('Player__ProfileImage'))
        
        for i in team1player_list:
            i['Rating']=PlayerRatings.objects.filter(PlayerRated=i['UserInvited_id'],HostMatch=request.POST['Match_id']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
        for i in team2player_list:
            i['Rating']=PlayerRatings.objects.filter(PlayerRated=i['UserInvited_id'],HostMatch=request.POST['Match_id']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
            
        # teamplayer_Rating = PlayerRatings.objects.filter(PlayerRated=OuterRef('Player_id'),HostMatch=request.POST['Match_id']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
        # team1player_list=Team1Players.objects.filter(HostMatch=request.POST['Match_id']).annotate(Rating=Subquery(PlayerRatings.objects.filter(PlayerRated=OuterRef('Player'),HostMatch=request.POST['Match_id']).values('Rating').aggregate(Avg('Rating'))['Rating__avg'])).values('Rating',UserInvited_id=F('Player_id'),FirstName=F('Player__FirstName'),LastName=F('Player__LastName'),ProfileImage=F('Player__ProfileImage'))
        # team2player_list=Team2Players.objects.filter(HostMatch=request.POST['Match_id']).annotate(Rating=Subquery(PlayerRatings.objects.filter(PlayerRated=OuterRef('Player'),HostMatch=request.POST['Match_id']).values('Rating').aggregate(Avg('Rating'))['Rating__avg'])).values('Rating',UserInvited_id=F('Player_id'),FirstName=F('Player__FirstName'),LastName=F('Player__LastName'),ProfileImage=F('Player__ProfileImage'))
        
        
        # team1player_list['Rating']=PlayerRatings.objects.filter(PlayerRated=OuterRef['Player_id'],HostMatch=request.POST['Match_id']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        # team2player_list['Rating']=PlayerRatings.objects.filter(HostMatch=request.POST['Match_id']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        return Response({
            'data':{'MatchDetails':m,'UserInvited':n,'Team1':team1player_list,'Team2':team2player_list,'RoundDetails':r},
            'msg':'MyProfile List',
            'status':200
        })  
        

class InvitationsAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=HostInvitations.objects.filter(UserInvited=request.POST['User']).values('HostMatch_id','HostMatch__Title','HostMatch__Date','HostMatch__Time','HostMatch__Location','HostMatch__SelectMode')
        return Response({
            'data':p.values(),
            'msg':'MyProfile List',
            'status':200
        })     

class InvitationDetailAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=HostInvitations.objects.filter(UserInvited=request.POST['Invite_id']).values('HostMatch_id','HostMatch__Title','HostMatch__Date','HostMatch__Time','HostMatch__Location','HostMatch__SelectMode','HostMatch__User_id','HostMatch__User__ProfileImage','HostMatch__User__FirstName','HostMatch__User__LastName','HostMatch__User__MatchesPlayed','HostMatch__User__MatchesWon','HostMatch__User__MatchesHosted')
        return Response({
            'data':p.values(),
            'msg':'MyProfile List',
            'status':200
        })     



class Home(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        filters={k: v for k, v in request.data.items() if (v and (k=='City' or k=='State' or k=='Country'))}    
        np=Profiles.objects.filter(**filters).values()
        Business=BusinessModel.objects.all().values()
        if not request.POST.get('City',False):
            filters['City']=Profiles.objects.filter(User=request.POST['User']).values()[0]['City']
        if not request.POST.get('State',False):
            filters['State']=Profiles.objects.filter(User=request.POST['User']).values()[0]['State']
        a=1
        if a==1:
            lat= request.POST.get('latitude',0) #profile['latitude']
            lon= request.POST.get('longitude',0) #profile['longitude']
            
            if request.POST.get('latitude',0)=='':
                lat=0
            if request.POST.get('longitude',0)=='':
                lon=0    
            
            lat=float(lat)
            lon=float(lon)
            
            profile=Profiles.objects.filter(User=request.POST['User']).update(latitude=lat,longitude=lon)
            
            if lat or lon:
                Friends1=FriendRequests.objects.filter(Sender=request.POST['User']).values_list('Receiver_id')        
                Friends2=FriendRequests.objects.filter(Receiver=request.POST['User']).values_list('Sender_id')        
                Friends=list(Friends1)+list(Friends2)
                all_l=Profiles.objects.filter(**filters).exclude(User=request.POST['User']).exclude(User__in=Friends).values("User_id","ProfileImage","FirstName","LastName","Country","City","State","latitude","longitude","ZipCode","CPFNumber","MatchesHosted","MatchesWon","MatchesPlayed","DateAdded",Email=F("User__email"))
                distanc=[]
                for i in all_l:
                    lat2=i['latitude']
                    lon2=i['longitude']
                    if lat2 or lon2:
                        from math import sin, cos, sqrt, atan2, radians
                        lat1 = radians(lat)
                        lon1 = radians(lon)
                        R = 6373.0
                        lat2=radians(lat2)
                        lon2=radians(lon2)
                        dlon = lon2 - lon1
                        dlat = lat2 - lat1
                        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        distanc.append(R * c)
                    else:
                        distanc.append(2*6.28*6500)
                # return Response({"all_l":pd.DataFrame(list(all_l)})  
                import pandas as pd
                df = pd.DataFrame(list(all_l)) ## this will save 50% memory
                df = df.where(pd.notnull(df), None)
                df['distance']=distanc
                df=df[df['distance']<10]
                df=df.sort_values('distance')
                df=df.to_dict('records')
                np=df
                
                all_l=BusinessModel.objects.all().values("User_id","ProfileImage","Name","Address","BusinessImages","Location","latitude","longitude","Contact","CPFNumber","Description","TennisCourts",Email=F("User__email"))
                distanc=[]
                for i in all_l:
                    i['BusinessImages']=filter(None,str(i['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
                    i['Email']=str(i['Email'])[9:]
                    lat2=i['latitude']
                    lon2=i['longitude']
                    if lat2 or lon2:
                        from math import sin, cos, sqrt, atan2, radians
                        lat1 = radians(lat)
                        lon1 = radians(lon)
                        R = 6373.0
                        lat2=radians(lat2)
                        lon2=radians(lon2)
                        dlon = lon2 - lon1
                        dlat = lat2 - lat1
                        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        distanc.append(R * c)
                    else:
                        distanc.append(2*6.28*6500)
                df = pd.DataFrame(list(all_l)) ## this will save 50% memory
                df=df.fillna({"User_id": 0,"ProfileImage": "","Name": "","Address": "","BusinessImages": "","Location": "","latitude": 0,"longitude": 0,"Contact": 0, "CPFNumber": "","Description": "","TennisCourts": 0,"Email": "","distance": 6500})
                df = df.where(pd.notnull(df), None)
                df['distance']=distanc
                df=df[df['distance']<10]
                df=df.sort_values('distance')
                df=df.to_dict('records') 
                Business=df
    
                return Response({'data':{'NearbyPlayers':np,'Business':Business},'msg':'Home with sort','status':200})
        return Response({'data':{'NearbyPlayers':np,'Business':Business},'msg':'Home','status':200})
        
class BussinessDetail(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=BusinessModel.objects.filter(User=request.POST['Business']).values('User__email','Name','ProfileImage','Address','Location','Contact','Description','TennisCourts','BusinessImages','latitude','longitude').values()[0]
        p['OnlinePlayers']=OnlineUsers.objects.filter(Business=request.POST['Business'],SelectMode='Open',DateOfRecord__date=datetime.now().date(),StartTime__lte=datetime.now().time(),CloseTime__gte=datetime.now().time()).values('SelectMode','Player')
        p['Email']=str(BusinessModel.objects.filter(User=request.POST['Business']).values('User__email')[0]['User__email'])[9:]
        p['BusinessImages']=filter(None,str(p['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
        s=BusinessServices.objects.filter(Business=request.POST['Business']).values('Service')
        p['Hours']=BusinessWeekHours.objects.filter(Business=request.POST['Business']).values()
        p['IsOnline']=OnlineUsers.objects.filter(Business=request.POST['Business'],Player=request.POST.get('Player',0),DateOfRecord__date=datetime.now().date(),StartTime__lte=datetime.now().time(),CloseTime__gte=datetime.now().time()).exists()
        return Response({
            'data':{'Profile':p,'Services':s},
            'msg':'MyProfile List',
            'status':200
        })                

class PlayerProfile(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=Profiles.objects.filter(User=request.POST['Player']).values()[0]#('FirstName','LastName','ProfileImage','State','State','ZipCode','CPFNumber')[0]
        p['Rating']=PlayerRatings.objects.filter(PlayerRated=request.POST['Player']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
        return Response({
            'data':p,
            'msg':'PlayerProfile List',
            'status':200
        })   
   
class MatchesAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(UserInvited=request.POST['UserInvited'],Status='Sent').values('DateAdded',Match_id=F('HostMatch_id'),User_id=F('HostMatch__User'),Title=F('HostMatch__Title'),Date=F('HostMatch__Date'),Time=F('HostMatch__Time'),Location=F('HostMatch__Location'),ProfileImage=F('HostMatch__User__ProfileImage'),FirstName=F('HostMatch__User__FirstName'),LastName=F('HostMatch__User__LastName'),Email=F('HostMatch__User__User__email'))
        return Response({
            'data':data,
            'msg':'Matches API',
            'status':200
        })
        
class AttendMatch(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(id=request.POST['User']).update(Status='Attend',DateAdded=datetime.now())
        return Response({
            'msg':'Attend Match',
            'status':200
        })
        
class DeclineMatch(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(id=request.POST['User']).delete()
        return Response({
            'msg':'Decline Match',
            'status':200
        })
        
        
class AttendMatchAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(UserInvited=request.POST['User'],HostMatch=request.POST['HostMatch'])
        
        if data.count()==0:
            d=dict()
            d['HostMatch']=request.POST['HostMatch']
            d['UserInvited']=request.POST['User']
            serializer2 = InvitationsSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            invite=serializer2.save()
            invite.Status='Attend'
            invite.save()
        else:
            if data.values()[0]['Status']=='Attend':
                return Response({'msg':'Already attending this Match','status':200})
        
        data.update(Status='Attend')
        
        match=HostMatches.objects.filter(id=request.POST['HostMatch']).values()[0]
        player_counts=match['player_counts']
        player_1=int(player_counts)/2
        
        team1_existing_count=Team1Players.objects.filter(HostMatch=request.POST['HostMatch']).count()
        team2_existing_count=Team2Players.objects.filter(HostMatch=request.POST['HostMatch']).count()
        
        d=dict()
        d['HostMatch']=request.POST['HostMatch']
        d['Player']=request.POST['User']
        
        
        if team1_existing_count<player_1:
            serializer2 = Team1Serializer(data=d)
        elif team2_existing_count<player_1:
            serializer2 = Team2Serializer(data=d)
            
        serializer2.is_valid(raise_exception=True)
        device=serializer2.save()
        
        MatchesPlayed1=Team1Players.objects.filter(Player=request.POST['User'])
        MatchesPlayed2=Team2Players.objects.filter(Player=request.POST['User'])
        MatchesPlayed=len(MatchesPlayed1)+len(MatchesPlayed2)
        
        Profiles.objects.filter(User=request.POST['User']).update(MatchesPlayed=MatchesPlayed)
        
        try:
            du=HostMatches.objects.filter(id=request.POST['HostMatch']).values()[0]['User_id']
            User_id=int(request.POST['User'])
            d['User']=du
            message_body='Great News,'+Profiles.objects.filter(User=request.POST['User']).values()[0]['FirstName']+' has accepted your invitation.'
            d['Text']=message_body
            d['UserSending']=User_id
            serializer2 = NotificationSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
            device=Devices.objects.filter(User=du).values()[0]
            DeviceToken=device['DeviceToken']
            DT=device['DeviceType']
            Ntype='AttendMatch'
            send_fcm(message_body,User_id,DeviceToken,DT,Ntype)
        except:
            do_nothing='do_nothing'
        return Response({
            'msg':'Attend Match',
            'status':200
        })

        
class DeclineMatchAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(UserInvited=request.POST['User'],HostMatch=request.POST['HostMatch'])
        data.update(Status='Decline')
        if data.count()==0:
            d=dict()
            d['HostMatch']=request.POST['HostMatch']
            d['UserInvited']=request.POST['User']
            serializer2 = InvitationsSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            invite=serializer2.save()
            invite.Status='Decline'
            invite.save()
        try:
            User_id=int(request.POST['User'])
            du=HostMatches.objects.filter(id=request.POST['HostMatch']).values()[0]['User_id']
            d['User']=du
            message_body='Sorry,'+Profiles.objects.filter(User=request.POST['User']).values()[0]['FirstName']+' is unableto accept your invitation.'
            d['Text']=message_body
            User_id=int(request.POST['User'])
            
            serializer2 = NotificationSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
            device=Devices.objects.filter(User=du).values()[0]
            DeviceToken=device['DeviceToken']
            DT=device['DeviceType']
            Ntype='DeclineMatch'
            send_fcm(message_body,User_id,DeviceToken,DT,Ntype)
        except:
            do_nothing='do_nothing'    
        return Response({
            'msg':'Cancel Match',
            'status':200
        })
   
class FindMatches(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        filters={k: v for k, v in request.data.items() if (v and (k=='Date'))}    
        np=HostMatches.objects.filter(SelectMode='Public').filter(**filters).values()
        a=1
        if a==1:
            lat= float(request.POST['latitude']) #profile['latitude']
            lon= float(request.POST['longitude']) #profile['longitude']
            if lat or lon:
                AttendingMatches=HostInvitations.objects.filter(UserInvited=request.POST['User'],Status='Attend').values_list('HostMatch',flat=True)
                DecliningMatches=HostInvitations.objects.filter(UserInvited=request.POST['User'],Status='Decline').values_list('HostMatch',flat=True)
                ExcludeMatches=list(AttendingMatches)+list(DecliningMatches)
                PublicMatches=HostMatches.objects.filter(SelectMode='Public').values_list('id',flat=True)
                InvitationsSent=HostInvitations.objects.filter(UserInvited=request.POST['User'],Status='Sent').values_list('HostMatch',flat=True)
                PrivateMatches=HostMatches.objects.filter(SelectMode='Private',id__in=InvitationsSent).values_list('id',flat=True)
                IncludeMatches=list(PublicMatches)+list(PrivateMatches)
                
                all_l=HostMatches.objects.filter(**filters).filter(id__in=IncludeMatches).exclude(User=request.POST['User']).exclude(id__in=ExcludeMatches).values('id','User_id','Title','Date','Time','Location','latitude','longitude',ProfileImage=F('User__ProfileImage'),FirstName=F('User__FirstName'),LastName=F('User__LastName'))
                distanc=[]
                for i in all_l:
                    lat2=i['latitude']
                    lon2=i['longitude']
                    if lat2 or lon2:
                        from math import sin, cos, sqrt, atan2, radians
                        lat1 = radians(lat)
                        lon1 = radians(lon)
                        R = 6373.0
                        lat2=radians(lat2)
                        lon2=radians(lon2)
                        dlon = lon2 - lon1
                        dlat = lat2 - lat1
                        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                        c = 2 * atan2(sqrt(a), sqrt(1 - a))
                        distanc.append(R * c)
                    else:
                        distanc.append(2*6.28*6500)
                df = pd.DataFrame(list(all_l)) 
                df = df.where(pd.notnull(df), None)
                df['distance']=distanc
                if not request.POST.get('distance',False):
                    df=df[df['distance']<10]
                else:
                    df=df[df['distance']<float(request.POST['distance'])]
                df=df.sort_values('distance')
                df=df.to_dict('records')
                np=df
                return Response({'data':np,'msg':'Home with sort','status':200})
        return Response({'data':np,'msg':'Home','status':200})
       

class Leaderboard(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        P=Profiles.objects.all().exclude(MatchesWon=0).order_by('-MatchesWon').values('ProfileImage','FirstName','LastName','MatchesWon')
        return Response({'data':P,'msg':'UserList','status':200})

class Notifications(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        N=Notification.objects.filter(User=request.POST['User']).values('User','HostMatch','Text','DateAdded',ProfileImage=F('HostMatch__User__ProfileImage'),FirstName=F('HostMatch__User__FirstName'),LastName=F('HostMatch__User__LastName'))
        return Response({
            'data':N,
            'msg':'FindMatches List',
            'status':200
        }) 
        
class LogOutAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        u=Devices.objects.filter(User=request.data['User']).delete()
        return Response({
            'msg':'Logout successful',
            'status':200
                
        })  


class SendRequest(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,) 
    serializer_class=FriendRequestsSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        try:
            message_body=Profiles.objects.filter(User=request.POST['Sender']).values()[0]['FirstName']+' has sent you a friend request.'
            User_id=int(request.POST['Sender'])
            d['UserSending']=User_id
            d['User']=request.POST['Reciever']
            d['Text']=message_body
            serializer2 = NotificationSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
            
            
            device=Devices.objects.filter(User=request.POST['Reciever']).values()[0]
            DeviceToken=device['DeviceToken']
            DT=device['DeviceType']
            Ntype='SentFriendRequest'
            send_fcm(message_body,User_id,DeviceToken,DT,Ntype)
        except:
            do_nothing='do_nothing'    
        return Response({'data':serializer.data,'msg':'Request Sent.','status':200})       


class CancelRequest(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        FriendRequests.objects.filter(id=request.POST['Request_id']).delete()
        return Response({'msg':'Request Cancelled.','status':200})


class Unfriend(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        FriendRequests.objects.filter(id=request.POST['Request_id'],Status='Accept').delete()
        return Response({'msg':'Unfriend.','status':200})

class MyFriends(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        f=dict()
        F1=FriendRequests.objects.filter(Receiver=request.POST['User'],Status='Accept').values('id','DateAdded',User_id=F('Sender_id'),ProfileImage=F('Sender__ProfileImage'),FirstName=F('Sender__FirstName'),LastName=F('Sender__LastName'),Email=F('Sender__User__email'),City=F('Sender__City'),State=F('Sender__State'),Country=F('Sender__Country'),latitude=F('Sender__latitude'),longitude=F('Sender__longitude'),ZipCode=F('Sender__ZipCode'),CPFNumber=F('Sender__CPFNumber'),MatchesHosted=F('Sender__MatchesHosted'),MatchesWon=F('Sender__MatchesWon'),MatchesPlayed=F('Sender__MatchesPlayed'))
        F2=FriendRequests.objects.filter(Sender=request.POST['User'],Status='Accept').values('id','DateAdded',User_id=F('Receiver_id'),ProfileImage=F('Receiver__ProfileImage'),FirstName=F('Receiver__FirstName'),LastName=F('Receiver__LastName'),Email=F('Receiver__User__email'),City=F('Receiver__City'),State=F('Receiver__State'),Country=F('Receiver__Country'),latitude=F('Receiver__latitude'),longitude=F('Receiver__longitude'),ZipCode=F('Receiver__ZipCode'),CPFNumber=F('Receiver__CPFNumber'),MatchesHosted=F('Receiver__MatchesHosted'),MatchesWon=F('Receiver__MatchesWon'),MatchesPlayed=F('Receiver__MatchesPlayed'))
        f=list(F1)+list(F2)
        return Response({'data':f,'msg':'Unfriend.','status':200})        


class SentRequestsListAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        requests=FriendRequests.objects.filter(Sender=request.POST['User'],Status='Sent').values('id','DateAdded',User_id=F('Receiver_id'),ProfileImage=F('Receiver__ProfileImage'),FirstName=F('Receiver__FirstName'),LastName=F('Receiver__LastName'),Email=F('Receiver__User__email'),City=F('Receiver__City'),State=F('Receiver__State'),Country=F('Receiver__Country'),latitude=F('Receiver__latitude'),longitude=F('Receiver__longitude'),ZipCode=F('Receiver__ZipCode'),CPFNumber=F('Receiver__CPFNumber'),MatchesHosted=F('Receiver__MatchesHosted'),MatchesWon=F('Receiver__MatchesWon'),MatchesPlayed=F('Receiver__MatchesPlayed'))
        return Response({
            'data':requests,
            'msg':'Send RequestsList',
            'status':200
        })

class AcceptFriendAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        data=FriendRequests.objects.filter(id=request.POST['Request_id'])
        data.update(Status='Accept')
        try:
            message_body=Profiles.objects.filter(User=data.values()[0]['Reciever_id']).values()[0]['FirstName']+' has accepted your friend request.'
            User_id=int(data.values()[0]['Reciever_id'])
            d['UserSending']=User_id
            d['User']=data.values()[0]['Sender_id']
            d['Text']=message_body
            serializer2 = NotificationSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
            device=Devices.objects.filter(User=data.values()[0]['Sender_id']).values()[0]
            DeviceToken=device['DeviceToken']
            DT=device['DeviceType']
            Ntype='AcceptFriendRequest'
            send_fcm(message_body,User_id,DeviceToken,DT,Ntype)
        except:
            do_nothing='do_nothing'    
        
        return Response({
            'msg':'Accept Friend',
            'status':200
        })
  
  
class DeclineFriendAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        FriendRequests.objects.filter(id=request.POST['Request_id']).delete()
        try:
            message_body=Profiles.objects.filter(User=data.values()[0]['Reciever_id']).values()[0]['FirstName']+' has accepted your friend request.'
            User_id=int(data.values()[0]['Reciever_id'])
            d['UserSending']=User_id
            d['User']=data.values()[0]['Sender_id']
            d['Text']=message_body
            serializer2 = NotificationSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            device=serializer2.save()
            device=Devices.objects.filter(User=data.values()[0]['Sender_id']).values()[0]
            DeviceToken=device['DeviceToken']
            DT=device['DeviceType']
            Ntype='DeclineFriendRequest'
            send_fcm(message_body,User_id,DeviceToken,DT,Ntype)
        except:
            do_nothing='do_nothing'    
        return Response({
            'msg':'Decline Friend',
            'status':200
        })
        
class ReceivedRequestsListAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        FR=FriendRequests.objects.filter(Receiver=request.POST['Receiver'],Status='Sent').values('id','DateAdded',User_id=F('Sender_id'),ProfileImage=F('Sender__ProfileImage'),FirstName=F('Sender__FirstName'),LastName=F('Sender__LastName'),Email=F('Sender__User__email'),City=F('Sender__City'),State=F('Sender__State'),Country=F('Sender__Country'),latitude=F('Sender__latitude'),longitude=F('Sender__longitude'),ZipCode=F('Sender__ZipCode'),CPFNumber=F('Sender__CPFNumber'),MatchesHosted=F('Sender__MatchesHosted'),MatchesWon=F('Sender__MatchesWon'),MatchesPlayed=F('Sender__MatchesPlayed'))
        return Response({
            'data':FR,
            'msg':'List',
            'status':200
        })

class ScoreMatchDetailsAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        data=request.data
        Round=data['Round']
        Team1Score=data['Team1Score']
        Team2Score=data['Team2Score']
        hostmatch=HostInvitations.objects.filter(HostMatch=request.POST['Match_id'],Status="Attend").values()[0]
        d=dict()
        d['HostMatch']=hostmatch['HostMatch_id']
        d['Team1Score']=Team1Score    
        d['Team2Score']=Team2Score    
        d['Round']=Round  
        HostMatches.objects.filter(id=request.POST['Match_id']).update(Status=Round)
        ser=MatchRoundSerializer(data=d)
        if ser.is_valid():
            ser.save()
            if Round=='3':
                all_rounds=MatchRounds.objects.filter(HostMatch=request.POST['Match_id']).values('Round','HostMatch_id').distinct()
                rounds_won_team1=0
                rounds_won_team2=0
                for j in all_rounds:
                    jj=MatchRounds.objects.filter(HostMatch=j['HostMatch_id'],Round=j['Round']).values('Team1Score','Team2Score')[0]
                    if int(jj['Team1Score'])>int(jj['Team2Score']):
                        rounds_won_team1=rounds_won_team1+1
                    if int(jj['Team1Score'])<int(jj['Team2Score']):
                        rounds_won_team2=rounds_won_team2+1  
                if rounds_won_team1>rounds_won_team2:
                    t1=Team1Players.objects.filter(HostMatch=request.POST['Match_id'])
                    t1.update(Result='Won')
                    t1_players=t1.values_list('Player',flat=True)
                    # for i in t1_players:
                    #     MatchesWon1=len(Team1Players.objects.filter(Player__in=i,Result='Won'))
                    #     MatchesWon2=len(Team2Players.objects.filter(Player__in=t1_players,Result='Won'))
                    #     MatchesWon=MatchesWon1+MatchesWon2
                    #     Profiles.objects.filter(User=i).update(MatchesWon=MatchesWon)
                    Profiles.objects.filter(User__in=t1_players).update(MatchesWon=F('MatchesWon')+1)
                if rounds_won_team1<rounds_won_team2:
                    t2=Team2Players.objects.filter(HostMatch=request.POST['Match_id'])
                    t2.update(Result='Won')    
                    t2_players=t2.values_list('Player',flat=True)
                    Profiles.objects.filter(User__in=t2_players).update(MatchesWon=F('MatchesWon')+1)
                if rounds_won_team1==rounds_won_team2:
                    Team1Players.objects.filter(HostMatch=request.POST['Match_id']).update(Result='Draw')
                    Team2Players.objects.filter(HostMatch=request.POST['Match_id']).update(Result='Draw')
                d['Team1']=rounds_won_team1    
                d['Team2']=rounds_won_team2
                summary=MatchSummarySerializer(data=d) 
                summary.is_valid(raise_exception=True)
                summary.save()
            return Response({
                        'msg':'Saves the scores according to hostmatch',
                        'status':200})   
        else:
            return Response({'msg':'does not exists','status':400})

class RoomList(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        
        mesages = SingleRoomMessage.objects.filter(Room=OuterRef('pk')).order_by('-timestamp')
        unread_mesages_list = SingleRoomMessage.objects.filter(Room=OuterRef('pk'),message_read=False).exclude(User=request.POST['User']).order_by().annotate(count=Func(F('id'), function='Count')).values('count')
        
        SC1=SingleChatRoom.objects.annotate(unread_messages=Subquery(unread_mesages_list)).annotate(recent_message=Subquery(mesages.values('content')[:1])).filter(user1=request.POST['User']).values('unread_messages','recent_message','DateAdded',Room_id=F('id'),User_id=F('user2_id'),FirstName=F('user2__FirstName'),LastName=F('user2__LastName'),ProfileImage=F('user2__ProfileImage'))
        SC2=SingleChatRoom.objects.annotate(unread_messages=Subquery(unread_mesages_list)).annotate(recent_message=Subquery(mesages.values('content')[:1])).filter(user2=request.POST['User']).values('unread_messages','recent_message','DateAdded',Room_id=F('id'),User_id=F('user1_id'),FirstName=F('user1__FirstName'),LastName=F('user1__LastName'),ProfileImage=F('user1__ProfileImage'))
        
        SC= SC1.union(SC2)
        
        data=SC.order_by('-DateAdded')
        
        return Response({
            'data':data,
            'msg':'Room List',
            'status':200
        })

class ChatHistory(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        SingleRoomMessage.objects.filter(Room=request.POST['Room_id'],User=request.POST['User_id']).update(message_read=True)
        
        data_own=SingleRoomMessage.objects.filter(Room=request.POST['Room_id'])
        
        data=data_own 
        data=data.order_by('timestamp').values('content','timestamp','User_id')#,'Status')
        Profile_User2=SingleChatRoom.objects.filter(id=request.POST['Room_id'],user2=request.POST['User_id'])
        Profile_User1=SingleChatRoom.objects.filter(id=request.POST['Room_id'],user1=request.POST['User_id'])
        Profile_User=[]
        if Profile_User2.exists():
            Profile_User=Profile_User2.values(User_id=F('user2_id'),FirstName=F('user2__FirstName'),LastName=F('user2__LastName'),ProfileImage=F('user2__ProfileImage'))
            
        if Profile_User1.exists():
            Profile_User=Profile_User1.values(User_id=F('user1_id'),FirstName=F('user1__FirstName'),LastName=F('user1__LastName'),ProfileImage=F('user1__ProfileImage'))
        return Response({
            'data':data,
            'profile':Profile_User,
            'msg':'Room List',
            'status':200
        })


def All(request):
    return render(request,'all.html')

from django.core.paginator import Paginator
@login_required(redirect_field_name='next', login_url='/BeachPlus/login/')
def index(request):
    data=Profiles.objects.all().order_by('-User_id')
    
    total_users=data.count()
    total_matches=HostMatches.objects.all().count()
    total_buisness=BusinessModel.objects.all().count()
    d=Profiles.objects.filter(IsSuspended=0)
    if request.method=='POST':
        UserId=request.POST['UserId']
        Profiles.objects.filter(User=UserId).update(IsSuspended=1)
        return redirect('/BeachPlus/index/')
    p = Paginator(data, 10) 
    page_number = request.GET.get('page',1)
    
    data = p.get_page(page_number)
        
    context={
        'd':d,
        'data':data,
        'total_users':total_users,
        'total_matches':total_matches,
        'total_buisness':total_buisness
    }
    return render(request,'index.html',context)
    


@login_required(redirect_field_name='next', login_url='/BeachPlus/login/')
def Business(request,pk):
    business=BusinessModel.objects.get(User_id=pk)
    services=BusinessServices.objects.filter(Business=pk).values()
    context={
        'business':business,
        'services':services
    }
    return render(request,'business_detail.html',context)   



@login_required(redirect_field_name='next', login_url='/BeachPlus/login/')
def BusinessManagement(request):
    data=BusinessModel.objects.all()
    p = Paginator(data, 10) 
    page_number = request.GET.get('page',1)
    
    data = p.get_page(page_number)
    return render(request,'business_management.html',{'data':data})
    


def login(request):
    dictValues={}
    dictValues['error'] = None
    if request.method=='POST':
        Email=request.POST.get('email')
        Password=request.POST.get('password')
        try:
            u=User.objects.get(username=Email,is_superuser=True)
            if u.check_password(Password):
                django_login(request,u)
                 
                return HttpResponseRedirect('/BeachPlus/index/')
            else:
                dictValues['error'] = 'Invalid username/password combination'
                return render(request,'login.html',dictValues)
        except:
            dictValues['error'] = 'You are not an admin.'
            return render(request,'login.html',dictValues)
    return render(request,'login.html',dictValues)



@login_required(login_url='/BeachPlus/login/')
def Report(request):
    data=Contact.objects.all()
    p = Paginator(data, 10) 
    page_number = request.GET.get('page',1)
    
    data = p.get_page(page_number)
    return render(request,'report_management.html',{'data':data})



# @login_required(redirect_field_name='next', login_url='/BeachPlus/login/')
# def UserManagement(request):
#     data=Profiles.objects.all()
#     return render(request,'user_management.html',{'data':data})

@login_required(redirect_field_name='next', login_url='/BeachPlus/login/')
def UserManagement(request):
    data=Profiles.objects.filter(IsSuspended=0).order_by('-User_id')
    if request.method=='POST':
        UserId=request.POST['UserId']
        Profiles.objects.filter(User=UserId).update(IsSuspended=1)
        return redirect('/BeachPlus/UserManagement/')
    p = Paginator(data, 10) 
    page_number = request.GET.get('page',1)
    
    data = p.get_page(page_number)    
    return render(request,'user_management.html',{'data':data})


from django.contrib import auth

def Logout(request):
    auth.logout(request)
    return redirect('login')
    
    
    
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from BeachPlus import settings
# from app.serializers import MessageModelSerializer, UserModelSerializer
# from app.models import MessageModel



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


# class MessageModelViewSet(ModelViewSet):
#     # queryset = MessageModel.objects.filter(user=request.POST['User'],recipient=request.POST['recipient'],Body=request.POST['Body'])
#     queryset=MessageModel.objects.all()
#     serializer_class = MessageModelSerializer
#     allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
#     # authentication_classes = (CsrfExemptSessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     pagination_class = MessagePagination
#     # def post(self,request,*args,**kwargs):
#     #     serializer=self.get_serializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     RA=serializer.save()
#     #     return Response(serializer.data)
#     def list(self, request, *args, **kwargs):
#         self.queryset = self.queryset.filter(Q(recipient=request.user) |
#                                              Q(user=request.user))
#         target = self.request.query_params.get('target', None)
#         if target is not None:
#             self.queryset = self.queryset.filter(
#                 Q(recipient=request.user, user__username=target) |
#                 Q(recipient__username=target, user=request.user))
#             self.queryset=self.queryset.create()
#         return super(MessageModelViewSet, self).list(request, *args, **kwargs)

#     def retrieve(self, request, *args, **kwargs):
#         msg = get_object_or_404(
#             self.queryset.filter(Q(recipient=request.user) |
#                                  Q(user=request.user),
#                                  Q(pk=kwargs['pk'])))
#         serializer = self.get_serializer(msg)
#         return Response(serializer.data)
   




# class UserModelViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserModelSerializer
#     allowed_methods = ('GET', 'HEAD', 'OPTIONS')
#     pagination_class = None  # Get all user

#     def list(self, request, *args, **kwargs):
#         # Get all users except yourself
#         self.queryset = self.queryset.exclude(id=request.user.id)
#         return super(UserModelViewSet, self).list(request, *args, **kwargs)


def lobby(request):
    return render(request,'lobby.html')
    
def lobby1(request):
    return render(request,'lobby1.html')    