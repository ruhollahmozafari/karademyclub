# Generated by Django 3.1.4 on 2020-12-03 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20201203_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubuser',
            name='gender',
            field=models.CharField(choices=[('male', 'آقا'), ('woman', 'خانم')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(blank=True, default='', null=True, unique=True),
        ),
    ]