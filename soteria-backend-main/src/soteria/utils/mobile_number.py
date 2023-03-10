import re

from django.conf import settings

DEFAULT_CALLING_CODE = settings.DEFAULT_CALLING_CODE
SUPPORTED_CALLING_CODES = settings.ALLOWED_CALLING_CODES

# a regex for mobile number without having calling code with valid
# significant digits count in mobile number
MOBILE_NUMBER_WITHOUT_CC_REGEX = re.compile("^(\\d{4,12})$")

# a regex for mobile number having calling code with valid
# significant digits count in calling code and mobile number
MOBILE_NUMBER_CC_REGEX = re.compile("^\\+(\\d{1,3}) (\\d{4,12})$")

# a regex for international format like (+91 9999999999) without any
# significant digits check
MOBILE_NUMBER_REGEX = re.compile("^\\+(\\d*) (\\d*)$")


class CallingCodeInvalid(Exception):
    """
    This exception is raised if calling code is not valid, means no country
    have this calling code
    """

    pass


class CallingCodeNotSupported(Exception):
    """
    This exception is raised if calling code is not supported by system
    """

    pass


class MobileNumberLengthInvalid(Exception):
    """
    This exception is raised if mobile number length is not as per
    the selected calling code
    """

    pass


def is_calling_code_supported(calling_code):
    return calling_code in SUPPORTED_CALLING_CODES


def is_valid_mobile_number_without_cc(mobile_number):
    return MOBILE_NUMBER_WITHOUT_CC_REGEX.match(str(mobile_number)) is not None


def is_valid_mobile_number_with_cc(mobile_number):
    return MOBILE_NUMBER_CC_REGEX.match(str(mobile_number)) is not None


def is_valid_mobile_number(mobile_number, calling_code=None, cc_support_check=True):
    """
    Checks whether the given mobile number is in any supported formats (i.e
    with cc or without cc). Can raise `CallingCodeInvalid` error on finding
    invalid calling code. Can also raise `CallingCodeNotSupported` error if
    calling code is not supported by the system. Can also raise
    `MobileNumberLengthInvalid` error if mobile number is not valid as per
    country specs
    :param mobile_number: mobile number
    :param calling_code: default calling code for mobile number have missing
    calling code
    :param cc_support_check: do calling code support check
    :return: boolean
    """
    if calling_code is None:
        calling_code = settings.DEFAULT_CALLING_CODE
    mobile_number = normalize_mobile_number(mobile_number, calling_code=calling_code)
    # validate mobile_number
    if not mobile_number:
        return False

    cc, mobile_number_without_cc = split_cc_and_mobile_number(mobile_number)

    if cc_support_check:
        # validate if the mobile services support that cc.
        if not is_calling_code_supported(cc):
            raise CallingCodeNotSupported(
                'Calling code "%s" of mobile number "%s" is not supported '
                "by the system, please try other calling code" % (cc, mobile_number)
            )
    return True


def normalize_mobile_number(mobile_number, calling_code=None):
    """
    Normalize the given mobile number to the international format
    (i.e +<calling code> <mobile number>) if possible otherwise return empty
    string
    :param mobile_number:
    :param calling_code: default calling code for mobile number have missing
    calling code
    :return:
    """
    if calling_code is None:
        calling_code = DEFAULT_CALLING_CODE
    mobile_number = str(mobile_number)
    if is_valid_mobile_number_with_cc(mobile_number):
        return mobile_number
    elif is_valid_mobile_number_without_cc(mobile_number):
        return "+%s %s" % (calling_code, mobile_number)
    return ""


def format_mobile_number(mobile_number: str, calling_code: str = None) -> str:
    """
    Format given mobile number by normalizing it to international format if
    possible otherwise return same mobile number
    :param mobile_number: mobile number
    :param calling_code: default calling code for mobile number have missing
    calling code
    :return: mobile number
    """
    m = normalize_mobile_number(mobile_number, calling_code=calling_code)
    # normalization return empty string for invalid mobile number format
    if not m:
        m = mobile_number
    return m


def split_cc_and_mobile_number(mobile_number):
    """
    Extract calling code and mobile number digits from given mobile number.
    Note: It doesn't do validation, please validate the mobile number first,
    if not sure.
    :param mobile_number: a mobile number
    :return: a tuple of calling code and mobile number digits
    """
    m = MOBILE_NUMBER_REGEX.match(str(mobile_number))
    return m.group(1), m.group(2)


def compare_mobile_number_equal(mobile1, mobile2):
    """
    Compare two mobile number and tells whether both are equal or not.
    Mobile number can be in any format with or without calling code.
    :param mobile1:
    :param mobile2:
    :return:
    """
    mobile1 = normalize_mobile_number(mobile1)
    mobile2 = normalize_mobile_number(mobile2)
    # normalization returns empty string for invalid formatted mobile number
    if not mobile1 or not mobile2:
        return False
    m1_cc, m1_number = split_cc_and_mobile_number(mobile1)
    m2_cc, m2_number = split_cc_and_mobile_number(mobile2)
    if m1_cc != m2_cc:
        return False
    if m1_number != m2_number:
        return False
    return True


def mask_mobile_number(mobile_number):
    mobile_number = normalize_mobile_number(mobile_number)
    if not mobile_number:
        return None
    cc, _ = split_cc_and_mobile_number(mobile_number)
    unmasked = len(cc) + 4
    mask_digit = len(mobile_number) - unmasked
    return mobile_number[:unmasked] + "X" * mask_digit + mobile_number[-2:]
