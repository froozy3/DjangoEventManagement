from django.http import Http404
from .models import Event
from django.core.mail import send_mail


def get_event_or_404(pk: int) -> Event:
    """
    Retrieve an event by its primary key or raise Http404 if not found.

    Args:
        pk (int): The primary key of the event to retrieve.

    Returns:
        Event: The requested event instance.

    Raises:
        Http404: If the event with the given pk does not exist.
    """
    try:
        event = Event.objects.get(pk=pk)
        return event
    except Event.DoesNotExist:
        raise Http404("Event not found by id")


def sending_email(user, event: Event) -> None:
    """
    Send a confirmation email to a user who registered for an event.

    Args:
        user: The user who registered for the event.
        event (Event): The event the user registered for.

    Returns:
        None

    Raises:
        SMTPException: If there's an error sending the email.
    """
    subject = f"Registration Confirmation {event.title}"
    message = (
        f"Hello,{user.username}\n\n"
        f"Thank you for registering for the event \"{event.title}\"!\n\n"
        f"Event Details:\n"
        f"- Title: {event.title}\n"
        f"- Date: {event.start_date.strftime('%A, %d %B %Y at %I:%M %p')}\n"
        f"- Location: {event.location}\n\n"
        f"We're excited to see you there!\n\n"
        f"If you have any questions, feel free to contact us at support@example.com.\n\n"
        f"Best regards,\n"
        f"The Event Team"
    )
    from_email = "tsemkalo2006@gmail.com"
    recipient_list = [user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )