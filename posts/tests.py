# Third party imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

# Internal imports
from .models import Post


class PostListViewTests(APITestCase):
    """
    Unit testing for the PostList view.
    """

    def setUp(self):
        """
        Creates a user instance at the start of every test method.
        """
        User.objects.create_user(username='adam', password='pass')

    def test_user_can_list_posts(self):
        """
        Ensures user can see list of posts.
        """
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        """
        Ensures logged-in user can create a post.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/posts/', {'title': 'a title', 'content': 'content'}
            )
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cannot_create_post(self):
        """
        Ensures logged-out user cannot create a post.
        """
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_must_include_required_fields(self):
        """
        Ensures a post cannot be created without mandatory fields
        (title and content).
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/posts/', {'title': 'a title', 'content': ''}
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostDetailViewTests(APITestCase):
    """
    Unit testing for the PostDetail view.
    """

    def setUp(self):
        """
        Creates two user instances with associated posts at the start of
        every test method.
        """
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')
        Post.objects.create(
            owner=adam, title='title 1', content='content 1'
        )
        Post.objects.create(
            owner=anna, title='title 2', content='content 2'
        )

    def test_can_retrieve_post_with_valid_id(self):
        """
        Ensures user can retrieve a post with valid id.
        """
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'title 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_retrieve_post_with_invalid_id(self):
        """
        Ensures user cannot retrieve a post with invalid id
        (non-existent post).
        """
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        """
        Ensures user can update their own post.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put(
            '/posts/1/', {'title': 'a new title', 'content': 'content 1'}
            )
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_another_users_post(self):
        """
        Ensures user cannot update someone else's post.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_post(self):
        """
        Ensures user can delete their own post.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_another_users_post(self):
        """
        Ensures user cannot delete other user's post.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/posts/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
