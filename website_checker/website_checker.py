import re
import time

import requests


def check(url, regexp=None):
    """
    Make a get request to a given url and return some metrics about the request.

    If the regexp parameter is present,
    check if this regular expression is present within the page returned by the request.

    :param url: url to be checked. if it does not start with http:// or https://, it will be prefixed with http://
    :param regexp: (compiled) regular expression, or None
    :return: if connection is successful, it returns a dictionary with the following keys:
        'timestamp': of the check,
        'url': the actual url checked (which may have been prefixed with 'http://'),
        'response_time': in seconds, see below note
        'status_code': from the response, as string
        'matched': True/False if the regular expression was matched within the page returned by the url

        if connection is unsuccessful, it returna a dictionary with the following keys:
        'timestamp': of the check,
        'url': the actual url checked (which may have been prefixed with 'http://'),
        'error_msg': the message explaining the connection failure

    Note that as the HTTP response time, the "elapsed" time provided by the request library is used,
    that is, the amount of time elapsed between sending the request and the arrival of the response (as a timedelta).
    This property specifically measures the time taken between sending
    the first byte of the request and finishing parsing the headers.
    It is therefore unaffected by consuming the response content or the value of the stream keyword argument.
    See also https://2.python-requests.org/en/master/api/#requests.Response.elapsed
    """
    if isinstance(regexp, str):
        regexp = re.compile(regexp)

    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url

    timestamp = time.time()
    metrics = {
        'timestamp': timestamp,
        'url': url,
    }
    try:
        resp = requests.get(url)
        metrics['response_time'] = resp.elapsed.total_seconds()
        metrics['status_code'] = str(resp.status_code)
        if regexp:
            metrics['matched'] = bool(regexp.search(resp.text))

    except requests.exceptions.RequestException as e:
        # we catch with this all exceptions explicitly raised from requests
        metrics['error_msg'] = "connection error" #str(e)

    return metrics
