from allauth.socialaccount.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Author


class AuthorSocialSignupForm(SignupForm):

    def save(self, request):
        user = super(AuthorSocialSignupForm, self).save(request)
        author_group = Group.objects.get(name='author')
        author_group.user_set.add(user)
        Author.objects.create(author=user, author_id=user.id)
        return user
