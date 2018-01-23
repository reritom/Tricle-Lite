from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from scramble.scramblecore import scrambler
from scramble.tools import mediaTools, uuidTools
from scramble.models import ActiveURL, ExpiredURL
from scramble.forms import ScrambleForm
from django.conf import settings
from django.utils import timezone

from datetime import datetime, timedelta
from hashlib import sha1
from pathlib import Path

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
    formdat = {'mode' : form['mode'], 'k1' : form['key_one'], 'k2' : form['key_two'], 'k3' : form['key_three']}

    if formdat['mode'] not in ['Scramble', 'Unscramble']:
        return JsonResponse({'post':'Invalid mode'})

    for key in ['key_one', 'key_two', 'key_three']:
        if len(formdat[key]) < 3:
            return JsonResponse({'post':'Key too short'})

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
    url = uuid
    #validate_uuid_request()
    if not ActiveURL.objects.filter(uuid=url).exists():
        return JsonResponse({"load":False})

    urlobj = ActiveURL.objects.get(uuid=url)

    if urlobj.expired == True:
        #check if it is expired, delete dir, redirect to home
        uuidTools.expire_uuid(url)



    expiration = urlobj.created + timedelta(minutes=settings.EXPIRATION_TIME_LIMIT)

    if timezone.now() > expiration:
        #url has expired, mark as expired, delete dirs, redirect to homepage
        uuidTools.expire_uuid(url)

    if "marked.txt" in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)):
        return JsonResponse({"load":"marked"})

    media_path = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)

    try:
        with open(os.path.join(media_path, 'data'), 'rb') as fp:
            form = pickle.load(fp)
    except:
        return JsonResponse({"load":'data load fail'})

    timehash = sha1(str(datetime.now().isoformat()).encode("UTF-8")).hexdigest()[:5]
    zipname = timehash + ".zip"
    zipadr = os.path.join(media_path, zipname)
    zf = zipfile.ZipFile(zipadr, mode='w')


    #process files
    for f in os.listdir(media_path):
        if f.lower().endswith(('bmp', 'jpg', 'png', 'jpeg')):
            image = Image.open(os.path.join(media_path, f))
            final = scrambler(form['mode'], form['k1'], form['k2'], form['k3'], image)

            if form['mode'] == "Scramble":
                name = str(Path(f).with_suffix('')) + ".BMP"
                final.save(os.path.join(media_path, name))
            else:
                try:
                    name = str(Path(f).with_suffix('')) + ".JPG"
                    final.save(os.path.join(media_path, name), format="JPEG", subsampling=0, quality=100)
                except Exception as e:
                    print("Error saving as JPG for user " + request.user + " in interaction " + urlobj.url + " : " + e)
                    try:
                        name = str(Path(f).with_suffix('')) + ".PNG"
                        final.save(os.path.join(media_path, name), format="PNG", subsampling=0, quality=100)
                    except Exception as e:
                        print("Error saving as PNG for user " + request.user + " in interaction " + urlobj.url + " : " + e)
                        try:
                            name = str(Path(f).with_suffix('')) + ".BMP"
                            final.save(os.path.join(media_path, name))
                        except Exception as e:
                            print("Error saving as BMP for user " + request.user + " in interaction " + urlobj.url + " : " + e)
                            print("Unable to save, expiring " + urlobj.url)
                            uuidTools.expire_uuid(url)

            zf = zipfile.ZipFile(zipadr, mode='a')
            try:
                zf.write(os.path.join(media_path, name), arcname=name)
            finally:
                zf.close()

    with open(os.path.join(media_path, "marked.txt"),"w+") as f:
        f.write("")
    #mark files as processed
    return JsonResponse({"load":uuid})

def download(request, uuid):
    '''
        This method retrieves the zipped download file
    '''
    #validate_uuid_request()
    url = uuid
    urlobj = ActiveURL.objects.get(uuid=url)

    if urlobj.down_count >= settings.DOWNLOAD_LIMIT:
        #to limit number of download attempts, for security
        uuidTools.expire_uuid(url)
        return JsonResponse({"Download":'limit reached'})
    else:
        urlobj.down_count += 1
        urlobj.save()

    if urlobj.expired == True:
        #check if it is expired, delete dir, redirect to home
        uuidTools.expire_uuid(url)
        return JsonResponse({"Download":'url expired'})

    expiration = urlobj.created + timedelta(minutes=settings.EXPIRATION_TIME_LIMIT)

    if timezone.now() > expiration:
        #url has expired, mark as expired, delete dirs, redirect to homepage
        uuidTools.expire_uuid(url)
        return JsonResponse({"Download":'url expired'})

    if url not in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp')):
        uuidTools.expire_uuid(url)
        return JsonResponse({"Download":'url not found'})

    if "marked.txt" not in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)):
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

    return JsonResponse({"Download":uuid})

def done(request, uuid):
    '''
        This method removes any transaction data for a given uuid
    '''
    if uuidTools.validate_uuid_in_db(uuid) or mediaTools.validate_uuid_in_media(uuid):
        # Check that the uuid is present in either location
        if uuidTools.validate_uuid_in_db(uuid):
            uuidTools.expire_uuid(uuid)
        if uuidTools.validate_uuid_in_media(uuid):
            mediaTools.delete_dir(uuid)

        return JsonResponse({"Done":uuid})
    else:
        return JsonResponse({"DoesNotExistDone":uuid})
