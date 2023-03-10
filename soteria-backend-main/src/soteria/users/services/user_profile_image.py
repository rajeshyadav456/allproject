import logging

from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)

USER_PROFILE_IMAGE_FILENAME_PATTERN = "user-profile/{user_id}/{random_str}-{file_name}"


def upload_user_profile(file, user) -> str:
    random_str = get_random_string(length=12)
    file_name = USER_PROFILE_IMAGE_FILENAME_PATTERN.format(
        **{
            "user_id": user.id,
            "random_str": random_str,
            "file_name": file.name,
        }
    )
    logger.info(f"Uploading user profile image :{file_name}")
    path = default_storage.save(name=file_name, content=file)
    file_url = default_storage.url(path)
    file_url = str(file_url).partition("?")[0]
    return file_url
