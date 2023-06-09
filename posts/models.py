# Third party imports
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Internal imports
from django.db import models


class Post(models.Model):
    """
    Post model, related to User and Comment.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = CountryField(default="IE", blank=True)
    city = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=150, blank=False)
    content = models.TextField(max_length=400, blank=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
