from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from scramble.tools.response_tools import response_ko, response_ok
from scramble.tools import media_tools, url_tools, common_tools
from scramble.models.active_url import ActiveURL
from scramble.models.zip_lock import ZipLock
from scramble.models.key_chain import KeyChain
from scramble.models.url_item import UrlItem
from scramble.forms import ScrambleForm

from datetime import datetime
from pathlib import Path
from PIL import Image
import os

@csrf_exempt
def post(request):
    '''
        This method accepts and stores the data for scrambling
    '''
    common_tools.show_request(request)

    form = ScrambleForm(request.POST, request.FILES)
    if not form.is_valid():
        return response_ko("Invalid form data")

    form = form.cleaned_data
    formdat = {'mode' : form['mode'], 'k1' : form['key_one'], 'k2' : form['key_two'], 'k3' : form['key_three']}

    if formdat['mode'] not in ['Scramble', 'Unscramble']:
        return response_ko('Invalid mode')

    for key in ['k1', 'k2', 'k3']:
        if len(formdat[key]) < 3:
            return response_ko('Key too short')

    if not len(request.FILES.getlist('images')) > 0:
        return response_ko("No images submitted")

    # Create an ActiveURL
    this_url = ActiveURL.generate_url()
    urlobj = ActiveURL.objects.create(url=this_url)

    if formdat['mode'] == 'Unscramble':
        urlobj.mode = 'Unscramble'
    urlobj.set_token(form['retrieve_token'])
    urlobj.save()

    # Create ZipCode object
    if form.get('zipcode', False):
        zipobj = ZipLock.objects.create(active=urlobj)
        zipobj.set_zipcode(form['zipcode'])
        zipobj.save()

    # Create KeyChain object
    keyobj = KeyChain.objects.create(active=urlobj)
    keyobj.set_keys([formdat['k1'], formdat['k2'], formdat['k3']])
    keyobj.save()

    # Create the dir for storing the files
    media_path = media_tools.make_dir(this_url)

    # Store the files and create a URL item for each
    for f in request.FILES.getlist('images'):
        if f.name.lower().endswith(('.jpg', '.bmp', '.png', '.jpeg')):

            file_name, file_type = os.path.splitext(f.name.lower())
            file_path = os.path.join(media_path, f.name)

            image = Image.open(f)
            image.save(file_path, subsampling=0, quality=100)

            file_size = os.path.getsize(file_path)

            # Create the UrlItem
            url_item = UrlItem.objects.create(id=UrlItem.create_url_item_uuid(),
                                              active=urlobj,
                                              file_name=file_name,
                                              file_type=file_type[1:],
                                              file_size=file_size,
                                              file_path=file_path)
            urlobj.increment_count()

    # return success to initate the load
    return response_ok({"url":this_url})
