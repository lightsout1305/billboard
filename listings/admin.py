from django.contrib import admin

from .models import Post, PostCategory, Category


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'register_date',
    )
    list_filter = (
        'author',
        'post_category',
        'rating'
    )
    search_fields = (
        'author',
        'title',
        'post_category',
        'register_date',
        'rating')


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Category)
