from django.shortcuts import render
from scramble.forms import ScrambleForm
from django.conf import settings
# Create your views here.

def start2(request):
    form = ScrambleForm
    return render(request, 'scramble/home.html', {'form':form, 'phase':settings.PHASE})

def start(request):
    return render(request, 'scramble/vue.html')
