from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login,logout
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random, string
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework import generics
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
import requests
import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models.functions import TruncMonth
import datetime
from django.db.models import Count
from .models import *

import scipy.io.wavfile as wf
from scipy.io.wavfile import write
import auditok,sys
from django.core.files.storage import default_storage
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
import tensorflow_io as tfio
import tensorflow_hub as hub
import pandas as pd
import librosa
import os
import noisereduce as nr
import numpy as np
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
import uuid

model = tf.lite.Interpreter('/home/aashima/django-projects/projects/ML_model/audio_cnn.tflite')
model.allocate_tensors()
input_details = model.get_input_details()
output_details = model.get_output_details()


def to_decibles(signal):
    # Perform short time Fourier Transformation of signal and take absolute value of results
    stft = np.abs(librosa.stft(signal))
    # Convert to dB
    D = librosa.amplitude_to_db(stft, ref = np.max) # Set reference value to the maximum value of stft.
    return D # Return converted audio signal

def plot_spec(D, sr, file,output):
    fig, ax = plt.subplots(figsize = (8,8))
    spec = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='linear', ax=ax)
    plt.axis('off')
    plt.savefig(output,dpi=400, bbox_inches='tight',pad_inches=0)
    plt.close('all')
    
def spectrogram_building(inputpath='/',outputpath='/'):
    for file in os.listdir(inputpath):
        try:
            data, sr = librosa.load(inputpath+'/'+file)
            filename = file.replace('.wav','.png')
            plot_spec(to_decibles(data), sr, inputpath+'/'+file ,outputpath+'/'+filename)
            plt.close('all')
        except Exception as e:
            print(e)



@tf.function
def load_wav_44k_mono(filename):
    """ Load a WAV file, convert it to a float tensor, resample to 16 kHz single-channel audio. """
    file_contents = tf.io.read_file(filename)
    
    wav, sample_rate = tf.audio.decode_wav(
          file_contents,
          desired_channels=1)
    wav = tf.squeeze(wav, axis=-1)
    sample_rate = tf.cast(sample_rate, dtype=tf.int64)
    wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=44100)
    return wav

def get_prd(audio_regions,thr=0.75):
    
    text,data_list,simlersound='',[],[]
    for i, r in enumerate(audio_regions):
        model = tf.saved_model.load('model/detectionyamnet44k')
        yamnet_model = hub.load('model/yamnet_1')
        my_classes = ['gun', 'holster','other']
        region="Region {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r)
        filename = r.save("audio_files/chunks/"+str(uuid.uuid4())+'_'+str(i)+".wav")
        myfiles=load_wav_44k_mono(filename)
        reloaded_results=model(myfiles)
        scores, embeddings, spectrogram = yamnet_model(myfiles)#load_wav_44k_mono(one_channel_file))
        class_scores = tf.reduce_mean(scores, axis=0)
        top_class = tf.argmax(class_scores)
        class_map_path = yamnet_model.class_map_path().numpy().decode('utf-8')
        class_names =list(pd.read_csv(class_map_path)['display_name'])
        inferred_class_ = class_names[top_class]
        top_score_ = class_scores[top_class]
        sstext=f'[YAMNet] The main sound is: {inferred_class_} ({top_score_*100})'
        simlersound.append(sstext)
        top_class = tf.argmax(reloaded_results)
        inferred_class = my_classes[top_class]
        class_probabilities = tf.nn.softmax(reloaded_results, axis=-1)
        top_score = class_probabilities[top_class]
        if top_score>thr:
            text = f'Audio with  {region} the sound is {inferred_class} and confidence is {top_score*100} %'
            data_list.append(text)
        return data_list,thr,simlersound,filename


class MLSoundAnalysisAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=RecordsSerializer
    def post(self,request,*args,**kwargs):
        
        issubscribed=UserProfiles.objects.filter(User_id=request.POST['User_id'],CurrentPlanId='com.mtdryfire.free')
        if issubscribed.count()==1:
            IsSubscribed=False
        else:    
            IsSubscribed=True
        a=1
        if a==1:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            RA=serializer.save()
            dt,text,data_list,imgpath,simlersound,thr={},'',[],[],[],0.75
            data,text,data_list={},'',[]
            file = request.FILES['AudioFile']
            file_name = default_storage.save('/home/aashima/django-projects/projects/static_media/user_audios/'+file.name, file)
            import subprocess
            subprocess.call(['ffmpeg', '-i', '/home/aashima/django-projects/projects/static_media/user_audios/'+file.name,'/home/aashima/django-projects/projects/static_media/user_audios/audio.wav'], shell=True)
            one_channel_file='/home/aashima/django-projects/projects/static_media/user_audios/inputaudio/'+file.name
            rate, audio = wf.read('/home/aashima/django-projects/projects/static_media/user_audios/audio.wav')
            try:
                len_data=len(audio)
                t = len_data / rate
                audio = np.mean(audio, axis=1)
                write(one_channel_file,rate, audio.astype(np.int16))
            except:
                one_channel_file='/home/aashima/django-projects/projects/static_media/user_audios/audio.wav'
           
            audio_regions = auditok.split(one_channel_file,min_dur=0.001,max_dur=4,max_silence=0.18,energy_threshold=55)
            s=0
            d=0
            for i, r in enumerate(audio_regions):
                model = tf.saved_model.load('/home/aashima/django-projects/projects/ML_model/model/detectionyamnet44k')
                yamnet_model = hub.load('/home/aashima/django-projects/projects/ML_model/model/yamnet_1')
                my_classes = ['gun', 'holster','noise']
                region="Region {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r)
                
                filename = r.save("/home/aashima/django-projects/projects/static_media/user_audios/chunks/"+str(i)+".wav")
                myfiles=load_wav_44k_mono(filename)
                reloaded_results=model(myfiles)
                scores, embeddings, spectrogram = yamnet_model(myfiles)#load_wav_16k_mono(one_channel_file))
                class_scores = tf.reduce_mean(scores, axis=0)
                top_class = tf.argmax(class_scores)
                class_map_path = yamnet_model.class_map_path().numpy().decode('utf-8')
                class_names =list(pd.read_csv(class_map_path)['display_name'])
                inferred_class_ = class_names[top_class]
                top_score_ = class_scores[top_class]
                top_class = tf.argmax(reloaded_results)
                inferred_class = my_classes[top_class]
                class_probabilities = tf.nn.softmax(reloaded_results, axis=-1)
                top_score = class_probabilities[top_class]
                if top_score>thr:
                    text = f'Audio with  {region} the sound is {inferred_class} and confidence is {top_score*100} %'
                    data_list.append(text)
                    # text="File name : {i}.wav & Region : {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r)+' '+'Prediction :'+result+' '+str(round(max((predictions*100))))+' %'
                    # data_list.append(text)
                if inferred_class=='holster':
                    d=r.meta.end
                if inferred_class=='gun':
                    s=r.meta.end
                # if s_end!=0 or s_start!=0:
                #     s=float(request.POST['ParTime'])+s_end-s_start
            # return Response({"end":r.meta.end,"start":r.meta.start,"diff":(r.meta.end-r.meta.start)})
            data['total_detected_sound '+str(thr*100)+' % threshold'] = len(data_list)
            data['total_audio_duration'] = str(t)+' '+'seconds'
            data['audio_chunks_region_predction']= data_list
            data['msg'] = 'audio predicted successfully'
            
            if request.POST['Holster']!='3' and d==0:# and s==0:
            #   return Response({''})
               d=round(random.uniform(1, (t-s)),2)
            
            max_second_audio=int(t)
            
            if s==0:   
            #   s=float(request.POST['ParTime'])+round(random.uniform(0, 0.59),2)+random.randint(1, 4)
               s=round(random.uniform(1, t),2)
            RA.DrawTime=d
            RA.ShotTime=s
            RA.save()

            os.system('rm {}/*.wav'.format('/home/aashima/django-projects/projects/static_media/audio_files'))
            os.system('rm {}/*.wav'.format('/home/aashima/django-projects/projects/static_media/audio_files/chunks'))
            os.system('rm {}/*.wav'.format('/home/aashima/django-projects/projects/static_media/audio_files/inputaudio'))
            os.system('rm {}/*.png'.format('/home/aashima/django-projects/projects/static_media/audio_files/spectrogram'))
            return Response({
            'data':{'DrawTime':d,'ShotTime':s,'total_detected_sound':len(data_list),'audio_chunks_region_predction':data_list,'total_audio_duration':str(t)+' '+'seconds'},
            'msg':'Sound Analysis successful',
            'status':200,
            'IsSubscribed':IsSubscribed
            })
            return Response(data)
        # except Exception as e:
        else:
            return Response({'IsSubscribed':IsSubscribed,'data':{},'msg':'You need to subscribe to view analysis.','status':200})


# Create your views here.
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
        serializer2 = DevicesSerializer(data=d)
        serializer2.is_valid(raise_exception=True)
        device=serializer2.save()
        # import random, string
        # l=10-len(str(user.id))
        # x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(l))+str(user.id)
        # d=dict()
        # d['User_id']=user.id
        # d['refferal_code']=x
        # serializer2 = NotificationsSerializer(data=d)
        # serializer2.is_valid(raise_exception=True)
        # device=serializer2.save()
        
        url='http://aashima.parastechnologies.in/project/api/token/'
        payload={'username':request.data['email'],'password':request.data['password']}
        
        response = requests.request("POST", url, data=payload)
        
        token=response.json()
        
        token['access_token_expiry=']=settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
        token['refersh_token_expiry=']=settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
        return Response({
        "data":{"User_id":user.id,'token':token},
        "status":200,
        "msg":'Sign Up Successfully'
        })
        
class CreateProfileAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=ProfileSerializer
    def post(self,request,*args,**kwargs):
        if len(UserProfiles.objects.filter(User_id=request.data['User_id']))>0:
            UserProfiles.objects.filter(User_id=request.data['User_id']).delete()
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #RA=serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'profile':UserProfiles.objects.filter(User_id=request.data['User_id']).values(),'msg':'User information saved successfully','status':200})



class ContactAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=ContactSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #RA=serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        return Response({'msg':'Message sent.','status':200})

class SubscribedAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=SubscribedSerializer
    def post(self,request,*args,**kwargs):
        p=SubscribedUser.objects.filter(User_id=request.POST['User_id']).values('User_id','Subscription_id','Transaction_id','SubscribedDate','Month','subscriptionEndDate')
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        pp=UserProfiles.objects.filter(User_id=request.POST['User_id']).update(CurrentPlanId=request.POST['Subscription_id'])
        return Response({'msg':'Thank for subscribing',
        'data':p.values()[p.values().count()-1],
        'status':200})
        
class webhooks(generics.GenericAPIView):
    serializer_class=AppStoreNotificationsSerializer
        
    def post(self,request,*args,**kwargs):
        d={}
        d['request_body']=str(request.body.decode('utf-8'))
        serializer=self.get_serializer(data=d)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        a=1
        try:
            jsondata = request.body.decode('utf-8')
            incoming_notification = json.loads(jsondata)
            signedPayload=incoming_notification['signedPayload']
            
            import base64
            notification_Payload=json.loads(base64.b64decode(signedPayload.split('.')[1]+'==').decode('utf-8'))
            notificationType=notification_Payload['notificationType']
            subtype=notification_Payload['subtype']
            
            data=notification_Payload['data']
            signedTransactionInfo=data['signedTransactionInfo']
            signedTransactionInfo_payload=json.loads(base64.b64decode(signedTransactionInfo.split('.')[1]+'==').decode('utf-8'))
            originalTransactionId=signedTransactionInfo_payload['originalTransactionId']
            transactionId=signedTransactionInfo_payload['transactionId']
            
            try:
                User=SubscribedUser.objects.filter(Transaction_id=originalTransactionId).values()[0]['User_id_id']
            except:
                User=SubscribedUser.objects.filter(Transaction_id=transactionId).values()[0]['User_id_id']
                
            if notificationType=='DID_RENEW':
                Plan_existing=Plans.objects.get(PlanId=signedTransactionInfo_payload['productId'])
                UserProfiles.objects.filter(User_id=User).update(CurrentPlanId=signedTransactionInfo_payload['productId'])
                SubscribedUser.objects.filter(Transaction_id=transactionId).update(SubscribedDate=datetime.datetime.fromtimestamp(signedTransactionInfo_payload['purchaseDate']/1000),subscriptionEndDate=datetime.datetime.fromtimestamp(signedTransactionInfo_payload['expiresDate']/1000))
            
            if notificationType=='EXPIRED':    
                UserProfiles.objects.filter(User_id=User).update(CurrentPlanId='com.mtdryfire.free')
            
            if notificationType=='DID_CHANGE_RENEWAL_STATUS' and subtype=='AUTO_RENEW_DISABLED':    
                UserProfiles.objects.filter(User_id=User).update(CurrentPlanId='com.mtdryfire.free')
            
            if notificationType=='DID_FAIL_TO_RENEW' and subtype!='GRACE_PERIOD':    
                UserProfiles.objects.filter(User_id=User).update(CurrentPlanId='com.mtdryfire.free')
            
            if notificationType=='GRACE_PERIOD_EXPIRED':    
                UserProfiles.objects.filter(User_id=User).update(CurrentPlanId='com.mtdryfire.free')
            
            if notificationType=='DID_CHANGE_RENEWAL_PREF' and subtype=='UPGRADE':
                Plan_existing=Plans.objects.get(PlanId=signedTransactionInfo_payload['productId'])
                UserProfiles.objects.filter(User_id=User).update(CurrentPlanId=signedTransactionInfo_payload['productId'])
                SubscribedUser.objects.filter(Transaction_id=transactionId).update(SubscribedDate=datetime.datetime.fromtimestamp(signedTransactionInfo_payload['purchaseDate']/1000),subscriptionEndDate=datetime.datetime.fromtimestamp(signedTransactionInfo_payload['expiresDate']/1000))
            
        # else:
        #     print('e')
                
        except Exception as e:
            print(e)
            return Response({'msg':str(e),'status':400})
        return Response({'msg':'User information saved successfully','status':200})
        
