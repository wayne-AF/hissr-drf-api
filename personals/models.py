# Third party imports
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User

# Internal imports
from django.db import models


class Personal(models.Model):
    """
    Personal model, related to User and Like.
    """
    CATEGORY_CHOICES = [
        ('grooming', 'grooming'),
        ('dogbullying', 'dog bullying'),
        ('birdwatching', 'bird watching'),
        ('stupidhumans', 'stupid humans'),
        ('thoughtoftheday', 'thought of the day')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=150, blank=False)
    content = models.TextField(max_length=400, blank=False)
    category = MultiSelectField(
        choices=CATEGORY_CHOICES, blank=True
        )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
