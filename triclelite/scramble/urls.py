from django.conf.urls import url, include
from . import views

app_name = 'scrambler'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'post/', views.post, name='post'),
    url(r'download/(?P<uuid>\w+)/', views.download, name='download'),
    url(r'done/(?P<uuid>\w+)/', views.done, name='done'),
]
