import logging

from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)

ASSET_IMAGE_FILENAME_PATTERN = "org-asset/images/{random_str}-{file_name}"


def upload_asset_image(file) -> str:
    """
    Upload asset image
    :return - file url
    """
    random_str = get_random_string(length=12)
    file_name = ASSET_IMAGE_FILENAME_PATTERN.format(
        **{
            "random_str": random_str,
            "file_name": file.name,
        }
    )
    logger.info(f"Uploading asset image :{file_name}")
    path = default_storage.save(name=file_name, content=file)
    file_url = default_storage.url(path)
    file_url = str(file_url).partition("?")[0]
    return file_url
