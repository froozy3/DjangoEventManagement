from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


# Create your models here.


class Event(models.Model):
    class Meta:
        db_table = "events"

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    registered_users = models.ManyToManyField(User, related_name="events")

    def average_rating(self) -> float:
        return (
            Rating.objects.filter(event=self).aggregate(Avg("rating"))["rating__avg"]
            or 0
        )

    def clean(self):
        if self.start_date > self.finish_date:
            raise ValidationError("Finish date must be greater than start date")

    def __str__(self):
        return f"{self.title}: {self.average_rating()}"


class Rating(models.Model):
    class Meta:
        unique_together = ("user", "event")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
