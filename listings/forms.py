from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_category']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title == content:
            raise ValidationError(
                'Название и содержимое статьи (новости) не должны совпадать'
            )
        return cleaned_data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text',]