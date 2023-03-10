from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import EmailUserCreationForm, EmailUserChangeForm

admin.site.register(Contacts)
admin.site.register(Devices)
admin.site.register(Categories)
admin.site.register(RequestedAudio)
admin.site.register(Items)
admin.site.register(LikedItems)
admin.site.register(Favourites)
admin.site.register(Friends)
admin.site.register(Comments)
admin.site.register(TermsAndPolicyText)
admin.site.register(Seasons)
admin.site.register(Episodes)
admin.site.register(UserNotifications)
admin.site.register(Profile)
admin.site.register(Reports)
# admin.site.register(RequestAudiomodel)
# admin.site.register(Reportmodel)
# admin.site.register(Profilemodel)
# admin.site.register(SignupCode)
# admin.site.register(PasswordResetCode)
# admin.site.register(EmailChangeCode)
