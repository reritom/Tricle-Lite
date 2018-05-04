from frontend.views import main_vue
from django.conf.urls import url, include

app_name = 'frontend'

urlpatterns = [
    url(r'^$', main_vue, name='start'),
]
