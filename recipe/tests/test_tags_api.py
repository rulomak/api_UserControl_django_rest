from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagApiTests(TestCase):
    ''' probar los api tag disponibles publicamente '''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        ''' prueba que login sea requerido para obtener los tags '''
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateTagsApiTests(TestCase):
    ''' probar los api tags disponibles privados  '''
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'raul@test.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """probar obtener tags"""
        Tag.objects.create(user=self.user, name='Meat')
        Tag.objects.create(user=self.user, name='Pepe')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, serializer.data)


    def test_tags_limited_to_user(self):
        ''' probar que los tags retornados sean del usuario '''
        user2 = get_user_model().objects.create_user(
            'otro@test.com',
            'otropass00'
        )
        Tag.objects.create(user=user2, name='trisme')
        tag =  Tag.objects.create(user=self.user, name='Coco a')

        res = self.client.get(TAGS_URL)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)
        self.assertEquals(res.data[0]['name'], tag.name)


    def test_create_tag_successful(self):
        ''' prueba creando nuevo tag'''
        payload = {'name': 'Simple'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
        
    def test_create_tag_invalid(self):
        ''' prueba crear un nuevo tag con un payload invalido '''
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)


