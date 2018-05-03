from django.http import JsonResponse
from scramble.tools import media_tools, url_tools

def done(request, url):
    '''
        This method removes any transaction data for a given url
    '''
    if url_tools.validate_url_in_db(url) or url_tools.url_in_media(url):
        # Check that the url is present in either location
        if url_tools.validate_url_in_db(url):
            url_tools.expire_url(url)
        if url_tools.url_in_media(url):
            media_tools.delete_dir(url)

        return JsonResponse({"status":True})
    else:
        return JsonResponse({"status":False, "message":"Invalid url"})
