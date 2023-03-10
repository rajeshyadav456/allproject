# from django.shortcuts import render
# from .serializers import *
# from .models import *
# from rest_framework.exceptions import APIException
# from rest_framework.response import Response
# from .views import *
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
# from django.contrib.auth import authenticate,login,logout
# import os
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import random, string
# import json
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.http import JsonResponse
# from rest_framework import generics
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import random, string
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse,HttpResponseRedirect
# from django.db.models import Q
# from django.urls import reverse
# import os
# from django.core.files.storage import FileSystemStorage
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth import get_user_model
# import requests
# import datetime
# from django.conf import settings
# from django.shortcuts import redirect
# from django.db.models import Sum
# from django.http import JsonResponse
# # Create your views here.

# class SignupAPI(generics.GenericAPIView):
#     serializer_class = SignupSerializer
        
#     def post(self, request, *args, **kwargs):#,exception):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
        
#         d=dict()
#         d['User_id']=user.id
#         d['DeviceToken']=request.data['DeviceToken']
#         d['DeviceType']=request.data['DeviceType']
#         Devices.objects.filter(DeviceToken=d['DeviceToken']).delete()
#         serializer2 = DevicesSerializer(data=d)
#         serializer2.is_valid(raise_exception=True)
#         device=serializer2.save()
#         # import random, string
#         # l=10-len(str(user.id))
#         # x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(l))+str(user.id)
#         # d=dict()
#         # d['User_id']=user.id
#         # d['refferal_code']=x
#         # serializer2 = NotificationsSerializer(data=d)
#         # serializer2.is_valid(raise_exception=True)
#         # device=serializer2.save()
        
#         url='http://aashima.parastechnologies.in/project/api/token/'
#         payload={'username':request.data['email'],'password':request.data['password']}
        
#         response = requests.request("POST", url, data=payload)
        
#         token=response.json()
        
#         token['access_token_expiry=']=settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
#         token['refersh_token_expiry=']=settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
#         return Response({
#         "data":{"User_id":user.id,'token':token},
#         "status":200,
#         "msg":'Sign Up Successfully'
#         })
  
        
# class CreateProfileAPI(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class=ProfileSerializer
#     def post(self,request,*args,**kwargs):
#         if len(UserProfiles.objects.filter(User_id=request.data['User_id']))>0:
#             UserProfiles.objects.filter(User_id=request.data['User_id']).delete()
#         serializer=self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         #RA=serializer.is_valid(raise_exception=True)
#         RA=serializer.save()
#         return Response({'profile':UserProfiles.objects.filter(User_id=request.data['User_id']).values(),'msg':'User information saved successfully','status':200})



# class ContactAPI(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class=ContactSerializer
#     def post(self,request,*args,**kwargs):
#         serializer=self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         #RA=serializer.is_valid(raise_exception=True)
#         RA=serializer.save()
#         return Response({'msg':'Thank for contacting','status':200})



# class SubscribedAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     serializer_class=SubscribedSerializer
#     def post(self,request,*args,**kwargs):
#         p=SubscribedUser.objects.filter(User_id=request.POST['User_id']).values('User_id','Subscription_id','Transaction_id','SubscribedDate','Month','subscriptionEndDate')
#         serializer=self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         RA=serializer.save()
#         pp=UserProfiles.objects.filter(User_id=request.POST['User_id']).update(CurrentPlanId=request.POST['Subscription_id'])
#         return Response({'msg':'Thank for subscribing',
#         'data':p.values()[p.values().count()-1],
#         'status':200})
        
       
       
       
# class LoginAPI(generics.GenericAPIView):
#     serializer_class=SubscribedSerializer
#     def post(self, request, *args, **kwargs):
#         # p=SubscribedUser.objects.filter(User_id=request.POST['User_id']).values('User_id','Subscription_id','Transaction_id','SubscribedDate','Month','subscriptionEndDate')
#         u=User.objects.filter(email__iexact=request.data['email'])
#         if len(u)>0:
#             user = authenticate(request, username=request.data['email'], password=request.data['password'])
#             if user is not None:
#                 up=UserProfiles.objects.filter(User_id_id=user.id)
#                 # return Response({"d":user.id})
#                 if len(up)==0:
#                         d=dict()
#                         d['User_id']=user.id
#                         d['Email']=request.data['email']
#                         serializer3 = ProfileSerializer(data=d)
#                         serializer3.is_valid(raise_exception=True)
#                         profile=serializer3.save()
#                         serializer4 = SubscribedSerializer(data=d)
#                         serializer4.is_valid(raise_exception=True)
#                         profile=serializer4.save()
#                 else:
#                     if up.values()[0]['IsSuspended']==1:
#                         return Response({"status":400,"msg":'This user is suspended.'})
#                 url='http://aashima.parastechnologies.in/project/api/token/'
#                 payload={'username':request.data['email'],'password':request.data['password']}
                
