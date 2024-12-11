from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Event
from rest_framework import status


class EventTests(APITestCase):

    def setUp(self):
        self.event = Event.objects.create(
            title="Old Title", description="Old Description")
        self.url = reverse('update_events', args=[self.event.pk])

        self.assertEqual(self.event.title, 'Old Title')
        self.assertEqual(self.event.description, 'Old Description')

    def test_update_event_with_valid_data(self):
        data = {'title': 'Test Title', 'description': 'Test Description'}

        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()

        self.assertEqual(self.event.title, 'Test Title')
        self.assertEqual(self.event.description, 'Test Description')
