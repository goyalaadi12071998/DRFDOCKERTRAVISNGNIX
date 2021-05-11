from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, name, email, phone, password=None):
        if email is None:
            raise ValueError('User must have an email address')
        if password is None:
            raise ValueError('User must have an  password')        
        if phone is None:
            raise ValueError('User must have an  phonennumber')
        if len(phone) != 10:
            raise ValueError('Phone Number must be length of 10')

        email = self.normalize_email(email)

        user = self.model(name=name, email=email, phone=phone)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, name, email, phone, password):
        user = self.create_user(name, email, phone, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserManager()
    