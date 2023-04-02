# Third party imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

# Internal imports
from .models import Personal


class PersonalListViewTests(APITestCase):
    """
    Unit testing for the PersonalList view.
    """

    def setUp(self):
        """
        Creates a user instance at the start of every test method.
        """
        User.objects.create_user(username='adam', password='pass')

    def test_user_can_list_personals(self):
        """
        Ensures user can see list of personals.
        """
        adam = User.objects.get(username='adam')
        Personal.objects.create(owner=adam, title='a title')
        response = self.client.get('/personals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_personal(self):
        """
        Ensures logged-in user can create a personal.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/personals/', {
                'title': 'a title', 'city': 'Dublin', 'content': 'content'
                }
            )
        count = Personal.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)