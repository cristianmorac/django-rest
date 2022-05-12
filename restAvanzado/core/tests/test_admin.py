from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTest(TestCase):
    def setUp(self):
        self.client=Client()

        #Usuario admin
        self.admin_user=get_user_model().objects.create_superuser(
            email= 'admin@gmail.com',
            password = 'Testpass123'
        )
        #Usuario administrador siempre haga login
        self.client.force_login(self.admin_user)

        # usuario normal
        self.user = get_user_model().objects.create_user(
            email= 'user@gmail.com',
            password = 'Testpass123',
            name ='pruebas de string'
        )

    def test_users_listed(self):
        ''' Testear que los usuarios han sido enlistados en la página de usuarios '''

        #Generar la url
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res,self.user.name)
        self.assertContains(res,self.user.email)


    def test_user_change_page(self):
        ''' Prueba que la pagina editada por el usuario funciona '''
        url = reverse('admin:core_user_change',args=[self.user.id])
        #url /admin/core/user/id
        res = self.client.get(url)
        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        ''' Testear que la página de crear usuarios funciona '''
        url =reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)
