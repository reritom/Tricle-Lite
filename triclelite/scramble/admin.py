from django.contrib import admin
from scramble.models import ActiveURL, ExpiredURL, ZipLock, KeyChain

# Register your models here.

admin.site.register(ActiveURL)
admin.site.register(ExpiredURL)
admin.site.register(ZipLock)
admin.site.register(KeyChain)
