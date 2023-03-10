from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *
from .models import *
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
from django.db.models import Q,F,Case, Value, When, FloatField
from django.urls import reverse
from datetime import datetime
import pandas as pd
User = get_user_model()

#admin pannel imports
from django.shortcuts import render , redirect , HttpResponseRedirect,HttpResponse    
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.decorators import login_required

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
            profile['Rating']=PlayerRatings.objects.filter(HostMatch=user.id).aggregate(Avg('Rating'))
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
                profile['Rating']=PlayerRatings.objects.filter(Player=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
            else:
                profile=up.values()[0]
                profile['Email']=User.objects.filter(id=user.id).values('email')[0]['email']
                profile['Rating']=PlayerRatings.objects.filter(Player=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
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
                if len(up)==0:
                    d=dict()
                    d['User']=user.id
                    serializer3 = ProfileSerializer(data=d)
                    serializer3.is_valid(raise_exception=True)
                    profile=serializer3.save()
                    profile=Profiles.objects.filter(User=user.id).values()[0]
                    profile['Email']=User.objects.filter(id=user.id).values('email')[0]['email']
                    # profile['Rating']=PlayerRatings.objects.filter(HostMatch=request.POST['HostMatch']).aggregate(Avg('Rating'))
                    profile['Rating']=PlayerRatings.objects.filter(Player=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
                else:
                    profile=up.values()[0]
                    profile['Email']=User.objects.filter(id=user.id).values('email')[0]['email']
                    profile['Rating']=PlayerRatings.objects.filter(Player=user.id).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
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
        profile['Rating']=PlayerRatings.objects.filter(Player=request.POST['User']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
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
        
        
# 'data':{'Business_id':RA.id},


class AddBusinessHours(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=BusinessHoursSerializer
    def post(self,request,*args,**kwargs):
        data=BusinessHours.objects.filter(Business=request.data['Business']).values()
        if len(BusinessHours.objects.filter(Day=request.POST['Day']))>0:
            return Response({
                'msg':'You cannot add same day',
                'status':400
            })
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'data':data,'msg':'Business Hours saved Successfully','status':200})
        
class AddBusinessAPI(generics.GenericAPIView):
    serializer_class=BusinessSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({
            'msg':'Business saved Successfully',
            'status':200
        })

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
    queryset = BusinessHours.objects.all()
    serializer_class=BusinessHoursSerializer
    def post(self, request, *args, **kwargs):
        p=BusinessHours.objects.filter(Business=request.POST['Business'],id=request.data['id']).values()
        p.update(Day=request.POST.get('Day',p.values()[0]['Day']),       
        StartTime=request.POST.get('StartTime',p.values()[0]['StartTime']),
        CloseTime=request.POST.get('CloseTime',p.values()[0]['CloseTime']))
        return Response({
            "msg":'BusinessHours saved successfully',
            "status":200,
        })
# class AddBusinessAPI(generics.GenericAPIView):
#     serializer_class=BusinessSerializer
#     def post(self,request,*args,**kwargs):
#         serializer=serializer
        


class GetBusinessHours(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        data=BusinessHours.objects.filter(Business=request.data['Business']).values()
        return Response({'data':data,'msg':'Business Hours.','status':200})        

class DeleteBusinessHours(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        data=BusinessHours.objects.filter(Business=request.data['Business'],id=request.data['BusinessHour']).delete()
        data=BusinessHours.objects.filter(Business=request.data['Business']).values()
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
                #return Response({'fn':fs.url(filename)})
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
        # profile['Email']=User.objects.filter(id=request.POST['User']).values('email')[0]['email']
        profile=p.values()[0]
        return Response({
            'data':{'Profile':profile},
            "msg":'Profile saved successfully',
            "status":200,
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
                #return Response({'fn':fs.url(filename)})
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
# @property
#     def average_rating(self):
#         return self.reviews.aggregate(Avg('rating'))['rating_avg']

from django.db.models import Avg
class MyProfileAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=Profiles.objects.filter(User=request.POST['User']).values('FirstName','LastName','ProfileImage','Country','State','ZipCode','CPFNumber').values()[0]
        p['Email']=User.objects.filter(id=request.POST['User']).values('email')[0]['email']
        p['Rating']=PlayerRatings.objects.filter(Player=request.POST['User']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        return Response({
            'data':{'Profile':p},
            'msg':'MyProfile List',
            'status':200
        })        

 
# class ForgotPasswordAPI(generics.GenericAPIView):
    
#     def post(self, request, *args, **kwargs):
#         u=User.objects.filter(email__iexact=request.data['email'])
#         if len(u)==0:
#             return Response({"status":400,"msg":"Email does not exist.Please signup first."})
#         else:
#             import smtplib
#             server = smtplib.SMTP('mail.aashima.parastechnologies.in', 587)
#             server.ehlo()
#             server.starttls()
#             server.ehlo()
#             server.login('guninstructor@aashima.parastechnologies.in','GunInstructor@123')
#             msg=MIMEMultipart()
#             msg['FROM']='guninstructor@aashima.parastechnologies.in'
#             msg['TO']=request.data['email']  
#             msg['SUBJECT']="Reset Password Gun Instructor"
#             x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(25))+str(u.values()[0]['id'])
#             #message = "Click on the below link to reset your password:\nhttps://radiocinema.parastechnologies.in/ResetPasswordRedirect/?code="+x+"&fr=reset"
#             message = "Click on the below link to reset your password:\nhttp://aashima.parastechnologies.in/project/ResetPwdTemplate/?User_id="+str(u.values()[0]['id'])
#             msg.attach(MIMEText(message, 'plain'))
#             server.send_message(msg)
#             return Response({"msg":'A Forgot Password link has been sent to your registered mail.',"status":200})

class ForgotPasswordAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        u=User.objects.filter(email__iexact=request.data['email'])
        if len(u)==0:
            return Response({"status":400,"msg":"Email does not exist.Please signup first."})
        else:
            import smtplib
            server = smtplib.SMTP('mail.parastechnologies.in', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('guninstructor@aashima.parastechnologies.in','GunInstructor@123')
            msg=MIMEMultipart()
            msg['FROM']='guninstructor@aashima.parastechnologies.in'
            msg['TO']=request.data['email']  
            msg['SUBJECT']="Reset Password Gun Instructor"
            x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(25))+str(u.values()[0]['id'])
            #message = "Click on the below link to reset your password:\nhttps://radiocinema.parastechnologies.in/ResetPasswordRedirect/?code="+x+"&fr=reset"
            message = "Click on the below link to reset your password:\nhttp://aashima.parastechnologies.in/BeachPlus/ResetPwdTemplate/?User_id="+str(u.values()[0]['id'])
            msg.attach(MIMEText(message, 'plain'))
            server.send_message(msg)
            return Response({"msg":'A Forgot Password link has been sent to your registered mail.',"status":200})



from django.http import HttpResponsePermanentRedirect


# class CustomRedirect(HttpResponsePermanentRedirect):
#     os.environ['APP_SCHEME'] = 'Radio_Cinema'
#     allowed_schemes = [os.environ['APP_SCHEME'], 'http', 'https']

#from django.http import HttpResponseRedirectBase
#HttpResponseRedirectBase.allowed_schemes += ['Radio_Cinema']

class ResetPasswordDirectAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        relativeLink = reverse('Forgot-Password')
        #return Response({'relativeLink':relativeLink}, status=status.HTTP_200_OK)
        #return Response({'scheme':os.environ.get('APP_SCHEME')})
        return CustomRedirect('https://www.google.com')#://radiocinema.parastechnologies.in/")#os.environ.get('APP_SCHEME', ''))
        # location = 'Radio_Cinema://reset'
        # res = HttpResponse(location, status=302)
        # res['Location'] = location 
        # return res
        response = HttpResponse("", status=302)
        response['Location'] = "Radio_cinema://Reset"
        return response

@api_view(['GET','POST'])
@csrf_exempt
def ResetPasswordAPI(request):
    User_id=request.GET['User_id']
    u=User.objects.get(id=User_id)
    dictValues={}
    dictValues['User_id']=User
    #return Response({"u":dir(u)})
    if u is not None:
        if request.method == 'POST':
            pwd=str(request.data['password'])
            ppwd=str(request.data['ppassword'])
        
            if pwd == ppwd and pwd != '' and ppwd != '':
                u.set_password(pwd)
                u.save()
                return HttpResponseRedirect('/PwdResetSuccess/')
            else:
                return render(request,'reset_password_redirect.html',error='Passwords do not match.')
            
    return render(request,'reset_password_redirect.html',dictValues)



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



class Contact(generics.GenericAPIView):
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

# class ContactBusiness(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     serializer_class=ContactFromBusinessSerializer
#     def post(self,request,*args,**kwargs):
#         serializer=self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         RA=serializer.save()
#         return Response({'msg':'Submitted.','status':200})

class InvitesList(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        h=Profiles.objects.all().values()
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
        return Response({'msg':'Host A Match','status':200})
    
        
class MyHostedOngoingMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        h=HostMatches.objects.filter(User=request.POST['User'],Date__gt=datetime.today()).values('id','User','Title','Date','Time','Location','SelectMode','Status','DateAdded',ProfileImage=F('User__ProfileImage'))
        return Response({
            'data':h,
            'msg':'MyHostedOngoingMatches List',
            'status':200
        })  

class MyHostedCompletedMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        h=HostMatches.objects.filter(User=request.POST['User'],Date__lte=datetime.today()).values('id','User','Title','Date','Time','Location','SelectMode','Status','DateAdded',ProfileImage=F('User__ProfileImage'))
        return Response({
            'data':h,
            'msg':'MyHostedCompletedMatches List',
            'status':200
        })

class MyAttendingOngoingMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        a_list=HostInvitations.objects.filter(UserInvited=request.POST['User'],Status='Accepted').values('HostMatch_id')
        a=HostMatches.objects.filter(id__in=a_list,Date__gt=datetime.today()).values()
        return Response({
            'data':a,
            'msg':'MyAttendingOngoingMatches List',
            'status':200
        })
        
class MyAttendingCompletedMatches(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        a_list=HostInvitations.objects.filter(UserInvited=request.POST['User'],Status='Accepted').values('HostMatch_id')
        a=HostMatches.objects.filter(id__in=a_list,Date__lte=datetime.today()).values()
        return Response({
            'data':a,
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
        
        
class MatchDetailAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        m=HostMatches.objects.filter(id=request.POST['Match_id']).values()
        team1player_list=Team1Players.objects.filter(HostMatch=request.POST['Match_id']).values('Player_id','Player__ProfileImage')
        team2player_list=Team2Players.objects.filter(HostMatch=request.POST['Match_id']).values('Player_id','Player__ProfileImage')
        r=MatchRounds.objects.filter(HostMatch=request.POST['Match_id']).values('Team1Score','Team2Score')
        return Response({
            'data':{'MatchDetails':m,'Team1':team1player_list,'Team2':team2player_list,'RoundDetails':r},
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
        # p=HostInvitations.objects.filter(UserInvited=request.POST['Invite_id']).values('HostMatch_id','HostMatch__Title','HostMatch__Date','HostMatch__Time','HostMatch__Location','HostMatch__SelectMode','HostMatch__User_id','HostMatch__User__ProfileImage','HostMatch__User__FirstName','HostMatch__User__LastName','HostMatch__User__MatchesPlayed','HostMatch__User__MatchesWon','HostMatch__User__MatchesHosted','HostMatch__User__id__email')
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
            # from django.contrib.gis.measure import D
            # from django.contrib.gis.geos import *
            profile=Profiles.objects.filter(User=request.POST['User']).update(latitude=request.POST['latitude'],longitude=request.POST['longitude'])
            lat= float(request.POST['latitude']) #profile['latitude']
            lon= float(request.POST['longitude']) #profile['longitude']
            if lat or lon:
                # import geopy.distance
                # coords_1 = (lat1, lon1)
                Friends1=FriendRequests.objects.filter(Sender=request.POST['User']).values_list('Receiver_id')        
                Friends2=FriendRequests.objects.filter(Receiver=request.POST['User']).values_list('Sender_id')        
                Friends=list(Friends1)+list(Friends2)
                all_l=Profiles.objects.filter(**filters).exclude(User=request.POST['User']).exclude(User__in=Friends).values("User_id","ProfileImage","FirstName","LastName","Country","City","State","latitude","longitude","ZipCode","CPFNumber","MatchesHosted","MatchesWon","MatchesPlayed","DateAdded",Email=F("User__email"))
                distanc=[]
                for i in all_l:
                    # i['Email']=i['User__email']
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
                        # return Response({'data':(R * c)})
                        # coords_2 = (lat2, lon2)
                        # distanc.append(geopy.distance.vincenty(coords_1, coords_2).km)
                    else:
                        distanc.append(2*6.28*6500)
                df = pd.DataFrame(list(all_l)) ## this will save 50% memory
                df = df.where(pd.notnull(df), None)
                df['distance']=distanc
                df=df[df['distance']<10]
                df=df.sort_values('distance')
                # df=df.drop(['distance'], axis=1)
                df=df.to_dict('records')
                # cases = [When(id=x, then=Value(i)) for i,x in enumerate(distanc)]         
                # case = Case(*cases, output_field=FloatField())
                # p=Profiles.objects.annotate(distance=case)    
                # np=p.all().order_by('distance').values()
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
                        # coords_2 = (lat2, lon2)
                        # distanc.append(geopy.distance.vincenty(coords_1, coords_2).km)
                    else:
                        distanc.append(2*6.28*6500)
                df = pd.DataFrame(list(all_l)) ## this will save 50% memory
                df = df.where(pd.notnull(df), None)
                df['distance']=distanc
                df=df[df['distance']<10]
                df=df.sort_values('distance')
                # df=df.drop(['distance'], axis=1)
                df=df.to_dict('records') 
                # cases = [When(id=x, then=Value(i)) for i,x in enumerate(distanc)]         
                # case = Case(*cases, output_field=FloatField())
                # p=BusinessModel.objects.annotate(distance=case)    
                # Business=p.all().order_by('distance').values()
                # df['BusinessImages']=filter(None,str(Business['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
                Business=df
    
                return Response({'data':{'NearbyPlayers':np,'Business':Business},'msg':'Home with sort','status':200})
        return Response({'data':{'NearbyPlayers':np,'Business':Business},'msg':'Home','status':200})
        
class BussinessDetail(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=BusinessModel.objects.filter(User=request.POST['Business']).values('User__email','Name','ProfileImage','Address','Location','Contact','Description','TennisCourts','BusinessImages','latitude','longitude').values()[0]
        p['Email']=str(BusinessModel.objects.filter(User=request.POST['Business']).values('User__email')[0]['User__email'])[9:]
        p['BusinessImages']=filter(None,str(p['BusinessImages']).replace('[','').replace(']','').replace('\'','').replace(" ","").split(','))
        s=BusinessServices.objects.filter(Business=request.POST['Business']).values('Service')
        p['Hours']=BusinessHours.objects.filter(Business=request.POST['Business']).values()
        return Response({
            'data':{'Profile':p,'Services':s},
            'msg':'MyProfile List',
            'status':200
        })                

class PlayerProfile(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=Profiles.objects.filter(User=request.POST['Player']).values()[0]#('FirstName','LastName','ProfileImage','State','State','ZipCode','CPFNumber')[0]
        # ratings=PlayerRatings.objects.filter(Player=request.POST['Player_id']).values('Player__ProfileImage','Player__FirstName','Player__LastName','Rating')
        p['Rating']=PlayerRatings.objects.filter(Player=request.POST['Player']).values('Rating').aggregate(Avg('Rating'))['Rating__avg']
        
        return Response({
            'data':p,
            'msg':'PlayerProfile List',
            'status':200
        })   
   
class MatchesAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(UserInvited=request.POST['UserInvited'],Status='Sent').values('id',User_id=F('HostMatch__User'),Title=F('HostMatch__Title'),Date=F('HostMatch__Date'),Time=F('HostMatch__Time'),Location=F('HostMatch__Location'),ProfileImage=F('HostMatch__User__ProfileImage'),FirstName=F('HostMatch__User__FirstName'),LastName=F('HostMatch__User__LastName'),Email=F('HostMatch__User__User__email'))
        return Response({
            'data':data,
            'msg':'Matches API',
            'status':200
        })
        
class AttendMatch(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(id=request.POST['User']).update(Status='Attend')
        return Response({
            'msg':'Attend Match',
            'Status':200
        })
        
class DeclineMatch(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(id=request.POST['User']).delete()
        return Response({
            'msg':'Decline Match',
            'Status':200
        })
        
        
class AttendMatchAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        data=HostInvitations.objects.filter(UserInvited=request.POST['User'],HostMatch=request.POST['HostMatch'])
        data.update(Status='Attend')
        if data.count()==0:
            d=dict()
            d['HostMatch']=request.POST['HostMatch']
            d['UserInvited']=request.POST['User']
            serializer2 = InvitationsSerializer(data=d)
            serializer2.is_valid(raise_exception=True)
            invite=serializer2.save()
            invite.Status='Attend'
            invite.save()
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
        return Response({
            'msg':'Cancel Match',
            'status':200
        })
   
class FindMatches(generics.GenericAPIView):
    # permission_classes=(IsAuthenticated,)
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
                # return Response({'AttendingMatches':AttendingMatches,'DecliningMatches':DecliningMatches,'ExcludeMatches':ExcludeMatches})
                
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
                    df=df[df['distance']<request.POST['distance']]
                df=df.sort_values('distance')
                # df=df.drop(['distance'], axis=1)
                df=df.to_dict('records')
                np=df
                return Response({'data':np,'msg':'Home with sort','status':200})
        return Response({'data':np,'msg':'Home','status':200})
       

class Leaderboard(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=Profiles.objects.all().order_by('-MatchesWon').values('ProfileImage','FirstName','LastName','MatchesWon')
        return Response({
            'data':p,
            'msg':'FindMatches List',
            'status':200
        })   

class Notifications(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        return Response({
            'data':{},
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
        # if len(FriendRequests.objets.filter(id=request.POST['Sender'])>1:
        #     return Response({
        #         'msg':'Already SentRequest',
        #         'Status':200
        #     })
            
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'data':serializer.data,'msg':'Request Sent.','status':200})        


class CancelRequest(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        # FriendRequests.objects.filter(Sender=request.POST['Sender'],Receiver=request.POST['Receiver']).delete()
        FriendRequests.objects.filter(id=request.POST['Request_id']).delete()
        return Response({'msg':'Request Cancelled.','status':200})


class Unfriend(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        # FriendRequests.objects.filter(Sender=request.POST['Sender'],Receiver=request.POST['Receiver'],Status='Accept').delete()
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
        # data=FriendRequests.objects.filter(Sender=request.POST['Sender'],Receiver=request.POST['Receiver']).update(Status='Accept')
        data=FriendRequests.objects.filter(id=request.POST['Request_id']).update(Status='Accept')
        return Response({
            'msg':'Accept Friend',
            'status':200
        })
  
  
class DeclineFriendAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        # FriendRequests.objects.filter(Sender=request.POST['Sender'],Receiver=request.POST['Receiver']).delete()
        FriendRequests.objects.filter(id=request.POST['Request_id']).delete()
        return Response({
            'msg':'Decline Friend',
            'status':200
        })
        
class ReceivedRequestsListAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        # FR=FriendRequests.objects.filter(Receiver=request.POST['Receiver'],Status='Accept').values(SenderId=F('Sender_id'),ProfileImage=F('Sender__ProfileImage'),FirstName=F('Sender__FirstName'),LastName=F('Sender__LastName'),Email=F('Sender__User__email'),City=F('Sender__City'),State=F('Sender__State'),Country=F('Sender__Country'))
        FR=FriendRequests.objects.filter(Receiver=request.POST['Receiver'],Status='Sent').values('id','DateAdded',User_id=F('Sender_id'),ProfileImage=F('Sender__ProfileImage'),FirstName=F('Sender__FirstName'),LastName=F('Sender__LastName'),Email=F('Sender__User__email'),City=F('Sender__City'),State=F('Sender__State'),Country=F('Sender__Country'),latitude=F('Sender__latitude'),longitude=F('Sender__longitude'),ZipCode=F('Sender__ZipCode'),CPFNumber=F('Sender__CPFNumber'),MatchesHosted=F('Sender__MatchesHosted'),MatchesWon=F('Sender__MatchesWon'),MatchesPlayed=F('Sender__MatchesPlayed'))
        # F['Profile']=Profiles.objects.filter(User=request.POST['Receiver']).values('FirstName','LastName','ProfileImage','Country','State','ZipCode','CPFNumber').values()
        return Response({
            'data':FR,
            'msg':'List',
            'status':200
        })
    
        
def All(request):
    return render(request,'all.html')

@login_required(redirect_field_name='next', login_url='/BeachPlus/login/')
def index(request):
    data=Profiles.objects.all()
    total_users=data.count()
    total_matches=HostMatches.objects.all().count()
    total_buisness=BusinessModel.objects.all().count()

    context={
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
    return render(request,'business_management.html',{'data':data})
    
from django.contrib.auth import login as django_login

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
        except:
            dictValues['error'] = 'You are not an admin.'
    return render(request,'login.html',dictValues)



@login_required(login_url='/BeachPlus/login/')
def Report(request):
    return render(request,'report_management.html')



@login_required(redirect_field_name='next', login_url='/BeachPlus/login/')
def UserManagement(request):
    return render(request,'user_management.html')


from django.contrib import auth

def Logout(request):
    auth.logout(request)
    return redirect('login')


