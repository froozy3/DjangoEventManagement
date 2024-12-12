from django.urls import path, include
from .views import EventList, EventUpdate, EventCreate, EventDelete,EventRegister,EventDetail


urlpatterns = [
    path('events/', EventList.as_view(), name='list_event'),
    path('events/<int:pk>/', EventDetail.as_view(), name='single_event'),
    path('events/update/<int:pk>/', EventUpdate.as_view(), name='update_event'),
    path('events/create/', EventCreate.as_view(), name='create_events'),
    path('events/delete/<int:pk>/', EventDelete.as_view(), name='delete_event'),
    path('events/register/<int:pk>/',EventRegister.as_view(),name='register_on_event')
]
