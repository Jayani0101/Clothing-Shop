from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class DisableCSRF(MiddlewareMixin):
    """Disable CSRF verification only when DEBUG = True (development only)"""
    def process_request(self, request):
        if settings.DEBUG:
            setattr(request, '_dont_enforce_csrf_checks', True)
