from scramble.tools.validation.decorators import validate_url
from scramble.tools.response_tools import response_ko, response_ok
from scramble.models.active_url import ActiveURL


@validate_url
def status(request, url):
    '''
        This method returns the status of the url,
        including whether it is still downloadable
    '''

    urlobj = ActiveURL.objects.get(url=url)
    return response_ok(urlobj.get_status())
