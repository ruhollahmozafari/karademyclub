# Generated by Django 3.1.4 on 2020-12-11 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20201208_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubuser',
            name='interest',
        ),
    ]
