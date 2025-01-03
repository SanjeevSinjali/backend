# Generated by Django 5.1.3 on 2024-12-24 15:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='jobmodel',
            name='posted_by',
            field=models.ForeignKey(limit_choices_to={'user_role': 'provider'}, on_delete=django.db.models.deletion.CASCADE, related_name='posted_jobs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobslikedmodel',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='jobs.jobmodel'),
        ),
        migrations.AddField(
            model_name='jobslikedmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='jobslikedmodel',
            unique_together={('user', 'job')},
        ),
    ]
