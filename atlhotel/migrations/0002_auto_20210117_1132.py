# Generated by Django 3.1.4 on 2021-01-17 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlhotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='langue',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='address_ar',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='address_en',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
