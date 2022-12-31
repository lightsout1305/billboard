from django.forms import ModelForm
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post, Comment, Author


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_category', ]

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
        fields = ['comment_text', ]


class AuthorSignupForm(SignupForm):

    def save(self, request):
        user = super(AuthorSignupForm, self).save(request)
        author_group = Group.objects.get(name='author')
        author_group.user_set.add(user)
        Author.objects.create(author=user, author_id=user.id)
        return user
