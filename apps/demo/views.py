from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import login

from pydantic import ValidationError

from django_ai_assistant.api.schemas import (
    ThreadIn,
    ThreadMessageIn,
)
from django_ai_assistant.helpers.use_cases import (
    create_message,
    create_thread,
    get_thread_messages,
    get_threads,
)
from django_ai_assistant.models import Thread

from apps.rag.ai_assistants import DjangoDocsAssistant


class HybridAuthMixin:
    """
    Mixin that allows both session and JWT authentication for views.
    This is useful for HTMX views that can be accessed from both
    Django templates (session auth) and React app (JWT auth).
    """
    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated via session
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        # Try JWT authentication
        jwt_auth = JWTAuthentication()
        try:
            auth_result = jwt_auth.authenticate(request)
            if auth_result:
                request.user = auth_result[0]
                request.auth = auth_result[1]
                return super().dispatch(request, *args, **kwargs)
        except Exception:
            pass
        
        # If neither authentication method works, redirect to login
        return redirect(f'/login?next={request.path}')


def react_index(request, **kwargs):
    return render(request, "demo/react_index.html")


class BaseAIAssistantView(HybridAuthMixin, TemplateView):
    def get_assistant_id(self, **kwargs):
        """Returns the DjangoDocsAssistant. Replace this with your own logic."""
        return DjangoDocsAssistant.id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        threads = list(get_threads(user=self.request.user))
        context.update(
            {
                "assistant_id": self.get_assistant_id(**kwargs),
                "threads": threads,
            }
        )
        return context


class AIAssistantChatHomeView(BaseAIAssistantView):
    template_name = "demo/chat_home.html"

    # POST to create thread:
    def post(self, request, *args, **kwargs):
        try:
            thread_data = ThreadIn(**request.POST)
        except ValidationError:
            messages.error(request, "Invalid thread data")
            return redirect("chat_home")

        thread = create_thread(
            name=thread_data.name,
            user=request.user,
            request=request,
        )
        return redirect("chat_thread", thread_id=thread.id)


class AIAssistantChatThreadView(BaseAIAssistantView):
    template_name = "demo/chat_thread.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread_id = self.kwargs["thread_id"]
        thread = get_object_or_404(Thread, id=thread_id)

        thread_messages = get_thread_messages(
            thread=thread,
            user=self.request.user,
            request=self.request,
        )
        context.update(
            {
                "thread_id": self.kwargs["thread_id"],
                "thread_messages": thread_messages,
            }
        )
        return context

    # POST to create message:
    def post(self, request, *args, **kwargs):
        assistant_id = self.get_assistant_id()
        thread_id = self.kwargs["thread_id"]
        thread = get_object_or_404(Thread, id=thread_id)

        try:
            message = ThreadMessageIn(
                assistant_id=assistant_id,
                content=request.POST.get("content") or None,
            )
        except ValidationError:
            messages.error(request, "Invalid message data")
            return redirect("chat_thread", thread_id=thread_id)

        create_message(
            assistant_id=assistant_id,
            thread=thread,
            user=request.user,
            content=message.content,
            request=request,
        )
        return redirect("chat_thread", thread_id=thread_id)

@api_view(['GET'])
def debug_auth(request):
    """Debug endpoint to check authentication status"""
    return Response({
        'user': str(request.user),
        'is_authenticated': request.user.is_authenticated,
        'auth_header': request.META.get('HTTP_AUTHORIZATION', 'None'),
        'session_key': request.session.session_key if hasattr(request, 'session') else 'No session',
        'has_jwt_auth': hasattr(request, 'auth') and request.auth is not None,
        'path': request.path,
    })

@api_view(['POST'])
def create_session_from_jwt(request):
    """
    Create a Django session from JWT token.
    This allows React app users to access HTMX views that require session auth.
    """
    jwt_auth = JWTAuthentication()
    try:
        auth_result = jwt_auth.authenticate(request)
        if auth_result:
            user, token = auth_result
            # Create a session for the user
            login(request, user)
            return Response({
                'success': True,
                'message': 'Session created successfully',
                'redirect_url': '/htmx/'
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid or missing JWT token'
            }, status=401)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Authentication failed: {str(e)}'
        }, status=401)