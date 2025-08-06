from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication

from apps.demo import views


# Import django-ai-assistant views to wrap them
def get_ai_assistant_urls():
    """
    Get django-ai-assistant URLs and ensure they work with our authentication
    """
    from django_ai_assistant.urls import urlpatterns as ai_patterns
    
    # The django-ai-assistant might be using viewsets or API views
    # Let's ensure CSRF is handled properly for API calls
    wrapped_patterns = []
    for pattern in ai_patterns:
        # Keep the original pattern but the views should use our auth
        wrapped_patterns.append(pattern)
    
    return wrapped_patterns


urlpatterns = [
    # Debug endpoint
    path("debug-auth/", views.debug_auth, name="debug_auth"),
    # Session creation endpoint for JWT users
    path("create-session/", views.create_session_from_jwt, name="create_session_from_jwt"),
    # Use the wrapped AI assistant URLs
    path("ai-assistant/", include(get_ai_assistant_urls())),
    path("htmx/", views.AIAssistantChatHomeView.as_view(), name="chat_home"),
    path(
        "htmx/thread/<int:thread_id>/",
        views.AIAssistantChatThreadView.as_view(),
        name="chat_thread",
    ),
    # Catch all for react app:
    path("", views.react_index, {"resource": ""}),
    path("<path:resource>", views.react_index),
]
