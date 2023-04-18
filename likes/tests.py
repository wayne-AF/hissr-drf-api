# Third party imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

# Internal imports
from .models import Like
from personals.models import Personal


class LikeListViewTests(APITestCase):
    """
    Unit testing for the LikeList view.
    """

    def setUp(self):
        """
        Creates a user instance at the start of every test method.
        """
        User.objects.create_user(username='adam', password='pass')

    def test_logged_out_user_cannot_like_personal(self):
        """
        Ensures logged-out user cannot like a personal.
        """
        response = self.client.post('/likes/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LikeDetailViewTests(APITestCase):
    """
    Unit testing for the LikeDetail view.
    """

    def setUp(self):
        """
        Creates two users, three personals, and two likes for personal 1 and 
        personal 2 at the start of every test method.
        """
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')

        Personal.objects.create(
            owner=adam, title='personal 1', content='content 1')
        Personal.objects.create(
            owner=anna, title='personal 2', content='content 2')
        Personal.objects.create(
            owner=anna, title='personal 3', content='content 3')

        Like.objects.create(owner=adam, personal_id=2)
        Like.objects.create(owner=anna, personal_id=1)

    def test_user_can_like_personal(self):
        """
        Ensures user can like a personal.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post('/likes/', {'personal': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unlike_personal(self):
        """
        Ensures user can unlike a personal they have liked.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/likes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_remove_other_users_like(self):
        """
        Ensures user cannot remove another user's like.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/likes/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_retrieve_like_with_valid_id(self):
        """
        Ensures user can retrieve a like with valid id.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.get('/likes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_like_with_invalid_id(self):
        """
        Ensures user cannot retrieve a like with invalid id.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.get('/likes/1234/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
