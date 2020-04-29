from django.urls import path
from loads.views import (LoadBuilderAjax, LoadBuilderAjaxSuccess, LoadCreate, LoadDelete, LoadDetail, LoadList, LoadNotificationGroupAjax, LoadNotificationGroupAjaxSuccess, LoadSupplierAjax, LoadSupplierAjaxSuccess, LoadUpdate, LoadUpdated, )

urlpatterns = [
    path('', LoadList.as_view(), name='loads'),
    path('create', LoadCreate.as_view(), name='load-create'),
    path('<int:pk>', LoadDetail.as_view(), name='load-detail'),
    path('<int:pk>/updated', LoadUpdated.as_view(), {'action':'updated'}, name='load-updated'),
    path('<int:pk>/created', LoadUpdated.as_view(), {'action':'created'}, name='load-created'),
    path('<int:pk>/update', LoadUpdate.as_view(), name='load-update'),
    path('<int:pk>/delete', LoadDelete.as_view(), name='load-delete'),
    path('load_ajax_builder', LoadBuilderAjax.as_view(), name='load_ajax_builder'),
    path('load_ajax_builder/<int:pk>', LoadBuilderAjaxSuccess.as_view(), name='load_ajaxsuccess_builder'),
    path('load_ajax_supplier', LoadSupplierAjax.as_view(), name='load_ajax_supplier'),
    path('load_ajax_supplier/<int:pk>', LoadSupplierAjaxSuccess.as_view(), name='load_ajaxsuccess_supplier'),
    path('load_ajax_notification_group', LoadNotificationGroupAjax.as_view(), name='load_ajax_notification_group'),
    path('load_ajax_notification_group/<int:pk>', LoadNotificationGroupAjaxSuccess.as_view(), name='load_ajaxsuccess_notification_group'),
]

# vim: ai ts=4 sts=4 et sw=4
