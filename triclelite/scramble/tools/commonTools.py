def show_request(request):
    '''
        This method prints the request data and images. Only to be used in local
    '''

    print("data: " + str(request.POST))

    print(request.FILES)
