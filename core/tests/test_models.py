from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='raul@test.com', password='testpass123'):
    ''' crear usuario ejemplo'''
    return get_user_model().objects.create_user(email, password)



class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        ''' Probar crear un nuevo usuario con un email correctamente '''
        email = 'test@pepepe.ve'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        ''' testea email para nuevos usuario normalizado ( minusculas ) '''
        email = 'test@PRUEBA.coM'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email = email, 
            password = password
        )

        self.assertEqual(user.email, email.lower())
        

    def test_new_user_invalid_email(self):
        ''' nuevo usuario email invalido '''
        with self.assertRaises(ValueError):  # todo lo que corremos dentro de este codigo nos tendria que dar un error de valor, si no da error el test falla
             get_user_model().objects.create_user(None, 'Testpass458')

    def test_create_new_superuser(self):
        ''' Probar super usuario creado '''
        email = 'test@pepepe.ve'
        password = 'TestPass123'
        user = get_user_model().objects.create_superuser(
            email = email,
            password = password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)



    def test_tag_str(self):
        ''' probar representacion en cadena de texto del tag '''
        tag = models.Tag.objects.create(
            user= sample_user(),
            name= 'nombre' 
        )

        self.assertEqual(str(tag), tag.name)

