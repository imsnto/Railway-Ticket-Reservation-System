# Generated by Django 4.1.3 on 2023-03-26 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0027_delete_demo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='tr_arrival',
        ),
        migrations.RemoveField(
            model_name='train',
            name='tr_departure',
        ),
        migrations.RemoveField(
            model_name='train',
            name='tr_destination',
        ),
        migrations.RemoveField(
            model_name='train',
            name='tr_source',
        ),
    ]