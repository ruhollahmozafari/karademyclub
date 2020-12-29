# Generated by Django 3.1.4 on 2020-12-29 23:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_auto_20201229_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='content_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='report',
            name='detail',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='object_id',
            field=models.PositiveIntegerField(default=None),
        ),
        migrations.AddField(
            model_name='report',
            name='reason',
            field=models.CharField(choices=[('not related to prongramin', 'not related to prongramin'), ('insulting', 'insulting'), ('sexual matters', 'sexual matters'), ('wrong answer', 'wrong answer'), ('inappropiate', 'inappropiate'), ('other', 'other')], default='publish', max_length=35),
        ),
        migrations.AddField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='report',
            name='reprted_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