#                 response = requests.request("POST", url, data=payload)
#                 p=SubscribedUser.objects.filter(User_id=user.id).values()
#                 try:
#                     token=response.json()
#                 except:
#                     token=response
#                 token['access_token_expiry=']=settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
#                 token['refersh_token_expiry=']=settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
                
#                 if p.count() > 0:
#                     return Response({'data':UserProfiles.objects.filter(User_id=user.id).values()[0],
#                 'token':token,
#                 'subscribeduser':p[p.count()-1],
#                 'msg':'Login Successfull',
#                 'status':200
                    
#                 })
#                 else: 
#                     return Response({'data':UserProfiles.objects.filter(User_id=user.id).values()[0],
#                 'token':token,
#                 'subscribeduser':{},
#                 'msg':'Login Successfull',
#                 'status':200
                    
#                 })
                
                
                
#             else:
#                 return Response({"status":400,"msg":'Incorrect credentials.'})
#         else:
#             return Response({"status":400,"msg":'This email does not exist.'})



# class InviteDetailsAPI(generics.GenericAPIView):
#     def post(self,request,*args,**kwargs):
#         return Response({
#             'data':{'InviteMessage':'You are invited to join Manzano Tactical Gun Instructor.'},
#             'msg':'Friend list',
#             'status':200
#         })


# class InviteAPI(generics.GenericAPIView):
#     serializer_class=InviteSerializer
#     permission_classes=(IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         RA = serializer.save()
#         server=smtplib.SMTP('mail.parastechnologies.in',587)
#         server.ehlo()
#         server.starttls()
#         server.ehlo()
#         server.login('guninstructor@aashima.parastechnologies.in','GunInstructor@123')
#         msg=MIMEMultipart()
#         msg['FROM']='guninstructor@aashima.parastechnoloiges.in'
#         msg['TO']=request.data['email']
#         msg['SUBJECT']='Invitation to join Manzano Tactical Gun Instructor'
#         message=request.data['message']
#         msg.attach(MIMEText(message,'plain'))
#         try:
#             server.send_message(msg)
#             return Response({'msg':'Invite Sent.','status':200})
#         except:
#             return Response({'msg':'Invalid email.','status':400})

# class TermAndPolicyAPI(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         return Response({
#             'data':{'text':TermAndPolicy.objects.all().order_by('-id').values()},
#             'msg':'Terms and Policies.',
#             'status':200
#         })


# class InstructionAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         return Response({
#             'data':GunInstruction.objects.all().values(),
#             'msg':'Gun Instruction',
#             'status':200
#         })



# class PrimaryGunTypeAPI(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self,request,*args,**Kwargs):
#         return Response({
#             'data':PrimaryGunType.objects.all().values(),
#             'msg':'Gun And Type',
#             'status':200
#         })


# class PrimaryHolsterTypeAPI(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         return Response({
#             'data':PrimaryHolsterType.objects.all().values(),
#             'msg':'Holster And Type',
#             'status':200
#         })
   
       
# class ChangePasswordAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self, request, *args, **kwargs):
#         passwordd=request.data['old_password']
#         u=User.objects.get(id=request.data['User_id'])
#         if u is not None and u.check_password(passwordd):
#             u.set_password(request.data['new_password'])
#             u.save()
#             return Response({"msg":'Password Updated.',"status":200})  
#         else:
#             return Response({"status":400,"msg":'Incorrect old password.'})


