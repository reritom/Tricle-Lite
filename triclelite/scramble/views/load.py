from scramble.tools.response_tools import response_ko, response_ok
from scramble.helpers.scrambler.manager import ScramblerManager
from scramble.tools.validation.decorators import validate_url
from scramble.models.active_url import ActiveURL

@validate_url
def load(request, url):
    '''
        This method processes the files.
    '''
    print("In LOAD")

    url_obj = ActiveURL.objects.get(url=url)

    if url_obj.is_processed():
        return response_ko("Already loaded")

    #process files
    print("At Manager")
    url_obj.set_start()
    with ScramblerManager(url) as manager:
        manager.run()
    url_obj.set_end()

    url_obj.processed = True
    url_obj.save()

    return response_ok({"url":url})
