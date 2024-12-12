from django.urls import path, include
from .views import ListEvents, EventUpdate, EventCreate, EventDelete


urlpatterns = [
    path('events/get', ListEvents.as_view(), name='list_events'),
    path('events/update/<int:pk>', EventUpdate.as_view(), name='update_events'),
    path('events/create', EventCreate.as_view(), name='create_events'),
    path('events/delete/<int:pk>', EventDelete.as_view(), name='delete_events'),
    
]
