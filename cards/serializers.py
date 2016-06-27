from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer
from cards.models import Card, CardType


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardType
        fields = ('title',)


class CardSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = UserSerializer(read_only=True)
    card_code = serializers.CharField()
    card_type = serializers.PrimaryKeyRelatedField(
        queryset=CardType.objects.all(),
    )
    company = UserSerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all().filter(role=User.COMPANY),
        source='company',
        write_only=True
    )

    class Meta:
        model = Card
        depth = 1
