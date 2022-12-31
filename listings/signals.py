from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from .models import PostCategory, CategorySubs, Comment
from billboard_project.settings import SERVER_EMAIL


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        for cat in instance.postcategory_set.all():
            for subscribe in CategorySubs.objects.filter(cat_sub_category_id=cat.category_id):
                msg = EmailMultiAlternatives(
                    subject=instance.title,
                    body=instance.content,
                    from_email=SERVER_EMAIL,
                    to=[subscribe.cat_sub_user.email, ],
                )
                html_content = render_to_string(
                    'email/notification.html',
                    {
                        'title': instance.title,
                        'recipient': subscribe.cat_sub_user,
                        'content': instance.content,
                        'pk': instance.id,
                        'site': Site.objects.get_current().domain
                    }
                )

                msg.attach_alternative(html_content, 'text/html')
                msg.send()

                print(f'Тема письма: {instance.title}\n')
                print(f'Уведомление отослано подписчику {subscribe.cat_sub_user} '
                      f'на почту {subscribe.cat_sub_user.email} '
                      f'на тему {subscribe.cat_sub_category}')


@receiver(post_save, sender=Comment)
def notify_author(sender, instance, **kwargs):
        msg = EmailMultiAlternatives(
            subject='На ваше объявление откликнулись',
            body=instance.comment_text,
            from_email=SERVER_EMAIL,
            to=[instance.comment_post.author.author.email, ],
        )
        html_content = render_to_string(
            'email/new_comment.html',
            {
                'recipient': instance.comment_post.author.author.username,
                'content': instance.comment_text,
                'title': instance.comment_post.title,
                'comment_author': instance.comment_author.username,
                'pk': instance.comment_post.pk,
                'site': Site.objects.get_current().domain
            }
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        print(f'Тема письма: "{instance.comment_text}"\n')
        print(f'Уведомление отослано подписчику {instance.comment_post.author.author.username} '
              f'на почту {instance.comment_post.author.author.email}\n')
