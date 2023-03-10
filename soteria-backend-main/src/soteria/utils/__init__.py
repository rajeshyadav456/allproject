import hashlib
import json
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit


def hash_hex(value):
    """
    Returns MD5 hash in hexadecimal form. This hash is fixed size of 32
    characters. MD5 is not secure hashing algorithm, so don't use this hash
    at sensitive places.

    :param value: string or bytes
    :return: hash string
    """
    if not isinstance(value, bytes):
        value = json.dumps(value).encode("utf-8")
    # deepcode ignore insecureHash: we are not using at sensitive places
    return hashlib.md5(value).hexdigest()  # nosec


def to_cs_str(arr):
    assert isinstance(arr, (list, tuple)), "argument should be list or tuple"
    return ",".join(list(map(str, arr)))


def to_pretty_str(arr, sep=",", last_sep="or"):
    if len(arr) >= 2:
        arr = [str(item) for item in arr]
        return f"{sep} ".join(arr[:-1]) + " " + last_sep + " " + arr[-1]
    return str(arr[0])


def to_safe_str(value, safe_length=30, suffix=None):
    value = str(value)
    safe_length = int(safe_length)
    if not suffix:
        suffix = ""
    return value[:safe_length] + suffix if len(value) > safe_length else value


def build_url(url, path_params=None, query_params=None):
    """Given a URL, set or replace a path and query parameters and return the
    modified URL.

    >>> build_url('https://example.com?foo=bar&biz=baz', query_params={'foo',
    ... 'stuff'})
    'https://example.com?foo=stuff&biz=baz'

    """
    url_no_qs, _, query_string = str(url).partition("?")
    try:
        url_no_qs = str(url_no_qs).format(**(path_params or {}))
    except KeyError as e:
        raise Exception("Missing %s key in path_params" % str(e)) from None
    try:
        query_string = str(query_string).format(**(query_params or {}))
    except KeyError as e:
        raise Exception("Missing %s key in query_params" % str(e)) from None
    scheme, netloc, path, _, fragment = urlsplit(url_no_qs)
    query_params = {**(query_params or {}), **parse_qs(query_string)}
    new_query_string = urlencode(query_params, doseq=True)
    return urlunsplit((scheme, netloc, path, new_query_string, fragment))


def bytes_to_mb(bytes_):
    return float(bytes_) / (1024 * 1024)
