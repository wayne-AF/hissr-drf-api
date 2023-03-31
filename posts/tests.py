from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        # print(len(response.data))

    def test_logged_in_user_can_create_posts(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title', 'content': 'content'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        anna = User.objects.create_user(username='anna', password='pass')
        Post.objects.create(
            owner=adam, title='title 1', content='content 1'
        )
        Post.objects.create(
            owner=anna, title='title 2', content='content 2'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'title 1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title', 'content': 'content 1'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# class PostListViewTests(APITestCase):
#     def setUp(self):
#         User.objects.create_user(username='amy', password='hissr')

#     def test_can_list_posts(self):
#         amy = User.objects.get(username='amy')
#         Post.objects.create(owner=amy, title='title')
#         response = self.client.get('/posts/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print(response.data)
#         print(len(response.data))

#     def test_logged_in_user_can_create_posts(self):
#         self.client.login(username='amy', password='hissr')
#         response = self.client.post('/posts/', {'title': 'title'})
#         count = Post.objects.count()
#         self.assertEqual(count, 1)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_logged_out_user_cant_create_post(self):
#         response = self.client.post('/posts/', {'title': 'title'})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class PostDetailViewTests(APITestCase):
#     def setUp(self):
#         amy = User.objects.create_user(username='amy', password='hissr')
#         alex = User.objects.create_user(username='alex', password='hissr')
#         Post.objects.create(
#             owner=amy, title='title 1', content='content 1'
#         )
#         Post.objects.create(
#             owner=alex, title='title 2', content='content 2'
#         )

#     def test_can_retrieve_post_using_valid_id(self):
#         response = self.client.get('/posts/1/')
#         self.assertEqual(response.data['title'], 'title 1')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_cant_retrieve_post_using_invalid_id(self):
#         response = self.client.get('/posts/999/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_user_can_update_own_post(self):
#         self.client.login(username='amy', password='hissr')
#         response = self.client.put('/posts/1/', {'title': 'a new title'})
#         post = Post.objects.filter(pk=1).first()
#         self.assertEqual(post.title, 'a new title')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_user_cant_update_another_users_post(self):
#         self.client.login(username='amy', password='hissr')
#         response = self.client.put('/posts/2/', {'title': 'a new title'})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)