from django.urls import path
from . import views
from app.views import *
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from app import views
from .views import *
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('message', MessageModelViewSet, basename='message-api')
# router.register('user', UserModelViewSet, basename='user-api')

# import subprocess
# subprocess.call(['daphne', '-b','208.109.12.159' ,'-p','9082' ,'/home/aashima/BeachPlus/BeachPlus/BeachPlus.asgi:application'], shell=True)

urlpatterns = [
    # path('BeachPlus/api/v1/', include((router.urls, 'app_name'), namespace='instance_name')),
    path('BeachPlus/Signup/',SignupAPI.as_view(),name='signup'),
    path('BeachPlus/Login/',LoginAPI.as_view(),name='login'),
    path('BeachPlus/CreateProfile/',CreateProfileAPI.as_view(),name='CreateProfile'),
    path('BeachPlus/EditProfile/',EditProfileAPI.as_view(),name='EditProfile'),
    path('BeachPlus/MyProfile/',MyProfileAPI.as_view(),name='myprofile'),
    path('BeachPlus/ForgotPassword/', ForgotPasswordAPI.as_view(), name='Forgot-Password'),
    path('BeachPlus/reset_password/',ResetPasswordAppAPI.as_view(),name="resetpassword"),
    path('BeachPlus/ResetPwdTemplate/', ResetPasswordAPI, name='Reset-Redirect'),#ResetPasswordAPI
    path('BeachPlus/PwdResetSuccess/', PwdResetSuccess.as_view(), name='Pwd-Reset-Success'),
    path('BeachPlus/Contact/',ContactUs.as_view(),name='ContactUs'),
    path('BeachPlus/Invites/',InvitesFriendAPI.as_view(),name='InvitesList'),
    path('BeachPlus/HostMatch/',HostMatchAPI.as_view(),name='HostMatch'),
    path('BeachPlus/MyHostedOngoingMatches/',MyHostedOngoingMatches.as_view(),name='MyHostedOngoingMatches'),
    path('BeachPlus/MyHostedCompletedMatches/',MyHostedCompletedMatches.as_view(),name='MyHostedCompletedMatches'),
    path('BeachPlus/MyAttendingOngoingMatches/',MyAttendingOngoingMatches.as_view(),name='MyAttendingOngoingMatches'),
    path('BeachPlus/MyAttendingCompletedMatches/',MyAttendingCompletedMatches.as_view(),name='MyAttendingCompletedMatches'),
    path('BeachPlus/EndRound/',EndRound.as_view(),name='EndRound'),
    path('BeachPlus/CancelMatch/',CancelMatch.as_view(),name='CancelMatch'),
    path('BeachPlus/MatchDetail/',MatchDetailAPI.as_view(),name='MatchDetailAPI'),
    path('BeachPlus/Invitations/',InvitationsAPI.as_view(),name='Invitations'),
    path('BeachPlus/InvitationDetail/',InvitationDetailAPI.as_view(),name='InvitationDetail'),
    path('BeachPlus/Home/',Home.as_view(),name='Home'),
    path('BeachPlus/BussinessDetail/',BussinessDetail.as_view(),name='BussinessDetail'),
    path('BeachPlus/PlayerProfile/',PlayerProfile.as_view(),name='PlayerProfile'),
    path('BeachPlus/Matches/',MatchesAPI.as_view(),name='Matches'),
    path('BeachPlus/Attend/',AttendMatch.as_view(),name='AttendMatch'),
    path('BeachPlus/Decline/',DeclineMatch.as_view(),name='DeclineMatch'),
    path('BeachPlus/AttendMatch/',AttendMatchAPI.as_view(),name='AttendMatch'),
    path('BeachPlus/DeclineMatch/',DeclineMatchAPI.as_view(),name='DeclineMatch'),
    path('BeachPlus/FindMatches/',FindMatches.as_view(),name='FindMatches'),
    path('BeachPlus/Leaderboard/',Leaderboard.as_view(),name='Leaderboard'),
    path('BeachPlus/Notifications/',Notifications.as_view(),name='Notifications'),
    path('BeachPlus/Logout/',LogOutAPI.as_view(),name='Logout'),
    path('BeachPlus/SendRequest/',SendRequest.as_view(),name='SendRequest'),
    path('BeachPlus/CancelRequest/',CancelRequest.as_view(),name='CancelRequest'),
    path('BeachPlus/Unfriend/',Unfriend.as_view(),name='Unfriend'),
    path('BeachPlus/MyFriends/',MyFriends.as_view(),name='MyFriends'),
    path('BeachPlus/Rate/',RatePlayer.as_view(),name='Rate'),
    path('BeachPlus/Score/',ScoreMatchDetailsAPI.as_view(),name='Score'),
    
    path('BeachPlus/CreateBusiness/',CreateBusiness.as_view(),name='CreateBusiness'),
    path('BeachPlus/DeleteBusinessImage/',DeleteBusinessIMageAPI.as_view(),name='DeleteBusinessIMage'),
    path('BeachPlus/AddBusinessImage/',AddBusinessIMageAPI.as_view(),name='DeleteBusinessIMage'),
    path('BeachPlus/AddBusinessHours/',AddBusinessHours.as_view(),name='AddBusinessImage'),
    path('BeachPlus/EditBusiness/',EditBusiness.as_view(),name='EditBusiness'),
    path('BeachPlus/GetBusinessHours/',GetBusinessHours.as_view(),name='GetBusinessHours'),
    path('BeachPlus/EditBusinessHours/',EditBusinessHoursAPI.as_view(),name='EditBusinessHours'),
    path('BeachPlus/DeleteBusinessHours/',DeleteBusinessHours.as_view(),name='DeleteBusinessHours'),
    path('BeachPlus/AcceptFriend/',AcceptFriendAPI.as_view(),name='Friend'),
    path('BeachPlus/DeclineFriend/',DeclineFriendAPI.as_view(),name='DeclineFriend'),
    path('BeachPlus/SentRequestsList/',SentRequestsListAPI.as_view(),name='SentRequestsList'),
    path('BeachPlus/ReceivedRequestsList/',ReceivedRequestsListAPI.as_view(),name='FriendList'),
    path('BeachPlus/CheckIn/',BusinessRecordSerializer.as_view(),name='CheckIn'),
    path('BeachPlus/OnlinePlayer/',OnlinePlayerAPI.as_view(),name='OnlinePlayer'),
    path('BeachPlus/index/',index,name='index'),
    path('BeachPlus/Business/<int:pk>/',Business,name='Business'),
    path('BeachPlus/BusinessManagement/',BusinessManagement,name='Businessmanagement'),
    path('BeachPlus/login/',login,name='login'),
    path('BeachPlus/Reset/',ResetPasswordAPI,name='Reset'),
    path('BeachPlus/report/',Report,name='report'),
    path('BeachPlus/UserManagement/',UserManagement,name='UserManagement'),
    path('BeachPlus/logout/',Logout,name='logout'),
    path('BeachPlus/lobby/',lobby,name='lobby'),
    path('BeachPlus/lobby1/',lobby1,name='lobby1'),
    path('BeachPlus/RoomList/',RoomList.as_view(),name='RoomList'),
    path('BeachPlus/ChatHistory/',ChatHistory.as_view(),name='ChatHistory'),
    path(
        'BeachPlus/auth-change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='commons/change_password.html',
            success_url = '/BeachPlus/index/'
        ),
        name='change_password'
    ),
    ]
