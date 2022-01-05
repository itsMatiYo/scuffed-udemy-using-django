from django.test import TestCase

from posts_api import models as md


class PostTestCase(TestCase):

    def setUp(self) -> None:
        self.post_1 = md.Post.objects.create(
            title='Post 1 Title', content="post 1 content", seo={})
        self.post_2 = md.Post.objects.create(
            title='Post 2 Title', content="post 2 content", seo={})

        self.postcopy_1 = md.PostCopy.objects.create(
            title='Post 1 Copy title test', content='Copy Content 1 Post', post=self.post_1, delete_request=True)

        comment_1 = md.Comment.objects.create(
            content='Comment 1 Test content', post=self.post_1)

    def test_post(self):
        post_1 = md.Post.objects.get(
            title='Post 1 Title', content="post 1 content")
        post_2 = md.Post.objects.get(
            title='Post 2 Title', content="post 2 content")
        self.assertEqual(post_1.title, 'Post 1 Title')
        self.assertEqual(post_2.title, 'Post 2 Title')

    def test_post_copy(self):
        postcopy_1 = md.PostCopy.objects.get(
            title='Post 1 Copy title test', content='Copy Content 1 Post', delete_request=True)
        self.assertEqual(postcopy_1.content, 'Copy Content 1 Post')
        self.assertEqual(postcopy_1.title, 'Post 1 Copy title test')

    def test_comment(self):
        comment = md.Comment.objects.get(
            content='Comment 1 Test content', post=self.post_1)
        self.assertEqual(comment.approved, False)
        self.assertEqual(comment.post, self.post_1)
