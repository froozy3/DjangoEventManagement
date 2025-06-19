from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework import permissions

from events.views import EventRegisterView, EventViewSet, RatingView


router = DefaultRouter()
router.register("events", EventViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("events/rating/<int:event_id>/", RatingView.as_view(), name="rating"),
    path(
        "events/register/<int:event_id>/", EventRegisterView.as_view(), name="register"
    ),
]
