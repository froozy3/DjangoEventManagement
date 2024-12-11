from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from .models import Event


# Create your tests here.


class EventTests(APITestCase):

    def setUp(self):
        self.user = User(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.event_1 = Event.objects.create(
            title='Event 1', description='Description 1', date='2024-12-12', location='Location 1', organizer=self.user)
        self.event_2 = Event.objects.create(
            title='Event 2', description='Description 2', date='2024-12-13', location='Location 2', organizer=self.user)

    def test_lists_event(self):
        url = reverse('list_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Проверяем, что два события
