from django.contrib.auth.models import User
from django.db import models


class Schedule(models.Model):
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)  # Correct annotation
    schedule = models.JSONField(default=dict)

    def __str__(self):
        return f"Schedule {self.id}"
