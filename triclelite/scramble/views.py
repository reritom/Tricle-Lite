from django.shortcuts import render
from django.http import JsonResponse
from .scramble import scrambler

# Create your views here.

def home(request):
    return render(request, 'scramble/home.html')

def post(request):
    pass
