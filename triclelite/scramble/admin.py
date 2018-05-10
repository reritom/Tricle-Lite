from django.contrib import admin
from scramble.models.active_url import ActiveURL
from scramble.models.expired_url import ExpiredURL
from scramble.models.zip_lock import ZipLock
from scramble.models.key_chain import KeyChain
from scramble.models.url_item import UrlItem

# Register your models here.

admin.site.register(ActiveURL)
admin.site.register(ExpiredURL)
admin.site.register(ZipLock)
admin.site.register(KeyChain)
admin.site.register(UrlItem)
