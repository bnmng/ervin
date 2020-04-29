from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomeView(TemplateView):

    template_name = "home/home.html"

class DirectionsView(TemplateView):

    template_name = "home/directions.html"

# vim: ai et sts=4 sw=4 ts=4
