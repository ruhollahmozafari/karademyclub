# Generated by Django 3.1.4 on 2020-12-14 14:48

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_auto_20201214_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
