def validate_uuid_request(uuid):
    '''
        This receives a uuid and validates that it exists in /media and the db
        If it doesn't exist in db, continue validation but return error
        If it doesn't exist in /media, return error
    '''
    validate_uuid_in_db(uuid)
    validate_uuid_in_media(uuid)
    get_uuid_status(uuid)
    pass

def generate_uuid():
    '''
        This function generates a uuid and validates that it doesnt already exist
        :returns: String
    '''
    pass

def validate_uuid_in_db(uuid):
    '''
        This function returns true if the uuid is in the db
        :returns: Bool
    '''
    pass

def validate_uuid_in_media(uuid):
    '''
        This function returns true if the uuid is in media
        :returns: Bool
    '''
    pass

def get_uuid_status(uuid):
    '''
        This function returns whether the uuid is still active or not
        :returns: Bool
    '''
    # Check timeout, if expired, delete transaction, move it to expired
    pass
