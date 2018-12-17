from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the Wine Reviews index page.")


class AboutPageView(generic.TemplateView):
    template_name = 'winereviews/about.html'


class HomePageView(generic.TemplateView):
    template_name = 'winereviews/home.html'


class WineListView(generic.ListView):
    model = Wine
    context_object_name = 'wines'
    template_name = 'winereviews/wine.html'
    paginate_by = 50

    def get_queryset(self):
        return Wine.objects.all().select_related('region1').order_by('wine_name')# TODO write ORM code to retrieve all Heritage Sites

class WineDetailView(generic.DetailView):
    model = Wine
    context_object_name = 'wine'
    template_name = 'winereviews/wine_detail.html'# TODO add the correct template string value