from rest_framework import serializers
from .models import Event, Rating
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    registered_users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description',
                  'date', 'location', 'organizer', 'average_rating', 'registered_users']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['organizer'] = user

        return super().create(validated_data)

    def get_average_rating(self, obj):
        return obj.average_raitng()


class EventRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'registered_users']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating']
