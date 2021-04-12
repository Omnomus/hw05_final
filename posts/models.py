from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Community for posts. Grouping by topic."""
    title = models.CharField('Имя группы', max_length=200,
                             help_text='Введите имя группы')
    slug = models.SlugField('Slug',
                            unique=True,
                            help_text='Придумайте короткое название (slug)')
    description = models.TextField('Описание группы',
                                   max_length=1000,
                                   help_text='Напишите описание группы')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Post(models.Model):
    """Just a user post."""
    text = models.TextField('Текст заметки',
                            help_text='Введите текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True,
                              related_name='posts',
                              verbose_name='Группа')
    image = models.ImageField(upload_to='posts/',
                              blank=True,
                              null=True,
                              verbose_name='Изображение')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Запись пользователя'
        verbose_name_plural = 'Записи пользователя'

    def __str__(self):
        """String for representing the Model object."""
        return self.text[:15]


class Comment(models.Model):
    """Users comments to Post."""
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    created = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField('Комментарий',
                            help_text='Оставьте свой комментарий')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """String for representing Model Object."""
        return self.text[:30]


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
