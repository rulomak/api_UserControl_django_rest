from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@gmail.com',
            password = 'Testpass999'
        )
        self.client.force_login(self.admin_user) # asi hacemos que el usuario admin siempre haga login  


        self.user = get_user_model().objects.create_user(
            email = 'testuser@gmail.com',
            password = 'pass1236T',
            name = 'Test Nombre '
        )

    def test_users_listed(self):
        ''' testear que los usuarios han sido enlistados en la  pagina de usuario '''
        url = reverse('admin:core_user_changelist') # genera el url para la lista de usuarios que tenemos / reverse se encarga de generarla   
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)


    def test_user_change_page(self):
        ''' prueba que la pagina editada por el usuario funciona '''
        url = reverse('admin:core_user_change', args=[self.user.id])
        # admin/core/user/id=5   ejemplo como se veria la ruta
        res = self.client.get(url) # respuesta

        self.assertEqual(res.status_code, 200)  


    def test_create_user_page(self):
        ''' Testear que la pagina de Crear usuario Funciona '''
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


        