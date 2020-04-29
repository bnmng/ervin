from django.urls import path
from .views import (DirectionsView, HomeView,)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('directions', DirectionsView.as_view(), name='directions'),
]

# vim: ai ts=4 sts=4 et sw=4
