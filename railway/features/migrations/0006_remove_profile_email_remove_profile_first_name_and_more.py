# Generated by Django 4.1.5 on 2023-03-12 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0005_profile_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
    ]