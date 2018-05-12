from scramble.models.active_url import ActiveURL
from scramble.tools.validation.decorators import validate_url_anywhere
from scramble.tools.response_tools import response_ko, response_ok
from scramble.tools import media_tools, url_tools, common_tools

@validate_url_anywhere
def eta(request):
    '''
        This view is for returning the estimated or actual processing time for a
        given ActiveUrl.
    '''
    urlobj = ActiveURL.objects.get(url=url)


    return response_ok({'type':"estimate/actual", 'estimate':"in seconds"})
