
from django.http import HttpResponse, JsonResponse
from scramble.tools import mediaTools, urlTools, commonTools
from scramble.models import ActiveURL, ZipLock, KeyChain
from scramble.forms import ScrambleForm

from datetime import datetime
from pathlib import Path
from PIL import Image
import os

def post(request):
    '''
        This method accepts and stores the data for scrambling
    '''
    #validate_keys()
    #valifate_files()
    commonTools.show_request(request)

    form = ScrambleForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({"status":False, "message":"Invalid form data"})

    form = form.cleaned_data
    formdat = {'mode' : form['mode'], 'k1' : form['key_one'], 'k2' : form['key_two'], 'k3' : form['key_three']}

    if formdat['mode'] not in ['Scramble', 'Unscramble']:
        return JsonResponse({"status":False, 'message':'Invalid mode'})

    for key in ['k1', 'k2', 'k3']:
        if len(formdat[key]) < 3:
            return JsonResponse({"status":False, 'message':'Key too short'})

    if not len(request.FILES.getlist('images')) > 0:
        return JsonResponse({"status":False, "message":"No images submitted"})

    # Create an ActiveURL
    urlobj = ActiveURL.objects.create()
    this_url = urlobj.get_url()
    if formdat['mode'] == 'Unscramble':
        urlobj.mode = 'Unscramble'
    urlobj.setToken(form['retrieve_token'])
    urlobj.save()

    # Create ZipCode object
    if form.get('zipcode', False):
        zipobj = ZipLock.objects.create(active=urlobj)
        zipobj.setZipcode(form['zipcode'])
        zipobj.save()

    # Create KeyChain object
    keyobj = KeyChain.objects.create(active=urlobj)
    keyobj.setKeys([formdat['k1'], formdat['k2'], formdat['k3']])
    keyobj.save()

    # Create the dir for storing the files
    media_path = mediaTools.make_dir(this_url)

    # Store the files
    for f in request.FILES.getlist('images'):
        if f.name.lower().endswith(('.jpg', '.bmp', '.png', '.jpeg')):
            image = Image.open(f)
            image.save(os.path.join(media_path, f.name), subsampling=0, quality=100)
            urlobj.increment_count()

    # return success to initate the load
    return JsonResponse({"status":True, "url":this_url})