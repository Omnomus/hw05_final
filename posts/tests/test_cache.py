import datetime as dt

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post
from posts.tests import const

User = get_user_model()


class PostsCacheTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username=const.USER_NAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.group = Group.objects.create(
            title=const.GROUP_NAME,
            slug=const.SLUG,
            description=const.DESCRIPTION
        )

        Post.objects.create(
            text=const.POST_TEXT,
            pub_date=dt.datetime.now(),
            author=self.user,
            group=self.group
        )

    def test_cache_index(self):
        """Cache works correctly on index page."""
        response = self.guest_client.get(const.INDEX_URL)
        data = {
            'text': const.POST_TEXT2,
            'group': self.group.id}
        self.authorized_client.post(
            const.NEW_POST_URL,
            data=data,
            follow=True)
        response2 = self.guest_client.get(const.INDEX_URL)
        self.assertEqual(response.content, response2.content)
