# Third party imports
from django.contrib.auth.models import User

# Internal imports
from django.db import models
from personals.models import Personal


class Like(models.Model):
    """
    Like model, related to 'owner' and 'personal'
    'owner' is a User instance and 'personal' is a Personal instance
    'unique_together' makes sure a user can't like the same personal twice
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    personal = models.ForeignKey(
        Personal, related_name='likes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'personal']

    def __str__(self):
        return f'{self.owner} {self.personal}'
