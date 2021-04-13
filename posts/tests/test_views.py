import datetime as dt
import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Follow, Group, Post
from posts.tests import const

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Group = Group.objects.create(
            title=const.GROUP_NAME,
            slug=const.SLUG,
            description=const.DESCRIPTION
        )
        cls.Group2 = Group.objects.create(
            title=const.GROUP_NAME2,
            slug=const.SLUG2,
            description=const.DESCRIPTION
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=const.USER_NAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author = User.objects.create_user(username=const.AUTHOR_NAME)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.author)

        self.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=const.PICT,
            content_type='image/gif'
        )

        self.Post = Post.objects.create(
            text=const.POST_TEXT,
            pub_date=dt.datetime.now(),
            author=self.user,
            group=PostPagesTest.Group,
            image=self.uploaded
        )
        self.POST_URL = reverse(
            'post',
            kwargs={
                'username': self.Post.author.username,
                'post_id': self.Post.id})
        self.EDIT_POST_URL = reverse(
            'post_edit',
            kwargs={
                'username': self.Post.author.username,
                'post_id': self.Post.id})
        self.ADD_COMMENT_URL = reverse(
            'add_comment',
            kwargs={
                'username': self.Post.author.username,
                'post_id': self.Post.id})

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

    def new_post(self, user, list):
        test_group = Group.objects.get(title=const.GROUP_NAME)
        form_data = {
            'text': const.POST_TEXT2,
            'group': test_group.id,
            'image': self.uploaded}
        response = user.post(
            const.NEW_POST_URL,
            data=form_data,
            follow=True)
        return response.context.get(list)[0]

    def test_new_post_displayed_correctly(self):
        """New post with choosen group displayed correctly on pages."""
        post = self.new_post(self.authorized_client, 'page')
        tested_url = [
            const.INDEX_URL,
            const.GROUP_URL
        ]
        for url in tested_url:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                first_object = response.context.get('page')[0]
                self.assertIs(first_object == post, True)

    def test_new_post_wrong_group(self):
        """New post with choosen group not displayed on wrong Group page."""
        post = self.new_post(self.authorized_client, 'page')
        response = self.guest_client.get(const.GROUP2_URL)
        self.assertNotIn(post, response.context['page'])

    def test_pages_uses_correct_templates(self):
        """URL uses correct template."""
        template_url_names = {
            const.INDEX_TMP: const.INDEX_URL,
            const.GROUP_TMP: const.GROUP_URL,
            const.NEW_POST_TMP: const.NEW_POST_URL,
            const.ABOUT_TMP: const.ABOUT_URL,
            const.ABOUT_TECH_TMP: const.ABOUT_TECH_URL,
        }
        for template, reverse_name in template_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_uses_correct_context(self):
        """Template index.html formed with correct context."""
        response = self.guest_client.get(const.INDEX_URL)
        self.assertEqual(
            response.context.get('page')[0].author, self.user)
        self.assertEqual(
            response.context.get('page')[0].pub_date, self.Post.pub_date)
        self.assertEqual(
            response.context.get('page')[0].text, const.POST_TEXT)
        self.assertEqual(
            response.context.get('page')[0].group, PostPagesTest.Group)
        self.assertEqual(
            response.context.get('page')[0].image, 'posts/small.gif')

    def test_group_page_uses_correct_context(self):
        """Template group.html formed with correct context."""
        response = self.guest_client.get(const.GROUP_URL)
        self.assertEqual(
            response.context.get('group').title, const.GROUP_NAME)
        self.assertEqual(
            response.context.get('group').description, const.DESCRIPTION)
        self.assertEqual(
            response.context.get('page')[0].author, self.user)
        self.assertEqual(
            response.context.get('page')[0].pub_date, self.Post.pub_date)
        self.assertEqual(
            response.context.get('page')[0].text, const.POST_TEXT)
        self.assertEqual(
            response.context.get('page')[0].image, 'posts/small.gif')

    def test_new_post_page_uses_correct_context(self):
        """Template new_post.html formed with correct context."""
        response = self.authorized_client.get(const.NEW_POST_URL)
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_uses_correct_context(self):
        """Template new_post.html (for edit) formed with correct context."""
        response = self.authorized_client.get(self.EDIT_POST_URL)
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields[value]
                self.assertIsInstance(form_field, expected)
        self.assertEqual(
            response.context.get('author').username, const.USER_NAME)
        self.assertEqual(response.context.get('post').text, const.POST_TEXT)

    def test_profile_page_uses_correct_context(self):
        """Template profile.html formed with correct context."""
        response = self.authorized_client.get(const.PROFILE_USER_URL)
        self.assertEqual(
            response.context.get('author').username, const.USER_NAME)
        self.assertEqual(
            response.context.get('page')[0].author, self.user)
        self.assertEqual(
            response.context.get('page')[0].pub_date, self.Post.pub_date)
        self.assertEqual(
            response.context.get('page')[0].text, const.POST_TEXT)
        self.assertEqual(
            response.context.get('page')[0].image, 'posts/small.gif')

    def test_post_page_uses_correct_context(self):
        """Template post.html formed with correct context."""
        response = self.authorized_client.get(self.POST_URL)
        self.assertEqual(
            response.context.get('author').username, const.USER_NAME)
        self.assertEqual(response.context.get('post').text, const.POST_TEXT)
        self.assertEqual(
            response.context.get('post').image, 'posts/small.gif')

    def test_paginator_provide_right_count(self):
        """Paginator provides right count of posts per page."""
        objs = (Post(text=const.POST_TEXT2 * i,
                     pub_date=dt.datetime.now(),
                     author=self.user,
                     group=PostPagesTest.Group) for i in range(12))
        Post.objects.bulk_create(objs)
        response = self.guest_client.get(const.INDEX_URL)
        posts_count = settings.PAGINATION_PER_PAGE
        self.assertEqual(len(response.context.get('page')), posts_count)

    def test_authorized_can_follow_and_unfollow(self):
        """Authorized user can subscribe and unsubscribe author."""
        self.authorized_client.get(const.FOLLOW_URL)
        self.assertTrue(
            Follow.objects.filter(user=self.user, author=self.author).exists())
        self.authorized_client.get(const.UNFOLLOW_URL)
        self.assertFalse(
            Follow.objects.filter(user=self.user, author=self.author).exists())

    def test_new_post_follow(self):
        """New post appears on follower's subscription page and
        does not appear on not follower's subscription page."""
        self.authorized_client.get(const.FOLLOW_URL)
        new_post = self.new_post(self.authorized_client2, 'page')
        response = self.authorized_client.get(const.FOLLOW_INDEX_URL)
        self.assertIn(new_post, response.context.get('page'))
        response = self.authorized_client2.get(const.FOLLOW_INDEX_URL)
        self.assertNotIn(new_post, response.context.get('page'))

    def test_add_comment_auth(self):
        """Authorized client can leave a comment."""
        data = {
            'text': const.COMMENT_TEXT
        }
        self.authorized_client.post(
            self.ADD_COMMENT_URL, data=data, follow=True)
        response = self.guest_client.get(self.POST_URL)
        self.assertEqual(
            response.context.get('comments')[0].text, const.COMMENT_TEXT)
