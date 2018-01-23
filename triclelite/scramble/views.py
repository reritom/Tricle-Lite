from django.shortcuts import render
from django.http import JsonResponse
from scramble.scramblecore import scrambler
from scramble.tools import mediaTools, uuidTools
from scramble.models import ActiveURL, ExpiredURL
from scramble.forms import ScrambleForm
from django.conf import settings

import uuid, shutil, zipfile, os, pickle
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
    form = ScrambleForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({"post":False, "detail":"Invalid form data"})

    form = form.cleaned_data
    form_data = formdat = {'mode' : form['mode'], 'k1' : form['key_one'], 'k2' : form['key_two'], 'k3' : form['key_three']}

    if not len(request.FILES.getlist('images')) > 0:
        return JsonResponse({"post":False, "detail":"No images submitted"})

    valid = True
    if valid:
        # Create an ActiveURL
        urlobj = ActiveURL.objects.create()
        this_uuid = uuidTools.generate_uuid()
        urlobj.uuid = this_uuid
        if formdat['mode'] == 'Unscramble':
            urlobj.mode = 'Unscramble'
        urlobj.save()
        mediaTools.make_dir(urlobj.uuid)

    # Create the dir for storing the files
    if 'temp' not in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble')):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp'))

    if this_uuid not in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp')):
            os.mkdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', this_uuid))

    media_path = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', this_uuid)

    # Store the keys
    with open(os.path.join(media_path, 'data'), 'wb') as fp:
        pickle.dump(formdat, fp)

    # Store the files
    for f in request.FILES.getlist('images'):
        if f.name.lower().endswith(('.jpg', '.bmp', '.png', '.jpeg')):
            image = Image.open(f)
            image.save(os.path.join(media_path, f.name), subsampling=0, quality=100)
            urlobj.number_of_files = urlobj.number_of_files + 1
            urlobj.save()

    # return success to initate the load
    return JsonResponse({"Post":urlobj.uuid})

def load(request, uuid):
    '''
        This method processes the files.
        This gets AJAX-ed straight after the post
    '''
    #validate_uuid_request()
    #process files
    #mark files as processed
    return JsonResponse({"load":uuid})

def download(request, uuid):
    '''
        This method retrieves the zipped download file
    '''
    #validate_uuid_request()
    #download if processed
    return JsonResponse({"Download":uuid})

def done(request, uuid):
    '''
        This method removes any transaction data for a given uuid
    '''
    if uuidTools.validate_uuid_in_db(uuid) or mediaTools.validate_uuid_in_media(uuid):
        # Check that the uuid is present in either location
        if uuidTools.validate_uuid_in_db(uuid):
            uuidTools.expire_uuid(uuid)
        if mediaTools.validate_uuid_in_media(uuid):
            mediaTools.delete_dir(uuid)

        return JsonResponse({"Done":uuid})
    else:
        return JsonResponse({"DoesNotExistDone":uuid})
