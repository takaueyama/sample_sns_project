# Generated by Django 4.1.5 on 2023-01-11 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='be_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='pre_be_read',
            field=models.BooleanField(default=False),
        ),
    ]
