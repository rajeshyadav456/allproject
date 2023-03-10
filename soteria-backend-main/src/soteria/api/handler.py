# Note: Don't import "exceptions_hog" package in top level of this module, otherwise our monkey
# patching will fail
import json
import logging
from typing import Dict, List, Optional, Union

import sentry_sdk
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.utils import encoders
from rest_framework_simplejwt.exceptions import InvalidToken as JWTInvalidToken

logger = logging.getLogger(__name__)


def exception_handler(exc: BaseException, context: Optional[Dict] = None) -> Optional[Response]:
    # NOTE: handling a special case of
    # rest_framework_simplejwt.exceptions.InvalidToken due to its breaking
    # nature with 'exceptions_hog' package when this error raised in
    # 'rest_framework_simplejwt.authentication.JWTAuthentication
    # .get_validated_token()' method
    if (
        isinstance(exc, JWTInvalidToken)
        and isinstance(exc.detail, dict)
        and "messages" in exc.detail
    ):
        logger.warning(
            f"Updating error detail of InvalidToken exception, original "
            f"error detail is : "
            f"{json.dumps(exc.detail, cls=encoders.JSONEncoder)} "
        )
        exc.detail = exceptions._get_error_details(exc.default_detail, exc.default_code)
    import exceptions_hog

    resp = exceptions_hog.exception_handler(exc, context)
    if isinstance(resp, Response):
        resp.data = {
            "success": False,
            "error": resp.data,
        }
    return resp


def exception_reporter(exc: BaseException, context: Optional[Dict] = None) -> None:
    """
    Logic for reporting an exception to any APMs.
    Example:
        if not isinstance(exc, exceptions.APIException):
            capture_exception(exc)
    """
    # log error to logger
    if not isinstance(exc, exceptions.APIException):
        request = context["request"]
        msg = f"Error while processing request '{request.path}' : {str(exc)}"
        logger.exception(msg)

    # log error to sentry
    if not isinstance(exc, exceptions.APIException):
        sentry_sdk.capture_exception(exc)


def monkey_patch_exceptions_hog():
    import exceptions_hog.handler

    _get_attr_original = exceptions_hog.handler._get_attr

    def _get_attr(exception_key: Optional[Union[str, List[str]]] = None) -> Optional[str]:
        # ensure each key should be of type string if we have list
        if isinstance(exception_key, list):
            exception_key = [key if isinstance(key, str) else str(key) for key in exception_key]
        return _get_attr_original(exception_key)

    exceptions_hog.handler._get_attr = _get_attr


monkey_patch_exceptions_hog()
