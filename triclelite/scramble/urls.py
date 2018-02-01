from django.conf.urls import url, include
from scramble import views

app_name = 'scrambler'

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'load/(?P<url>\w+)/', views.load, name='load'),
    url(r'down/(?P<url>\w+)/', views.download, name='download'),
    url(r'status/(?P<url>\w+)/', views.status, name='status'),
    url(r'done/(?P<url>\w+)/', views.done, name='done'),
    url(r'iaw/', views.cleanup, name='cleanup'),
]
