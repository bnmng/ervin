from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from datetime import date

class Status(models.Model):
    name = models.CharField('Name',max_length=50, blank=True, help_text='the name of this status')
    send_email = models.BooleanField('Send Email', default=True, help_text='if an email should be sent when a load changes to this status')
    order = models.IntegerField('Display Order', null=True, blank=True, help_text='where this status should be displayed on a list of statuses')
    is_complete = models.BooleanField('Is Complete', default=False, help_text='if this the completion status')
    is_canceled = models.BooleanField('Is Canceled', default=False, help_text='if this the cancelation status')

    class Meta:
        verbose_name = 'satus'
        verbose_name_plural = 'statuses'
        ordering = ['order']

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField('Name', max_length=50, help_text='the name of the supplier')
    notes = models.TextField('Notes', blank=True, help_text='any notes about this supplier (contact info, etc)')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Builder(models.Model):
    name = models.CharField('Name', max_length=50, help_text='the name of the builder')
    notes = models.TextField('Notes', blank=True, help_text='any notes about this builder (contact info, etc)')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class NotificationGroup(models.Model):
    name = models.CharField('Group Name', max_length=50, help_text='The name of the group')
    emails = models.TextField('Notification Emails', blank=True, help_text='The emails to notify when a new load of this group is created')

    class Meta:
        verbose_name = "notification group"
        ordering = ('name',)

    def __str__(self):
        return self.name

class Load(models.Model):

    notification_group = models.ManyToManyField(NotificationGroup, blank=True, verbose_name="Notification Group", help_text='The groups to which this load belongs')
    job_name = models.CharField('Job Name', max_length=100, help_text='the name of the job')
    ponumber = models.CharField('PO Number', max_length=50, help_text='our PO number')
    description = models.CharField('Description', max_length=255, blank=True, help_text='The description of this load')
    builder = models.ForeignKey(Builder, on_delete=models.SET_NULL, null=True, blank=True, help_text='the builder for this load')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, help_text='the supplier for this load')
    sponumber = models.CharField('Suppliers PO Number', blank=True, max_length=50, help_text='the supplier\'s PO number')
    do_install = models.BooleanField('Install?', default=False, help_text='if we are to install this')
    status = models.ManyToManyField(Status, help_text='the status of this load')
    location = models.CharField('Location', max_length=100, blank=True, help_text='the location of this load')
    notes = models.TextField('Notes and Details',  blank=True, help_text='notes or details associated with this load')
    mod_date = models.DateField('Date Modified', default=date.today, help_text='the date this was last modified')
    photo = models.URLField('Photo',blank=True,help_text='A link to a photo')

    class Meta:
        ordering = ('-mod_date',)

    def get_absolute_url(self):
        return reverse('load-detail', kwargs = {'pk': self.pk}) 

    def __str__(self):
        return (str(self.ponumber))


class LoadHistory(models.Model):
    load = models.ForeignKey('Load', related_name='history', on_delete=models.SET_NULL, null=True, blank=True, help_text='the initial load record for this update')
    date = models.DateTimeField('date', auto_now_add=True, help_text='The date this record was created')
    description = models.TextField('description', blank=True, help_text='The description of what happened')

    def __str__(self):
        return "{:%Y%B%d} - {} - {}".format(self.date, self.load, self.description)

    class Meta:
        ordering = ['load', '-date']

class Photo(models.Model):
	title = models.CharField('Title', max_length=50, blank=True, help_text='the title of this photo')
	description = models.CharField('Description', max_length=255, blank=True, help_text='the description of this photo')
	date = models.DateTimeField('Updated', default=timezone.now, help_text='the date and time of this photo')

class UserParameter(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, verbose_name="user", on_delete=models.SET_NULL, help_text="The user associated with the setting", null=True, blank=True, related_name="inventory_parameter", ) 
    key = models.CharField( "value", max_length=130, help_text="The name of the setting", blank=True ) 
    value = models.TextField("value", help_text="The value of the setting", blank=True)

# vim: ai ts=4 sts=4 et sw=4
