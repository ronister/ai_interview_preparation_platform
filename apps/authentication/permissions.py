from rest_framework import permissions


class IsAuthenticatedForAIAssistant(permissions.BasePermission):
    """
    Custom permission to allow authenticated users to access AI Assistant endpoints
    """
    def has_permission(self, request, view):
        # Allow OPTIONS requests for CORS
        if request.method == 'OPTIONS':
            return True
        
        # Require authentication for all other requests
        return request.user and request.user.is_authenticated 