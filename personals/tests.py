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

    def test_logged_out_user_cannot_create_personal(self):
        """
        Ensures logged-out user cannot create a personal.
        """
        response = self.client.post('/personals/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_personal_must_include_required_fields(self):
        """
        Ensures a personal cannot be created without mandatory fields
        (title and content).
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/personals/', {'title': 'a title', 'content': ''}
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PersonalDetailViewTests(APITestCase):
    """
    Unit testing for the PersonalDetail view.
    """

    def setUp(self):
        """
        Creates two user instances with associated posts at the start of
        every test method.
        """
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')
        Personal.objects.create(
            owner=adam, title='title 1', content='content 1'
        )
        Personal.objects.create(
            owner=anna, title='title 2', content='content 2'
        )

    def test_can_retrieve_personal_with_valid_id(self):
        """
        Ensures user can retrieve a personal with valid id.
        """
        response = self.client.get('/personals/1/')
        self.assertEqual(response.data['title'], 'title 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_personal_with_invalid_id(self):
        """
        Ensures user cannot retrieve a personal with invalid id
        (non-existent personal).
        """
        response = self.client.get('/personals/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_personal(self):
        """
        Ensures user can update their own personal.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put(
            '/personals/1/', {'title': 'a new title', 'content': 'content 1'}
            )
        personal = Personal.objects.filter(pk=1).first()
        self.assertEqual(personal.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_another_users_personal(self):
        """
        Ensures user cannot update someone else's personal.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put('/personals/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_personal(self):
        """
        Ensures user can delete their own personal.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/personals/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_another_users_personal(self):
        """
        Ensures user cannot delete other user's personal.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/personals/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)