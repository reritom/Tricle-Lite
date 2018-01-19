from django.shortcuts import render
from django.http import JsonResponse
from scramble.scramblecore import scrambler
from scramble.tools import mediaTools, uuidTools
from scramble.models import ActiveURL, ExpiredURL
import uuid

# Create your views here.

def home(request):
    #transaction_daemon()
    return render(request, 'scramble/home.html')

def post(request):
    '''
        This method accepts and stores the data for scrambling
    '''
    #validate_keys()
    #valifate_files()
    valid = True
    if valid:
        # Create an ActiveURL
        urlobj = ActiveURL.objects.create()
        urlobj.uuid = uuidTools.generate_uuid()
        urlobj.save()

    #for each: scrambler()
    #create_transaction()
    #return transaction uuid
    return JsonResponse({"Post":urlobj.uuid})

def download(request, uuid):
    '''
        This method retrieves the zipped download file
    '''
    #validate_uuid_request()
    #process files
    #mark files as processed
    return JsonResponse({"Download":uuid})

def done(request, uuid):
    '''
        This method removes any transaction data for a given uuid
    '''
    if uuidTools.validate_uuid_request(uuid):
        uuidTools.expire_uuid(uuid)
        return JsonResponse({"Done":uuid})
    else:
        return JsonResponse({"DoesNotExistDone":uuid})
