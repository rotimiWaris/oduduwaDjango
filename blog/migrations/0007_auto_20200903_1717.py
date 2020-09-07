# Generated by Django 3.0.8 on 2020-09-03 16:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_auto_20200902_2306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(related_name='blog_posts_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]