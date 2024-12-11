from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from .models import Event
from .serializers import EventSerializer
from django.contrib.auth.models import User

# Create your views here.


# class EventViewSet(APIView):
#     def post(self, request):
#         serializer = EventSerializer(data=request.data)

class EventUpdate(APIView):
    def patch(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"deatil": "Event not found by id"}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get('title', None)

        if not title:
            return Response({"deatil": "Missing required title/"}, status=status.HTTP_404_NOT_FOUND)

        event.title = title
        event.save()

        serializer = EventSerializer(event)
        return Response(serializer.data)


class ListEvents(APIView):

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