# class AboutUsAPI(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         return Response({
#             'data':{'text':AboutUs.objects.all().values()},
#             'msg':'Terms and Policies',
#             'status':200
#         })


# class SubscriptionsAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         return Response({
#             'data':SubscriptionPlan.objects.all().values(),
#             'msg':'Subscribed User',
#             'status':200
#         })
        
 
# class EditProfileAPI(generics.GenericAPIView):
#     queryset = UserProfiles.objects.all()
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         p=UserProfiles.objects.filter(User_id=request.data['User_id'])
#         if len(p)>0:
#             try:
#                 ProfileImage=request.FILES['ProfileImage']
#                 fs = FileSystemStorage()
#                 filename = fs.save('UserProfileImages/'+ProfileImage.name, ProfileImage)
#                 #return Response({'fn':fs.url(filename)})
#                 uploaded_file_url = fs.url(filename).replace("/project/media/",'')
                
#                 old_image = UserProfiles.objects.get(User_id=request.data['User_id'])
#                 try:
#                     image_path = old_image.ProfileImage.path
#                     if os.path.exists(image_path):
#                         os.remove(image_path)
#                 except:
#                     a='leave it'
#                 p.update(ProfileImage=uploaded_file_url)
#             except:
#                 a=1
#         p.update(FirstName=request.POST.get('FirstName',p.values()[0]['FirstName']),
#         LastName=request.POST.get('LastName',p.values()[0]['LastName']),
#         Email=request.POST.get('Email',p.values()[0]['Email']),
#         Country=request.POST.get('Country',p.values()[0]['Country']), 
#         username=request.POST.get('username',p.values()[0]['username']),
#         State=request.POST.get('State',p.values()[0]['State']),
#         Gun=request.POST.get('Gun',p.values()[0]['Gun_id']),
#         Holster=request.POST.get('Holster',p.values()[0]['Holster_id']))
#         u=User.objects.get(id=request.data['User_id'])
#         if request.POST.get('password') is not None:
#             u.set_password(request.data['password'])
#             u.save()
#         return Response({
#             "msg":'Profile saved successfully',
#             "status":200,
#         })


# class MyProfileAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         p=UserProfiles.objects.filter(User_id=request.POST['User_id']).values('User_id','ProfileImage','FirstName','LastName','Email','Country','Gun','Holster')
#         return Response({
#             'data':{'Profile':p.values()[0],'serverdate':datetime.datetime.utcnow()},
#             'msg':'MyProfile List',
#             'status':200
#         })


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
            

# @api_view(['GET','POST'])
# @csrf_exempt
# def ResetPasswordAPI(request):
#     User_id=request.GET['User_id']
#     u=User.objects.get(id=User_id)
#     dictValues={}
#     dictValues['User_id']=User_id
#     #return Response({"u":dir(u)})
#     if u is not None:
#         if request.method == 'POST':
#             pwd=str(request.data['password'])
#             ppwd=str(request.data['ppassword'])
        
#             if pwd == ppwd and pwd != '' and ppwd != '':
#                 u.set_password(pwd)
#                 u.save()
#                 return HttpResponseRedirect('/PwdResetSuccess/')
#             else:
#                 return render(request,'reset_password_redirect.html',error='Passwords do not match.')
            
#     return render(request,'reset_password_redirect.html',dictValues)


# class ResetPasswordAppAPI(generics.GenericAPIView):
#     def post(self, request, *args, **kwargs):
#         User_id=request.data['User_id']
#         u=User.objects.get(id=User_id)
#         pwd=str(request.data['password'])
#         u.set_password(pwd)
#         u.save()
#         return Response({"msg":'Password Updated.',"status":200})  