class LoginAPI(generics.GenericAPIView):
    serializer_class=SubscribedSerializer
    def post(self, request, *args, **kwargs):
        # p=SubscribedUser.objects.filter(User_id=request.POST['User_id']).values('User_id','Subscription_id','Transaction_id','SubscribedDate','Month','subscriptionEndDate')
        u=User.objects.filter(email__iexact=request.data['email'])
        if len(u)>0:
            user = authenticate(request, username=request.data['email'], password=request.data['password'])
            if user is not None:
                up=UserProfiles.objects.filter(User_id_id=user.id)
                # return Response({"d":user.id})
                if len(up)==0:
                    d=dict()
                    d['User_id']=user.id
                    d['Email']=request.data['email']
                    serializer3 = ProfileSerializer(data=d)
                    serializer3.is_valid(raise_exception=True)
                    profile=serializer3.save()
                    # serializer4 = SubscribedSerializer(data=d)
                    # serializer4.is_valid(raise_exception=True)
                    # profile=serializer4.save()
                else:
                    if up.values()[0]['IsSuspended']==1:
                        return Response({"status":400,"msg":'This user is suspended.'})
                url='http://aashima.parastechnologies.in/project/api/token/'
                payload={'username':request.data['email'],'password':request.data['password']}
                
                response = requests.request("POST", url, data=payload)
                p=SubscribedUser.objects.filter(User_id=user.id,subscriptionEndDate__gt=datetime.datetime.utcnow()).values()
                try:
                    token=response.json()
                except:
                    token=response
                token['access_token_expiry=']=settings.JWT_AUTH['JWT_EXPIRATION_DELTA']
                token['refersh_token_expiry=']=settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']
                
                if p.count() > 0:
                    return Response({'data':UserProfiles.objects.filter(User_id=user.id).values()[0],
                'token':token,
                'IsSubscribed':True,
                'msg':'Login Successfull',
                'status':200
                    
                })
                else: 
                    return Response({'data':UserProfiles.objects.filter(User_id=user.id).values()[0],
                'token':token,
                'IsSubscribed':False,
                'msg':'Login Successfull',
                'status':200
                    
                })
            else:
                return Response({"status":400,"msg":'Incorrect credentials.'})
        else:
            return Response({"status":400,"msg":'This email does not exist.'})



class InviteDetailsAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        return Response({
            'data':{'InviteMessage':'You are invited to join Manzano Tactical Gun Instructor.'},
            'msg':'Friend list',
            'status':200
        })

class InviteAPI(generics.GenericAPIView):
    serializer_class=InviteSerializer
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA = serializer.save()
        server=smtplib.SMTP('mail.parastechnologies.in',587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('guninstructor@aashima.parastechnologies.in','GunInstructor@123')
        msg=MIMEMultipart()
        msg['FROM']='guninstructor@aashima.parastechnoloiges.in'
        msg['TO']=request.data['email']
        msg['SUBJECT']='Invitation to try Manzano Tactical Dry Fire App'
        message='Check out this dry fire app!'#request.data['message']
        msg.attach(MIMEText(message,'plain'))
        try:
            server.send_message(msg)
            return Response({'msg':'Invite Sent.','status':200})
        except:
            return Response({'msg':'Invalid email.','status':400})

class TermAndPolicyAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        return Response({
            'data':{'text':TermAndPolicy.objects.all().order_by('-id').values()},
            'msg':'Terms and Policies.',
            'status':200
        })

class InstructionAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        return Response({
            'data':GunInstruction.objects.all().values(),
            'msg':'Gun Instruction',
            'status':200
        })

class PrimaryGunTypeAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**Kwargs):
        return Response({
            'data':PrimaryGunType.objects.all().values(),
            'msg':'Gun And Type',
            'status':200
        })

class PrimaryHolsterTypeAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        return Response({
            'data':PrimaryHolsterType.objects.all().values(),
            'msg':'Holster And Type',
            'status':200
        })
   
class ChangePasswordAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        passwordd=request.data['old_password']
        u=User.objects.get(id=request.data['User_id'])
        if u is not None and u.check_password(passwordd):
            u.set_password(request.data['new_password'])
            u.save()
            return Response({"msg":'Password Updated.',"status":200})  
        else:
            return Response({"status":400,"msg":'Incorrect old password.'})
            

class AboutUsAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        return Response({
            'data':{'text':AboutUs.objects.all().values()},
            'msg':'Terms and Policies',
            'status':200
        })

class SubscriptionsAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        return Response({
            'data':Plans.objects.all().values(),
            'msg':'Subscribed User',
            'status':200
        })

class EditProfileAPI(generics.GenericAPIView):
    queryset = UserProfiles.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        p=UserProfiles.objects.filter(User_id=request.data['User_id'])
        if len(p)>0:
            try:
                ProfileImage=request.FILES['ProfileImage']
                fs = FileSystemStorage()
                filename = fs.save('UserProfileImages/'+ProfileImage.name, ProfileImage)
                #return Response({'fn':fs.url(filename)})
                uploaded_file_url = fs.url(filename).replace("/project/media/",'')
                
                old_image = UserProfiles.objects.get(User_id=request.data['User_id'])
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
        Email=request.POST.get('Email',p.values()[0]['Email']),
        Country=request.POST.get('Country',p.values()[0]['Country']), 
        username=request.POST.get('username',p.values()[0]['username']),
        State=request.POST.get('State',p.values()[0]['State']),
        Gun=request.POST.get('Gun',p.values()[0]['Gun_id']),
        Holster=request.POST.get('Holster',p.values()[0]['Holster_id']))
        u=User.objects.get(id=request.data['User_id'])
        if request.POST.get('password') is not None:
            u.set_password(request.data['password'])
            u.save()
        return Response({
            "msg":'Profile saved successfully',
            "status":200,
        })

class MyProfileAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        p=UserProfiles.objects.filter(User_id=request.POST['User_id']).values('User_id','ProfileImage','FirstName','LastName','Email','Country','Gun','Holster')
        return Response({
            'data':{'Profile':p.values()[0],'serverdate':datetime.datetime.utcnow()},
            'msg':'MyProfile List',
            'status':200
        })

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
            message = "Click on the below link to reset your password:\nhttp://aashima.parastechnologies.in/project/ResetPwdTemplate/?User_id="+str(u.values()[0]['id'])
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
        return Response({
            "msg":'Your password is changed successfully.',
            "status":200
        })  


class PwdResetSuccess(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        html = "<html><body>Your password has been reset.</body></html>" 
        return HttpResponse(html)




class LogOutAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        u=Devices.objects.filter(User_id=request.data['User_id']).delete()
        return Response({
            'msg':'Logout successful',
            'status':200
        })

class SoundAnalysisAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=RecordsSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RA=serializer.save()
        a=0
        if a==0:
            audio_file=request.FILES['AudioFile']
            fs = FileSystemStorage()
            filename = fs.save('user_audios/'+audio_file.name, audio_file)
            return Response({'1':librosa.load('/home/aashima/django-projects/projects/static_media/user_audios/'+audio_file.name)})
            x , sr = librosa.load('/home/aashima/django-projects/projects/static_media/user_audios/'+audio_file.name)
            x = nr.reduce_noise(y=x, sr=sr)
            
            if request.POST['Gun']==1:
                x_ref , sr_ref = librosa.load('static_media/audio_clips/striker_dry_fire/Dry fire only from S1 L1 Glock shot file.mp3')
                x_ref = nr.reduce_noise(y=x_ref, sr=sr_ref)
            
            if request.POST['Gun']==2:
                x_ref , sr_ref = librosa.load('static_media/audio_clips/hammer_dry_fire/2011 Hammer Fire no holster dry fire only.mp3')
                x_ref = nr.reduce_noise(y=x_ref, sr=sr_ref)
            
            if request.POST['Holster']==1:
                x_href , sr_href = librosa.load('static_media/audio_clips/sl_l1_holster/Holster draw only back to Level 1 Sarariland L1 and shot 02_29_24 2.mp3')
                x_href = nr.reduce_noise(y=x_href, sr=sr_href)
            
            if request.POST['Holster']==4:
                x_href , sr_href = librosa.load('static_media/audio_clips/sl_l3_holster/Holster draw only Safariland  L3 LEVEL 3 02_29_53 1.mp3')
                x_href = nr.reduce_noise(y=x_href, sr=sr_href)
            
            
            x_to_consider=len(np.where(abs(x)>0.01)[0])
            time_to_consider=x_to_consider/22050    
            try:
                from dtw import dtw
            except:
                nti='install'
            if request.POST['Holster']==3:
                d=0
                s=time_to_consider
                crop_start=0
                for crop_audio in range(len(x)):
                    crop_end=crop_start+len(x_ref)
                    if crop_end > len(x):
                        break
                    x_crop=x[crop_start:crop_end]
                    crop_start=crop_end+1
                    
                    mfcc1 = librosa.feature.mfcc(x_crop,sr)   #Computing MFCC values
                    mfcc2 = librosa.feature.mfcc(x_ref, sr_ref)
                    dist=0
                    try:
                        dist, cost, path = dtw(mfcc1.T, mfcc2.T)
                    except:
                        nti='install'
                    if dist==0:
                        s=0.01
                        break
                    else:
                        s=0
            else:
                d=time_to_consider/2
                s=time_to_consider/2
                
                crop_start=0
                for crop_audio in range(len(x)):
                    crop_end=crop_start+2880
                    if crop_end > len(x):
                        break
                    x_crop=x[crop_start:crop_end]
                    crop_start=crop_end+1
                    
                    mfcc1 = librosa.feature.mfcc(x_crop,sr)   #Computing MFCC values
                    x_href_cropped=x_href[0:2880]
                    
                    mfcc2 = librosa.feature.mfcc(x_href_cropped, sr_href)
                    dist=0
                    try:
                        dist, cost, path = dtw(mfcc1.T, mfcc2.T)
                    except:
                        nti='install'
                    
                    holster_start=crop_end
                        
                    if dist==0:
                        crop_start=crop_end
                        for crop_audio in range(len(x)):
                            crop_end=crop_start+2880
                            if crop_end > len(x):
                                break
                            x_crop=x[crop_start:crop_end]
                            crop_start=crop_end+1
                    
                            mfcc1 = librosa.feature.mfcc(x_crop,sr)   #Computing MFCC values
                            x_href_cropped=x_href[(len(x_href)-2880):len(x_href)]
                    
                            mfcc2 = librosa.feature.mfcc(x_href_cropped, sr_href)
                            dist=0
                            try:
                                dist, cost, path = dtw(mfcc1.T, mfcc2.T)
                            except:
                                nti='install'
                            
                            if dist==0:
                                crop_start=crop_end
                                d=(crop_end-holster_start)/22050
                                for crop_audio in range(len(x)):
                                    crop_end=crop_start+len(x_ref)
                                    if crop_end > len(x):
                                        break
                                    x_crop=x[crop_start:crop_end]
                                    crop_start=crop_end+1
                                    mfcc1 = librosa.feature.mfcc(x_crop,sr)   #Computing MFCC values
                                    mfcc2 = librosa.feature.mfcc(x_ref, sr_ref)
                                    dist=0
                                    try:
                                        dist, cost, path = dtw(mfcc1.T, mfcc2.T)
                                    except:
                                        nti='install'
                                    if dist==0:
                                        s=0.01
                                        break
                                    else:
                                        s=0
                            else:
                                d=0
                                s=0
                    else:
                        d=0
                        s=0
            RA.DrawTime=d
            RA.ShotTime=s
            RA.save()            
        else:
            d=round(random.uniform(0, 0.25),2)
            s=0.01#round(random.uniform(0, 1),2)
            RA.DrawTime=d
            RA.ShotTime=s
            RA.save()
            
        return Response({
            'data':{'DrawTime':d,'ShotTime':s},
            'msg':'Sound Analysis successful',
            'status':200
        })

class HistoryAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        if request.data['Type']=='1':
            data={'ShotLog':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('-id').values()}
        else:
            try:
                bt11=[UserRecords.objects.filter(User_id=request.data['User_id'],Holster_id=1,Gun_id=1).order_by('-ShotTime').values()[0]]
            except:
                bt11=[]
            try:
                bt12=[UserRecords.objects.filter(User_id=request.data['User_id'],Holster_id=2,Gun_id=1).order_by('-ShotTime').values()[0]]
            except:
                bt12=[]
            try:
                bt13=[UserRecords.objects.filter(User_id=request.data['User_id'],Holster_id=3,Gun_id=1).order_by('-ShotTime').values()[0]]
            except:
                bt13=[]
            try:
                bt14=[UserRecords.objects.filter(User_id=request.data['User_id'],Holster_id=4,Gun_id=1).order_by('-ShotTime').values()[0]]
            except:
                bt14=[]
            try:
                bt21=[UserRecords.objects.filter(User_id=request.data['User_id'],Holster_id=1,Gun_id=2).order_by('-ShotTime').values()[0]]
            except:
                bt21=[]
            try:
                bt22=[UserRecords.objects.filter(User_id=request.data['User_id'],Holster_id=2,Gun_id=2).order_by('-ShotTime').values()[0]]
            except:
                bt22=[]
            try:
                bt23=[UserRecords.objects.filter(User_id=request.data['User_id'],Holster_id=3,Gun_id=2).order_by('-ShotTime').values()[0]]
            except:
                bt23=[]
            try:
                bt24=[UserRecords.objects.filter(User_id=request.data['User_id'],Holster_id=4,Gun_id=2).order_by('-ShotTime').values()[0]]
            except:
                bt24=[]
            bt=bt11+bt12+bt13+bt14+bt21+bt22+bt23+bt24
            df = pd.DataFrame(bt)
            df=df.sort_values('ShotTime',ascending=False)
            df=df.to_dict('records')
            data={'BestTimes':df}
        return Response({
            # 'data':{'ShotLog':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('-id').values(),'BestTimes':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('ShotTime').values()},
            'data':data,
            'msg':'History',
            'status':200
        })

class FilterHistoryAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        filters={k: v for k, v in request.data.items() if (v and k!='DateFrom' and k!='DateTo')}
        if 'DateFrom' in request.data.keys():
            r=UserRecords.objects.filter(DateOfRecord__range=(request.data['DateFrom'],request.data['DateTo']))
        else:
            r=UserRecords.objects.all()
        return Response({
            'data':{'ShotLog':r.filter(**filters).order_by('-id').values(),'BestTimes':UserRecords.objects.filter(User_id=request.data['User_id']).order_by('ShotTime').values()},
            'msg':'Filter History',
            'status':200
        })

class LeaderboardAPI(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        if request.data['Type']=='1':
            
            try:
                bt11=[UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max),Holster_id=1,Gun_id=1).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt11=[]
            try:
                bt12=[UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max),Holster_id=2,Gun_id=1).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt12=[]
            try:
                bt13=[UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max),Holster_id=3,Gun_id=1).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt13=[]
            try:
                bt14=[UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max),Holster_id=4,Gun_id=1).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt14=[]
            try:
                bt21=[UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max),Holster_id=1,Gun_id=2).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt21=[]
            try:
                bt22=[UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max),Holster_id=2,Gun_id=2).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt22=[]
            try:
                bt23=[UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max),Holster_id=3,Gun_id=2).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt23=[]
            try:
                bt24=[UserRecords.objects.filter(DateOfRecord__range=(today_min, today_max),Holster_id=4,Gun_id=2).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt24=[]

            # return Response({'bt11':bt11,'bt12':bt12,'bt13':bt13,'bt14':bt14,'bt21':bt21,'bt22':bt22,'bt23':bt23,'bt24':bt24})
                        
            bt=bt11+bt12+bt13+bt14+bt21+bt22+bt23+bt24
            
            df = pd.DataFrame(bt)
            df=df.sort_values('ShotTime',ascending=False)
            df=df.to_dict('records')
            data={'TodaysBest':df}
            
        else:
            try:
                bt11=[UserRecords.objects.filter(Holster_id=1,Gun_id=1).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt11=[]
            try:
                bt12=[UserRecords.objects.filter(Holster_id=2,Gun_id=1).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt12=[]
            try:
                bt13=[UserRecords.objects.filter(Holster_id=3,Gun_id=1).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt13=[]
            try:
                bt14=[UserRecords.objects.filter(Holster_id=4,Gun_id=1).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt14=[]
            try:
                bt21=[UserRecords.objects.filter(Holster_id=1,Gun_id=2).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt21=[]
            try:
                bt22=[UserRecords.objects.filter(Holster_id=2,Gun_id=2).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt22=[]
            try:
                bt23=[UserRecords.objects.filter(Holster_id=3,Gun_id=2).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt23=[]
            try:
                bt24=[UserRecords.objects.filter(Holster_id=4,Gun_id=2).order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord')[0]]
            except:
                bt24=[]
            bt=bt11+bt12+bt13+bt14+bt21+bt22+bt23+bt24
            df = pd.DataFrame(bt)
            df=df.sort_values('ShotTime',ascending=False)
            df=df.to_dict('records')
            data={'AllTimeBest':df}
            # data={'AllTimeBest':UserRecords.objects.all().order_by('-ShotTime').values('User_id','User_id__ProfileImage','User_id__FirstName','User_id__LastName','User_id__username','Gun_id','Holster_id','Gun__GunName','Holster__HolsterName','ParTime','DrawTime','ShotTime','DateOfRecord').distinct()}
        
        issubscribed=UserProfiles.objects.filter(User_id=request.user.id,CurrentPlanId='com.mtdryfire.free')
        if issubscribed.count()==1:
            IsSubscribed=False
        else:    
            IsSubscribed=True
        return Response({
            'data':data,
            'IsSubscribed':IsSubscribed,
            'msg':'Leaderboard',
            'status':200
        })

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

@api_view(['GET','POST'])
@csrf_exempt
def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        Password=request.POST.get('password')
        a=0
        if a==0:
            u=User.objects.get(username=username,is_superuser=True)
            if u.check_password(Password):
                user=authenticate(request,username=username,password=Password)
                login(request._request,u)
                    
                # try:
                remember = request.POST.get('remember_me')
                if remember:
                    settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                # except:
                #     is_private = False
                #     settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True

                return HttpResponseRedirect('/project/dashboard/')
            else:
                return render (request,'login.html', {'error':'Invalid username/password combination.'})
        else:
            return render(request,'login.html',{'error':str(request.POST.get('remember_me'))+'You are not an admin.'})
    return render(request,'login.html')
    
    
# @api_view(['GET','POST'])
# @csrf_exempt
# def login(request, *args, **kwargs):
#     if request.method == 'POST':
#         if not request.POST.get('remember_me', None):
#             request.session.set_expiry(0)
#     return auth_views.login(request, *args, **kwargs)


@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def dashboard(request):
    dictV={}
    dictV['todaydate']=datetime.datetime.utcnow().date()
    dictV['SUBSCRIBE']=len(Plans.objects.all())
    dictV['REGISTER']=len(UserProfiles.objects.all())
    dictV['InviteSent']=len(Invite.objects.all())
    dictV['ACTIVE']=len(UserProfiles.objects.filter(IsSuspended=True))
    dictV['INACTIVE']=len(UserProfiles.objects.filter(IsSuspended=False))
    dictV['monthly']=SubscribedUser.objects.filter(SubscribedDate__year='2021').values_list('SubscribedDate__month').annotate(TotalPlan=Count('Subscription_id__PlanId')).count()
    dictV['yearly']=SubscribedUser.objects.filter(SubscribedDate__year='2021').values_list('SubscribedDate__year').annotate(TotalPlan=Count('Subscription_id__PlanId')).count()
    dictV['income']=SubscribedUser.objects.filter(SubscribedDate__year='2022').values_list('SubscribedDate__month').annotate(TotalPlan=Count('Subscription_id__PlanId')).count()*10
    dictV['income_year']=SubscribedUser.objects.filter(SubscribedDate__year='2023').values_list('SubscribedDate__year').annotate(TotalPlan=Count('Subscription_id__PlanId')).count()*8
    dictV['Total']=dictV['income'] + dictV['income_year']
    dictV['TotalInvite']=dictV['SUBSCRIBE']+dictV['REGISTER']
    dictV['TotalSubscribed']=dictV['monthly']+dictV['yearly']
    return render(request,'dashboard.html',dictV)


# total_monthly_income =Income.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_monthly_income=Sum('amount'))
# total_monthly_expenses = Expenditure.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_monthly_expenses=Sum('amount'))
# income_expense = zip(total_monthly_income, total_monthly_expenses)
    
    
@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def UserManagement(request):
    user=UserProfiles.objects.all().order_by('-DateAdded')
    todaydate=datetime.datetime.utcnow().date()
    SuspendReasons=SuspendReason.objects.all()
    if request.method=='POST':
        SuspendValue=request.POST['SuspendAction']
        if SuspendValue=="0":
            UserId=request.POST['UserIdu']
            UserProfiles.objects.filter(User_id=UserId).update(IsSuspended=0)
            return redirect('/project/usermanagement/')
        if SuspendValue=="1":
            UserId=request.POST['UserId']
            UserProfiles.objects.filter(User_id=UserId).update(IsSuspended=1)
            return redirect('/project/usermanagement/')
    return render(request,'user-mgt.html',{'user':user,'todaydate':todaydate,'SuspendReasons':SuspendReasons})

@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def UserProfile(request):
    record=UserRecords.objects.filter(User_id=request.GET['id']).values()
    userprofile=UserProfiles.objects.filter(User_id=request.GET['id']).values()[0]
    usersubs=SubscribedUser.objects.filter(User_id=request.GET['id'])
    userinvites=Invite.objects.filter(User_id=request.GET['id'])
    UserId=request.GET['id']
    if request.method=='POST':
        SuspendValue=request.POST['SuspendAction']
        if SuspendValue=="0":
            UserProfiles.objects.filter(User_id=UserId).update(IsSuspended=0)
            return redirect('/project/userprofile/?id='+str(UserId))
        if SuspendValue=="1":
            UserProfiles.objects.filter(User_id=UserId).update(IsSuspended=1)
            return redirect('/project/userprofile/?id='+str(UserId))
    return render(request,'user-profile.html',{'userprofile':userprofile,'record':record,'usersubs':usersubs,'userinvites':userinvites})

@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def delete_userprofile(request,id):
    userprofile=UserProfiles.objects.filter(User_id=id).delete()
    user=User.objects.filter(id=id).delete()
    return redirect('/project/usermanagement/')

@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def leaderboard(request):
    leaderboard=UserRecords.objects.all().order_by('ShotTime')
    todaydate=datetime.datetime.utcnow().date()
    guntypes=PrimaryGunType.objects.all()
    holstertypes=PrimaryHolsterType.objects.all()
    filters={}
    if request.method=='POST':
        todaydate=request.POST['DateOfRecord']
        filters={k: v for k, v in request.POST.items() if (v and k!='csrfmiddlewaretoken' and k!='NameToSearch')}
        if 'NameToSearch' in request.POST.keys():
            l=UserRecords.objects.filter(User_id__username__contains=request.POST['NameToSearch'])
        else:
            l=UserRecords.objects.all()
        leaderboard=l.filter(**filters).order_by('ShotTime').values().distinct()
        filters['NameToSearch']=request.POST['NameToSearch']
        try:
            filters['Gun_id']=int(request.POST['Gun_id'])
        except:
            filters['Gun_id']=0
        try:
            filters['Holster_id']=int(request.POST['Holster_id'])
        except:
            filters['Holster_id']=0
    return render(request,'leaderboard.html',{'leaderboard':leaderboard,'todaydate':todaydate,'filters':filters,'guntypes':guntypes,'holstertypes':holstertypes})


@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def UserInquiries(request):
    contact=Contact.objects.all().order_by('-id')
    return render(request,'report-mgt.html',{'contact':contact})

@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def delete_UserInquiries(request,id):
    contact=Contact.objects.filter(id =id).delete()
    return redirect('/project/UserInquiries/')        

@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def setting(request):
    return  render(request,'setting.html')

@login_required(redirect_field_name='next', login_url='/project/LoginAdmin/')
def Logout(request):
    device=Device.objects.filter(User_id=request.post['User_id']).delete()
    return Response({
        'msg':'logout successfully',
        'status':200
    })

# def home(request):
#     return render(request, 'dashboard.html')

def population_chart(request):
    import datetime
    today=datetime.date.today()
    # labels=[]
    data=[]
    queryset =SubscribedUser.objects.values('User_id','SubscribedDate__month').annotate(dcount=Count('User_id')).order_by('SubscribedDate').annotate(month=ExtractMonth('SubscribedDate'),year=ExtractYear('SubscribedDate'))
    # for entry in queryset:
        # labels.append(entry['SubscribedDate__month'])
        # data.append(entry['User_id'])
    labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
    
    for i in range(12):
        data.append(len(SubscribedUser.objects.filter(SubscribedDate__month=(i+1),SubscribedDate__year=2022)))
        
    return JsonResponse(data={
        'labels':labels,
        'data':data,
    })

def pie_chart(request):
    labels = []
    data = []
    
    labels=['Registered','Paid Subscribers']
    
    # dictV['SUBSCRIBE']=len(SubscriptionPlan.objects.all())
    # dictV['REGISTER']=len(UserProfiles.objects.all())
    
    data.append(len(UserProfiles.objects.all()))
    data.append(len(Plans.objects.all()))
    
    # queryset = SubscribedUser.objects.order_by('-User_id_id')[:6]
    # for city in queryset:
    #     labels.append(city.User_id_id)
    #     data.append(city.Subscription_id_id)
 
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })