from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)


class JWTOnlyAuthentication(JWTAuthentication):
    """
    JWT-only authentication for API endpoints.
    Simple and clean - no session fallbacks.
    """
    
    def authenticate(self, request):
        logger.debug(f"[JWTOnlyAuthentication] Authenticating request to {request.path}")
        
        # Get the JWT token from the Authorization header
        header = self.get_header(request)
        if header is None:
            logger.debug(f"[JWTOnlyAuthentication] No Authorization header found")
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            logger.debug(f"[JWTOnlyAuthentication] No valid token in header")
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        
        logger.info(f"[JWTOnlyAuthentication] Authenticated user: {user.username} (ID: {user.id})")
        
        return (user, validated_token) 


class HybridAuthentication(JWTAuthentication):
    """
    Hybrid authentication for django-ai-assistant endpoints.
    Tries JWT first, then session auth for non-API endpoints only.
    """
    
    def authenticate(self, request):
        logger.debug(f"[HybridAuthentication] Authenticating request to {request.path}")
        
        # First try JWT authentication
        try:
            jwt_result = super().authenticate(request)
            if jwt_result:
                user, token = jwt_result
                logger.info(f"[HybridAuthentication] JWT authenticated user: {user.username}")
                return jwt_result
        except AuthenticationFailed:
            logger.debug(f"[HybridAuthentication] JWT auth failed for path: {request.path}")
        except Exception as e:
            logger.error(f"[HybridAuthentication] JWT auth error: {e}")
        
        # Fall back to session auth for non-API endpoints only
        if not request.path.startswith('/api/'):
            try:
                session_auth = SessionAuthentication()
                session_result = session_auth.authenticate(request)
                if session_result:
                    user, auth = session_result
                    logger.info(f"[HybridAuthentication] Session authenticated user: {user.username}")
                    return session_result
            except Exception as e:
                logger.error(f"[HybridAuthentication] Session auth error: {e}")
        
        return None 