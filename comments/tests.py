# External imports
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

# Internal imports
from .models import Comment
from posts.models import Post


class CommentListViewTests(APITestCase):
    """
    Unit testing for the CommentList view.
    """

    def setUp(self):
        """
        Creates a user instance at the start of every test method.
        """
        User.objects.create_user(username='adam', password='pass')

    def test_logged_out_user_cannot_create_comments(self):
        """
        Ensures logged-out user cannot create a comment.
        """
        response = self.client.post('/comments/', {'content': 'comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailViewTests(APITestCase):
    """
    Unit testing for the CommentDetail view.
    """

    def setUp(self):
        """
        Creates two user instances with associated posts and comments at the
        start of every test method.
        """
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')
        Post.objects.create(
            owner=adam, title='title 1', content='content 1'
        )
        Post.objects.create(
            owner=anna, title='title 2', content='content 2'
        )
        Comment.objects.create(owner=adam, post_id=1, content='comment 1')
        Comment.objects.create(owner=anna, post_id=2, content='comment 2')

    def test_can_retrieve_comment_with_valid_id(self):
        """
        Ensures user can retrieve a comment with valid id.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.get('/comments/1/')
        self.assertEqual(response.data['content'], 'comment 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_retrieve_comment_with_invalid_id(self):
        """
        Ensures user cannot retrieve a comment with invalid id
        (non-existent comment).
        """
        self.client.login(username='adam', password='pass')
        response = self.client.get('/comments/123/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_must_include_required_fields(self):
        """
        Ensures comment cannot be created without mandatory field (content).
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/comments/', {'post': 1, 'content': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logged_in_user_can_create_comment(self):
        """
        Ensures logged-in user can create a comment.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/comments/', {'post': 1, 'content': 'updated comment'}
        )
        count = Comment.objects.count()
        self.assertEqual(count, 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_update_own_comment(self):
        """
        Ensures user can update their own comment.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put(
            '/comments/1/', {'content': 'updated comment'}
        )
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'updated comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_another_users_comment(self):
        """
        Ensures user cannot update another user's comment.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.put(
            '/comments/2/', {'content': 'updated comment'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_comment(self):
        """
        Ensures user can delete their own comment.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_another_users_comment(self):
        """
        Ensures user cannot delete another user's comment.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.delete('/comments/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
