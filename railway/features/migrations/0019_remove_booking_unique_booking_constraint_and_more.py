# Generated by Django 4.1.7 on 2023-03-15 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0018_remove_booking_unique_booking_constraint_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='booking',
            name='unique_booking_constraint',
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(fields=('train', 'seat_number', 'booking_date'), name='unique_booking_constraint'),
        ),
    ]