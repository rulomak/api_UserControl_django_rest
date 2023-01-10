from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    ''' serializador para el objeto de usuarios '''

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password':{'write_only': True, 'min_length': 5}}


    def create(self, validated_data):
        ''' crear nuevo usuario con clave encriptada y retornarlo'''
        return get_user_model().objects.create_user(**validated_data)


    def update(self, intance, validated_data):
        ''' Actualiza el usuario, configura el password correctamente y lo retorna  '''
        password = validated_data.pop('password', None) # optendra el password y luego de usarlo lo borra  
        user = super().update(intance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user




class AuthTokenSerializer(serializers.Serializer):
    ''' serializador para el objento de autenticacion del usuario '''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        ''' Validar y autenticar usuarios '''
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
