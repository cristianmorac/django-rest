from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**param):
    return get_user_model().objects.create_user(**param)

#Usuarios publicos
class PublicUserApiTest(TestCase):
    ''' Testear el api publico del usuario '''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_succes(self):
        ''' Probar crear usuario con payload exitoso '''
        payload = {
            'email':'test4@prueba.com',
            'password':'testpassword',
            'name':'testname1'
        }

        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # doble * pasar todos los parametros
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)
    
    def test_user_exists(self):
        ''' Probar crear un user que ya existe falla '''
        payload = {
            'email':'test5@prueba-com',
            'password':'testpassword',
            'name':'testname2',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        payload = {
            'email':'test6@prueba-com',
            'password':'pw',
            'name':'testname6',
        }

        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        ''' probar que el token sea creado para el usuario '''
        payload = {
            'email':'test@prueba.com',
            'password':'prueba021',
            'name':'testname1',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        ''' probar que el token no es creado con credenciales invalidas '''
        create_user(email='test@prueba.com',password='testprueba123')
        payload = {'email':'test@prueba.com','password':'12345678prueba'}
        res = self.client.post(TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        payload = {
            'name':'test@prueba.com',
            'password':'prueba021',
            'name':'testname1',
        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_token_missing_field(self):
        ''' probar que el email y contraseña sean requeridas '''
        res = self.client.post(TOKEN_URL,{'email':'one','password':''})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        ''' Prueba que la autenticación sea requerida para los usuarios '''
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    ''' Testear el API privado del usuario '''
    def setUp(self):
        self.user=create_user(
            email='prueba@gmail.com',
            password = 'testpass',
            name = 'name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_profile_success(self):
        ''' Probar obtener perfil para usuario con login '''
        res= self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name':self.user.name,
            'email':self.user.email,            
        })
    
    def test_post_me_not_allowed(self):
        ''' Prueba que el POST no sea permitido '''
        res = self.client.post(ME_URL,{})
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        
        payload = {'name':'new name','password':'testpasspass'}
        
        res = self.client.patch(ME_URL,payload)
        #actualizar la base de datos
        self.user.refresh_from_db()
        # Test de validación
        self.assertEqual(self.user.name,payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code,status.HTTP_200_OK)

