# Generated by Django 3.1.4 on 2020-12-18 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20201217_0049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='user_id',
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='سوال کننده'),
        ),
    ]