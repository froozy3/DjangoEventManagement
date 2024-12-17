from django.http import Http404
from .models import Event
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta


def get_event_or_404(pk):
    try:
        event = Event.objects.get(pk=pk)
        return event
    except Event.DoesNotExist:
        raise Http404("Event not found by id")


def sending_email(user, event):

    subject = f"Registration Confirmation {event.title}"
    message = (
        f"Hello,{user.username}\n\n"
        f"Thank you for registering for the event \"{event.title}\"!\n\n"
        f"Event Details:\n"
        f"- Title: {event.title}\n"
        f"- Date: {event.date.strftime('%A, %d %B %Y at %I:%M %p')}\n"
        f"- Location: {event.location}\n\n"
        f"We're excited to see you there!\n\n"
        f"If you have any questions, feel free to contact us at support@example.com.\n\n"
        f"Best regards,\n"
        f"The Event Team"
    )
    from_email = 'tsemkalo2006@gmail.com'
    recipient_list = [user.email]

    send_mail(subject=subject, message=message,
              from_email=from_email, recipient_list=recipient_list, fail_silently=False)
