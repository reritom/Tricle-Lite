from django.conf.urls import url, include
from scramble import base_views
from scramble.views.cleanup import cleanup
from scramble.views.done import done
from scramble.views.load import load
from scramble.views.post import post
from scramble.views.down import download
from scramble.views.status import status

app_name = 'scrambler'

urlpatterns = [
    url(r'^$', base_views.start, name='start'),
    url(r'api/post', post, name='post'),
    url(r'api/load/(?P<url>\w+)/', load, name='load'),
    url(r'api/down/(?P<url>\w+)/', download, name='download'),
    url(r'api/status/(?P<url>\w+)/', status, name='status'),
    url(r'api/done/(?P<url>\w+)/', done, name='done'),
    url(r'api/iaw/', cleanup, name='cleanup'),
]
