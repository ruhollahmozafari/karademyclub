# Generated by Django 3.1.4 on 2020-12-03 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20201203_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubuser',
            name='gender',
            field=models.CharField(choices=[('woman', 'خانم'), ('male', 'آقا')], max_length=10, null=True),
        ),
    ]
