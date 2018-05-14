from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta
import uuid

class ImageDataStore(models.Model):
    id = models.CharField(default=str(uuid.uuid4()).replace('-',''), max_length=255, primary_key=True)
    file_type = models.CharField(default=0, max_length=255)
    file_size = models.IntegerField(default=0)
    file_name = models.CharField(default=0, max_length=255)
    related_url = models.CharField(default=0, max_length=255)
    mode = models.CharField(default=0, max_length=255)

    # In seconds
    process_time = models.IntegerField(default=0)

    # Predicted
    predicted_time = models.IntegerField(default=0)

    # Used for indexing in estimation predictions
    created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.related_url + "_" + self.file_name

    @staticmethod
    def generate_id():
        this_id = str(uuid.uuid4()).replace('-','')

        if ImageDataStore.objects.filter(id=this_id).exists():
            return ImageDataStore.generate_id()
        else:
            return this_id

    def set_related_url(self, url):
        self.related_url = url
        self.save()

    def set_file_size(self, file_size):
        self.file_size = file_size
        self.save()

    def set_file_type(self, file_type):
        self.file_type = file_type
        self.save()

    def set_file_name(self, name):
        self.file_name = name
        self.save()

    def set_process_time(self, time):
        self.process_time = time
        self.save()

    def set_predicted_time(self, time):
        self.predicted_time = time
        self.save()
