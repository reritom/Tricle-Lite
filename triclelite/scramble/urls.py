from django.conf.urls import url, include
from . import views

app_name = 'scrambler'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'post/', views.post, name='post'),
]
