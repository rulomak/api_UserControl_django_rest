from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# valor constante  
CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    ''' Testea Api publica de usuario '''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        ''' probar crear usuario con un payload exitoso '''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)  # optenemos los datos del usuario 
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data) # que no estemos pasando el password en la data  



    def test_user_exists(self):
        ''' probar crear usuario que ya existe '''
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        ''' la contraseña debe ser mayor a 5 caracteres '''
        payload = {
            'email': 'test@gmail.com',
            'password': 'po',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

