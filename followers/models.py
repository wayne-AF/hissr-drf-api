from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    """
    'Owner' is a user that is following a user.
    'Followed' is a user that is followed by 'owner'.
    'Related_name' makes sure Django can differentiate between 'owner'
    and 'user' who are both User model instances.
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
        )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followed'
        )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self):
        return f'{self.owner} {self.followed}'
