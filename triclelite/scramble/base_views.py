from django.shortcuts import render
from scramble.forms import ScrambleForm
from django.conf import settings
# Create your views here.

def start(request):
    form = ScrambleForm
    return render(request, 'scramble/home.html', {'form':form, 'phase':settings.PHASE})
