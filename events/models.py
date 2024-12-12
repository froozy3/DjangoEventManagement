from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Event(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    registered_users = models.ManyToManyField(User, related_name='events')

    class Meta:
        db_table = 'events'

    def __str__(self):
        return self.title
