from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('hangout', 'Hang out'),
        ('groupchat', 'Group chat'),
        ('groomingparty', 'Grooming party'),
        ('dogbullying', 'Dog bullying'),
        ('birdwatching', 'Bird watching'),
        ('newfriends', 'New friends'),
        ('stupidhumans', 'Stupid humans')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = CountryField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    category = MultiSelectField(
        choices=CATEGORY_CHOICES, max_choices=3, blank=True
        )
    title = models.CharField(max_length=150, blank=False)
    content = models.TextField(max_length=400, blank=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
