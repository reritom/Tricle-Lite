from django.contrib import admin
from scramble.models import ActiveURL, ExpiredURL

# Register your models here.

admin.site.register(ActiveURL)
admin.site.register(ExpiredURL)
