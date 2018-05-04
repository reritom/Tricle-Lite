from django.shortcuts import render

# Create your views here.

def main_vue(request):
    return render(request, 'scramble/vue.html')
