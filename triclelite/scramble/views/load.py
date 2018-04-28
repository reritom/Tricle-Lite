from django.http import JsonResponse
from scramble.tools import mediaTools, urlTools, commonTools
from scramble.core.manager import ScramblerManager
from scramble.models import ActiveURL, ExpiredURL, ZipLock, KeyChain
from scramble.forms import ScrambleForm
from django.conf import settings
from django.utils import timezone

from datetime import datetime, timedelta
from hashlib import sha1
from pathlib import Path

import shutil, zipfile, os, pickle

def load(request, url):
    '''
        This method processes the files.
        This gets AJAX-ed straight after the post
    '''

    if not urlTools.validate_url_request(url):
        return JsonResponse({"load":False})

    urlobj = ActiveURL.objects.get(url=url)

    if urlobj.is_expired():
        #url has expired, mark as expired, delete dirs, redirect to homepage
        urlTools.expire_url(url)

    if urlobj.is_processed():
        return JsonResponse({"load":"processed"})

    media_path = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)

    #process files
    print("At Manager")
    with ScramblerManager(media_path, url) as manager:
        manager.run()

    return JsonResponse({"load":True, "url":url})
