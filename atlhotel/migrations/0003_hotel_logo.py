# Generated by Django 3.1.4 on 2021-01-17 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlhotel', '0002_auto_20210117_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
