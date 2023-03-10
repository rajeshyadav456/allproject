import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from soteria.exception import AccountAlreadyExists
from soteria.models import InvitationCode, User

logger = logging.getLogger(__name__)


def create_user(
    first_name: str,
    last_name: str,
    email: str,
    mobile: str,
    password: str,
    username: str = None,
    invitation_code: str = None,
    can_create_org: bool = True,
) -> User:
    """
    creating user , if user not exists with same email and mobile
    """
    if User.objects.filter(email=email).exists():
        logger.info(f"User with {email} is already exists.")
        raise AccountAlreadyExists(_("A user with this email address already exists"))

    if User.objects.filter(mobile=mobile).exists():
        logger.info(f"User with {mobile} is already exists.")
        raise AccountAlreadyExists(_("A user with this mobile number already exists"))

    email = User.normalize_email(email)
    _invitation_code = InvitationCode.objects.filter(
        user_id=None, is_used=False, code=invitation_code
    ).first()

    # if invitation code belong to org member then we set `can_create_org` to False.
    if _invitation_code and _invitation_code.belongs_to_invited_org_member():
        can_create_org = False

    if not username:
        username = email

    with transaction.atomic():
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            username=username,
            can_create_org=can_create_org,
        )
        user.set_password(password)
        user.save()

        if invitation_code:
            _invitation_code.user = user
            _invitation_code.is_used = True
            _invitation_code.save()

        return user
