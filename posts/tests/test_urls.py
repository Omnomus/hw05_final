import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post
from posts.tests import const

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.author = User.objects.create_user(username=const.AUTHOR_NAME)
        self.user = User.objects.create_user(username=const.USER_NAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

        self.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=const.PICT,
            content_type='image/gif'
        )

        self.Group = Group.objects.create(
            title=const.GROUP_NAME,
            slug=const.SLUG,
            description=const.DESCRIPTION
        )
        self.Post = Post.objects.create(
            text=const.POST_TEXT,
            author=self.author,
            group=self.Group,
            image=self.uploaded
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
        self.ADD_COMMENT_URL = reverse(
            'add_comment',
            kwargs={
                'username': const.AUTHOR_NAME,
                'post_id': self.Post.id}
        )

    def test_url_available(self):
        """URL available for client."""
        author = self.authorized_author
        guest = self.guest_client
        user = self.authorized_client
        tested_urls = [
            [author, self.EDIT_POST_URL],
            [guest, const.INDEX_URL],
            [guest, const.GROUP_URL],
            [guest, const.PROFILE_AUTHOR_URL],
            [guest, self.POST_URL],
            [guest, const.ABOUT_URL],
            [guest, const.ABOUT_TECH_URL],
            [user, const.NEW_POST_URL],
        ]
        for client, url in tested_urls:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_not_available(self):
        """URL not available for client."""
        guest = self.guest_client
        user = self.authorized_client
        tested_urls = [
            [guest, self.EDIT_POST_URL],
            [user, self.EDIT_POST_URL],
        ]
        for client, url in tested_urls:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertNotEqual(response.status_code, 200)

    def test_url_redirects(self):
        """URL redirects client correctly."""
        guest = self.guest_client
        user = self.authorized_client
        tested_urls = [
            [guest, self.EDIT_POST_URL,
                const.REDIRECT_AUTH + self.EDIT_POST_URL],
            [guest, const.NEW_POST_URL,
                const.REDIRECT_AUTH + const.NEW_POST_URL],
            [guest, self.ADD_COMMENT_URL,
                const.REDIRECT_AUTH + self.ADD_COMMENT_URL],
            [user, self.EDIT_POST_URL, self.POST_URL],
        ]
        for client, url, redirect in tested_urls:
            with self.subTest(url=url):
                self.assertRedirects(client.get(url, follow=True), redirect)

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
                self.assertTemplateUsed(
                    self.authorized_author.get(url), template)

    def test_page_not_found(self):
        """Site returns 404 if page not found."""
        response = self.guest_client.get(const.NOT_EXIST_URL, follow=True)
        self.assertEqual(response.status_code, 404)
