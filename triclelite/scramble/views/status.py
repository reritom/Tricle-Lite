from scramble.tools.validation.decorators import validate_url
from scramble.tools.response_tools import response_ko, response_ok
from scramble.models.active_url import ActiveURL
from scramble.tools import url_tools


@validate_url
def status(request, url):
    '''
        This method returns the status of the url,
        including whether it is still downloadable
    '''

    urlobj = ActiveURL.objects.get(url=url)
    status = urlobj.get_status()

    if not status['downloadable'] and status['processed']:
        # Is processed, but can't be downloaded
        url_tools.expire_url(url)

    return response_ok(status)
