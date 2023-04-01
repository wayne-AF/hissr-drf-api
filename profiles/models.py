from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField


class Profile(models.Model):
    SEEKING_CHOICES = [
        ('love', 'love'),
        ('friends', 'friends'),
        ('playdates', 'play dates'),
        ('chatonly', 'chat only'),
        ('huntingpartner', 'hunting partner')
    ]
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = CountryField(default='IE', blank=False)
    city = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    about = models.TextField(max_length=300, blank=True)
    ask_me = models.TextField(max_length=300, blank=True)
    tell_me = models.TextField(max_length=300, blank=True)
    seeking = MultiSelectField(choices=SEEKING_CHOICES, blank=True)
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