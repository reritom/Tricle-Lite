from django.utils.functional import wraps

def validate_url(view):
    @wraps(view)
    def inner(request, url):
        print("In inner with url {0}".format(url))
        return view(request, url)
    return inner

def generate_response(view):
    pass
