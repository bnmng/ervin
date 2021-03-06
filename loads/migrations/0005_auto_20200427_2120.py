# Generated by Django 3.0.5 on 2020-04-27 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loads', '0004_remove_load_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverystatus',
            name='is_canceled',
            field=models.BooleanField(default=False, help_text='if this is the status to set if the "canceled" button is clicked', verbose_name='Is Canceled'),
        ),
        migrations.AddField(
            model_name='deliverystatus',
            name='is_complete',
            field=models.BooleanField(default=False, help_text='if this is the status to set if the "complete" button is clicked', verbose_name='Is Complete'),
        ),
        migrations.AddField(
            model_name='installationstatus',
            name='is_canceled',
            field=models.BooleanField(default=False, help_text='if this is the status to set if the "canceled" button is clicked', verbose_name='Is Canceled'),
        ),
        migrations.AddField(
            model_name='installationstatus',
            name='is_complete',
            field=models.BooleanField(default=False, help_text='if this is the status to set if the "complete" button is clicked', verbose_name='Is Complete'),
        ),
        migrations.AddField(
            model_name='receiptstatus',
            name='is_canceled',
            field=models.BooleanField(default=False, help_text='if this is the status to set if the "canceled" button is clicked', verbose_name='Is Canceled'),
        ),
        migrations.AddField(
            model_name='receiptstatus',
            name='is_complete',
            field=models.BooleanField(default=False, help_text='if this is the status to set if the "complete" button is clicked', verbose_name='Is Complete'),
        ),
    ]
