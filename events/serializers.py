from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description','date', 'location', 'organizer']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['organizer'] = user

        return super().create(validated_data)
