# Generated by Django 3.1.4 on 2020-12-03 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20201203_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='total_like',
            field=models.IntegerField(default=0, null=True),
        ),
    ]