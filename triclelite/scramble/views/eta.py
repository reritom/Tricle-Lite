from scramble.models.active_url import ActiveURL
from scramble.tools.validation.decorators import validate_url
from scramble.tools.response_tools import response_ko, response_ok
from scramble.tools import media_tools, url_tools, common_tools

@validate_url
def eta(request, url):
    '''
        This view is for returning the estimated or actual processing time for a
        given ActiveUrl.
    '''
    urlobj = ActiveURL.objects.get(url=url)

    # Compare the files, file sizes and filetypes with that of the expired url durations, and the image data stores to predict the loading time

    # Add the predicted time for each image to its url item (on expiration, this gets added to the data store)

    return response_ok({'type':"estimate/actual", 'estimate':"in seconds"})
