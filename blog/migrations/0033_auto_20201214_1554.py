# Generated by Django 3.1.4 on 2020-12-14 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_auto_20201214_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='blog.Tag'),
        ),
    ]
