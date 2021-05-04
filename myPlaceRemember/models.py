from django.db import models
from django.shortcuts import reverse
from login.models import Profile


class RememberModel(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    body = models.TextField(blank=True, db_index=True)
    slug = models.CharField(max_length=100, unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('remember_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
