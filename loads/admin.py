from django.contrib import admin
from .models import (Builder, Load, NotificationGroup, LoadHistory, Status, Supplier, )

admin.site.register(LoadHistory)

admin.site.register(NotificationGroup)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'send_email', 'order')

admin.site.register(Status, StatusAdmin)

admin.site.register:(Builder)

admin.site.register(Supplier)


