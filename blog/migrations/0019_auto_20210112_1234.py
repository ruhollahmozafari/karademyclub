# Generated by Django 3.1.4 on 2021-01-12 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20210110_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='read',
        ),
        migrations.AddField(
            model_name='notification',
            name='view',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)]),
        ),
    ]
