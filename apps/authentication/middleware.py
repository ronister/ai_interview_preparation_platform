from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForAPIMiddleware(MiddlewareMixin):
    """
    Middleware to disable CSRF protection for API endpoints.
    API authentication is handled by JWT tokens which are not vulnerable to CSRF.
    """
    def process_request(self, request):
        # Disable CSRF for all /api/ endpoints
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None


class ClearSessionForAPIMiddleware(MiddlewareMixin):
    """
    Middleware to ensure API endpoints use JWT authentication only.
    This prevents session authentication from interfering with JWT auth.
    """
    def process_request(self, request):
        # For API endpoints, clear any session-based user to ensure JWT takes precedence
        if request.path.startswith('/api/'):
            # Save the session key for logging
            session_key = getattr(request.session, 'session_key', None) if hasattr(request, 'session') else None
            
            # Set user to anonymous to force JWT authentication
            request.user = AnonymousUser()
            
            # Log if we're overriding a session user
            if session_key and hasattr(request, 'session') and '_auth_user_id' in request.session:
                import logging
                logger = logging.getLogger(__name__)
                logger.debug(f"[ClearSessionForAPIMiddleware] Cleared session user for API endpoint: {request.path}")
        
        return None 