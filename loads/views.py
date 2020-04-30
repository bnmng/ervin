import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from datetime import date, timedelta
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import ( DetailView, )
from django.views.generic.edit import (CreateView, DeleteView, UpdateView,)
from django.views.generic.list import ListView
from loads.forms import (BuilderForm, LoadForm, NotificationGroupForm, SupplierForm )
from loads.models import(Builder, Load, LoadHistory, NotificationGroup, Photo, Status, Supplier, UserParameter,  )
import copy
import json
import sys

class LoadList(PermissionRequiredMixin, ListView):
    permission_required = "loads.view_load"
    model = Load
    paginate_by=10

    filter_parameter_specs = {
        'job_name_': {
            'label': "Job Name",
            'operators': {
                'job_name__icontains': {'label': 'Contains',},
                'job_name__iexact': {'label': 'Equals',},
            },
        },
        'ponumber_': {
            'label': "PO Number",
            'operators': {
                'ponumber__icontains': {'label': 'Contains',},
                'sponumber__iexact': {'label': 'Equals',},
            },
        },
        'do_install_': {
            'label': "Install",
            'operators': {
                'do_install__exact': {'label': 'Is',},
            },
        },
        'builder': {
            'label': 'Builder',
            'operators': {
                'builder__in': {'label': 'is',},
            },
            'input': {
                'type': 'select',
                'multiple': 'multiple',
                'option_type': 'model',
                'options': Builder.objects.all(),
            },
        },
        'supplier': {
            'label': 'Supplier',
            'operators': {
                'supplier__in': {'label': 'is',},
            },
            'input': {
                'type': 'select',
                'multiple': 'multiple',
                'option_type': 'model',
                'options': Supplier.objects.all(),
            },
        },
        'sponumber_': {
            'label': "SPO Number",
            'operators': {
                'sponumber__icontains': {'label': 'Contains',},
                'sponumber__iexact': {'label': 'Equals',},
            },
        },
        'status_': {
            'label': 'Status',
            'operators': {
                'status__in': {'label': 'Is',},
            },
            'input': {
                'type': 'select',
                'multiple': 'multiple',
                'option_type': 'model',
                'options': Status.objects.all(),
            },
            'default': {
                Status.objects.filter(is_complete=False, is_canceled=False)
            }
        },
        'notification_group_': {
            'label': "Notification Group",
            'operators': {
                'notification_group__in': {'label': 'Is',},
            },
            'input': {
                'type': 'select',
                'multiple': 'multiple',
                'option_type': 'model',
                'options': NotificationGroup.objects.all(),
            },
        },
        'location_': {
            'label': 'Location',
            'operators': {
                'location__icontains': {'label': 'Contains',},
                'location__iexact': {'label': 'Equals',},
            },
        },
        'notes_': {
            'label': 'Notes',
            'operators': {
                'sponumber__icontains': {'label': 'Contains',},
            },
        },
        'mod_date_': {
            'label': "Mod Date",
            'operators': {
                'mod_date__range': {'label': 'Between',},
            },
            'input': {
                'type': 'dates',
            },
        }
    }
    orderby_parameter_specs = {
        'job_name_': {
            'label': "Job Name",
        },
        'ponumber_': {
            'label': "PO Number",
        },
        'do_install_': {
            'label': "Install?",
        },
        'builder': {
            'label': 'Builder',
        },
        'supplier': {
            'label': 'Supplier',
        },
        'sponumber_': {
            'label': "SPO Number",
        },
        'status_': {
            'label': 'Status',
        },
        'notification_group_': {
            'label': "Notification Group",
        },
        'location_': {
            'label': 'Location',
        },
        'mod_date_': {
            'label': "Mod Date",
        }
    }

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        user_parameters, created = UserParameter.objects.get_or_create(user=self.request.user, key='previous_query')
        user_parameters.save()
        constructed_query_data = {}
        print ('self.request.GET.keys()')
        print (self.request.GET.keys())
        set_default=False
        has_filter=False
        has_order_by=False
        has_paginate_by=False
        if self.request.GET:
            for key in self.request.GET.keys():
                if key.find('default') == 0:
                    set_default=True
                if key.find('filter') == 0:
                    has_filter=True
                if key.find('order_by') == 0:
                    has_order_by=True
                if key.find('paginate_by') == 0:
                    has_paginate_by=True
                if set_default and has_paginate_by:
                    break

        if set_default:

            for filterkey in self.filter_parameter_specs:
                if 'default' in filter_parameter_specs[filterkey]:
                    constructed_query_data['filter'][filterkey] = filter_parameter_specs['default']



