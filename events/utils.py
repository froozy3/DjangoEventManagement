from django.http import Http404
from .models import Event


def get_event_or_404(pk):
    try:
        event = Event.objects.get(pk=pk)
        return event
    except Event.DoesNotExist:
        raise Http404("Event not found by id")
   
