# django Imports

# Third Party Imports
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# Locale Imports
from .serializers import ObtainPairTokenSerializer

class JWTLoginView(TokenObtainPairView):
    """
    Custom LoginView for API JWT authentication.
    """
    serializer_class=ObtainPairTokenSerializer

class JWTRefreshView(TokenRefreshView):
    pass

class JWTVerifyView(TokenVerifyView):
    pass