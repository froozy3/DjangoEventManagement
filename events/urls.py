from django.urls import path, include


from .views import EventRegisterView, EventCreateView, EventDeleteView, EventListView, EventListView, EventSingleView, EventUpdateView


urlpatterns = [
    path('events/', EventListView.as_view(), name='list_event'),
    path('events/<int:pk>/', EventSingleView.as_view(), name='single_event'),
    path('events/update/<int:pk>/', EventUpdateView.as_view(), name='update_event'),
    path('events/create/', EventCreateView.as_view(), name='create_event'),
    path('events/delete/<int:pk>/', EventDeleteView.as_view(), name='delete_event'),
    path('events/register/<int:pk>/',EventRegisterView.as_view(), name='register_event'),
]
