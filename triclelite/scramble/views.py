from django.shortcuts import render
from django.http import JsonResponse
from scramble.scramblecore import scrambler

# Create your views here.

def home(request):
    return render(request, 'scramble/home.html')

def post(request):
    #validate_keys()
    #valifate_files()
    #for each: scrambler()
    #create_transaction()
    #return transaction uuid
    return JsonResponse({"Post":True})

def download(request, uuid):
    #validate_uuid_request()
    #
    return JsonResponse({"Download":uuid})

def done(request, uuid):
    #validate_uuid_request()
    #remove_uuid_from_media()
    #end_transaction()
    return JsonResponse({"Done":uuid})
