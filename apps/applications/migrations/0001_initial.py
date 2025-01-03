# Generated by Django 5.1.3 on 2024-12-24 16:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(upload_to='applications/cvs/%Y/%m/%d/')),
                ('cover_letter', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('shortlisted', 'Shortlisted'), ('rejected', 'Rejected'), ('hired', 'Hired')], default='pending', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('interview_scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('applicant', models.ForeignKey(limit_choices_to={'user_role': 'seeker'}, on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobs.jobmodel')),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
                'constraints': [models.UniqueConstraint(fields=('job', 'applicant'), name='unique_application_per_job')],
            },
        ),
    ]
