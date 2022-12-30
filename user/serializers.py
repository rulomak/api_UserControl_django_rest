from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    ''' serializador para el objeto de usuarios '''

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwatgs = {'password':{'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        ''' crear nuevo usuario con clave encriptada y retornarlo'''
        