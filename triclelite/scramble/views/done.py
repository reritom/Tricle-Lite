from django.http import JsonResponse
from scramble.tools import mediaTools, urlTools

def done(request, url):
    '''
        This method removes any transaction data for a given url
    '''
    if urlTools.validate_url_in_db(url) or urlTools.url_in_media(url):
        # Check that the url is present in either location
        if urlTools.validate_url_in_db(url):
            urlTools.expire_url(url)
        if urlTools.url_in_media(url):
            mediaTools.delete_dir(url)

        return JsonResponse({"done":url})
    else:
        return JsonResponse({"done":False})
