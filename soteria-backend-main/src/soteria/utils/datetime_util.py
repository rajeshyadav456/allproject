from datetime import datetime
from typing import Union

import pytz
from django.utils import timezone as dj_timezone

get_default_timezone = dj_timezone.get_default_timezone


def get_current_datetime(tz_name=None) -> datetime:
    now = dj_timezone.now()
    if tz_name:
        now = now.astimezone(pytz.timezone(tz_name))
    return now


def dt_to_epoch(dt: datetime) -> Union[int, None]:
    if isinstance(dt, datetime):
        return int(dt.timestamp())
    return None


def dt_to_epoch_millis(dt: datetime) -> Union[int, None]:
    if isinstance(dt, datetime):
        return int(int(dt.timestamp() * 1e3))
    return None


def epoch_to_epoch_millis(epoch: int) -> int:
    return int(int(epoch) * 1e3)


def epoch_to_dt(epoch, tz=pytz.utc):
    """
    Convert given epoch/unix timestamp (i.e 1575397800) to python datetime
    object.
    :param epoch: epoch timestamp
    :param tz: timezone of datetime object
    :return:
    """
    epoch = int(epoch)
    return datetime.utcfromtimestamp(epoch).replace(tzinfo=tz)


def dt_to_str(dt: datetime, str_format: str = None, tz_name: str = None) -> str:
    if str_format is None:
        str_format = "%Y-%m-%d %H:%M:%S"
    if tz_name is None:
        tz_name = "UTC"
    timezone = pytz.timezone(tz_name)
    return dt.replace(tzinfo=pytz.utc).astimezone(timezone).strftime(str_format)
