from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from scramble.tools import media_tools, url_tools, common_tools
from scramble.models import ActiveURL, ExpiredURL, ZipLock, KeyChain
from django.conf import settings
from django.utils import timezone

from datetime import datetime, timedelta
from hashlib import sha1
from pathlib import Path

import shutil, zipfile, os, pickle

def status(request, url):
    '''
        This method returns the status of the url,
        including whether it is still downloadable
    '''

    status = {'processed':'?',
              'downloadable':'?',
              'expires_at':'?',
              'downloads_remaining':'?',
              'valid':'?'}

    if not url_tools.validate_url_request(url):
        status['valid'] = False
        return JsonResponse(status)

    urlobj = ActiveURL.objects.get(url=url)

    if urlobj.is_expired():
        #url has expired, mark as expired, delete dirs, redirect to homepage
        url_tools.expire_url(url)
        status['valid'] = False
        return JsonResponse(status)
    else:
        status['valid'] = True
        status['expires_at'] = urlobj.get_expiration()

    if urlobj.is_processed():
        status['processed'] = True
    else:
        status['processed'] = False

    status['downloads_remaining'] = settings.DOWNLOAD_LIMIT - urlobj.down_count

    if urlobj.is_downloadable():
        status['downloadable'] = True
    else:
        status['downloadable'] = False

    if urlobj.down_count == settings.DOWNLOAD_LIMIT:
        url_tools.expire_url(url)

    return JsonResponse(status)
