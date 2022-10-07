from rest_framework.views import exception_handler
def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError': handle_generic_error,
        'Http404': handle_generic_error,
        'PermissionDenied': handle_generic_error,
        'NotAuthenticated': handle_authentication_error,
    }

    response = exception_handler(exc, context)

    if response is not None:
        if "AuthUserAPIView" in str(context['view']) and exc.status_code == 401:
            response.status_code = 200
            response.data = {'is_logged_in': False, 'status_code': 200}

            return response
        response.data['status_code'] = response.status_code

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response



def handle_authentication_error(exc, context, response):
    response.data = {
        'error': 'Please login to proceed',
        'status_code' : response.status_code
    }

    return response

def handle_generic_error(exc, context, response):
    return response