from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = CountryField(default='IE', blank=False)
    city = models.CharField(max_length=150, blank=True)
    name = models.CharField(max_length=150, blank=True)
    ask_me = models.TextField(blank=True)
    tell_me = models.TextField(blank=True)
    # looking_for = 
    image = models.ImageField(
        upload_to='images/', default='../hissr_profile_default_ftjipg',
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)