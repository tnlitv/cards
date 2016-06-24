from django.contrib.auth import get_user_model
from rest_framework import serializers

from cards.models import Card, CardType, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'role', 'userpic', 'phone')


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
    number = serializers.CharField()
    type = serializers.PrimaryKeyRelatedField(
        queryset=CardType.objects.all(),
    )

    class Meta:
        model = Card
        depth = 1

    def create(self, validated_data):
        print(validated_data)
        return Card.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        print('updated')
        instance.save()
        return instance

    def validate(self, data):
        if self.context['method'] == 'POST':
            return self.post_validation(data)
        else:
            return self.put_validation(data)

    def post_validation(self, data):
        company_id = int(self.initial_data['company_id'])
        type_id = int(self.initial_data['type'])
        data['user_id'] = self.context["user"].id

        try:
            data['company'] = User.objects.all().filter(pk=company_id, role='C').first()
        except:
            raise serializers.ValidationError("Company does not exist")

        try:
            data['type'] = CardType.objects.get(pk=type_id)
        except:
            raise serializers.ValidationError("Type does not exist")
        print("---------------------------------")
        if (Card.objects.all().filter(
                company__id=company_id,
                number=data['number'])
            .first()):
            raise serializers.ValidationError("Card already exists")
        Card.objects.filter(
            company__id=company_id,
            number=data['number']).first()
        print("---------------------------------")

        return data

    def put_validation(self, data):
        if data.get('user'):
            raise serializers.ValidationError("Cannot modify owner")
        return data
