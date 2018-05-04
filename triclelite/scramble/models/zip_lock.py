from django.db import models
from scramble.models.active_url import ActiveURL

# Create your models here.

class ZipLock(models.Model):
    active = models.OneToOneField(ActiveURL,
                                  on_delete=models.CASCADE,
                                  primary_key=True)
    zipcode = models.CharField(default=0, max_length=255)

    def __str__(self):
        return self.active.url + "_ZL"

    def set_zipcode(self, code):
        '''
            Expected a code in string format
        '''
        print("setting zipcode to " + code)
        self.zipcode = code

    def get_zipcode(self):
        return self.zipcode
