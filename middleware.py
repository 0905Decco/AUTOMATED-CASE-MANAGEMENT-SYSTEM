from django.shortcuts import redirect
from django.conf import settings

class EnsureAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the path starts with /dashboard/ and the user is not authenticated
        if request.path.startswith('/dashboard/') and not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