#            for r in range(1, 4):
#                if "orderby[" + str(r) + "]" in get_dict:
#                    if not 'orderby' in constructed_query_data:
#                        constructed_query_data['orderby'] = []
#                    constructed_query_data['orderby'].append(
#                        get_dict["orderby[" + str(r) + "]"][0]
#                    )

            # save the query in the UserParameters object
            constructed_query_json = json.dumps(constructed_query_data)
            user_parameters.value = constructed_query_json
            user_parameters.save()

        elif has_filter:

            # convert the GET querydict into a regular dictionary

            get_list = self.request.GET.lists()
            get_dict = {}
            for key in get_list:
                get_dict[key[0]] = key[1]

            for filterkey in self.filter_parameter_specs:
                if "filter[" + filterkey + "][use]" in get_dict:
                    if 'on' == get_dict["filter[" + filterkey + "][use]"][0]:
                        if not 'filter' in constructed_query_data:
                            constructed_query_data['filter'] = {}
                        if not filterkey in constructed_query_data['filter']:
                            constructed_query_data['filter'][filterkey] = {}
                        constructed_query_data['filter'][filterkey]['use'] = 'on'
                if "filter[" + filterkey + "][value]" in get_dict:
                    if not 'filter' in constructed_query_data:
                        constructed_query_data['filter'] = {}
                    if not filterkey in constructed_query_data['filter']:
                        constructed_query_data['filter'][filterkey] = {}
                    as_multi = False
                    if 'input' in self.filter_parameter_specs[filterkey]:
                        if ('multiple' in self.filter_parameter_specs[filterkey]['input']):
                            if ('multiple' == self.filter_parameter_specs[filterkey]['input']['multiple']):
                                constructed_query_data['filter'][filterkey]['value'] = get_dict["filter[" + filterkey + "][value]"]
                                as_multi = True
                    if not as_multi:
                        constructed_query_data['filter'][filterkey]['value'] = get_dict["filter[" + filterkey + "][value]"][0]
                if "filter[" + filterkey + "][operators]" in get_dict:
                    for optkey in self.filter_parameter_specs[filterkey]['operators']:
                        if (optkey == get_dict["filter[" + filterkey + "][operators]"][0]):
                            if not 'filter' in constructed_query_data:
                                constructed_query_data['filter'] = {}
                            if not filterkey in constructed_query_data['filter']:
                                constructed_query_data['filter'][filterkey] = {}
                            if (not 'operators' in constructed_query_data['filter'][filterkey]):
                                constructed_query_data['filter'][filterkey]['operators'] = {}
                            if (not optkey in constructed_query_data['filter'][filterkey]['operators']):
                                constructed_query_data['filter'][filterkey]['operators'][optkey] = {}
                            constructed_query_data['filter'][filterkey]['operators'][optkey]['use'] = 'on'


            for r in range(1, 4):
                if "orderby[" + str(r) + "]" in get_dict:
                    if not 'orderby' in constructed_query_data:
                        constructed_query_data['orderby'] = []
                    constructed_query_data['orderby'].append(
                        get_dict["orderby[" + str(r) + "]"][0]
                    )

            # save the query in the UserParameters object
            constructed_query_json = json.dumps(constructed_query_data)
            user_parameters.value = constructed_query_json
            user_parameters.save()


        else:  # if no GET, look for the recent query from the UserParameters
            try:
                constructed_query_data = json.loads(user_parameters.value)
            except:
                constructed_query_data = {}

        try:  # filter the record
            if 'filter' in constructed_query_data:
                for filterkey in self.filter_parameter_specs:
                    if filterkey in constructed_query_data['filter']:
                        if 'use' in constructed_query_data['filter'][filterkey]:
                            if ('on' == constructed_query_data['filter'][filterkey]['use']):
                                for optkey in self.filter_parameter_specs[filterkey]['operators']:
                                    if (optkey in constructed_query_data['filter'][filterkey]['operators']):
                                        if ('use' in constructed_query_data['filter'][filterkey]['operators'][optkey]):
                                            if ('on' == constructed_query_data['filter'][filterkey]['operators'][optkey]['use']):
                                                if ('value' in constructed_query_data['filter'][filterkey]):
                                                    try:
                                                        queryset = queryset.filter(**{optkey: constructed_query_data['filter'][filterkey]['value']})
                                                    except ValueError:
                                                        print('sys.exc_info()[0]:')
                                                        print(sys.exc_info()[0])
                                                        print('sys.exc_info()[1]:')
                                                        print(sys.exc_info()[1])
                                                        print('sys.exc_info()[2].tb_lineno:')
                                                        print(sys.exc_info()[2].tb_lineno)
                                                        try:
                                                            constructed_query_data['filter'][filterkey]['operators'][optkey]['use'] = ''
                                                        except:
                                                            print('Error turning off ' + optkey )

                                                    # todo: refactor this so it filters in one step

