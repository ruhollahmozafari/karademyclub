# Generated by Django 3.1.4 on 2021-01-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubuser', '0003_auto_20210121_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubuser',
            name='facebook',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clubuser',
            name='github',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clubuser',
            name='instagram',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clubuser',
            name='twitter',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clubuser',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
