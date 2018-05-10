from scramble.tools.response_tools import response_ko, response_ok
from scramble.core.manager import ScramblerManager
from scramble.tools.validation.decorators import validate_url
from scramble.models.active_url import ActiveURL

@validate_url
def load(request, url):
    '''
        This method processes the files.
        This gets AJAX-ed straight after the post
    '''

    urlobj = ActiveURL.objects.get(url=url)

    if urlobj.is_processed():
        return response_ko("Already loaded")

    #process files
    print("At Manager")
    with ScramblerManager(url) as manager:
        manager.run()

    return response_ok({"url":url})
