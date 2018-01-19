'''
    This module contains tools for dealing with the Media directory
'''
import os, shutil
from scramble.models import ActiveURL, ExpiredURL
from django.conf import settings

def delete_dir(uuid):
    '''
        This method checks if the uuid dir is present
        and deletes it if it is.
    '''
    if 'scramble' in os.listdir(settings.MEDIA_ROOT):
        if 'temp' in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble')):
            if uuid in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp')):
                url_dir = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', uuid)
                shutil.rmtree(url_dir)

def make_dir(uuid):
    '''
        This method makes a directory for a uuid
    '''
    pass
