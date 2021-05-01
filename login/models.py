from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"User: {self.user.username}"
