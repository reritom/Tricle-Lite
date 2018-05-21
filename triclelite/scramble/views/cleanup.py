from scramble.models.active_url import ActiveURL
from scramble.tools import url_tools, media_tools
from scramble.tools.response_tools import response_ok
from scramble.tools.validation.decorators import superuser_only

def cleanup(request):
    '''
        This method checks all active urls and expires accordingly.
    '''

    expired_count = 0

    for url_obj in ActiveURL.objects.all():
        if url_obj.is_expired():
            url_tools.expire_url(url_obj.get_url())
            expired_count += 1

    return response_ok({'message': "{0} successfully removed in cleanup".format(expired_count)})