# class LogOutAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         u=Devices.objects.filter(User_id=request.data['User_id']).delete()
#         return Response({
#             'msg':'Logout successful',
#             'status':200
#         })

# class SoundAnalysisAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     serializer_class=RecordsSerializer
#     def post(self,request,*args,**kwargs):
#         serializer=self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         RA=serializer.save()
#         x=round(random.uniform(0, 1),1)
#         y=round(random.uniform(0, 1),1)
#         RA.DrawTime=x
#         RA.ShotTime=y
#         RA.save()
#         return Response({
#             'data':{'DrawTime':x,'ShotTime':y},
#             'msg':'Sound Analysis successful',
#             'status':200
#         })

# class HistoryAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         if request.data['Type']=='1':
#             data={'ShotLog':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('-id').values()}
#         else:
#             data={'BestTimes':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('ShotTime').values()}
#         return Response({
#             # 'data':{'ShotLog':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('-id').values(),'BestTimes':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('ShotTime').values()},
#             'data':data,
#             'msg':'History',
#             'status':200
#         })


# class FilterHistoryAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         filters={k: v for k, v in request.data.items() if (v and k!='DateFrom' and k!='DateTo')}
#         if 'DateFrom' in request.data.keys():
#             r=UserRecords.objects.filter(DateOfRecord__range=(request.data['DateFrom'],request.data['DateTo']))
#         else:
#             r=UserRecords.objects.all()
#         return Response({
#             'data':{'ShotLog':r.filter(**filters).order_by('-id').values(),'BestTimes':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('ShotTime').values()},
#             'msg':'Filter History',
#             'status':200
#         })


        
# class LeaderboardAPI(generics.GenericAPIView):
#     permission_classes=(IsAuthenticated,)
#     def post(self,request,*args,**kwargs):
#         today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
#         today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
#         if request.data['Type']=='1':
#             data={'TodaysBest':UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max)).order_by('-id').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')}
#         else:
#             data={'AllTimeBest':UserRecords.objects.all().order_by('ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')}
#         return Response({
#             'data':data,
#             'msg':'Leaderboard',
#             'status':200
#         })
        
        
# @api_view(['GET','POST'])
# @csrf_exempt
# def Login(request):
#     dictValues={}
#     dictValues['error'] = None
#     if request.method=='POST':
#         username=request.POST.get('username')
#         Password=request.POST.get('password')
#         try:
#             u=User.objects.get(username=username,is_superuser=True)
#             if u.check_password(Password):
#                 user = authenticate(request, username=username, password=Password)
#                 login(request,u)
#                 return HttpResponseRedirect('/project/dashboard/')
#             else:
#                 dictValues['error'] = 'Invalid username/password combination'
#         except:
#             dictValues['error'] = 'You are not an admin.'
        
#     return render(request,'login.html',dictValues)

# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def dashboard(request):
#     dictV={}
#     dictV['SUBSCRIBE']=len(Subscription.objects.all())
#     dictV['REGISTER']=len(UserProfiles.objects.all())
#     dictV['InviteSent']=len(Invite.objects.all())
#     dictV['ACTIVE']=len(UserProfiles.objects.filter(IsSuspended=True))
#     dictV['INACTIVE']=len(UserProfiles.objects.filter(IsSuspended=False))
#     return render(request,'dashboard.html',dictV)


# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def UserManagement(request):
#     user=UserProfiles.objects.all().order_by('-DateAdded')
#     if request.method=='POST':
#         SuspendValue=request.POST['SuspendAction']
#         UserId=request.POST['UserId']
#         if SuspendValue=="0":
#             UserProfiles.objects.filter(User_id=UserId).update(IsSuspended=0)
#             return redirect('/project/usermanagement/')
#         if SuspendValue=="1":
#             UserProfiles.objects.filter(User_id=UserId).update(IsSuspended=1)
#             return redirect('/project/usermanagement/')
#     return render(request,'user-mgt.html',{'user':user})

# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def UserProfile(request):
#     record=UserRecords.objects.filter(User_id=request.GET['id'])
#     userprofile=UserProfiles.objects.filter(User_id=request.GET['id']).values()[0]
#     usersubs=SubscribedUser.objects.filter(User_id=request.GET['id'])
#     userinvites=Invite.objects.filter(User_id=request.GET['id'])
#     UserId=request.GET['id']
#     if request.method=='POST':
#         SuspendValue=request.POST['SuspendAction']
#         if SuspendValue=="0":
#             UserProfiles.objects.filter(User_id=UserId).update(IsSuspended=0)
#             return redirect('/project/userprofile/?id='+str(UserId))
#         if SuspendValue=="1":
#             UserProfiles.objects.filter(User_id=UserId).update(IsSuspended=1)
#             return redirect('/project/userprofile/?id='+str(UserId))
#     return render(request,'user-profile.html',{'userprofile':userprofile,'record':record,'usersubs':usersubs,'userinvites':userinvites})

# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def delete_userprofile(request,id):
#     userprofile=UserProfiles.objects.filter(User_id=id).delete()
#     user=User.objects.filter(id=id).delete()
#     return redirect('/project/usermanagement/')

# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def leaderboard(request):
#     leaderboard=UserRecords.objects.all().order_by('ShotTime')
#     todaydate=datetime.datetime.utcnow().date()
#     guntypes=PrimaryGunType.objects.all()
#     holstertypes=PrimaryHolsterType.objects.all()
#     filters={}
#     if request.method=='POST':
#         todaydate=request.POST['DateOfRecord']
#         filters={k: v for k, v in request.POST.items() if (v and k!='csrfmiddlewaretoken' and k!='NameToSearch')}
#         if 'NameToSearch' in request.POST.keys():
#             l=UserRecords.objects.filter(User_id__username__contains=request.POST['NameToSearch'])
#         else:
#             l=UserRecords.objects.all()
#         leaderboard=l.filter(**filters).order_by('ShotTime')
#         filters['NameToSearch']=request.POST['NameToSearch']
#         try:
#             filters['Gun_id']=int(request.POST['Gun_id'])
#         except:
#             filters['Gun_id']=0
#         try:
#             filters['Holster_id']=int(request.POST['Holster_id'])
#         except:
#             filters['Holster_id']=0
#     return render(request,'leaderboard.html',{'leaderboard':leaderboard,'todaydate':todaydate,'filters':filters,'guntypes':guntypes,'holstertypes':holstertypes})


# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def UserInquiries(request):
#     contact=Contact.objects.all()
#     return render(request,'report-mgt.html',{'contact':contact})


# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def delete_UserInquiries(request,id):
#     contact=Contacts.objects.filter(id =id).delete()
#     return redirect('/project/UserInquiries/')        


# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def setting(request):
#     return  render(request,'setting.html')


# @login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
# def Logout(request):
#     device=Device.objects.filter(User_id=request.post['User_id']).delete()
#     return Response({
#         'msg':'logout successfully',
#         'status':200
#     })


# def home(request):
#     return render(request, 'dashboard.html')
    

# # def population_chart(request):
# #     labels = []
# #     data = []
# #     # queryset = SubscribedUser.objects.annotate(month=TruncMonth('SubscribedDate')).values('month').annotate(c=Count('Subscription_id')).values('month','c')
# #     # queryset=SubscribedUser.objects.annotate(month=TruncMonth('SubscriptionDate')).values('month').annotate(c=Count('id')).values('month', 'c')                    
# #     for entry in queryset:
# #         labels.append(entry['month'])
# #         data.append(entry['c'])
    
# #     return JsonResponse(data={
# #         'labels': labels,
# #         'data': data,
# #     })



# def population_chart(request):
#     labels=[]
#     data=[]
#     queryset =SubscribedUser.objects.values('Subscription_id').annotate(User_id=Sum('User_id')).order_by('-User_id')
#     for entry in queryset:
#         labels.append(entry['Subscription_id'])
#         data.append(entry['User_id'])
        
#     return JsonResponse(data={
#         'labels':labels,
#         'data':data,
#     })



