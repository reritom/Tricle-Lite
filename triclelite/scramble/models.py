from django.db import models
from django.utils import timezone
from django.conf import settings

from datetime import datetime, timedelta
import uuid
# Create your models here.

class ActiveURL(models.Model):
    url = models.CharField(default=0, max_length=255, unique=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    expired = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    number_of_files = models.IntegerField(default=0)
    mode = models.CharField(default="Scramble", max_length=255)
    down_count = models.IntegerField(default=0)

    def __str__(self):
        return self.url

    def get_status(self):
        return self.expired

    def validate(self):
        return self.expired

    def is_processed(self):
        print("Getting processed status")
        return self.processed

    def set_processed(self):
        print("Setting urlobj to processed")
        self.processed = True
        self.save()

    def is_expired(self):
        expiration = self.get_expiration()
        if timezone.now() > expiration:
            self.expired = True
            return self.expired

    def get_expiration(self):
        return self.created + timedelta(minutes=settings.EXPIRATION_TIME_LIMIT)

    def is_downloadable(self):
        return self.down_count <= settings.DOWNLOAD_LIMIT

    def inc_down_count(self):
        self.down_count += 1

        if not self.is_downloadable():
            self.expired = True

        self.save()

    def generate_url(self):
        new_url = str(uuid.uuid4()).replace('-','')

        if ActiveURL.objects.filter(url=new_url).exists() or ExpiredURL.objects.filter(url=new_url).exists():
            return generate_url()
        else:
            self.url = new_url
            self.save()
            return self.url

    def get_url(self):
        if self.url != 0:
            return self.url
        else:
            return self.generate_url()

    def increment_count(self):
        self.number_of_files +=1
        self.save()
        return

class ExpiredURL(models.Model):
    url = models.CharField(default=0, max_length=255, unique=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    number_of_files = models.IntegerField(default=0)
    mode = models.CharField(default="Scramble", max_length=255)

    def __str__(self):
        return self.url

class KeyChain(models.Model):
    active = models.OneToOneField(ActiveURL,
                                  on_delete=models.CASCADE,
                                  primary_key=True)
    key_one = models.CharField(default=0, max_length=255)
    key_two = models.CharField(default=0, max_length=255)
    key_three = models.CharField(default=0, max_length=255)

    def __str__(self):
        return self.active.url + "_KC"

    def setKeys(self, keys):
        '''
            This method sets the keys, expected in a list format
        '''
        key_one = keys[0]
        key_two = keys[1]
        key_three = keys[2]

    def getKeys(self):
        return [self.key_one, self.key_two, self.key_three]

class ZipLock(models.Model):
    active = models.OneToOneField(ActiveURL,
                                  on_delete=models.CASCADE,
                                  primary_key=True)
    zipcode = models.CharField(default=0, max_length=255)

    def __str__(self):
        return self.active.url + "_ZL"

    def setZipcode(self, code):
        '''
            Expected a code in string format
        '''
        print("setting zipcode to " + code)
        self.zipcode = code

    def getZipcode(self):
        return self.zipcode
