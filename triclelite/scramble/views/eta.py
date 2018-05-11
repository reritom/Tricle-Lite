from scramble.tools.response_tools import response_ok

def eta(request):
    return response_ok({'type':"estimate/actual", 'estimate':"in seconds"})
