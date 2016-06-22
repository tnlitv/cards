from django.contrib import admin

from .models import CustomUser, CardType, Card


admin.site.register(CustomUser)
admin.site.register(Card)
admin.site.register(CardType)
