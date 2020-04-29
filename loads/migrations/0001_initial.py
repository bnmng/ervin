# Generated by Django 3.0.5 on 2020-04-27 12:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Builder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='the name of the builder', max_length=50, verbose_name='Name')),
                ('notes', models.TextField(blank=True, help_text='any notes about this builder (contact info, etc)', verbose_name='Notes')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(help_text='the name of the job', max_length=100, verbose_name='Job Name')),
                ('ponumber', models.CharField(help_text='our PO number', max_length=50, verbose_name='PO Number')),
                ('sponumber', models.CharField(help_text="the supplier's PO number", max_length=50, verbose_name='Suppliers PO Number')),
                ('location', models.CharField(blank=True, help_text='the location of this load', max_length=100, verbose_name='Location')),
                ('notes', models.TextField(blank=True, help_text='notes or details associated with this load', verbose_name='Notes and Details')),
                ('mod_date', models.DateField(default=datetime.date.today, help_text='the date this was last modified', verbose_name='Date Modified')),
                ('builder', models.ForeignKey(blank=True, help_text='the builder for this load', null=True, on_delete=django.db.models.deletion.SET_NULL, to='loads.Builder')),
            ],
            options={
                'ordering': ('-mod_date',),
            },
        ),
        migrations.CreateModel(
            name='NotificationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the group', max_length=50, verbose_name='Group Name')),
                ('emails', models.TextField(blank=True, help_text='The emails to notify when a new load of this group is created', verbose_name='Notification Emails')),
            ],
            options={
                'verbose_name': 'notification group',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='the title of this photo', max_length=50, verbose_name='Title')),
                ('description', models.CharField(blank=True, help_text='the description of this photo', max_length=255, verbose_name='Description')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, help_text='the date and time of this photo', verbose_name='Updated')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='the name of this status', max_length=50, verbose_name='Name')),
                ('send_email', models.BooleanField(default=True, help_text='if an email should be sent when a load changes to this status', verbose_name='Send Email')),
                ('order', models.IntegerField(blank=True, help_text='where this status should be displayed on a list of statuses', null=True, verbose_name='Display Order')),
            ],
            options={
                'verbose_name': 'satus',
                'verbose_name_plural': 'statuses',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='the name of the supplier', max_length=50, verbose_name='Name')),
                ('notes', models.TextField(blank=True, help_text='any notes about this supplier (contact info, etc)', verbose_name='Notes')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='The name for this type of work', max_length=30, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='UserParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, help_text='The name of the setting', max_length=130, verbose_name='value')),
                ('value', models.TextField(blank=True, help_text='The value of the setting', verbose_name='value')),
                ('user', models.ForeignKey(blank=True, help_text='The user associated with the setting', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_parameter', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='LoadHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, help_text='The date this record was created', verbose_name='date')),
                ('description', models.TextField(blank=True, help_text='The description of what happened', verbose_name='description')),
                ('load', models.ForeignKey(blank=True, help_text='the initial load record for this update', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='history', to='loads.Load')),
            ],
            options={
                'ordering': ['load', '-date'],
            },
        ),
        migrations.AddField(
            model_name='load',
            name='notification_group',
            field=models.ManyToManyField(help_text='The groups to which this load belongs', to='loads.NotificationGroup', verbose_name='Notification Group'),
        ),
        migrations.AddField(
            model_name='load',
            name='status',
            field=models.ForeignKey(blank=True, help_text='the status of this load', null=True, on_delete=django.db.models.deletion.SET_NULL, to='loads.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='load',
            name='supplier',
            field=models.ForeignKey(blank=True, help_text='the supplier for this load', null=True, on_delete=django.db.models.deletion.SET_NULL, to='loads.Supplier'),
        ),
        migrations.AddField(
            model_name='load',
            name='work_type',
            field=models.ForeignKey(blank=True, help_text='the type of work to be done with this job', null=True, on_delete=django.db.models.deletion.SET_NULL, to='loads.WorkType', verbose_name='Work Type'),
        ),
    ]