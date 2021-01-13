# Generated by Django 3.1.4 on 2021-01-12 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20210112_1239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='published',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='published',
            new_name='active',
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='report',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.question'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(blank=True, choices=[('question liked', 'question likedd'), ('answer liked', 'answer liked'), ('action reported', 'action reported'), ('question answered', 'question answered'), ('question commented', 'question commented')], default='', max_length=35),
        ),
    ]
