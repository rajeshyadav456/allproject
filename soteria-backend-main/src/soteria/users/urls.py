from django.urls import path

from soteria.users.views.user_info import UserInfoAPI
from soteria.users.views.user_profile_image import UploadProfileImageAPI

urlpatterns = [
    path("api/v1/user/", UserInfoAPI.as_view(), name="user-info"),
    path("api/v1/me/avatar/", UploadProfileImageAPI.as_view(), name="user-avatar"),
]