#            if 'orderby' in constructed_query_data:
#                queryset = queryset.order_by(*constructed_query_data['orderby'])
        except Exception as e:
            print('sys.exc_info()[0]:')
            print(sys.exc_info()[0])
            print('sys.exc_info()[1]:')
            print(sys.exc_info()[1])
            print('sys.exc_info()[2].tb_lineno:')
            print(sys.exc_info()[2].tb_lineno)
            user_search_data = {}

        return queryset

    def get_context_data(self, **kwargs):

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print( 'BASE_DIR=')
        print( BASE_DIR)

        context_data = super().get_context_data()

        user_parameters, created = UserParameter.objects.get_or_create(user=self.request.user, key='previous_query')
        try:
            user_query_data = json.loads(user_parameters.value)
        except:
            user_query_data = {}

        context_data['filter_parameters'] = copy.deepcopy(self.filter_parameter_specs)
        if 'filter' in user_query_data:
            for filterkey in self.filter_parameter_specs:
                try:
                    if filterkey in user_query_data['filter']:
                        if 'use' in user_query_data['filter'][filterkey]:
                            if 'on' == user_query_data['filter'][filterkey]['use']:
                                context_data['filter_parameters'][filterkey]['use'] = 'on'
                        if 'value' in user_query_data['filter'][filterkey]:
                            input_handled = False
                            if 'input' in self.filter_parameter_specs[filterkey]:
                                if ('option_type' in self.filter_parameter_specs[filterkey]['input']):
                                    if ('model' == self.filter_parameter_specs[filterkey]['input']['option_type']):
                                        multiple=''
                                        if ('multiple' in self.filter_parameter_specs[filterkey]['input']):
                                            if ('multiple' == self.filter_parameter_specs[filterkey]['input']['multiple']):
                                                multiple='multiple'
                                        if( 'multiple' == multiple ):
                                            values=[]
                                            for option in user_query_data['filter'][filterkey]['value']:
                                                if(option.isdigit()):
                                                    values.append(int(option))
                                            context_data['filter_parameters'][filterkey]['value']=values
                                            input_handled = True
                                        else:
                                            if(user_query_data['filter'][filterkey]['value'].isdigit()):
                                                context_data['filter_parameters'][filterkey]['value'] = user_query_data['filter'][filterkey]['value']
                                                input_handled = True

                            if not input_handled:
                                context_data['filter_parameters'][filterkey]['value'] = user_query_data['filter'][filterkey]['value']
                        if 'operators' in user_query_data['filter'][filterkey]:
                            for optkey in user_query_data['filter'][filterkey]['operators']:
                                if ('use' in user_query_data['filter'][filterkey]['operators'][optkey]):
                                    if ('on' == user_query_data['filter'][filterkey]['operators'][optkey]['use']):
                                        context_data['filter_parameters'][filterkey]['operators'][optkey]['use'] = 'on'

                                        if 'use' in user_query_data['filter'][filterkey]:
                                            if 'on' == user_query_data['filter'][filterkey]['use']:
                                                if 'filter_display' in context_data:
                                                    context_data['filter_display'] = context_data['filter_display'] + ' AND '
                                                else:
                                                    context_data['filter_display'] = ''
                                                context_data['filter_display'] = context_data['filter_display'] + self.filter_parameter_specs[filterkey]['label']
                                                context_data['filter_display'] = context_data['filter_display'] + ' ' +  self.filter_parameter_specs[filterkey]['operators'][optkey]['label'] 
                                                input_handled = False
                                                if 'input' in self.filter_parameter_specs[filterkey]:
                                                    if ('option_type' in self.filter_parameter_specs[filterkey]['input']):
                                                        if('model' == self.filter_parameter_specs[filterkey]['input']['option_type']):
                                                            multiple=''
                                                            if('multiple' in self.filter_parameter_specs[filterkey]['input']):
                                                                if('multiple' == self.filter_parameter_specs[filterkey]['input']['multiple']):
                                                                    display_values=[]
                                                                    for value in user_query_data['filter'][filterkey]['value']:
                                                                        display_values.append( self.filter_parameter_specs[filterkey]['input']['options'].filter(pk=value).get().__str__())
                                                                    context_data['filter_display'] = context_data['filter_display'] + ' ' +  ', '.join(display_values)
                                                                    input_handled=True
                                                                else:
                                                                    diplay_values = display_values + self.filter_parameter_specs[filterkey]['input']['options'].filter(pk=user_query_data['filter'][filterkey]['value'])[0]
                                                                    input_handled=True
                                                if not input_handled:
                                                    context_data['filter_display'] = context_data['filter_display'] + ' ' + str(user_query_data['filter'][filterkey]['value'])
                                                

                except Exception as e:
                    print('sys.exc_info()[0]:')
                    print(sys.exc_info()[0])
                    print('sys.exc_info()[1]:')
                    print(sys.exc_info()[1])
                    print('sys.exc_info()[2].tb_lineno')
                    print(sys.exc_info()[2].tb_lineno)
                    context_data['filter_parameters'][filterkey]['use'] = ""

