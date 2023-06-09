# Generated by Django 4.1.5 on 2023-03-14 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0012_alter_route_serial_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='arrival_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='route',
            name='departure_time',
            field=models.DateTimeField(),
        ),
    ]
