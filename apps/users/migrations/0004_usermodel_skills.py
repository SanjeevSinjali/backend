# Generated by Django 5.1.3 on 2024-12-24 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_usermodel_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='skills',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
