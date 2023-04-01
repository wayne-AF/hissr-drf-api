from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Personal(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = CountryField(blank=False)
    city = models.CharField(max_length=50, blank=False)
    title = models.CharField(max_length=150, blank=False)
    content = models.TextField(max_length=400, blank=False)
    connection_made = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
