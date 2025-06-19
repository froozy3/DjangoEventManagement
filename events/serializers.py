from rest_framework import serializers

from auth.serializers import UserSerializer
from .models import Event, Rating


class EventSerializer(serializers.ModelSerializer):
    registered_users = UserSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "finish_date",
            "location",
            "organizer",
            "average_rating",
            "registered_users",
        ]
        read_only_fields = ["organizer"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["organizer"] = user
        return super().create(validated_data)

    def get_average_rating(self, obj):
        return obj.average_rating()


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    event = serializers.CharField(source="event.title", read_only=True)
    organizer = serializers.CharField(source="event.organaier", read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "rating", "user", "event", "organizer"]
