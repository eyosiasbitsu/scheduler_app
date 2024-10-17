from django.db import models


class Schedule(models.Model):
    schedule = models.JSONField(default=dict)

    def __str__(self):
        return f"Schedule {self.id}"
