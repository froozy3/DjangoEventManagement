from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    registered_users = models.ManyToManyField(User, related_name='events')

    class Meta:
        db_table = 'events'

    def average_raitng(self) -> float:
        return Rating.objects.filter(event=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return f"{self.title}: {self.average_raitng()}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])

    class Meta():
        unique_together = ('user', 'event')
