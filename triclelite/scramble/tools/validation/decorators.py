from django.utils.functional import wraps
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

    print("Inner is {0}".format(inner))

    return inner
'''
def generate_response(view):
    print("In generate response for view {0}".format(view.__name__))
    @wraps(view)
    def inner(request, url):
        return view(request, url)
    return inner
'''
