from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from scramble.scramblecore import scrambler
from scramble.tools import mediaTools, urlTools, commonTools
from scramble.core.manager import ScramblerManager
from scramble.models import ActiveURL, ExpiredURL
from scramble.forms import ScrambleForm
from django.conf import settings
from django.utils import timezone

from datetime import datetime, timedelta
from hashlib import sha1
from pathlib import Path

import shutil, zipfile, os, pickle
from PIL import Image

# Create your views here.

def start(request):
    if request.method == 'GET':
        form = ScrambleForm
        return render(request, 'scramble/home.html', {'form':form})
    if request.method == 'POST':
        return post(request)
    #transaction_daemon()
    return render(request, 'scramble/home.html')

def post(request):
    '''
        This method accepts and stores the data for scrambling
    '''
    #validate_keys()
    #valifate_files()
    commonTools.show_request(request)

    form = ScrambleForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({"post":False, "detail":"Invalid form data"})

    form = form.cleaned_data
    formdat = {'mode' : form['mode'], 'k1' : form['key_one'], 'k2' : form['key_two'], 'k3' : form['key_three']}

    if formdat['mode'] not in ['Scramble', 'Unscramble']:
        return JsonResponse({'post':'Invalid mode'})

    for key in ['k1', 'k2', 'k3']:
        if len(formdat[key]) < 3:
            return JsonResponse({'post':'Key too short'})

    if not len(request.FILES.getlist('images')) > 0:
        return JsonResponse({"post":False, "detail":"No images submitted"})

    # Create an ActiveURL
    urlobj = ActiveURL.objects.create()
    this_url = urlobj.get_url()
    if formdat['mode'] == 'Unscramble':
        urlobj.mode = 'Unscramble'
    urlobj.save()

    # Create the dir for storing the files
    media_path = mediaTools.make_dir(this_url)

    # Store the keys
    with open(os.path.join(media_path, 'data'), 'wb') as fp:
        pickle.dump(formdat, fp)

    # Store the files
    for f in request.FILES.getlist('images'):
        if f.name.lower().endswith(('.jpg', '.bmp', '.png', '.jpeg')):
            image = Image.open(f)
            image.save(os.path.join(media_path, f.name), subsampling=0, quality=100)
            urlobj.increment_count()

    # return success to initate the load
    return JsonResponse({"post":True, "url":this_url})

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
    manager = ScramblerManager(media_path, url)
    manager.run()

    #mark files as processed
    urlobj.set_processed()
    '''
    # Remove the unprocessed files and the data file
    for filename in os.listdir(media_path):
        if not (filename.endswith('.txt') or filename.endswith('.zip')):
            mediaTools.delete_file(os.path.join(media_path, filename))
    '''
    return JsonResponse({"load":True, "url":url})

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

    if not urlTools.validate_url_request(url):
        status['valid'] = False
        return JsonResponse(status)

    urlobj = ActiveURL.objects.get(url=url)

    if urlobj.is_expired():
        #url has expired, mark as expired, delete dirs, redirect to homepage
        urlTools.expire_url(url)
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
        urlTools.expire_url(url)

    return JsonResponse(status)

def download(request, url):
    '''
        This method retrieves the zipped download file
    '''
    if not urlTools.validate_url_request(url):
        return JsonResponse({"Download":False})

    urlobj = ActiveURL.objects.get(url=url)

    if not urlobj.is_downloadable():
        #to limit number of download attempts, for security
        urlTools.expire_url(url)
        return JsonResponse({"Download":'limit reached'})
    else:
        urlobj.inc_down_count()

    if urlobj.is_expired():
        #url has expired, mark as expired, delete dirs, redirect to homepage
        urlTools.expire_url(url)
        return JsonResponse({"Download":'url expired'})

    if not urlTools.url_in_media(url):
        urlTools.expire_url(url)
        return JsonResponse({"Download":'url not found'})

    if urlobj.is_processed():
        return JsonResponse({"Download":'url not processed'})

    #download if processed
    for files in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)):
        if files.lower().endswith(('.zip')):
            prezipped = files

    prezipped_address = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url, prezipped)
    response = HttpResponse(open(prezipped_address, 'rb').read(),
                         content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + prezipped
    return response

    return JsonResponse({"Download":url})

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

def cleanup(request):
    '''
        This method checks all active urls and expires accordingly.
    '''
    pass
