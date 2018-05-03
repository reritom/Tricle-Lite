from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from scramble.tools.validation.decorators import validate_url
from scramble.tools.response_tools import response_ko, response_ok
from scramble.tools import media_tools, url_tools, common_tools
from scramble.models import ActiveURL
from django.conf import settings

from datetime import datetime
from pathlib import Path

import os

@validate_url
@csrf_exempt
def download(request, url):
    '''
        This method retrieves the zipped download file
    '''
    print("In download")

    urlobj = ActiveURL.objects.get(url=url)

    # Validate the request token
    token = request.GET.get('token', False)
    if token is False:
        return response_ko({"Missing token"})

    if not urlobj.validateToken(token):
        return response_ko({"Invalid token"})

    # Valiate download-ability
    if not urlobj.is_downloadable():
        #to limit number of download attempts, for security
        url_tools.expire_url(url)
        return response_ko({'limit reached'})
    else:
        urlobj.inc_down_count()

    if not url_tools.url_in_media(url):
        url_tools.expire_url(url)
        return response_ko({'url not found'})

    if not urlobj.is_processed():
        return response_ko({'url not processed'})

    # Download if processed
    for files in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)):
        if files.lower().endswith(('.zip')):
            prezipped = files

    prezipped_address = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url, prezipped)
    response = HttpResponse(open(prezipped_address, 'rb').read(),
                         content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + prezipped
    return response
