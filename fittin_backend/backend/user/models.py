from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=90, unique=True, blank=False)
    name = models.CharField('name', max_length=100, blank=False)
    surname = models.CharField('name', max_length=100, blank=True)
    password = models.CharField('password', max_length=128, blank=False)
    code = models.CharField('code', max_length=5, default='', blank=True)
    code_expires = models.DateTimeField('code_expires', blank=True, null=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
