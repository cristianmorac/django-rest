from django.shortcuts import render
from profile_api import serializers, models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
''' realizar filtros '''
from rest_framework import filters

''' obtener tocken '''
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

''' **** '''
from rest_framework.permissions import IsAuthenticated

''' permisos de usuario '''
from rest_framework.authentication import TokenAuthentication

from profile_api import serializers, models, permissions

#importación viewset
from rest_framework import viewsets

class HellowApiView(APIView):
    """Api de prueba"""
    serializer_class = serializers.HelloSerializer
    def get(self,request, format=None):
        """Retornar lista de caracteristicas del APIView"""
        an_apiview = ['usamos motodos HTTP como (get,post,patch,put,delete)',
        'Es similar a una vista tradicional de django',
        'Nos da el mayor control sobre la logica de nuestra aplicación',
        'esta mapeado manualmente a las urls',]
            
        return Response({'message':'Hello','an_apiview':an_apiview})
    
    def post(self,request):
        """Crear un mensaje con nuestro nombre"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}'
            return Response({'message': message})
        
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST 
            )
    
    def put(self,request,pk=None):
        """Actualiza un objeto"""
        return Response({'method':'PUT'})
    
    def patch(self,request,pk=None):
        """Maneja Actualización parcial de un objeto"""
        return Response({'Method':'PATCH'})
    
    def delete(self,request,pk=None):
        """Borrar objetos"""
        return Response({'Method':'delete'})

class HelloViewSet(viewsets.ViewSet):

    """Test APi VIewset"""

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """Retornar mensaje"""
        a_viewset= [
            'Usa acciones (list,create,retrieve,update,partial_update',
            'Automaticamente mapea las urls usando router'
            'Provee mas funcionalidad con menos código'
        ]

        return Response({'message':'Hola','a_viewset':a_viewset})

    def create(self,request):
        """Crear nuevo mensaje"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'hello {name}'
            return Response({'message': message})
        
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST 
            )

    def retrieve(self,request,pk=None):
        '''Obtener un objeto y su ID'''

        return Response({'method':'GET'})
    
    def update(self,request,pk=None):
        '''Actualiza un objeto'''

        return Response({'method':'PUT'})
    
    def partial_update(self,request,pk=None):
        '''Actualiza parcialmente un objeto'''

        return Response({'method':'PACH'})
    
    def destroy(self,request,pk=None):
        '''Elimina un objeto'''

        return Response({'method':'delete'})



class UserProfileViewSet(viewsets.ModelViewSet):
    ''' crear y actualizar los usuarios a los modelos a traves de API '''
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    ''' Validar la autenticación del usuario '''
    authentication_classes = (TokenAuthentication,)
    permissions_classes = (permissions.UpdateOwnProfile,)
    ''' crear filtros '''
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class UserLoginApiView(ObtainAuthToken):
    ''' crear token de autenticación de usuario '''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    ''' Maneja el crear, leer, Actualizar el profile feed '''
    authentication_classes=(TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    ''' Visibilidad a las personas autenticadas '''
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    
    def perform_create(self, serializer):
        ''' Setear el perfil de usuario que esta logueado '''
        serializer.save(user_profile=self.request.user)


