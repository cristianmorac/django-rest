from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.settings import api_settings
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    ''' Crear nuevo usuario en el sistema '''
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    ''' Crear un nuevo auth token para usuario '''
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManagerUserView(generics.RetrieveUpdateAPIView):
    ''' Manejar el usuario autenticado '''
    serializer_class = UserSerializer
    # Autenticacion 
    authentication_classes = (authentication.TokenAuthentication,)
    # Permisos
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        ''' Obtener y retornar ususario auternticado '''
        return self.request.user


