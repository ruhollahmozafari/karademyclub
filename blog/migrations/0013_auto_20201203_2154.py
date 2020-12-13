# Generated by Django 3.1.4 on 2020-12-03 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20201203_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='total_like',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='clubuser',
            name='gender',
            field=models.CharField(choices=[('male', 'آقا'), ('woman', 'خانم')], max_length=10, null=True),
        ),
    ]