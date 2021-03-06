# Generated by Django 3.1.4 on 2021-02-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlhotel', '0006_reservation_roomsprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='date_arrival',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='date_departure',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='np',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
