# Generated by Django 3.1.4 on 2021-01-13 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20210113_2147'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='report',
            name='duplicate_report',
        ),
    ]
