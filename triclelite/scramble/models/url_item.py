from django.db import models
from scramble.models.active_url import ActiveURL

from datetime import datetime, timedelta
from django.utils import timezone
import uuid

# Create your models here.

class UrlItem(models.Model):
    '''
        This exists only for the lifespan of an ActiveURL
        The relevent data gets put in an ImageDataStore model when this is deleted
    '''
    active = models.ForeignKey(ActiveURL,
                               on_delete=models.CASCADE)

    id = models.CharField(default=str(uuid.uuid4()).replace('-',''), max_length=255, primary_key=True)

    file_name = models.CharField(default=0, max_length=255)
    file_type = models.CharField(default=0, max_length=255)
    file_size = models.IntegerField(default=0)
    file_path = models.CharField(default=0, max_length=255)

    processed = models.BooleanField(default=False)
    process_start = models.DateTimeField(default=timezone.now, null=True)
    process_end = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.active.url + "_" + self.file_name

    def set_file_path(self, file_path):
        self.file_path = file_path
        self.save()

    def get_file_path(self):
        return self.file_path

    @classmethod
    def create_url_item_uuid(cls):
        this_uuid = str(uuid.uuid4()).replace('-','')

        if UrlItem.objects.filter(id=this_uuid).exists():
            return create_url_item_uuid()
        else:
            return this_uuid

    def set_processed(self):
        self.processed = True
        self.save()

    def get_processed(self):
        return self.processed

    def set_process_start(self):
        print("Setting start time as {0} for {1}".format(timezone.now, self.file_name))
        self.process_start = timezone.now()
        self.save()

    def set_process_end(self):
        print("Setting end time as {0} for {1}".format(timezone.now, self.file_name))
        self.process_end = timezone.now()
        self.save()

    def get_process_duration(self):
        return self.process_end - self.process_start

    def set_file_size(self, file_size):
        self.file_size = file_size
        self.save()

    def get_file_size(self):
        return self.file_size

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.save()

    def get_file_name(self):
        return self.file_name

    def set_file_type(self, file_type):
        self.file_type = file_type
        self.save()

    def get_file_type(self):
        return self.file_type
