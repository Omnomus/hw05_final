from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Form for making a new post"""
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        widgets = {'text':
                   forms.Textarea(attrs={'placeholder': 'Напишите здесь)'})}
        labels = {'group': 'Выберите группу для публикации',
                  'text': 'Напишите заметку'}


class CommentForm(forms.ModelForm):
    """Form for leaving a comment to post."""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text':
                   forms.Textarea(attrs={
                       'placeholder': 'Оставьте свой комментарий'})}
