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

    def test_logged_out_user_cannot_follow_user(self)


class FollowerDetailViewTests(APITestCase):
    """
    Unit testing for the FollowerDetail view.
    """

    def setUp(self):


    def test_user_can_follow_other_user(self):


    def test_user_can_unfollow_user(self):


    def test_user_can_retrieve_following_with_valid_id(self):


    def test_user_cannot_retrieve_following_with_invalid_id(self):


    def test_user_cannot_perform_unfollow_for_another_user(self):