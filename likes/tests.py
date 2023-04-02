# External imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

# Internal imports
from .models import Like
from posts.models import Post


class LikeListViewTests(APITestCase):
    """
    Unit testing for the LikeList view.
    """

    def setUp(self):
        """
        Creates a user instance at the start of every test method. 
        """
        User.objects.create_user(username='adam', password='pass')

    def test_logged_out_user_cannot_like_post(self):
        """
        Ensures logged-out user cannot like a post.
        """
        response = self.client.post('/likes/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeDetailViewTests(APITestCase):
    """
    Unit testing for the LikeDetail view.
    """

    def setUp(self):
        """
        Creates two users, three posts, and two likes for post 1 and post 2 at
        the start of every test method.
        """
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')

        Post.objects.create(owner=adam, title='post 1', content='content 1')
        Post.objects.create(owner=anna, title='post 2', content='content 2')
        Post.objects.create(owner=anna, title='post 3', content='content 3')

        Follower.objects.create(owner=adam, followed_id=2)
        Follower.objects.create(owner=anna, followed_id=3)

        Like.objects.create(owner=adam, post_id=2)
        Like.objects.create(owner=anna, post_id=1)