# Generated by Django 3.0.5 on 2020-04-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='description',
            field=models.CharField(blank=True, help_text='The description of this load', max_length=255, verbose_name='Description'),
        ),
    ]
