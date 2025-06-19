from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Rating
from .serializers import EventSerializer, RatingSerializer
from .utils import get_event_or_404, sending_email
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request


class EventGetMixin:
    """
    Mixin that provides a method to retrieve an event by its ID.
    """

    def get_event(self):
        """
        Retrieves an event instance or returns 404 if not found.

        Returns:
            Event: The requested event instance.

        Raises:
            Http404: If the event is not found.
        """
        return get_event_or_404(pk=self.kwargs["event_id"])


class RatingView(EventGetMixin, generics.CreateAPIView):
    """
    API view for creating event ratings.

    Allows authenticated users to rate events they have attended after the event has finished.
    Each user can only rate an event once.
    """

    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Creates a new rating for an event.

        Args:
            serializer: The rating serializer instance.

        Raises:
            ValidationError: If the user is not registered for the event,
                           has already left a review, or if the event hasn't ended yet.
        """
        event = self.get_event()
        user = self.request.user

        if user not in event.registered_users.all():
            raise ValidationError("You are not registered for this event.")

        if Rating.objects.filter(user=user, event=event).exists():
            raise ValidationError("You have already left your review.")

        if event.finish_date > timezone.now():
            raise ValidationError("Event has not ended yet.")

        serializer.save(user=user, event=event)


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and manipulating event instances.

    Provides default `create()`, `reading()`, `update()`,
    `partial_update()`, `()` and `delete()` actions.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRegisterView(EventGetMixin, generics.GenericAPIView):
    """
    API view for registering users for events.

    Allows authenticated users to register for events and sends
    a confirmation email upon successful registration.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Register current user for an event.

        Returns: List of all registered usernames
        Raises: ValidationError if already registered
        """
        event = self.get_event()
        user = self.request.user

        if user in event.registered_users.all():
            raise ValidationError("You are already registered for this event.")

        event.registered_users.add(user)

        try:
            sending_email(user, event)
        except Exception as e:
            print(f"Failed to send email: {e}")

        registered_user = [user.username for user in event.registered_users.all()]

        return Response(
            {
                "registered_users": registered_user,
            },
            status.HTTP_200_OK,
        )
