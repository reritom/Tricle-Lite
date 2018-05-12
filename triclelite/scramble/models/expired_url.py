from django.db import models
from django.utils import timezone
# Create your models here.

class ExpiredURL(models.Model):
    url = models.CharField(default=0, max_length=255, unique=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    number_of_files = models.IntegerField(default=0)
    mode = models.CharField(default="Scramble", max_length=255)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.url
