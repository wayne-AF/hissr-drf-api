# External imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

# Internal imports
from .models import Follower


class FollowerListViewTest(APITestCase):
    """
    Unit testing for the FollowerList view.
    """

    def setUp(self):
        """
        Creates a user instance at the start of every test method.
        """
        User.objects.create_user(username='adam', password='pass')

    def test_logged_out_user_cannot_follow_user(self):
        """
        Ensures logged-out user cannot follow user.
        """
        response = self.client.post('/followers/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FollowerDetailViewTests(APITestCase):
    """
    Unit testing for the FollowerDetail view.
    """

    def setUp(self):
        """
        Creates three users and two follows of user 1 and user 2 at the start
        of every test method.
        """
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')
        bobby = User.objects.create_user(username='bobby', password='pass')

        Follower.objects.create(owner=adam, followed_id=2)
        Follower.objects.create(owner=anna, followed_id=3)

    def test_user_can_follow_other_user(self):
        """
        Ensures user can follow another user.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post('/followers/', {'followed': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unfollow_user(self):
        """
        Ensures user can unfollow a user.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/followers/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_perform_unfollow_for_another_user(self):
        """
        Ensures user cannot perform unfollow on behalf of another user.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/followers/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_retrieve_following_with_valid_id(self):
        """
        Ensures user can retrieve a following user with valid id.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.get('/followers/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_following_with_invalid_id(self):
        """
        Ensures user cannot retrieve a following user with invalid id.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.get('/followers/1234/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
