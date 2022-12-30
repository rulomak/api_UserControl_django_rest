from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
''' con Abstrac estamos creando el usuario, con Baseuser estamos creando el manager de ese usuario  y con permission le damos los permisos  '''


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fiels):
        ''' crea y guarda un nuevo usuario '''
        if not email:
            raise ValueError('User mst have an email')

        user = self.model(email=self.normalize_email(email), **extra_fiels)
        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password):
        ''' crea super usuarios'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user





class User(AbstractBaseUser, PermissionsMixin):
    ''' Modelo personalizado de usuario que soporta hacer login con email '''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # le dicimo que queremos hacer login con el email 

