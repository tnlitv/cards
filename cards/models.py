from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from card_project import settings


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    REQUIRED_FIELDS = ['email', 'password', 'role', 'userpic', 'username']
    USERNAME_FIELD = 'phone'
    COMPANY = 'C'
    USER = 'U'
    ROLES = [
        ('U', 'User'),
        ('C', 'Company')
    ]
    userpic = models.ImageField(upload_to='userpics/', blank=True, null=True)
    role = models.CharField(max_length=4, choices=ROLES, default=USER)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: \
                                 '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], unique=True, max_length=15)

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
