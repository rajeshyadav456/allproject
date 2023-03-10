from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions,generics,mixins,viewsets,status
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
from rest_framework.decorators import action,api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly
from datetime import date
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model,login
from django.utils.translation import gettext as _
from rest_framework import status,permissions,generics
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import requests
from .permissions import *
# from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from knox.views import LoginView as KnoxLoginView
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random, string
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse
import os
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
# Create your views here.
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from .helpers import send_forgot_password_mail
import django

class SignupAPI(generics.GenericAPIView):
    serializer_class = SignupSerializer
        
    def post(self, request, *args, **kwargs):#,exception):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        d=dict()
        d['User_id']=user.id
        d['DeviceToken']=request.data['DeviceToken']
        d['DeviceType']=request.data['DeviceType']
        Devices.objects.filter(DeviceToken=d['DeviceToken']).delete()
        serializer2 = DeviceSerializer(data=d)
        serializer2.is_valid(raise_exception=True)
        device=serializer2.save()
        
        l=6-len(str(user.id))
        x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(l))+str(user.id)
        n=Notifications.objects.create(User_id=user,ReferalCode=x)
        n.save()
        return Response({
        "UserType":'User',
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "status":200,
        "msg":'Sign Up Successfully',
        "IsProfileCreated":0
        })


    
