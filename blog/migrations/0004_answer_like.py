# Generated by Django 3.1.4 on 2020-12-29 13:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20201228_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='like',
            field=models.ManyToManyField(related_name='like_answer', to=settings.AUTH_USER_MODEL),
        ),
    ]