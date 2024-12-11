from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer

# Create your views here.


class EventCreate(APIView):
    """
    API View для создания нового события.
    """

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
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
            return Response(
                {"detail": "Event not found by id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        title = request.data.get('title')
        description = request.data.get('description')

        if not title and not description:
            return Response(
                {"detail": "Missing required title/description"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if title:
            event.title = title

        if description:
            event.description = description

        event.save()

        serializer = EventSerializer(event)
        return Response(serializer.data)


class ListEvents(APIView):
    """
    API View для получения списка всех событий.
    """

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDelete(APIView):
    """
    API View для удаления существующего события.
    """

    def delete(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found by id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        event.delete()

        return Response(
            {"detail": "Event deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
