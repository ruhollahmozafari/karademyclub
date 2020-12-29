# Generated by Django 3.1.4 on 2020-12-30 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20201229_2331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='reprted_date',
            new_name='report_date',
        ),
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.CharField(choices=[('not related to programing', 'not related to programing'), ('insulting', 'insulting'), ('sexual matters', 'sexual matters'), ('wrong answer', 'wrong answer'), ('inappropiate', 'inappropiate'), ('other', 'other')], default='publish', max_length=35),
        ),
    ]
