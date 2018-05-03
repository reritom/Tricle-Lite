import uuid, os
from django.conf import settings
from scramble.models import ActiveURL, ExpiredURL
from scramble.tools import mediaTools

def validate_url_request(url):
    '''
        This receives a url and validates that it exists in /media and the db
        If it doesn't exist in db, continue validation but return error
        If it doesn't exist in /media, return error
    '''
    return validate_url_in_db(url) and url_in_media(url)

def validate_url_in_db(url):
    '''
        This function returns true if the url is in the db
        :returns: Bool
    '''
    return ActiveURL.objects.filter(url=url).exists()


def url_in_media(url):
    '''
        This function returns true if the url is in media
        :returns: Bool
    '''
    # This assumes that the 'temp' directory exists
    return url in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp'))


def get_url_status(url):
    '''
        This function returns whether the url is still active or not
        :returns: Bool
    '''
    # Check timeout, if expired, delete transaction, move it to expired
    return ActiveURL.objects.filter(url=url).getStatus()

def expire_url(url):
    '''
        This method deletes the active transaction object
        and creates an expired object
    '''
    url_obj = ActiveURL.objects.get(url=url)
    mediaTools.delete_dir(url)
    expired_url, created = ExpiredURL.objects.get_or_create(url=url_obj.get_url())
    if created:
        expired_url.created = url_obj.created
        expired_url.number_of_files = url_obj.number_of_files
        expired_url.mode = url_obj.mode
        expired_url.save()
    url_obj.delete()
