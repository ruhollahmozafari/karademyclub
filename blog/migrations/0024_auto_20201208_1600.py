# Generated by Django 3.1.4 on 2020-12-08 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20201208_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubuser',
            name='gender',
            field=models.CharField(choices=[('male', 'آقا'), ('woman', 'خانم')], max_length=10, null=True),
        ),
    ]