from django.db import models
from django.utils import timezone

class Entry(models.Model):
    workout = models.CharField(max_length=200)
    order_in_workout = models.CharField(max_length=100)
    seconds = models.CharField(max_length=30)
    minutes = models.CharField(max_length=30)

    def __str__(self):
        return self.workout

    class Meta:
        verbose_name_plural = "Entries"
