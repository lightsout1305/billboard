from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Sum
from django.db import models
from django.urls import reverse


class Author(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        cont_rating = self.post_set.aggregate(contentRating=Sum('rating'))
        contRat = 0
        contRat += cont_rating.get('contentRating')

        comm_rating = self.author.comment_set.aggregate(commentRating=Sum('comment_rating'))
        commRat = 0
        commRat += comm_rating.get('commentRating')

        self.author_rating = contRat * 3 + commRat
        self.save()

    def __str__(self):
        return self.author.username


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField()
    rating = models.SmallIntegerField(default=0)
    register_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField('Category', through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{str(self.content)[:125].strip()}...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_subs = models.ManyToManyField(User, through='CategorySubs', blank=True)

    def __str__(self):
        return self.category_name


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = RichTextUploadingField()
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_rating = models.SmallIntegerField(default=0)
    comment_date = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class CategorySubs(models.Model):
    cat_sub_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cat_sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
