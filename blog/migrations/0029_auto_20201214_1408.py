# Generated by Django 3.1.4 on 2020-12-14 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20201213_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
