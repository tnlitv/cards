from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(User):
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom User'
    REQUIRED_FIELDS = ['email', 'role']

    COMPANY = 'C'
    USER = 'U'
    roles = (('C', 'Company'), ('U', 'User'))
    role = models.CharField(max_length=2,
                            choices=roles,
                            default='U')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. \
                                         Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    userpic = models.ImageField(upload_to='userpic/', blank=True, null=True)
    objects = UserManager()


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get('created', False):
        CustomUser.objects.get_or_create(user=kwargs.get('instance'))

post_save.connect(create_custom_user, User)


class CardType(models.Model):
    title = models.CharField(max_length=30)


class Card(models.Model):
    number = models.CharField(max_length=30)
    user = models.ForeignKey(CustomUser, limit_choices_to={'role': CustomUser.USER}, related_name='user')
    company = models.ForeignKey(CustomUser, limit_choices_to={'role': CustomUser.COMPANY}, related_name='company')
    type = models.ForeignKey(CardType)
    created_at = models.DateTimeField(auto_now_add=True)
