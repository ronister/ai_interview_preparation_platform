from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .authentication import JWTOnlyAuthentication
import logging

logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            
            return Response({
                'user': user_serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user and blacklist their JWT token"""
    logger.info(f"[logout_view] Logging out user: {request.user.username}")
    
    try:
        # Get the refresh token from request body
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            logger.info(f"[logout_view] Blacklisting refresh token")
            token = RefreshToken(refresh_token)
            token.blacklist()
        else:
            logger.warning(f"[logout_view] No refresh token provided")
        
        logger.info(f"[logout_view] Logout completed for user: {request.user.username}")
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        logger.error(f"[logout_view] Error during logout: {str(e)}")
        return Response({'error': 'Logout failed'}, status=400)


@api_view(['GET'])
@authentication_classes([JWTOnlyAuthentication])
@permission_classes([IsAuthenticated])
@never_cache
def user_profile_view(request):
    """Get current user profile"""
    logger.info(f"[user_profile_view] Request user: {request.user.username}")
    
    serializer = UserSerializer(request.user)
    response_data = serializer.data
    
    response = Response(response_data)
    # Add cache control headers to prevent browser caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    try:
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        return Response({
            'access': str(token.access_token),
            'refresh': str(token),
        })
    except Exception as e:
        return Response(
            {'error': 'Invalid refresh token'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token_view(request):
    """Verify if an access token is still valid"""
    try:
        token = request.data.get('token')
        if not token:
            return Response(
                {'valid': False, 'error': 'No token provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to decode and validate the token
        try:
            access_token = AccessToken(token)
            # Token is valid
            return Response({
                'valid': True,
                'user_id': access_token['user_id'],
                'exp': access_token['exp'],
                'token_type': access_token['token_type']
            })
        except TokenError as e:
            return Response({
                'valid': False,
                'error': str(e)
            })
            
    except Exception as e:
        return Response(
            {'valid': False, 'error': 'Invalid token'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
