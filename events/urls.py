from django.urls import path, include
from .views import ListEvents, EventUpdate


urlpatterns = [
    path('events/', ListEvents.as_view(), name='list_events'),
    path('events/<int:pk>', EventUpdate.as_view(), name='update_events')
]
