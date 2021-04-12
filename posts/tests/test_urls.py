from django.contrib.auth import get_user_model
from django.core.cache import caches
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post
from posts.tests import const

User = get_user_model()


class PostsURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.author = User.objects.create_user(username=const.AUTHOR_NAME)
        self.user = User.objects.create_user(username=const.USER_NAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

        self.my_cache = caches['default']
        self.my_cache.clear()
        self.my_cache.close()

        self.Group = Group.objects.create(
            title=const.GROUP_NAME,
            slug=const.SLUG,
            description=const.DESCRIPTION
        )
        self.Post = Post.objects.create(
            text=const.POST_TEXT,
            author=self.author,
            group=self.Group
        )
        self.POST_URL = reverse(
            'post',
            kwargs={
                'username': const.AUTHOR_NAME,
                'post_id': self.Post.id})
        self.EDIT_POST_URL = reverse(
            'post_edit',
            kwargs={
                'username': const.AUTHOR_NAME,
                'post_id': self.Post.id}
        )

    def test_url_is_available_for_guest(self):
        """URL is available for guests."""
        url_names = [
            const.INDEX_URL,
            const.GROUP_URL,
            const.PROFILE_AUTHOR_URL,
            self.POST_URL,
            const.ABOUT_URL,
            const.ABOUT_TECH_URL,
        ]
        for url in url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEquals(response.status_code, 200)

    def test_url_is_available_for_authorized(self):
        """URL is available for authorized."""
        url_names = [
            const.INDEX_URL,
            const.GROUP_URL,
            const.PROFILE_AUTHOR_URL,
            self.POST_URL,
            const.ABOUT_URL,
            const.ABOUT_TECH_URL,
            const.NEW_POST_URL,
        ]
        for url in url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEquals(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL uses correct template."""
        url_templates_names = {
            const.INDEX_URL: const.INDEX_TMP,
            const.GROUP_URL: const.GROUP_TMP,
            const.NEW_POST_URL: const.NEW_POST_TMP,
            const.PROFILE_AUTHOR_URL: const.PROFILE_TMP,
            self.POST_URL: const.POST_TMP,
            self.EDIT_POST_URL: const.NEW_POST_TMP,
        }
        for url, template in url_templates_names.items():
            with self.subTest(url=url):
                response = self.authorized_author.get(url)
                self.assertTemplateUsed(response, template)

    def test_post_edit_url_available_for_authorized_author(self):
        """'post_edit' URL is available for authorized author."""
        response = self.authorized_author.get(self.EDIT_POST_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_url_unavailable_for_authorized(self):
        """'post_edit' URL is unavailable for authorized not author."""
        response = self.authorized_client.get(self.EDIT_POST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_post_edit_url_unavailable_for_guest(self):
        """'post_edit' URL is unavailable for guest."""
        response = self.guest_client.get(self.EDIT_POST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_new_url_redirect_guest_on_login(self):
        """'/new/' URL redirect guest to log in."""
        response = self.guest_client.get(const.NEW_POST_URL, follow=True)
        redirect = f'/auth/login/?next={const.NEW_POST_URL}'
        self.assertRedirects(response, redirect)

    def test_post_edit_url_redirect_guest_on_login(self):
        """'/post_edit/' URL redirect guest to login."""
        response = self.guest_client.get(self.EDIT_POST_URL, follow=True)
        redirect = f'/auth/login/?next={self.EDIT_POST_URL}'
        self.assertRedirects(response, redirect)

    def test_post_edit_url_redirect_not_author_on_post(self):
        """'/post_edit/' URL redirect not author to post."""
        response = self.authorized_client.get(self.EDIT_POST_URL, follow=True)
        redirect = self.POST_URL
        self.assertRedirects(response, redirect)

    def test_page_not_found(self):
        """Site returns 404 if page not found."""
        response = self.guest_client.get(const.NOT_EXIST_URL, follow=True)
        self.assertEqual(response.status_code, 404)
