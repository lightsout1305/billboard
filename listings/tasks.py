from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import CategorySubs, Category, PostCategory
from billboard_project.settings import SERVER_EMAIL


@shared_task
def weekly_content_update():
    for cat in Category.objects.all():
        for subscribe in CategorySubs.objects.filter(cat_sub_category=cat):
            postcat = PostCategory.objects.filter(category=cat)
            msg = EmailMultiAlternatives(
                subject=f'Weekly content for {subscribe.cat_sub_category} category',
                from_email=SERVER_EMAIL,
                to=[subscribe.cat_sub_user.email, ],
            )
            html_content = render_to_string(
                'listing/weekly_posts.html',
                {
                    'recipient': subscribe.cat_sub_user,
                    'category': cat,
                    'week_feed': postcat,
                }
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()
