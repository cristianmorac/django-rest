'''testeo de configuraciones '''
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models

def sample_user(email='prueba@gmail.com',password='testpass'):
    ''' Crear usuario de ejemplo '''
    return get_user_model().objects.create_user(email,password)

class model_test(TestCase):

    def test_create_user_with_email_successful(self):
        ''' Probrar creando un nuevo usuario con email correctamente '''
        email = 'test@datadosis.com'
        password = 'Testpass123'

        ''' definir que esten correctos los parametros del user '''
        user = get_user_model().objects.create_user(
            email = email,
            password = password)
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_mormalized(self):

        ''' test para normalizar la letra a minuscula '''
        email = 'test@Gmail.COM'
        user = get_user_model().objects.create_user(
            email,'Testprueba123'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):

        ''' Nuevo usuario email invalido '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'Testprueba123')

    def test_create_new_superuser(self):

        ''' probar superusuario creado '''
        email = 'test2@datadosis.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_superuser(

            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    # Pruebas de Tags
    def test_tag_str(self):
        ''' Probar representación en cadena de texto del tag '''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Meat'
        )

        self.assertEqual(str(tag),tag.name)

    def test_ingridients_str(self):
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Banana'
        )

        self.assertEqual(str(ingredient),ingredient.name)

    def test_recipe_str(self):
        '''Probar representacion en cadena de texto de las recetas'''
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe),recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self,mock_uuid):
        '''Probar que imagen ha sido guardada en lugar correcto'''
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None,'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
