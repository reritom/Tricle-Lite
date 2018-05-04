from django.utils.functional import wraps
from django.core.exceptions import PermissionDenied

from scramble.tools import media_tools, url_tools, common_tools
from scramble.tools.response_tools import response_ko, response_ok

def validate_url(view):
    @wraps(view)
    def inner(request, url):
        print("In inner validator")
        # Validate that the URL exists
        if not url_tools.validate_url_request(url):
            return response_ko("Invalid URL")

        # Validate that the URL isn't expired
        if not url_tools.validate_url_not_expired(url):
            url_tools.expire_url(url)
            return response_ko("URL has expired")

        return view(request, url)
    return inner

def superuser_only(function):
    def inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return inner
