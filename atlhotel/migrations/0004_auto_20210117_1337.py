# Generated by Django 3.1.4 on 2021-01-17 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlhotel', '0003_hotel_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='facebook_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='instagram_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='tripadvisor_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='youtube_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]