class ForgotPasswordAPI(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        u=User.objects.filter(email__iexact=request.data['email'])
        if len(u)==0:
            return Response({"status":400,"msg":"Email does not exist.Please signup first."})
        else:
            server = smtplib.SMTP('mail.parastechnologies.in', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login('jwrrh4rkzumv@a2plvcpnl258197.prod.iad2.secureserver.net','2hGU4>$rKI')
            msg=MIMEMultipart()
            msg['FROM']='jwrrh4rkzumv@a2plvcpnl258197.prod.iad2.secureserver.net'
            msg['TO']=request.data['email']  
            msg['SUBJECT']="Reset Password Radio Cinema"
            x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(25))+str(u.values()[0]['id'])
            #message = "Click on the below link to reset your password:\nhttps://radiocinema.parastechnologies.in/ResetPasswordRedirect/?code="+x+"&fr=reset"
            message = "Click on the below link to reset your password:\nhttps://radiocinema.parastechnologies.in/ResetPwdTemplate/?User_id="+str(u.values()[0]['id'])
            msg.attach(MIMEText(message, 'plain'))
            server.send_message(msg)
            return Response({"msg":'A Forgot Password link has been sent to your registered mail.',"status":200})

from django.http import HttpResponsePermanentRedirect


class CustomRedirect(HttpResponsePermanentRedirect):
    os.environ['APP_SCHEME'] = 'Radio_Cinema'
    allowed_schemes = [os.environ['APP_SCHEME'], 'http', 'https']

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
    dictValues['User_id']=User_id
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
        return Response({"msg":'Password Updated.',"status":200})  
        
        
class PwdResetSuccess(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        html = "<html><body>Your password has been reset.</body></html>" 
        return HttpResponse(html)

class CreateProfile(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        d=dict()
        u=User.objects.filter(id=request.data['User_id'])
        d['email']=u.values()[0]['email']
        d['ProfileImage']=request.data['ProfileImage']
        d['FirstName']=request.data['FirstName']
        d['LastName']=request.data['LastName']
        d['PhoneNumber']=request.data['PhoneNumber']
        d['User_id']=request.data['User_id']
        Profile.objects.filter(User_id=request.data['User_id']).delete()
        serializer = self.get_serializer(data=d)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "UserType":'User',
        "msg":'Profile Created successfully.',
        "status":200
        })


class LoginAPI(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        u=User.objects.filter(email__iexact=request.data['email'])
        if len(u)>0:
            user = authenticate(request, username=request.data['email'], password=request.data['password'])
            if user is not None:
                d=dict()
                d['User_id']=u.values()[0]['id']
                d['DeviceToken']=request.data['DeviceToken']
                d['DeviceType']=request.data['DeviceType']
                Devices.objects.filter(DeviceToken=d['DeviceToken']).delete()
                serializer2 = DeviceSerializer(data=d)
                serializer2.is_valid(raise_exception=True)
                device=serializer2.save()
                PC=0
                if len(Profile.objects.filter(User_id=u.values()[0]['id']))>0:
                    PC=1
                return Response({'UserType':'User',"user": u.values('id','username','email')[0],"status":200,"msg":'Login Successful',"UserType":"User","IsProfileCreated":PC})
            else:
                return Response({"status":400,"msg":'Incorrect credentials.'})
        else:
            return Response({"status":400,"msg":'This email does not exist.'})
            
class GuestLoginAPI(generics.GenericAPIView):
    serializer_class = GuestLoginSerializer
    def post(self, request, *args, **kwargs):
        u=Guests.objects.filter(DeviceToken__iexact=request.data['DeviceToken'])
        if len(u)>0:
            return Response({"Guest_id": u.values()[0]['id'],"status":200,"msg":'Login Successful',"UserType":"Guest"})
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            u = serializer.save()
          
            return Response({'UserType':'Guest',"Guest_id": u.id,"status":200,"msg":'Login Successful',"UserType":"Guest"})
    
class EditProfileAPI(generics.GenericAPIView):
    serializer_class = EditProfileSerializer
    queryset = Profile.objects.all()
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        p=Profile.objects.filter(User_id=request.data['User_id'])
        if len(p)>0:
            try:
                ProfileImage=request.FILES['ProfileImage']
                fs = FileSystemStorage()
                filename = fs.save('UserProfileImages/'+ProfileImage.name, ProfileImage)
                uploaded_file_url = fs.url(filename).replace("/media/",'')
                
                old_image = Profile.objects.get(User_id=request.data['User_id'])
                
                image_path = old_image.ProfileImage.path
                if os.path.exists(image_path):
                    os.remove(image_path)
                    
                p.update(ProfileImage=uploaded_file_url)
            except:
                a=1
                
            p.update(FirstName=request.POST.get('FirstName',p.values()[0]['FirstName']),LastName=request.POST.get('LastName',p.values()[0]['LastName']),PhoneNumber=request.POST.get('PhoneNumber',p.values()[0]['PhoneNumber']))
            u=User.objects.get(id=request.data['User_id'])
            if request.POST.get('password') is not None:
                u.set_password(request.data['password'])
                u.save()
            return Response({"data":{"user": p.values()[0]},"msg":'Profile Updated successfully.',"status":200})
        else:
            return Response({"msg":'User has not created a profile yet.',"status":400})



class NotificationsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        n=Notifications.objects.filter(User_id=request.POST['User_id'])
        n.update(Status=request.POST['Status'])
        return Response({
        "data":{"Notifications": n.values('Status','User_id')[0]},
        "msg":'Notifications Updated successfully.',
        "status":200
        }) 
        
        
class NotificationsListAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        n=UserNotifications.objects.filter(User_id=request.data['User_id'])
        return Response({
        "data":{"Notifications": n.values('Name','text','DateAdded')},
        "msg":'Notifications List.',
        "status":200
        })         
        
class DeleteAccountAPI(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        u=User.objects.get(id=request.data['User_id'])
        if u.check_password(request.data['password']):
            u.delete()
            return Response({"msg":'Account Deleted successfully.',"status":200})        
        else:
            return Response({"msg":'Incorrect password.',"status":400})        
        
        
class TermAndPolicyAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        return Response({
        "data":{"text":TermsAndPolicyText.objects.all().values()[0]['policy']},
        "msg":'Terms and Policies.',
        "status":200
        })     
        
class ChangePasswordAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        passwordd=request.data['old_password']
        u=User.objects.get(id=request.data['User_id'])
        if u is not None and u.check_password(passwordd):
            u.set_password(request.data['new_password'])
            u.save()
            return Response({"msg":'Password Updated.',"status":200})  
        else:
            return Response({"status":400,"msg":'Incorrect old password.'})
                   
class RequestAudioAPI(generics.GenericAPIView):
    serializer_class = RequestAudioSerializer
    def post(self, request, *args, **kwargs):
        
        d=dict()
        p=Profile.objects.filter(User_id=request.data['User_id'])
        d['image']=p.values()[0]['ProfileImage']
        d['FirstName']=p.values()[0]['FirstName']
        d['LastName']=p.values()[0]['LastName']
        d['SongName']=request.data['SongName']
        d['CategoryName']=request.data['CategoryName']
        d['User_id']=request.data['User_id']
        d['Message']=request.data['Message']
        
        serializer = self.get_serializer(data=d)
        serializer.is_valid(raise_exception=True)
        RA = serializer.save()
        return Response({"msg":'Audio requested.',"status":200})  
        
class ContactUsAPI(generics.GenericAPIView):
    serializer_class = ContactUsSerializer
    def post(self, request, *args, **kwargs):
        if User.objects.filter(id=request.data['User_id']).values()[0]['email']==request.data['Email']:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            RA = serializer.save()
            return Response({"msg":'Your message has been submitted.We will contact you soon.',"status":200})  
        else:
            return Response({"msg":'Enter your registered email address..',"status":400})  

class ReportPodcastAPI(generics.GenericAPIView):
    serializer_class = ReportSerializer
    def post(self, request, *args, **kwargs):
        d=dict()
        p=Profile.objects.filter(User_id=request.data['User_id'])
        d['User_id']=request.data['User_id']
        d['image']=p.values()[0]['ProfileImage']
        d['FirstName']=p.values()[0]['FirstName']
        d['LastName']=p.values()[0]['LastName']
        d['Item_id']=request.data['Item_id']
        d['Title']=request.data['Title']
        d['Message']=request.data['Message']
        
        serializer = self.get_serializer(data=d)
        serializer.is_valid(raise_exception=True)
        RA = serializer.save()
        return Response({"msg":'Your report has been submitted.Thankyou.',"status":200})  

class MarkFavouriteAPI(generics.GenericAPIView):
    serializer_class = MarkFavouriteSerializer
    def post(self, request, *args, **kwargs):
        l=Favourites.objects.filter(Item_id=request.data['Item_id'],User_id=request.data['User_id'])
        if len(l)==0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            RA = serializer.save()
            return Response({"msg":'Marked favourite.',"status":200})          
        else:
            return Response({"msg":'Already a favourite.',"status":400})

class MarkUnFavouriteAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        Favourites.objects.filter(Item_id=request.data['Item_id'],User_id=request.data['User_id']).delete()
        return Response({"msg":'Marked unfavourite.',"status":200})

class FavouritesAPI(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        
        #if request.data['SearchString']=='':
        Itemids=Favourites.objects.filter(User_id=request.data['User_id']).values_list('Item_id')
        AllFavourites=Items.objects.filter(id__in=Itemids).values()
        #else:
        #    Itemids=LikedItems.objects.filter(User_id=request.data['User_id']).values_list('Item_id')
        #    AllFavourites=Items.objects.filter(id__in=Itemids,Name__contains=request.data['SearchString']).values()
        return Response({"data":{"AllFavourites":AllFavourites},"msg":'Favourites.',"status":200})  

class FriendsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        
        FollowingIDs=Friends.objects.filter(User_id=request.data['User_id']).values_list('OtherUser_id')
        return Response({"data":{"FriendsList":Profile.objects.filter(User_id__in=FollowingIDs).values()},"msg":'Friends.',"status":200})  
        
class LikeItemAPI(generics.GenericAPIView):
    serializer_class = LikedItemsSerializer
    def post(self, request, *args, **kwargs):
        l=LikedItems.objects.filter(Item_id=request.data['Item_id'],User_id=request.data['User_id'])
        if len(l)==0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            RA = serializer.save()
            item=Items.objects.filter(id=request.data['Item_id'])
            #CurrentLikes=item.values()[0]['Likes']
            #NewLikes=CurrentLikes+1
            NewLikes=len(LikedItems.objects.filter(Item_id=request.data['Item_id']))
            item.update(Likes=NewLikes)
            return Response({"msg":'Liked.',"status":200})          
        else:
            return Response({"msg":'Already Liked.',"status":400})          

class DisLikeItemAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        LikedItems.objects.filter(Item_id=request.data['Item_id'],User_id=request.data['User_id']).delete()
        item=Items.objects.filter(id=request.data['Item_id'])
        CurrentLikes=item.values()[0]['Likes']
        #NewLikes=CurrentLikes-1
        NewLikes=len(LikedItems.objects.filter(Item_id=request.data['Item_id']))
        if NewLikes<0:
            NewLikes=0
        item.update(Likes=NewLikes)
        return Response({"msg":'DisLiked.',"status":200})

class InviteDetailsAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        n=Notifications.objects.filter(User_id=request.data['User_id'])
        return Response({'data':{'Referalcode':n.values('ReferalCode')[0]},'msg':'Invite Details','status':200})



class InviteAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        server = smtplib.SMTP('mail.parastechnologies.in', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('jwrrh4rkzumv@a2plvcpnl258197.prod.iad2.secureserver.net','2hGU4>$rKI')
        msg=MIMEMultipart()
        msg['FROM']='jwrrh4rkzumv@a2plvcpnl258197.prod.iad2.secureserver.net'
        msg['TO']=request.data['email']
        msg['SUBJECT']="Invitation to join Radio Cinema"
        message = "You’ve been invited to join radio cinema where you can listen to audio-only versions of your favorite movies, tv shows, interviews, sports, news articles, comedy specials and much more. Join today to get started."
        msg.attach(MIMEText(message, 'plain'))
        try:
            server.send_message(msg)
            return Response({"msg":'Invite Sent.',"status":200})  
        except:
            return Response({"msg":'Invalid email.',"status":400})  
        
class LogOutAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        n=Devices.objects.filter(User_id=request.data['User_id']).delete()
        return Response({"msg":'Log out successful.',"status":200})
        
class TVShowSeasonsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        n=Seasons.objects.filter(Item_id=request.data['Item_id'])
        n1=[]
        for i in n.values():
            i['NumberOfEpisodes']=len(Episodes.objects.filter(Season_id=i['id']))
            i["NumberOfSeasons"]=len(n)
            n1.append(i)
        return Response({"Seasons":n1,"msg":'TV Show Seasons.',"status":200})
        


class TVShowEpisodeAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        if request.data['SearchString']=='':
            n=Episodes.objects.filter(Item_id=request.data['Item_id'],Season_id=request.data['Season_id']).values()
        else:
            n=Episodes.objects.filter(Item_id=request.data['Item_id'],Season_id=request.data['Season_id']).filter(Q(Name__contains=request.data['SearchString']) | Q(Description__contains=request.data['SearchString'])).values()
        data={}
        SeasonsList=Seasons.objects.filter(Item_id=request.data['Item_id']).values('id','SeasonName')
        data['Name']=Seasons.objects.filter(id=request.data['Season_id']).
        data['Image']=Seasons.objects.filter(id=request.data['Season_id']).values()[0]['PosterImage']
        data['Description']=Seasons.objects.filter(id=request.data['Season_id']).values()[0]['Description']
        data['NumberOfEpisodes']=len(Episodes.objects.filter(Season_id=request.data['Season_id']))
        data['SeasonsList']=SeasonsList
        data['Episodes']=n
        return Response({"data":data,"msg":'TV Show Episodes.',"status":200})



class TVShowEpisodeDetailAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        n=Episodes.objects.filter(id=request.data['Episode_id'])
        return Response({"data":{"Episodes":n.values()[0]},"msg":'TV Show Episodes.',"status":200})
    
class ItemDetailsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            n=Items.objects.filter(id=request.data.get('Item_id',0))
            NewViews=n.values()[0]['Views']+1
            n.update(Views=NewViews)
            IsFavourite=1
            if len(Favourites.objects.filter(User_id=request.data['User_id'],Item_id=request.data['Item_id']))==0:
                IsFavourite=0
            return Response({"data":{"ItemDetails":n.values()[0],"IsFavourite":IsFavourite},"msg":'Item Details.',"status":200})    
        except:
            n=Episodes.objects.filter(id=request.data.get('Episode_id',0))
            z=n.values()[0]
            i=Items.objects.filter(id=n.values()[0]['Item_id_id'])
            NewViews=i.values()[0]['Views']+1
            i.update(Views=NewViews)
            z = {**n.values()[0], **i.values()[0]}    
            
            IsFavourite=1
            if len(Favourites.objects.filter(User_id=request.data['User_id'],Item_id=n.values()[0]['Item_id_id']))==0:
                IsFavourite=0
            z['IsFavourite']=IsFavourite
            
            return Response({"data":{"ItemDetails":z},"msg":'Item Details.',"status":200})             


class FollowUserAPI(generics.GenericAPIView):
    serializer_class = FollowUserSerializer
        
    def post(self, request, *args, **kwargs):
        if request.data['User_id']==request.data['OtherUser_id']:
            return Response({"msg":'Can not Follow self.',"status":400}) 
        if len(Friends.objects.filter(User_id=request.data['User_id'],OtherUser_id=request.data['OtherUser_id']))>0:
            return Response({"msg":'Already Followed.',"status":400}) 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA = serializer.save()
        return Response({"msg":'Followed.',"status":200})         

class UnFollowUserAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        Friends.objects.filter(User_id=request.data['User_id'],OtherUser_id=request.data['OtherUser_id']).delete()
        return Response({"msg":'UnFollowed.',"status":200})

class GetCommentsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        c=Comments.objects.filter(Item_id=request.data['Item_id'])
        CommentsList=[]
        for i in range(len(c)):
            User_id=c.values()[i]['User_id_id']
            u=User.objects.filter(id=User_id)
            dictV=dict()
            prfle=Profile.objects.filter(User_id=User_id).values('FirstName','LastName','ProfileImage','DateAdded')[0]
            cmnt={"UserComment":c.values()[i]['Comment']}
            dictV={**prfle, **cmnt} 
            CommentsList.append(dictV)
        return Response({"data":{"Comments":CommentsList,"NumberOfComments":len(c)},"msg":'Comments List.',"status":200})   
        
class CommentAPI(generics.GenericAPIView):
    serializer_class = CommentSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA = serializer.save()
        c=Comments.objects.filter(Item_id=request.data['Item_id'])
        n=Items.objects.filter(id=request.data['Item_id'])
        #NewComments=n.values()[0]['Comments']+1
        NewComments=len(Comments.objects.filter(Item_id=request.data['Item_id']))
        n.update(Comments=NewComments)
        CommentsList=[]
        for i in range(len(c)):
            User_id=c.values()[i]['User_id_id']
            u=User.objects.filter(id=User_id)
            dictV=dict()
            prfle=Profile.objects.filter(User_id=User_id).values('FirstName','LastName','ProfileImage','DateAdded')[0]
            cmnt={"UserComment":c.values()[i]}
            dictV={**prfle, **cmnt} 
            CommentsList.append(dictV)
        return Response({"data":{'Comments':CommentsList,"NumberOfComments":len(c)},"msg":'Added Comment.',"status":200})   
        
class GetCategoriesAPI(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        return Response({'Categories':Categories.objects.all().values(),"msg":'All Categories.',"status":200})
        
class UserProfileAPI(generics.GenericAPIView): 
    def post(self, request, *args, **kwargs):
        if len(Profile.objects.filter(User_id=request.data['User_id']))>0:
            dictV=dict()
            dictV['UserProfile']=Profile.objects.filter(User_id=request.data['User_id']).values()[0]
            dictV['UserProfile']['email']=User.objects.filter(id=request.data['User_id']).values()[0]['email']
            Itemids=LikedItems.objects.filter(User_id=request.data['User_id']).values_list('Item_id')
            dictV['Feed']=Items.objects.filter(id__in=Itemids).values()
            for i in dictV['Feed']:
                i['IsFavourite']=1
                if len(Favourites.objects.filter(User_id=request.data['User_id'],Item_id=i['id']))==0:
                    i['IsFavourite']=0
            
            FollowingIDs=Friends.objects.filter(User_id=request.data['User_id']).values_list('OtherUser_id')
            dictV['Following']=Profile.objects.filter(User_id__in=FollowingIDs).values()
        
            Itemids=Favourites.objects.filter(User_id=request.data['User_id']).values_list('Item_id')
            dictV['Favourites']=Items.objects.filter(id__in=Itemids).values()
        
            dictV['IsFollowed']=False
            try:
                if len(Friends.objects.filter(User_id=request.data['User_id'],OtherUser_id=request.data['OtherUser_id']))>0:
                    dictV['IsFollowed']=True
            except:
                dictV['IsFollowed']=False
         
            return Response({'data':{'UserProfile':dictV},"msg":'User Profile',"status":200})   
        else:
            return Response({"msg":'User has not created Profile yet.',"status":400})   




class HomeScreenAPI(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        
        dictV=dict()
        if request.data['UserType']=='User':
            try:
                dictV['user']=Profile.objects.filter(User_id=request.data['User_id']).values('FirstName','LastName','ProfileImage')[0]
            except:
                dictV["msg"]='Create Profile first.'
                dictV["status"]=400
                return Response(dictV) 
            dictV['UserType']='User'
            dictV['Trending']=Items.objects.all().values()#filter(id__in=Itemids).values()
            
            Itemids=LikedItems.objects.all().values_list('Item_id')
            dictV['ForYou']=Items.objects.filter(id__in=Itemids).values()
            
            Friends_ids=Friends.objects.filter(User_id=request.data['User_id']).values('OtherUser_id')
            Itemids=LikedItems.objects.filter(User_id__in=Friends_ids).values_list('Item_id')
            dictV['FriendsListen']=Items.objects.filter(id__in=Itemids).values()
            dictV['CurrentDate']=django.utils.timezone.now()
            try:
                dictV['SubscriptionDate']=Transactions.objects.filter(User_id=request.data['User_id']).values()[0]['DateAdded']
            except:
                dictV['SubscriptionDate']=None
        else:
            dictV['UserType']='Guest'
            dictV['user']={"FirstName":'Guest',"LastName":'',"ProfileImage":''}
            dictV['Trending']=Items.objects.all().values()
            dictV['ForYou']=Items.objects.all().values()
            dictV['FriendsListen']=[]
            dictV['SubscriptionDate']=None
            dictV['CurrentDate']=django.utils.timezone.now()
        dictV["msg"]='Home Screen'
        dictV["status"]=200
        return Response(dictV)        





class SearchHomeScreenAPI(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        dictV=dict()
        dictV["data"]={}
        sr=Items.objects.filter(Name__icontains=request.data['SearchString']).exclude(Category_id=2)
        sr_list=[]
        sr_list_1=sr.values('id','Category_id','Name','PosterImage','File','Description')
        sr_tv_show=Items.objects.filter(Name__icontains=request.data['SearchString'],Category_id=2).values('id','Category_id','Name','PosterImage','File','Description')
        if len(sr_tv_show)>0:
            for i in sr_tv_show:
                tv_season=Seasons.objects.filter(Item_id=i['id']).values()
                i['Seasons']=tv_season
                for j in tv_season:
                    tv_episode=Episodes.objects.filter(Season_id=j['id']).values()
                    j['Episodes']=tv_episode
        sr_list=list(sr_list_1)+list(sr_tv_show)
        
        dictV["data"]["SearchResult"]=sr_list        
        dictV["msg"]='Home Screen'
        dictV["status"]=200
        return Response(dictV)     





class GetItemsCategoryWiseAPI(generics.GenericAPIView):
   
    def post(self, request, *args, **kwargs):
        ItemsIDs=Items.objects.filter(Category_id=request.data['Category_id']).values()
        ItemsList=[]
        for i in range(len(ItemsIDs)):
            d=Items.objects.filter(Category_id=request.data['Category_id']).values()[i]
            d['NumberOfSeasons']=None
            d['NumberOfEpisodes']=None
            if request.data['Category_id']=="2":
                d['NumberOfSeasons']=len(Seasons.objects.filter(Item_id=d['id']))
                d['NumberOfEpisodes']=len(Episodes.objects.filter(Item_id=d['id']))
            ItemsList.append(d)
        
        if len(ItemsList)>0:
            return Response({'ItemsList':ItemsList,"msg":'Items Category Wise',"status":200})            
        else:
            return Response({'ItemsList':ItemsList,"msg":'Record not found.',"status":400})            

class TransactionAPI(generics.GenericAPIView):
    serializer_class = TransactionSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA = serializer.save()
        
        return Response({"msg":'Transaction added.',"status":200})            
           

@api_view(['GET','POST'])
@csrf_exempt
def Login(request):
    dictValues={}
    dictValues['error'] = None
    if request.method=='POST':
        Email=request.POST.get('email')
        Password=request.POST.get('password')
        try:
            u=User.objects.get(email=Email,is_superuser=True)
            if u.check_password(Password):
                login(request,u)
                return HttpResponseRedirect('/index/')
            else:
                dictValues['error'] = 'Invalid username/password combination'
        except:
            dictValues['error'] = 'You are not an admin.'
        
    return render(request,'login.html',dictValues)


# def Login(request):
#     if request.method=='POST':
#         dictValues={}
#         email = request.POST['email']
#         password = request.POST['password']
#         #user=authenticate(request,email=email,password=password)
#         userObj = authenticate(email=email,password=password)
#         u=User.objects.filter(is_superuser=True,email=email,password=password)
#         if userObj is not None or len(u)>0:
#             if userObj.is_staff or userObj.is_superuser:
#                 login(request,userObj)
#                 return HttpResponseRedirect('/index/')
#             else:
#                 return HttpResponse('You are not authorised to view this content.')
#         else:
#             dictValues['error'] = 'Invalid username/password combination.'
    
#     return render(request,'login.html',dictValues)


def ChangePassword(request , id):
    context = {}        
    try:
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            if  new_password != confirm_password:
                dictValues['error']='Passwords do not match.'
                return render(request,'change-password.html',dictValues)
                     
            user_obj = User.objects.get(id = id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/logins/')                  
        
    except Exception as e:
        print(e)
    return render(request , 'change-password.html')



import uuid
def ForgotPassword(request):
    dictValues={}
    try:
        if request.method=='POST':
            email=request.POST['email']
    
            if not User.objects.filter(email=email,is_superuser=True).first():
                dictValues['error']='Email does not exist.'
                return render(request,'forgot-password.html',dictValues)
            
            user_obj = User.objects.get(email = email)
            token = user_obj.id#str(uuid.uuid4())
            send_forgot_password_mail(user_obj.email , token)
            dictValues['error']='Email sent.'
            return render(request,'forgot-password.html',dictValues)
    
    except Exception as e:
        print(e)
    return render(request , 'forgot-password.html')


@login_required(redirect_field_name='next', login_url='/logins/')
def index(request):
    dictV={}
    dictV['SUBSCRIBE']=len(Transactions.objects.all().values('User_id').distinct())
    dictV['REGISTER']=len(Profile.objects.all())
    return render(request,'index-1.html',dictV)


@login_required(redirect_field_name='next', login_url='/logins/')
def views(request):
    form=Items.objects.all()
    return render(request,'podcast-management-1.html',{'form':form})

@login_required(redirect_field_name='next', login_url='/logins/')
def seasons(request):
    form=Seasons.objects.all()
    return render(request,'season-management-1.html',{'form':form})

@login_required(redirect_field_name='next', login_url='/logins/')
def episodes(request):
    form=Episodes.objects.all()
    return render(request,'episode-management-1.html',{'form':form})

@login_required(redirect_field_name='next', login_url='/logins/')
def ReportManage(request):
    report=Reports.objects.all()
    return render(request,'report-management-1.html',{'report':report})

@login_required(redirect_field_name='next', login_url='/logins/')    
def viewreport(request):
    view=Reports.objects.filter(id=request.GET['reportid']).values()[0]
    itemdetails=Items.objects.filter(id=view['Item_id_id']).values()[0]
    return render(request,'report-detail-1.html',{'view':view,'itemdetails':itemdetails})

@login_required(redirect_field_name='next', login_url='/logins/')    
def requestaudio(request):
    audio=RequestedAudio.objects.all()
    return render(request,'request-audio-1.html',{'audio':audio})

@login_required(redirect_field_name='next', login_url='/logins/')    
def viewrequest(request):
    view=RequestedAudio.objects.filter(id=request.GET['requestid']).values()
    return render(request,'audio-request-detail-1.html',{'view':view})

@login_required(redirect_field_name='next', login_url='/logins/')
def AddPodcast(request):
    categories=Categories.objects.all()
    if request.method=="POST":
        selectedcategory=request.POST['selectedcategory']
        # poster_image=request.POST['poster_image']
        # audio_file=request.POST['audio_file']
        duration=request.POST['duration']
        artist_name=request.POST['artist_name']
        description=request.POST['description']
        title=request.POST['title']
        
        selectedcategory=Categories.objects.get(id=selectedcategory)
        i=Items.objects.create(Category_id=selectedcategory,Name=title,Description=description,Duration=duration,ArtistName=artist_name)
        i.save()
        
        poster_image=request.FILES['poster_image']
        fs = FileSystemStorage()
        filename = fs.save('ItemFiles/'+poster_image.name, poster_image)
        uploaded_file_url = fs.url(filename).replace("/media/",'')
        i.PosterImage=uploaded_file_url
        
        try:
            audio_file=request.FILES['audio_file']
            fs = FileSystemStorage()
            filename = fs.save('ItemFiles/'+audio_file.name, audio_file)
            uploaded_file_url = fs.url(filename).replace("/media/",'')
            i.File=uploaded_file_url
        except:
            a=1
        i.save()
        return redirect('/podcast/')
        
    return render(request,'add-podcast-1.html',{'categories':categories})

@login_required(redirect_field_name='next', login_url='/logins/')
def AddSeason(request):
    tvshows=Items.objects.filter(Category_id=2)
    if request.method=="POST":
        selectedcategory=request.POST['selectedcategory']
        description=request.POST['description']
        title=request.POST['title']
        
        selectedcategory=Items.objects.get(id=selectedcategory)
        i=Seasons.objects.create(Item_id=selectedcategory,SeasonName=title,Description=description)
        i.save()
        
        poster_image=request.FILES['poster_image']
        fs = FileSystemStorage()
        filename = fs.save('SeasonImages/'+poster_image.name, poster_image)
        uploaded_file_url = fs.url(filename).replace("/media/",'')
        i.PosterImage=uploaded_file_url
        
        i.save()
        return redirect('/season/')
        
    return render(request,'add-season-1.html',{'tvshows':tvshows})
    
@login_required(redirect_field_name='next', login_url='/logins/')
def AddEpisode(request):
    tvshows=Items.objects.filter(Category_id=2)
    tvshowid=int(tvshows.values()[0]['id'])
    seasons=Seasons.objects.filter(Item_id=tvshowid)
    if request.method=="POST":
        selectedcategory=request.POST['selectedcategory']
        tvshowid=int(selectedcategory)
        #return Response({'tvshowid':tvshowid})
        SA=request.POST['SelectedAction']
        seasons=Seasons.objects.filter(Item_id=selectedcategory)
        if SA=="1":
            return render(request,'add-episode-1.html',{'tvshows':tvshows,'seasons':seasons,'tvshowid':tvshowid})
        
        
        duration=request.POST['duration']
        description=request.POST['description']
        title=request.POST['title']
        selectedseason=request.POST['selectedseason']
        selectedcategory=Items.objects.get(id=selectedcategory)
        selectedseason=Seasons.objects.get(id=selectedseason)
        i=Episodes.objects.create(Item_id=selectedcategory,Season_id=selectedseason,Name=title,Description=description,Duration=duration)
        i.save()
        
        audio_file=request.FILES['audio_file']
        fs = FileSystemStorage()
        filename = fs.save('ItemFiles/'+audio_file.name, audio_file)
        uploaded_file_url = fs.url(filename).replace("/media/",'')
        i.File=uploaded_file_url
        
        poster_image=request.FILES['poster_image']
        fs = FileSystemStorage()
        filename = fs.save('ItemFiles/'+poster_image.name, poster_image)
        uploaded_file_url = fs.url(filename).replace("/media/",'')
        i.PosterImage=uploaded_file_url
        
        i.save()
        return redirect('/episode/')
        
    return render(request,'add-episode-1.html',{'tvshows':tvshows,'seasons':seasons,'tvshowid':tvshowid})    

@login_required(redirect_field_name='next', login_url='/logins/')
def viewuser(request):
    view=Profile.objects.filter(User_id=request.GET['User_id']).values()
    return render(request,'view-detail-1.html',{'view':view})

@login_required(redirect_field_name='next', login_url='/logins/')
def usermanage(request):
    data=Profile.objects.all()
    return render(request,'user-management-1.html',{'data':data}) 

# @login_required(redirect_field_name='next', login_url='/logins/')
# def logout(request):
#     logout(request)        

@login_required(redirect_field_name='next', login_url='/logins/')
def delete(request, id):
    podcast = Items.objects.filter(id =id).delete()
    return redirect('/podcast/')

@login_required(redirect_field_name='next', login_url='/logins/')
def deleteseason(request, id):
    podcast = Seasons.objects.filter(id =id).delete()
    return redirect('/season/')
    
@login_required(redirect_field_name='next', login_url='/logins/')
def deleteepisode(request, id):
    podcast = Episodes.objects.filter(id =id).delete()
    return redirect('/episode/')    

# class ReportPodcastAPI(generics.GenericAPIView):
#     serializer_class = ReportSerializer
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         RA = serializer.save()
#         return Response({"msg":'Your report has been submitted.Thankyou.',"status":200})  

class PodcastAPI(generics.GenericAPIView):
    serializer_class=PodcastSerializer
    def post(self,request,*args,**kwargs):
        seriailizer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=seriailizer.save()
        return Response({'msg':'your view padcast  has been submitted. Thankyou','status':200})


class PodcastManagementAPI(generics.GenericAPIView):
    serializer_class=PodcastManagement
    def post(self,request,*args,**kwargs):
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'msg':'your padcast management has been submitted.ThankYou','status':200})
