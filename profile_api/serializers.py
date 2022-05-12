from rest_framework import serializers

#import models profile
from profile_api import models

class HelloSerializer(serializers.Serializer):
    """Serializa un campo para probar nuestra APIView"""
    name = serializers.CharField(max_length=100)

#class para serializar un modelo
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializa el objeto de un perfil de un usuario"""
    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password')
        #proteger la clave de visualizacion
        extra_kwargs = {
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }

    #sobreescribir una función
    def create(self,validated_data):
        """Crear y retornar nuevo usuario"""

        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password=validated_data['password']
        )
        return user
    
    #Actualizar la clave del usuario
    def update(self, instance,validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        return super().update(instance,validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    ''' Serializador de profile feed items '''
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id','user_profile','status_text','created_on')
        ''' Campos que se van a serializar '''
        extra_kwargs = {'user_profile': {'read_only':True}}
        

