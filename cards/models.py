from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# class CustomUserManager(UserManager):
#     def _create_user(self, username, email=None, password=None, role='U', **extra_fields):
#         print('Here')
#         print(role)
#         print(extra_fields)
#         print('there')
#         return super(CustomUserManager, self)._create_user(username, email, password, **extra_fields)
from card_project import settings


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    REQUIRED_FIELDS = ['email', 'password', 'role', 'userpic']
    COMPANY = 'C'
    USER = 'U'
    ROLES = [
        ('U', 'User'),
        ('C', 'Company')
    ]
    userpic = models.ImageField(upload_to='userpics/', blank=True, null=True)
    role = models.CharField(max_length=4, choices=ROLES, default=USER)

    def __str__(self):
        return str(self.username)


class CardType(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return str(self.title)


class Card(models.Model):
    number = models.CharField(max_length=30)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='company')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
    type = models.ForeignKey(CardType)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.number) + str(self.type_id) + str(self.user_id)
