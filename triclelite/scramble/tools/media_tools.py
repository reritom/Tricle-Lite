'''
    This module contains tools for dealing with the Media directory
'''
import os, shutil
from scramble.models.active_url import ActiveURL
from scramble.models.expired_url import ExpiredURL
from django.conf import settings

def get_media_path(url):
    return os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)

def get_base_media_path():
    return os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp')

def delete_temp():
    media = get_base_media_path()
    shutil.rmtree(media)

def delete_dir(url):
    '''
        This method checks if the url dir is present
        and deletes it if it is.
    '''
    if 'scramble' in os.listdir(settings.MEDIA_ROOT):
        if 'temp' in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble')):
            if url in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp')):
                url_dir = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)
                shutil.rmtree(url_dir)

def make_dir(url):
    '''
        This method makes a directory for a url
    '''
    if not 'scramble' in os.listdir(settings.MEDIA_ROOT):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'scramble'))

    if not 'temp' in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble')):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp'))

    if not url in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp')):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url))

    media_path = os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp', url)

    return media_path

def delete_file(name):
    '''
        This method deletes a file.
    '''
    os.remove(name)
