from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.tests import const

User = get_user_model()


class AboutURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_url_available(self):
        """URL available for client."""
        guest = self.guest_client
        tested_urls = [
            [guest, const.ABOUT_URL],
            [guest, const.ABOUT_TECH_URL],
        ]
        for client, url in tested_urls:
            with self.subTest(url=url):
                response = client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL uses correct template."""
        url_templates_names = {
            const.ABOUT_URL: const.ABOUT_TMP,
            const.ABOUT_TECH_URL: const.ABOUT_TECH_TMP,
        }
        for url, template in url_templates_names.items():
            with self.subTest(url=url):
                self.assertTemplateUsed(
                    self.guest_client.get(url), template)
