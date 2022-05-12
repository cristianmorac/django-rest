from django.db import models
''' Utilizar los settings del proyecto '''
from django.conf import settings

#modulo de django que se sobreescribe
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Manager para perfil de usuarios"""
    
    def create_user(self,email,name,password=None):
        '''Crear nuevo User Profile'''

        if not email:
            raise ValueError('Usuario debe tener un Email')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Modelo base de datos para usuarios en el sistema
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        '''Obtener nombre completo'''
        return self.name

    def get_short_name(self):
        '''obtener nombre corto'''
        return self.name

    def __str__(self):
        '''Retornar cadena Representando nuestro email'''
        return self.email

class ProfileFeedItem(models.Model):
    ''' Perfil de status update '''
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text
    
