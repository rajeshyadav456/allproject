import logging

from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)

FORM_IMAGE_FILENAME_PATTERN = "org-forms/images/{random_str}-{file_name}"


def upload_form_image(file) -> str:
    """
    Upload form image
    :return - file url
    """
    random_str = get_random_string(length=12)
    file_name = FORM_IMAGE_FILENAME_PATTERN.format(
        **{
            "random_str": random_str,
            "file_name": file.name,
        }
    )
    logger.info(f"Uploading form image :{file_name}")
    path = default_storage.save(name=file_name, content=file)
    file_url = default_storage.url(path)
    file_url = str(file_url).partition("?")[0]
    return file_url
