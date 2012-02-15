# -*- coding: utf-8 -*-

#   __
#  /__)  _  _     _   _ _/   _
# / (   (- (/ (/ (- _)  /  _)
#          /

"""
requests
~~~~~~~~

:copyright: (c) 2011 by Kenneth Reitz.
:license: ISC, see LICENSE for more details.

"""

__title__ = 'requests'
__version__ = '0.8.6'
__build__ = 0x000806
__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = 'Copyright 2011 Kenneth Reitz'



from . import utils
from .models import Request, Response
from .api import request, get, head, post, patch, put, delete, options
from .sessions import session, Session
from .status_codes import codes
from .exceptions import (
    RequestException, Timeout, URLRequired,
    TooManyRedirects, HTTPError, ConnectionError
)

# The following patch allows requests to be compatible with urllib2 
def _patched_build_opener(*handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP and FTP.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """
    import types
    import httplib
    from urllib2 import OpenerDirector, ProxyHandler, UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, HTTPRedirectHandler, FTPHandler, FileHandler, HTTPErrorProcessor
    def isclass(obj):
        return isinstance(obj, types.ClassType) or hasattr(obj, "__bases__")

    try:
        from urllib2 import HTTPSHandler
    except ImportError:
        pass

    opener = OpenerDirector()
    default_classes = [ProxyHandler, UnknownHandler, HTTPHandler,
                       HTTPDefaultErrorHandler, HTTPRedirectHandler,
                       FTPHandler, FileHandler, HTTPErrorProcessor]
    if hasattr(httplib, 'HTTPS'):
        default_classes.append(HTTPSHandler)
    skip = []
    for klass in default_classes:
        for check in handlers:
            if isclass(check):
                if issubclass(check, klass):
                    skip.append(klass)
            elif isinstance(check, klass):
                skip.append(klass)
    for klass in skip:
        if klass in default_classes:  # This simple if statement is the source of all my troubles...
            default_classes.remove(klass)

    for klass in default_classes:
        opener.add_handler(klass())

    for h in handlers:
        if isclass(h):
            h = h()
        opener.add_handler(h)
    return opener

# Monkey patch that bad library
import urllib2
urllib2.build_opener = _patched_build_opener
