from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date',
                  'location', 'organizer', 'registered_user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['organizer'] = user

        return super().create(validated_data)


class EventRegisteredUser(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ['id', 'registered_user']
