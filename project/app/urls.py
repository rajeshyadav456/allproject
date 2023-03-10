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
from django.conf.urls import url
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


urlpatterns = [
    path('CreateProfile/',CreateProfileAPI.as_view(),name='profile'),
    path('Contact/',ContactAPI.as_view(),name='contact'),
    path('signup/',SignupAPI.as_view(),name='signup'),
    path('login/',LoginAPI.as_view(),name='login'),
    path('TermAndPolicy/',TermAndPolicyAPI.as_view(),name='TermAndPolicy'),
    path('ChangePassword/', ChangePasswordAPI.as_view(),name='change'),
    path('about/',AboutUsAPI.as_view(),name='about'),
    path('instruction/',InstructionAPI.as_view(),name='instruction'),
    path('editprofile/',EditProfileAPI.as_view(),name='edit'),
    path('primarygun/',PrimaryGunTypeAPI.as_view(),name='primarygun'),
    path('holster/',PrimaryHolsterTypeAPI.as_view(),name='holster'),
    path('ForgotPassword/', ForgotPasswordAPI.as_view(), name='Forgot-Password'),
    path('ResetPwdTemplate/', ResetPasswordAPI, name='Reset-Redirect'),
    path('ResetPassword/', ResetPasswordAppAPI, name='Reset-Password'),
    path('InviteDetails/',InviteDetailsAPI.as_view(),name='Pwd-Reset-Success'),
    path('invite/',InviteAPI.as_view(),name='invite'),
    path('myprofile/',MyProfileAPI.as_view(),name='MyProfile'),
    path('InviteFriend/',InviteDetailsAPI.as_view(),name='InviteFriend'),
    path('logout/',LogOutAPI.as_view(),name='logout'),
    path('SoundAnalysis/',SoundAnalysisAPI.as_view(),name='SoundAnalysis'),
    path('History/',HistoryAPI.as_view(),name='History'),
    path('FilterHistory/',FilterHistoryAPI.as_view(),name='FilterHistory'),
    path('Leaderboard/',LeaderboardAPI.as_view(),name='Leaderboard'),
    path('SubscriptionPlans/',SubscriptionsAPI.as_view(),name='Subscriptions'),
    path('SubscribeUser/',SubscribedAPI.as_view(),name='SubscribeUser'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^$', TemplateView.as_view(template_name=''), name='home'),
    path('LoginAdmin/',Login,name='login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('usermanagement/',UserManagement,name='usermanagement'),
    path('userprofile/',UserProfile,name='userprofile'),
    path('delete_userprofile/<int:id>/',delete_userprofile,name='delete'),
    path('leaderboard/',leaderboard,name='leaderboard'),
    path('UserInquiries/',UserInquiries,name='UserInquiries'),
    path('delete_UserInquiries/<int:id>',views.delete_UserInquiries,name='delete'),
    path('setting/',setting,name='setting'),
    path('logout/',Logout,name='logout'),
    path('Subscribed/',SubscribedAPI.as_view(),name='Subscribed'),
    # path('', views.home, name='dashboard'),
    # path('', views.dashboard, name='dashboard'),
    path('population-chart/', views.population_chart, name='population-chart'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
   # Change Password
    #path('project/Login/', auth_views.LoginView.as_view(),{'template_name': 'registration/login.html'}, name='login'),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html',success_url='/project/dashboard/'),name='change_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


