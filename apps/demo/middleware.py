from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.models import AnonymousUser


class DjangoAIAssistantAuthMiddleware(MiddlewareMixin):
    """
    Middleware to handle authentication for django-ai-assistant endpoints
    """
    def process_request(self, request):
        # Skip authentication for logout endpoint
        if request.path == '/api/auth/logout/':
            print(f"[DjangoAIAssistantAuthMiddleware] Skipping auth for logout endpoint")
            return
            
        # Only process AI assistant endpoints
        if request.path.startswith('/ai-assistant/'):
            # Try JWT authentication first
            jwt_auth = JWTAuthentication()
            try:
                auth_result = jwt_auth.authenticate(request)
                if auth_result:
                    request.user = auth_result[0]
                    request.auth = auth_result[1]
                    print(f"[DjangoAIAssistantAuthMiddleware] JWT auth successful for user: {request.user}")
                    return
            except Exception as e:
                print(f"[DjangoAIAssistantAuthMiddleware] JWT auth failed: {e}")
            
            # Fall back to session authentication
            session_auth = SessionAuthentication()
            try:
                auth_result = session_auth.authenticate(request)
                if auth_result:
                    request.user = auth_result[0]
                    request.auth = auth_result[1]
                    print(f"[DjangoAIAssistantAuthMiddleware] Session auth successful for user: {request.user}")
                    return
            except Exception as e:
                print(f"[DjangoAIAssistantAuthMiddleware] Session auth failed: {e}")
            
            print(f"[DjangoAIAssistantAuthMiddleware] No authentication found for {request.path}")
            if not hasattr(request, 'user') or isinstance(request.user, AnonymousUser):
                print(f"[DjangoAIAssistantAuthMiddleware] User is anonymous") 