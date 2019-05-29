from django.db import models
from django.contrib.auth.models import User

class Date(models.Model):
    """
    A model representing a date instance
    """
    date_id = models.BigAutoField(primary_key=True)
    day = models.DateTimeField()
    text = models.TextField(null=True, blank=True)