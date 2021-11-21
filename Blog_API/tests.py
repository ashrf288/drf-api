from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Blog

class BlogModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Blog.objects.create(
            author = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )
        test_post.save()

    def test_blog_content(self):
        post = Blog.objects.get(id=1)

        self.assertEqual(str(post.author), 'tester')
        self.assertEqual(post.title, 'Title of Blog')
        self.assertEqual(post.body, 'Words about the blog')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Blog.objects.create(
            author = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )
        test_post.save()

        response = self.client.get(reverse('posts_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertContains(response,'id' )
        self.assertEqual(response.data['title'],'Title of Blog' )


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        url = reverse('posts_list')
        data = {
            "title":"Testing is Fun!!!",
            "body":"when the right tools are available",
            "author":test_user.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_Blog = Blog.objects.create(
            author = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )

        test_Blog.save()

        url = reverse('posts_detail',args=[test_Blog.id])
        data = {
            "title":"Testing is Still Fun!!!",
            "author":test_Blog.author.id,
            "body":test_Blog.body,
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Blog.objects.count(), test_Blog.id)
        self.assertEqual(Blog.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a post."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Blog.objects.create(
            author = test_user,
            title = 'Title of Blog',
            body = 'Words about the blog'
        )

        test_post.save()

        post = Blog.objects.get()

        url = reverse('posts_detail', kwargs={'pk': post.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)