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


# Create your views here.


class EventGetMixin:
    def get_event(self):
        return get_event_or_404(pk=self.kwargs["event_id"])


class RatingView(EventGetMixin, generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
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
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRegisterView(EventGetMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
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
