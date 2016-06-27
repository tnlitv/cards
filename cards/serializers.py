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
    company = UserSerializer(read_only=True)

    company_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='company',
        write_only=True
    )
    card_code = serializers.CharField()
    card_type = serializers.PrimaryKeyRelatedField(
        queryset=CardType.objects.all(),
    )

    class Meta:
        model = Card
        depth = 1

    def create(self, validated_data):
        return Card.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.card_code = validated_data.get('card_code', instance.card_code)
        instance.save()
        return instance

    def validate(self, data):
        if self.context['method'] == 'POST':
            return self.validate_post_request(data)
        else:
            return self.validate_put_request(data)

    def validate_post_request(self, data):
        company_id = int(self.initial_data.get('company_id'))
        card_type_id = int(self.initial_data.get('card_type'))
        data['user_id'] = self.context.get('user').id

        try:
            data['company'] = User.objects.get(pk=company_id, role=User.COMPANY)
        except User.DoesNotExist:
            raise serializers.ValidationError("Company does not exist")

        try:
            data['card_type'] = CardType.objects.get(pk=card_type_id)
        except Card.DoesNotExist:
            raise serializers.ValidationError("Card type does not exist")

        if (Card.objects.filter(
                company__id=company_id,
                card_code=data.get('card_code')).count() > 0):
            raise serializers.ValidationError("Card already exists")
        return data

    def validate_put_request(self, data):
        if data.get('user'):
            raise serializers.ValidationError("Cannot modify owner")
        return data
