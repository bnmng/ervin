from .models import (Builder, Load, NotificationGroup, Photo, Status, Supplier,)
from datetime import date, timedelta
from django import forms
from django.forms import ModelForm 
from django.urls import reverse_lazy
from addable.forms import Addable, AddableMultiple

class LoadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['mod_date'] = date.today 

    class Meta:
        model=Load
        fields = [
            'notification_group',
            'job_name',
            'ponumber',
            'builder',
            'supplier',
            'sponumber',
            'do_install',
            'status',
            'location',
            'notes',
            'mod_date',
        ]
        widgets = {
            'builder': Addable(attrs={'data-add_url':reverse_lazy('load_ajax_builder'), 'data-iframe':'iframe_builder', 'data-primaries':'id_builder', 'data-secondaries':''}),
            'supplier': Addable(attrs={'data-add_url':reverse_lazy('load_ajax_supplier'), 'data-iframe':'iframe_supplier', 'data-primaries':'id_supplier', 'data-secondaries':''}),
            'notification_group': AddableMultiple(attrs={'data-add_url':reverse_lazy('load_ajax_notification_group'), 'data-iframe':'iframe_notification_group', 'data-primaries':'id_notification_group', 'data-secondaries':''}),
        }

class NotificationGroupForm(ModelForm):
    class Meta:
        model = NotificationGroup
        fields = [
            'name',
            'emails',
        ]

class BuilderForm(ModelForm):
    class Meta:
        model = Builder
        fields = [
            'name',
            'notes',
        ]

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name',
            'notes',
        ]


# vim ai et ts=4 sts=4 sw=4
