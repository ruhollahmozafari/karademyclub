# Generated by Django 3.1.4 on 2020-12-16 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubuser', '0007_auto_20201214_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubuser',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
