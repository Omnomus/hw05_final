from django.urls import reverse

AUTHOR_NAME = 'leo'
COMMENT_TEXT = 'some comment here'
DESCRIPTION = 'group_description'
GROUP_NAME = 'title_group'
GROUP_NAME2 = 'title_group2'
POST_TEXT = 'привет' * 20
POST_TEXT2 = 'текст' * 20
SLUG = 'slug'
SLUG2 = 'slug2'
USER_NAME = 'test_username'

# URL

ABOUT_TECH_URL = reverse('about:tech')
ABOUT_URL = reverse('about:author')
FOLLOW_INDEX_URL = reverse('follow_index')
FOLLOW_URL = reverse('profile_follow', kwargs={'username': AUTHOR_NAME})
GROUP_URL = reverse('group_posts', kwargs={'slug': SLUG})
GROUP2_URL = reverse('group_posts', kwargs={'slug': SLUG2})
INDEX_URL = reverse('index')
NEW_POST_URL = reverse('new_post')
NOT_EXIST_URL = '/about/tech15667/'
PROFILE_AUTHOR_URL = reverse('profile', kwargs={'username': AUTHOR_NAME})
PROFILE_USER_URL = reverse('profile', kwargs={'username': USER_NAME})
UNFOLLOW_URL = reverse('profile_unfollow', kwargs={'username': AUTHOR_NAME})

REDIRECT_AUTH = '/auth/login/?next='

# templates

ABOUT_TECH_TMP = 'about/tech.html'
ABOUT_TMP = 'about/author.html'
GROUP_TMP = 'posts/group.html'
INDEX_TMP = 'posts/index.html'
NEW_POST_TMP = 'posts/new.html'
POST_TMP = 'posts/post.html'
PROFILE_TMP = 'posts/profile.html'

# picture
PICT = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B')
