from django.db import models
'''
AbstractBaseUser = creando un usuario
BaseUserManager = Creación del manager del usuario
PermissionsMixin = permisos del usuario

'''
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

'''imagenes'''
import uuid
import os

def recipe_image_file_path(instance,filename):
    '''Genera path para imagenes'''
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/',filename)



class UserManager(BaseUserManager):

    ''' si se requiere otro campo estara en **extra_fields'''

    def create_user(self,email,password=None,**extra_fields):
        ''' Crea y guarda un nuevo usuario normal'''

        #validar que el usuario coloque un email
        if not email:
            raise ValueError('El usuario debe tener un email')

        #para colocar todo en minusculas self.normalize_email
        user = self.model(email=self.normalize_email(email), **extra_fields)
        #Contraseña hasheada
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        ''' Crear un super usuario '''
        user = self.create_user(email,password)
        user.is_staff= True
        user.is_superuser= True
        user.save(using=self._db)

        return user

class user(AbstractBaseUser,PermissionsMixin):
    ''' Modelo personalizado de usuario que soporta hacer login con email en vez de usuario '''
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # Con que campo nos vamos a loguear
    USERNAME_FIELD = 'email'

class Tag(models.Model):
    ''' Modelo del Tag para la receta '''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        # esta al final de settings
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    ''' Modelo de Ingredentes para usarse en la receta '''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        # esta al final de settings
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Recipe(models.Model):
    '''Receta objeto'''
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True,upload_to=recipe_image_file_path)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255,blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
