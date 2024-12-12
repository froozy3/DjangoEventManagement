from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    registered_users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description',
                  'date', 'location', 'organizer', 'registered_users']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['organizer'] = user

        return super().create(validated_data)


class EventRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'registered_users']
