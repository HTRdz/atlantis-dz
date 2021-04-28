# Generated by Django 3.1.4 on 2020-12-29 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('atlhotel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextSousPageAr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('texte', models.TextField(blank=True, null=True)),
                ('etiquette', models.CharField(blank=True, max_length=300, null=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True)),
                ('sous_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atlhotel.souspage')),
            ],
        ),
        migrations.CreateModel(
            name='TextPageAr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('texte', models.TextField(blank=True, null=True)),
                ('etiquette', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atlhotel.page')),
            ],
        ),
    ]
