"""projects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
# from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from app import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

urlpatterns = [
    path('project/CreateProfile/',CreateProfileAPI.as_view(),name='profile'),
    path('project/Contact/',ContactAPI.as_view(),name='contact'),
    path('project/signup/',SignupAPI.as_view(),name='signup'),
    path('project/login/',LoginAPI.as_view(),name='login'),
    path('project/TermAndPolicy/',TermAndPolicyAPI.as_view(),name='TermAndPolicy'),
    path('project/ChangePassword/', ChangePasswordAPI.as_view(),name='change'),
    path('project/about/',AboutUsAPI.as_view(),name='about'),
    path('project/instruction/',InstructionAPI.as_view(),name='instruction'),
    path('project/editprofile/',EditProfileAPI.as_view(),name='edit'),
    path('project/primarygun/',PrimaryGunTypeAPI.as_view(),name='primarygun'),
    path('project/holster/',PrimaryHolsterTypeAPI.as_view(),name='holster'),
    path('project/ForgotPassword/', ForgotPasswordAPI.as_view(), name='Forgot-Password'),
    path('project/reset_password/',ResetPasswordAppAPI.as_view(),name="resetpassword"),
    path('project/ResetPwdTmpDirecti/', ResetPasswordDirectAPI.as_view(), name='Reset-Redirect'),#ResetPasswordAPI
    path('project/ResetPwdTemplate/', ResetPasswordAPI, name='Reset-Redirect'),#ResetPasswordAPI
    path('project/PwdResetSuccess/', PwdResetSuccess.as_view(), name='Pwd-Reset-Success'),
    path('project/InviteDetails/',InviteDetailsAPI.as_view(),name='Pwd-Reset-Success'),
    path('project/invite/',InviteAPI.as_view(),name='invite'),
    path('project/myprofile/',MyProfileAPI.as_view(),name='MyProfile'),
    path('project/InviteFriend/',InviteDetailsAPI.as_view(),name='InviteFriend'),
    path('project/logout/',LogOutAPI.as_view(),name='logout'),
    path('project/SoundAnalysis/',MLSoundAnalysisAPI.as_view(),name='SoundAnalysis'),
    path('project/History/',HistoryAPI.as_view(),name='History'),
    path('project/FilterHistory/',FilterHistoryAPI.as_view(),name='FilterHistory'),
    path('project/Leaderboard/',LeaderboardAPI.as_view(),name='Leaderboard'),
    path('project/SubscriptionPlans/',SubscriptionsAPI.as_view(),name='Subscriptions'),
    path('project/SubscribeUser/',SubscribedAPI.as_view(),name='SubscribeUser'),
    path('project/webhooks/',webhooks.as_view(),name='webhooks'),
    path('project/api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('project/api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # url(r'^$', TemplateView.as_view(template_name=''), name='home'),
    path('project/LoginAdmin/',Login,name='login'),
    path('project/dashboard/',dashboard,name='dashboard'),
    path('project/usermanagement/',UserManagement,name='usermanagement'),
    path('project/userprofile/',UserProfile,name='userprofile'),
    path('project/delete_userprofile/<int:id>/',delete_userprofile,name='delete'),
    path('project/leaderboard/',leaderboard,name='leaderboard'),
    path('project/UserInquiries/',UserInquiries,name='UserInquiries'),
    path('project/delete_UserInquiries/<int:id>',views.delete_UserInquiries,name='delete'),
    path('project/setting/',setting,name='setting'),
    path('project/logout/',Logout,name='logout'),
    path('project/Subscribed/',SubscribedAPI.as_view(),name='Subscribed'),
    # path('project/login/','django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    # path('', views.home, name='dashboard'),
    # path('', views.dashboard, name='dashboard'),
    path('project/population-chart/', views.population_chart, name='population-chart'),
    path('project/pie-chart/', views.pie_chart, name='pie-chart'),
   # Change Password
    #path('project/Login/', auth_views.LoginView.as_view(),{'template_name': 'registration/login.html'}, name='login'),
    path('project/change-password/',auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html',success_url='/project/dashboard/'),name='change_password'),
    path('project/logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


