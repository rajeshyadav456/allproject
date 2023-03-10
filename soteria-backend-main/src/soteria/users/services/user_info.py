import logging
from typing import Dict

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.models import User

logger = logging.getLogger(__name__)


def update_user_details(user: User, data: Dict):

    email = data.get("email", None)
    if email:
        data = run_email_validation(user, data)

    mobile_number = data.get("mobile", None)
    if mobile_number:
        logger.info("Mobile update requested received, running mobile validation.")
        data = run_mobile_validation(user, data)

    update_fields = []
    for field, value in data.items():
        setattr(user, field, value)
        update_fields.append(field)

    if "email" in update_fields:
        logger.info("Email update requested, 'email_verified' field set to 'false'.")
        user.email_verified = False
        update_fields.append("email_verified")

    if "mobile" in update_fields:
        logger.info("Mobile update requested, 'mobile_verified' field set to 'false'.")
        user.mobile_verified = False
        update_fields.append("mobile_verified")

    if update_fields:
        user.updated_by = user
        update_fields.append("updated_by")
        user.save(update_fields=update_fields)

    return user


def run_email_validation(user: User, data: dict) -> dict:
    new_email = data["email"]
    if user.email == new_email:
        data.pop("email")
        # check again if username is set correct
        if user.username != user.email:
            data["username"] = user.email
        return data

    if User.objects.filter(email=new_email).exists():
        raise serializers.ValidationError(
            _("This email has already been registered with another user.")
        )

    # check if email is username or username is None.
    # add username field in data with value of new email.
    if user.username != new_email or not user.username:
        data["username"] = new_email

    return data


def run_mobile_validation(user: User, data: dict) -> dict:
    new_mobile_number = data["mobile"]
    if user.mobile == new_mobile_number:
        data.pop("mobile")
        return data
    if User.objects.filter(mobile=new_mobile_number).exists():
        serializers.ValidationError(_("This mobile has already been registered with another user."))

    return data
