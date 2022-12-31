# Generated by Django 4.1.2 on 2022-12-30 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='listings.comment')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='listings.post')),
            ],
        ),
    ]
