from django.db.models.signals import post_save
from cards.models import CustomUser
from django.contrib.auth.models import User


def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = CustomUser(**values)
        user.save()
    print('saved-----------------------------------------')

post_save.connect(create_custom_user, User)
