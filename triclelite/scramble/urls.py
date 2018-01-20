from django.conf.urls import url, include
from scramble import views

app_name = 'scrambler'

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'load/(?P<uuid>\w+)/', views.load, name='load'),
    url(r'download/(?P<uuid>\w+)/', views.download, name='download'),
    url(r'done/(?P<uuid>\w+)/', views.done, name='done'),
]
