import uuid, os
from django.conf import settings
from scramble.models.active_url import ActiveURL
from scramble.models.expired_url import ExpiredURL
from scramble.models.url_item import UrlItem
from scramble.models.image_data_store import ImageDataStore
from scramble.tools import media_tools

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

def validate_url_in_expired(url):
    '''
        This function returns true if the url is in the db
        :returns: Bool
    '''
    return ExpiredURL.objects.filter(url=url).exists()

def validate_url_not_expired(url):
    '''
        This function returns true if the url is in the db and isnt expired
        :returns: Bool
    '''
    if validate_url_in_db(url) and not ActiveURL.objects.get(url=url).get_expired():
        return True
    else:
        return False


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
    expired_url, created = ExpiredURL.objects.get_or_create(url=url_obj.get_url())
    if created:
        expired_url.created = url_obj.created
        expired_url.number_of_files = url_obj.number_of_files
        expired_url.mode = url_obj.mode
        expired_url.duration = url_obj.get_duration().seconds
        expired_url.save()

        # Transfer the url items to image data stores
        for url_item in UrlItem.objects.filter(active=url_obj):
            image_data_store = ImageDataStore.objects.create(file_type=url_item.get_file_type(),
                                                             file_size=url_item.get_file_size(),
                                                             file_name=url_item.get_file_name(),
                                                             process_time=url_item.get_process_duration().seconds,
                                                             predicted_time=url_item.get_predicted_time(),
                                                             related_url=url_obj.get_url(),
                                                             mode=url_obj.get_mode(),
                                                             id=ImageDataStore.generate_id())

    url_obj.delete()

    media_tools.delete_dir(url)
