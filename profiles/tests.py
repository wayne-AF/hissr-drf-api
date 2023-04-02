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

    def test_user_can_retrieve_profile_with_valid_id(self):
        """
        Ensures user can retrieve a profile with valid id.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_profile_with_invalid_id(self):
        """
        Ensures user cannot retrieve a profile with invalid id.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.get('/profiles/1234/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_profile(self):
        """
        Ensures user can update their own profile.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put('/profiles/1/', {'about': 'hi there'})
        profile = Profile.objects.filter(pk=1).first()
        self.assertEqual(profile.about, 'hi there')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_another_users_profile(self):
        """
        Ensures user cannot update another user's profile.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put('/profiles/2/', {'about': 'hi there'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
