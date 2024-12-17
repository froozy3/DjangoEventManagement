from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Rating
from .serializers import EventSerializer, EventRegisterSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated
from .utils import get_event_or_404, sending_email
from django.utils.dateparse import parse_datetime


# Create your views here.


class EventCreateView(APIView):

    def post(self, request):
        request.data['organizer'] = request.user.id

        serializer = EventSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventUpdateView(APIView):

    def patch(self, request, pk):
        event = get_event_or_404(pk)

        if event.organizer != request.user:
            return Response({"detail": "You do not have permission to edit this event"}, status=status.HTTP_403_FORBIDDEN)

        title = request.data.get('title')
        date = request.data.get('date')

        if not title and not date:
            return Response({"detail": "Missing required title/description/date"}, status=status.HTTP_400_BAD_REQUEST)

        if title:
            event.title = title

        if date:
            event.date = date

        event.save()
        serializer = EventSerializer(event)

        return Response(serializer.data)


class EventListView(APIView):
    def get(self, request):
        title = request.query_params.get('title', None)
        location = request.query_params.get('location', None)
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)
        organizer = request.query_params.get('organizer', None)

        events = Event.objects.all()

        events = events.filter(title__icontains=title) if title else events
        events = events.filter(
            location__icontains=location) if location else events
        events = events.filter(
            organizer__username__icontains=organizer) if organizer else events
        events = events.filter(date__gte=parse_datetime(
            date_from)) if date_from else events
        events = events.filter(date__lte=parse_datetime(
            date_to)) if date_to else events

        serializer = EventSerializer(events, many=True)

        return Response(serializer.data)


class EventSingleView(APIView):
    def get(self, request, pk):
        event = get_event_or_404(pk)

        serializer = EventSerializer(event)

        return Response(serializer.data)


class EventDeleteView(APIView):
    def delete(self, request, pk):
        event = get_event_or_404(pk)

        if event.organizer != request.user:
            return Response(
                {"detail": "You do not have permission to edit this event"}, status=status.HTTP_403_FORBIDDEN)

        event.delete()

        return Response({"detail": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class EventRegisterView(APIView):
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


class AddRatingView(APIView):
    def post(self, request, event_id):
        event = get_event_or_404(pk=event_id)

        if Rating.objects.filter(user=request.user, event=event).exists():
            return Response({'detail': "You are alredy leave your review"}, status.HTTP_400_BAD_REQUEST)

        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, event=event)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
