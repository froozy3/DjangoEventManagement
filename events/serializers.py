from rest_framework import serializers
from auth.serializers import UserSerializer
from .models import Event, Rating


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.

    Handles serialization and deserialization of Event objects, including nested
    relationships with users and calculated average ratings.

    Attributes:
        registered_users (UserSerializer): Nested serializer for event participants
        average_rating (float): Calculated average rating for the event
    """

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

    def create(self, validated_data: dict) -> Event:
        """
        Create a new event instance.

        Args:
            validated_data (dict): Validated data for creating the event

        Returns:
            Event: Newly created event instance with organizer set
        """
        user = self.context["request"].user
        validated_data["organizer"] = user
        return super().create(validated_data)

    def get_average_rating(self, obj: Event) -> float:
        """
        Calculate average rating for an event.

        Args:
            obj (Event): Event instance to calculate rating for

        Returns:
            float: Average rating value
        """
        return obj.average_rating()


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for Rating model.

    Handles serialization and deserialization of Rating objects, including
    read-only fields for associated user, event, and organizer information.

    Attributes:
        user (str): Username of the rating creator
        event (str): Title of the rated event
        organizer (str): Username of the event organizer
    """

    user = serializers.CharField(source="user.username", read_only=True)
    event = serializers.CharField(source="event.title", read_only=True)
    organizer = serializers.CharField(
        source="event.organizer", read_only=True
    )  # Fixed typo

    class Meta:
        model = Rating
        fields = ["id", "rating", "user", "event", "organizer"]