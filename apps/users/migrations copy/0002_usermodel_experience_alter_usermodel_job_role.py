# Generated by Django 5.1.3 on 2024-12-22 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='experience',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='job_role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
