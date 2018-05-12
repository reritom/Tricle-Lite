from django.conf.urls import url, include
from scramble.views.cleanup import cleanup
from scramble.views.done import done
from scramble.views.load import load
from scramble.views.post import post
from scramble.views.down import download
from scramble.views.status import status
from scramble.views.hard import hard
from scramble.views.eta import eta

app_name = 'scrambler'

urlpatterns = [
    url(r'post', post, name='post'),
    url(r'load/(?P<url>\w+)/', load, name='load'),
    url(r'down/(?P<url>\w+)/', download, name='download'),
    url(r'status/(?P<url>\w+)/', status, name='status'),
    url(r'done/(?P<url>\w+)/', done, name='done'),
    url(r'iaw/', cleanup, name='cleanup'),
    url(r'hard/', hard, name='hard'),
    url(r'eta/(?P<url>\w+)/', eta, name='eta'),
]
