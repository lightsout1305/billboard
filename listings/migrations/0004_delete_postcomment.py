# Generated by Django 4.1.2 on 2022-12-31 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_alter_postcomment_comment_alter_postcomment_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PostComment',
        ),
    ]
