from django.test import TestCase

from posts.models import Group, Post, User
from posts.tests import const


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Group = Group.objects.create(title=const.GROUP_NAME)

    def test_verbose_name(self):
        """verbose_name in field matches the expected value."""
        group = GroupModelTest.Group
        verbose = group._meta.get_field('title').verbose_name
        self.assertEquals(verbose, 'Имя группы')

    def test_help_text(self):
        """help_text in field matches the expected value."""
        group = GroupModelTest.Group
        verbose = group._meta.get_field('title').help_text
        self.assertEquals(verbose, 'Введите имя группы')

    def test_object_name_is_title_field(self):
        """in object field __str__ is recorded object title."""
        group = GroupModelTest.Group
        expected_object_name = group.title
        self.assertEquals(expected_object_name, str(group))


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user(username=const.USER_NAME)
        cls.Post = Post.objects.create(
            text=const.POST_TEXT,
            author=user)

    def test_verbose_name(self):
        """verbose_name in field matches the expected value."""
        post = PostModelTest.Post
        verbose = post._meta.get_field('text').verbose_name
        self.assertEquals(verbose, 'Текст заметки')

    def test_help_text(self):
        """help_text in fields matches the expected value."""
        post = PostModelTest.Post
        verbose = post._meta.get_field('text').help_text
        self.assertEquals(verbose, 'Введите текст')

    def test_object_name_is_title_field(self):
        """in object field __str__ is recorded text's first 15 symbols."""
        post = PostModelTest.Post
        expected_object_name = post.text[:15]
        self.assertEquals(expected_object_name, str(post))
