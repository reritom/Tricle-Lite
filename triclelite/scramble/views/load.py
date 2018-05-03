from scramble.tools import media_tools, url_tools, common_tools
from scramble.tools.response_tools import response_ko, response_ok
from scramble.core.manager import ScramblerManager
from scramble.tools.validation.decorators import validate_url
from scramble.models import ActiveURL, ExpiredURL, ZipLock, KeyChain
from scramble.forms import ScrambleForm
from django.conf import settings
from django.utils import timezone

from datetime import datetime, timedelta
from hashlib import sha1
from pathlib import Path

import shutil, zipfile, os, pickle

@validate_url
def load(request, url):
    '''
        This method processes the files.
        This gets AJAX-ed straight after the post
    '''

    urlobj = ActiveURL.objects.get(url=url)

    if urlobj.is_processed():
        return response_ko("Already loaded")

    media_path = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)

    #process files
    print("At Manager")
    with ScramblerManager(media_path, url) as manager:
        manager.run()

    return response_ok({"url":url})
