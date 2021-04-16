import datetime as dt
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Group, Post
from posts.tests import const

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsFormsTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=const.USER_NAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.Group = Group.objects.create(
            title=const.GROUP_NAME,
            slug=const.SLUG,
            description=const.DESCRIPTION
        )
        self.Group2 = Group.objects.create(
            title=const.GROUP_NAME2,
            slug=const.SLUG2,
            description=const.DESCRIPTION
        )
        self.Post = Post.objects.create(
            text=const.POST_TEXT,
            pub_date=dt.datetime.now(),
            author=self.user,
            group=self.Group
        )
        self.EDIT_POST_URL = reverse(
            'post_edit',
            kwargs={
                'username': self.Post.author.username,
                'post_id': self.Post.id})

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def test_new_post_appear_in_database(self):
        """New post appear in database."""
        posts_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=const.PICT,
            content_type='image/gif'
        )
        form_data = {
            'text': const.POST_TEXT2,
            'group': self.Group.id,
            'image': uploaded}
        response = self.authorized_client.post(
            const.NEW_POST_URL,
            data=form_data,
            follow=True)
        redirect = const.INDEX_URL
        response2 = self.guest_client.get(const.INDEX_URL)
        self.assertTrue(Post.objects.filter(text=const.POST_TEXT2).exists())
        self.assertEqual(
            response2.context.get('page')[0].image, 'posts/small.gif')
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, redirect)

    def test_edited_post_appear_in_database(self):
        """Post has been changed in database."""
        posts_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=const.PICT,
            content_type='image/gif'
        )
        form_data = {
            'text': const.POST_TEXT2,
            'group': self.Group2.id,
            'image': uploaded}
        self.authorized_client.post(
            self.EDIT_POST_URL,
            data=form_data,
            follow=True)
        self.assertTrue(Post.objects.filter(
            id=self.Post.id,
            text=const.POST_TEXT2,
            image='posts/small.gif').exists())
        self.assertFalse(Post.objects.filter(text=const.POST_TEXT).exists())
        self.assertEqual(Post.objects.count(), posts_count)


class CommentFormTests(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username=const.AUTHOR_NAME)
        self.user = User.objects.create_user(username=const.USER_NAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.Group = Group.objects.create(
            title=const.GROUP_NAME,
            slug=const.SLUG,
            description=const.DESCRIPTION
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=const.PICT,
            content_type='image/gif'
        )
        self.Post = Post.objects.create(
            text=const.POST_TEXT,
            author=self.author,
            group=self.Group,
            image=uploaded
        )
        self.POST_URL = reverse(
            'post',
            kwargs={
                'username': self.Post.author.username,
                'post_id': self.Post.id})
        self.ADD_COMMENT_URL = reverse(
            'add_comment',
            kwargs={
                'username': self.Post.author.username,
                'post_id': self.Post.id})

    def test_new_comment(self):
        """New comment appears on post's page."""
        count = self.Post.comments.count()
        data = {'text': const.COMMENT_TEXT}
        response = self.authorized_client.post(
            self.ADD_COMMENT_URL,
            data=data,
            follow=True)
        self.assertEqual(self.Post.comments.count(), count + 1)
        self.assertEqual(self.Post.comments.all()[0].text, const.COMMENT_TEXT)
        self.assertRedirects(response, self.POST_URL)
