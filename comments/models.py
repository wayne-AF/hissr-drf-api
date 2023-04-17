# Third party imports
from django.db import models
from django.contrib.auth.models import User

# Internal imports
from posts.models import Post
from personals.models import Personal


class Comment(models.Model):
    """
    Comment model, related to User, Post and Personal.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
