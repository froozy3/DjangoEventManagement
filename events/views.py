from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer, EventRegisteredUser
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class EventCreate(APIView):
    """
    API View для создания нового события.
    """

    def post(self, request):
        serializer = EventSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            event = serializer.save(organizer=request.user)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventUpdate(APIView):
    """
    API View для обновления существующего события.
    """

    def patch(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found by id"}, status=status.HTTP_400_BAD_REQUES)

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
    """
    API View для получения списка всех событий.
    """

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDetail(APIView):

    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"detail": "Even not found"}, status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event)
        return Response(serializer.data, status.HTTP_200_OK)


class EventDelete(APIView):
    """
    API View для удаления существующего события.
    """

    def delete(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found by id"}, status=status.HTTP_400_BAD_REQUEST)

        if event.organizer != request.user:
            return Response(
                {"detail": "You do not have permission to edit this event"}, status=status.HTTP_403_FORBIDDEN)

        event.delete()

        return Response(
            {"detail": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class EventRegister(APIView):

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found by id"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user  # get current user

        if user in event.registered_user.all():
            return Response({"detail": "You are already registered for this event."}, status.HTTP_400_BAD_REQUEST)

        event.registered_user.add(user)

        serializer = EventRegisteredUser(event)
        return Response({"detail": "Successfully registered for the event.",
                         "Users which already registered": serializer.data}, status.HTTP_200_OK)
