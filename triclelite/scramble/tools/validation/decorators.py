from django.utils.functional import wraps
from django.core.exceptions import PermissionDenied

from scramble.tools import media_tools, url_tools, common_tools
from scramble.tools.response_tools import response_ko, response_ok

def validate_url(view):
    '''
        Validate that the Url exists and is active
    '''
    @wraps(view)
    def inner(request, url):
        print("In inner validator")
        # Validate that the URL exists
        if not url_tools.validate_url_request(url):
            print("Invalid URL")
            return response_ko("Invalid URL")

        # Validate that the URL isn't expired
        if not url_tools.validate_url_not_expired(url):
            url_tools.expire_url(url)
            print("URL has expired")
            return response_ko("URL has expired")

        return view(request, url)
    return inner

def validate_url_anywhere(view):
    '''
        Validate that the Url exists and is active
    '''
    @wraps(view)
    def inner(request, url):
        print("In inner validator")
        # Validate that the URL exists as either an active or expired url
        if not (url_tools.validate_url_request(url) or url_tools.validate_url_in_expired(url)):
            return response_ko("Invalid URL")

        return view(request, url)
    return inner

def superuser_only(function):
    def inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            return response_ko("Invalid permissions")
        return function(request, *args, **kwargs)
    return inner
