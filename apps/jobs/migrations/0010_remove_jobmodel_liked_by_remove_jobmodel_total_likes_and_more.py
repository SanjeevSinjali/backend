# Generated by Django 5.1.3 on 2024-12-15 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_jobmodel_liked_by_jobmodel_total_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobmodel',
            name='liked_by',
        ),
        migrations.RemoveField(
            model_name='jobmodel',
            name='total_likes',
        ),
        migrations.AddField(
            model_name='jobmodel',
            name='liked_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
