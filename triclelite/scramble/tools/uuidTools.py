import uuid, os
from django.conf import settings
from scramble.models import ActiveURL, ExpiredURL
from scramble.tools import mediaTools

def validate_uuid_request(uuid):
    '''
        This receives a uuid and validates that it exists in /media and the db
        If it doesn't exist in db, continue validation but return error
        If it doesn't exist in /media, return error
    '''
    return validate_uuid_in_db(uuid) and validate_uuid_in_media(uuid)

def generate_uuid():
    '''
        This function generates a uuid and validates that it doesnt already exist
        :returns: String
    '''
    new_uuid = str(uuid.uuid4()).replace('-','')

    if ActiveURL.objects.filter(uuid=new_uuid).exists() or ExpiredURL.objects.filter(uuid=new_uuid).exists():
        return generate_uuid()
    else:
        return new_uuid


def validate_uuid_in_db(uuid):
    '''
        This function returns true if the uuid is in the db
        :returns: Bool
    '''
    return ActiveURL.objects.filter(uuid=uuid).exists()


def validate_uuid_in_media(uuid):
    '''
        This function returns true if the uuid is in media
        :returns: Bool
    '''
    # This assumes that the 'temp' directory exists
    return uuid in os.listdir(os.path.join(settings.MEDIA_ROOT, 'scramble', 'temp'))


def get_uuid_status(uuid):
    '''
        This function returns whether the uuid is still active or not
        :returns: Bool
    '''
    # Check timeout, if expired, delete transaction, move it to expired
    return ActiveURL.objects.filter(uuid=uuid).getStatus()

def expire_uuid_in_db(uuid):
    '''
        This method deletes the active transaction object
        and creates an expired object
    '''
    uuid_obj = ActiveURL.objects.get(uuid=uuid)
    expired_uuid, created = ExpiredURL.objects.get_or_create(uuid=uuid_obj.uuid)
    if created:
        expired_uuid.created = uuid_obj.created
        expired_uuid.number_of_files = uuid_obj.number_of_files
        expired_uuid.mode = uuid_obj.mode
        expired_uuid.save()
    uuid_obj.delete()
