from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer, EventRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .utils import get_event_or_404, sending_email

# Create your views here.


class EventCreate(APIView):

    def post(self, request, format=None):
        request.data['organizer'] = request.user.id
        serializer = EventSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventUpdate(APIView):

    def patch(self, request, pk, format=None):
        event = get_event_or_404(pk)

        if event.organizer != request.user:
            return Response({"detail": "You do not have permission to edit this event"}, status=status.HTTP_403_FORBIDDEN)

        title = request.data.get('title')
        description = request.data.get('description')

        if not title and not description:
            return Response({"detail": "Missing required title/description"}, status=status.HTTP_400_BAD_REQUEST)

        if title:
            event.title = title

        if description:
            event.description = description

        event.save()

        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventList(APIView):

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventSingle(APIView):

    def get(self, request, pk):
        event = get_event_or_404(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventDelete(APIView):

    def delete(self, request, pk, format=None):
        event = get_event_or_404(pk)

        if event.organizer != request.user:
            return Response(
                {"detail": "You do not have permission to edit this event"}, status=status.HTTP_403_FORBIDDEN)

        event.delete()

        return Response(
            {"detail": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class EventRegister(APIView):
    def post(self, request, pk):
        event = get_event_or_404(pk=pk)

        user = request.user  # get current user

        if user in event.registered_users.all():
            return Response({"detail": "You are already registered for this event."}, status.HTTP_400_BAD_REQUEST)

        event.registered_users.add(user)
        sending_email(user, event)

        serializer = EventRegisterSerializer(event)

        return Response({"detail": "Successfully registered for the event.",
                         "Users which already registered": serializer.data}, status.HTTP_200_OK)
