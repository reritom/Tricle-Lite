from scramble.models.active_url import ActiveURL
from scramble.tools import url_tools, media_tools
from scramble.tools.response_tools import response_ok
from scramble.tools.validation.decorators import superuser_only

@superuser_only
def hard(request):
    '''
        This request expires all active urls and deletes all url temporary files.
        It can only be performed by a superuser
    '''
    all_urls = ActiveURL.objects.all()

    for url_obj in all_urls:
        url = url_obj.get_url()
        url_tools.expire_url(url)

    media_tools.delete_temp()

    return response_ok({'hard':"OK"})
