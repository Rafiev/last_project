

class MyMiddleware:

    def __init__(self, ger_response):
        self.get_response = ger_response

    def __call__(self, request):
        print('----HELLO-----')
        request.hello = 'My name is my name'
        response = self.get_response(request)
        return response