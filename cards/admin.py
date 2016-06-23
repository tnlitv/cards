from django.contrib import admin

from .models import User, CardType, Card

admin.site.register(User)
admin.site.register(CardType)
admin.site.register(Card)
