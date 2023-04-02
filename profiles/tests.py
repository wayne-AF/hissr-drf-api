# Third party imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

# Internal imports
from .models import Profile


class ProfileListViewTests(APITestCase):
    """
    Unit testing for ProfileList view.
    """

    def setUp(self):
        """
        Creates a user instance at the start of every test method.
        """
        User.objects.create_user(username='adam', password='pass')

    def test_user_can_list_profiles(self):
        """
        Ensures user can see list of profiles.
        """
        adam = User.objects.get(username='adam')
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailViewTests(APITestCase):
    """
    Unit testing for ProfileDetail view.
    """

    def setUp(self):
        """
        Creates two user instances at the start of every test method.
        """
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')

    # def test_user_can_retrieve_profile_with_valid_id


    # def test_user_cannot_retrieve_profile_with_invalid_id


    # def test_user_can_update_own_profile


    # def test_user_cannot_update_another_users_profile

