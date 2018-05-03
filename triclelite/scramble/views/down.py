from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from scramble.tools import media_tools, url_tools, common_tools
from scramble.models import ActiveURL
from django.conf import settings

from datetime import datetime
from pathlib import Path

import os

@csrf_exempt
def download(request, url):
    '''
        This method retrieves the zipped download file
    '''
    print("In download")
    if not url_tools.validate_url_request(url):
        return JsonResponse({"status":False})

    urlobj = ActiveURL.objects.get(url=url)

    # Validate the request token
    token = request.GET.get('token', False)

    if token is False:
        return JsonResponse({"status":False, "message":"Missing token"})

    if not urlobj.validateToken(token):
        return JsonResponse({"status":False, "message":"Invalid token"})

    # Valiate download-ability
    if not urlobj.is_downloadable():
        #to limit number of download attempts, for security
        url_tools.expire_url(url)
        return JsonResponse({"status":False, "message":'limit reached'})
    else:
        urlobj.inc_down_count()

    if urlobj.is_expired():
        #url has expired, mark as expired, delete dirs, redirect to homepage
        url_tools.expire_url(url)
        return JsonResponse({"status":False, "message":'url expired'})

    if not url_tools.url_in_media(url):
        url_tools.expire_url(url)
        return JsonResponse({"status":False, "message":'url not found'})

    if not urlobj.is_processed():
        return JsonResponse({"status":False, "message":'url not processed'})

    #download if processed
    for files in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)):
        if files.lower().endswith(('.zip')):
            prezipped = files

    prezipped_address = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url, prezipped)
    response = HttpResponse(open(prezipped_address, 'rb').read(),
                         content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + prezipped
    return response