#        context_data['orderby_parameters'] = copy.deepcopy(self.orderby_parameter_specs)
#        if 'orderby' in user_query_data:
#            for orderbykey in self.orderby_parameter_specs:
#                for r in range(0, 3):
#                    if r < len(user_query_data['orderby']):
#                        if orderbykey == user_query_data['orderby'][r]:
#                            if not orderbykey in context_data['orderby_parameters']:
#                                context_data['orderby_parameters'][orderbykey] = {}
#                            context_data['orderby_parameters'][orderbykey]['use'] = (r + 1)


        return context_data

class LoadCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'loads.add_load'
    model = Load
    form_class=LoadForm
    template_name='loads/load_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        description = 'Created: '
        firstloop=True
        for fieldname in form.cleaned_data:
            try:
                load_his = LoadHistory.objects.create(load=self.object, description = 'created with {} =  {}'.format(Load._meta.get_field(fieldname).verbose_name, form.cleaned_data[fieldname]))
            except:
                print ("Error creating history, fieldname=" + fieldname)
                print(sys.exc_info()[0])
                print(sys.exc_info()[1])
                print(sys.exc_info()[2].tb_lineno)
                
        load_his = LoadHistory(load=self.object, description=description)
        load_his.save()
        return response

    def get_success_url(self):
        return  reverse_lazy('load-created', kwargs={'pk': self.object.id})

class LoadUpdated(PermissionRequiredMixin, DetailView):
    permission_required = 'loads.view_load'
    model = Load

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if( self.kwargs.get('action')):
            context_data['action'] = self.kwargs.get('action')
        context_data['email_to'] = ''
        emails=[]
        for group in self.object.notification_group.all():
            split_emails = group.emails.split(',')
            for each_email in split_emails:
                each_email = each_email.strip()
                if each_email not in emails:
                    emails.append(each_email)
        
        context_data['email_to']=', '.join(emails)

        status_names_string=''

        for status in self.object.status.all():
            if status_names_string > '':
                status_names_string = status_names_string + ', '
            status_names_string = status_names_string + status.name 

        context_data['email_subject']='Load {} for {} {}'.format(self.object.ponumber, self.object.job_name, status_names_string),
        email_body=''
        email_body = email_body + 'Job: ' + self.object.job_name  + "\r\n"
        email_body = email_body + 'PO Number: ' + self.object.ponumber + "\r\n"
        if self.object.builder:
            email_body = email_body + 'Builder:' + self.object.builder.name + "\r\n"
        if self.object.supplier:
            email_body = email_body + 'Supplier:' + self.object.supplier.name + "\r\n"
        email_body = email_body + 'Suplier PO: ' + self.object.sponumber + "\r\n"
        if self.object.do_install:
            email_body = email_body + 'Install?: Yes' + "\r\n"
        else:
            email_body = email_body + 'Install?: No' + "\r\n"
        email_body = email_body + 'Status: ' + status_names_string + "\r\n"
        email_body = email_body + 'Location: ' + self.object.location + "\r\n"
        email_body = email_body + 'Notes: ' + self.object.notes  + "\r\n"
        context_data['email_body'] = email_body

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        for fieldname in form.changed_data:
            try:
                load_his = LoadHistory.objects.create(load=self.object, description = '{} changed from {} to {}'.format(Load._meta.get_field(fieldname).verbose_name, form.initial[fieldname], form.cleaned_data[fieldname]))
            except:
                print ("Error creating history, fieldname=" + fieldname)
                print(sys.exc_info()[0])
                print(sys.exc_info()[1])
                print(sys.exc_info()[2].tb_lineno)

        return response

class LoadDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'loads.view_load'
    model = Load

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        action = self.kwargs.get('action')
        if(action):
            print("action")
            print(action)
            context_data['action'] = action

        status_names_string=''

        for status in self.object.status.all():
            if status_names_string > '':
                status_names_string = status_names_string + ', '
            status_names_string = status_names_string + status.name 

        if 'created' == action:
            context_data['email_subject']='Load {} for {} added'.format(self.object.ponumber, self.object.job_name)
        else:
            context_data['email_subject']='Load {} for {} status changed to {}'.format(self.object.ponumber, self.object.job_name, status_names_string)

            context_data['email_to'] = ''
            emails=[]
            for group in self.object.notification_group.all():
                split_emails = group.emails.split(',')
                for each_email in split_emails:
                    each_email = each_email.strip()
                    if each_email not in emails:
                        emails.append(each_email)
            
            context_data['email_to']=', '.join(emails)

            email_body=''
            email_body = email_body + 'Job: ' + self.object.job_name  + "\r\n"
            email_body = email_body + 'PO Number: ' + self.object.ponumber + "\r\n"
            if self.object.builder:
                email_body = email_body + 'Builder:' + self.object.builder.name + "\r\n"
            if self.object.supplier:
                email_body = email_body + 'Supplier:' + self.object.supplier.name + "\r\n"
            email_body = email_body + 'Suplier PO: ' + self.object.sponumber + "\r\n"
            if self.object.do_install:
                email_body = email_body + 'Install?: Yes' + "\r\n"
            else:
                email_body = email_body + 'Install?: No' + "\r\n"
            email_body = email_body + 'Status: ' + status_names_string + "\r\n"
            email_body = email_body + 'Location: ' + self.object.location + "\r\n"
            email_body = email_body + 'Notes: ' + self.object.notes  + "\r\n"
            context_data['email_body'] = email_body

        return context_data

class LoadUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'loads.change_load'
    model = Load
    form_class = LoadForm
    template_name='loads/load_form.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        for fieldname in form.changed_data:
            try:
                item_his = ItemHistory.objects.create(item=self.object, description = '{} changed from {} to {}'.format(Item._meta.get_field(fieldname).verbose_name, form.initial[fieldname], form.cleaned_data[fieldname]))
            except:
                print ("Error creating history, fieldname=" + fieldname)
                print(sys.exc_info()[0])
                print(sys.exc_info()[1])
                print(sys.exc_info()[2].tb_lineno)
        
        return response


    def get_success_url(self):
        return reverse_lazy('load-updated', kwargs={'pk':self.object.pk})


class LoadDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'loads.delete_load'
    model = Load
    template_name = 'loads/load_delete.html'
    def get_success_url(self):
        return reverse_lazy('loads')


class LoadNotificationGroupAjax(PermissionRequiredMixin, CreateView):
    permission_required = "loads.add_notificationgroup"
    model = NotificationGroup
    form_class = NotificationGroupForm
    template_name = "loads/load_ajax_notification_group.html"

    def get_success_url(self):
        return reverse_lazy("load_ajaxsuccess_notification_group", kwargs={'pk': self.object.id})

class LoadNotificationGroupAjaxSuccess(PermissionRequiredMixin, UpdateView):
    permission_required = "loads.add_notificationgroup"
    model = NotificationGroup
    form_class = NotificationGroupForm
    template_name = "loads/load_ajax_notification_group.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['success'] = 'success'
        return context_data

class LoadBuilderAjax(PermissionRequiredMixin, CreateView):
    permission_required = "loads.add_builder"
    model = Builder
    form_class = BuilderForm
    template_name = "loads/load_ajax_builder.html"

    def get_success_url(self):
        return reverse_lazy("load_ajaxsuccess_builder", kwargs={'pk': self.object.id})

class LoadBuilderAjaxSuccess(PermissionRequiredMixin, DetailView):
    permission_required = "loads.add_builder"

    model = Builder
    template_name = "loads/load_ajax_builder.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['success'] = 'success'
        return context_data

class LoadSupplierAjax(PermissionRequiredMixin, CreateView):
    permission_required = "loads.add_supplier"
    model = Supplier
    form_class = SupplierForm
    template_name = "loads/load_ajax_supplier.html"

    def get_success_url(self):
        return reverse_lazy("load_ajaxsuccess_supplier", kwargs={'pk': self.object.id})

class LoadSupplierAjaxSuccess(PermissionRequiredMixin, DetailView):
    permission_required = "loads.add_supplier"

    model = Supplier
    template_name = "loads/load_ajax_supplier.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['success'] = 'success'
        return context_data

# vim: ai ts=4 sts=4 et sw=4
