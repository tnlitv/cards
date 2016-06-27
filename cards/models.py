from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from card_project import settings


class CardType(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return str(self.title)


class Card(models.Model):
    card_code = models.CharField(max_length=40)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='company')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
    card_type = models.ForeignKey(CardType)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.card_code) + str(self.type_id) + str(self.user_id)
