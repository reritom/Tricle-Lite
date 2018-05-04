from django.db import models
from scramble.models.active_url import ActiveURL

# Create your models here.

class KeyChain(models.Model):
    active = models.OneToOneField(ActiveURL,
                                  on_delete=models.CASCADE,
                                  primary_key=True)
    key_one = models.CharField(default=0, max_length=255)
    key_two = models.CharField(default=0, max_length=255)
    key_three = models.CharField(default=0, max_length=255)

    def __str__(self):
        return self.active.url + "_KC"

    def set_keys(self, keys):
        '''
            This method sets the keys, expected in a list format
        '''
        print("Setting KeyChain keys")
        self.key_one = keys[0]
        self.key_two = keys[1]
        self.key_three = keys[2]
        self.save()

    def get_keys(self):
        return [self.key_one, self.key_two, self.key_three]
