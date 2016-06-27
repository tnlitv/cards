from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_invalid_message = "Phone card_code must be entered in the format: '+999999999'. Up to 15 digits allowed."


class User(AbstractUser):
    COMPANY = 'C'
    USER = 'U'
    ROLES = [
        (USER, 'User'),
        (COMPANY, 'Company')
    ]

    role = models.CharField(max_length=2, choices=ROLES, default=USER)
    userpic = models.ImageField(upload_to='userpics/', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=phone_invalid_message)
    phone = models.CharField(validators=[phone_regex], unique=True, max_length=15)

    class Meta:
        db_table = 'auth_user'
    REQUIRED_FIELDS = ['email', 'password', 'role', 'userpic', 'username']
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return str(self.username)
