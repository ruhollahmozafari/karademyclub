# Generated by Django 3.1.4 on 2021-01-13 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20210112_2048'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='report',
            constraint=models.UniqueConstraint(fields=('reporter', 'content_object'), name='duplicate_report'),
        ),
    ]
