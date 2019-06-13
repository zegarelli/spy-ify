from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Post(models.Model):
    """
    A model representing a date instance
    """
    id = models.BigAutoField(primary_key=True)
    day = models.DateTimeField(auto_now_add=True)
    referenceDay = models.DateTimeField(default=now, blank=True)
    text = models.TextField(null=True, blank=True)
    summary = models.CharField(null=True, blank=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_posts = models.ManyToManyField("self", blank=True)
