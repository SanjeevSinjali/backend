# Generated by Django 5.1.3 on 2024-12-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_alter_companymodel_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymodel',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]