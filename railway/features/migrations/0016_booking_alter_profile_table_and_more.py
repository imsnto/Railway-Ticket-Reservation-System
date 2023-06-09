# Generated by Django 4.1.7 on 2023-03-15 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0015_alter_route_arrival_time_alter_route_departure_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_id', models.IntegerField()),
                ('seat_number', models.IntegerField()),
                ('booking_date', models.DateField()),
            ],
        ),
        migrations.AlterModelTable(
            name='profile',
            table='profile',
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(fields=('train_id', 'seat_number', 'booking_date'), name='unique_booking_constraint'),
        ),
    ]
