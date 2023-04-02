# from django.contrib.auth.models import User
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import Comment
# from posts.models import Post


# class CommentListViewTests(APITestCase):
#     """
#     Creates a user instance at the start of every test method.
#     """
#     def setUp(self):
#         User.objects.create_user(username='adam', password='pass')

#     def test_logged_out_user_cant_create_comments(self):
#         """
#         Ensures logged-out user cannot create a comment.
#         """
#         response = self.client.post('/comments/', {'content': 'comment'})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)