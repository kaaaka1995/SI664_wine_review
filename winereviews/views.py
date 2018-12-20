from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse_lazy
from .models import *

from .filters import WineFilter
from django_filters.views import FilterView

from .forms import WineForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView


def index(request):
    return HttpResponse("Hello, world. You're at the Wine Reviews index page.")


class AboutPageView(generic.TemplateView):
    template_name = 'winereviews/about.html'


class HomePageView(generic.TemplateView):
    template_name = 'winereviews/home.html'

@method_decorator(login_required, name='dispatch')
class WineListView(generic.ListView):
    model = Wine
    context_object_name = 'wines'
    template_name = 'winereviews/wine.html'
    paginate_by = 50

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Wine.objects.all().select_related('region1').order_by('wine_name')# TODO write ORM code to retrieve all Heritage Sites


@method_decorator(login_required, name='dispatch')
class WineDetailView(generic.DetailView):
    model = Wine
    context_object_name = 'wine'
    template_name = 'winereviews/wine_detail.html'# TODO add the correct template string value

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



@method_decorator(login_required, name='dispatch')
class WineCreateView(generic.View):
    model = Wine
    form_class = WineForm
    success_message = "Wine created successfully"
    template_name = 'winereviews/wine_new.html'
    # fields = '__all__' <-- superseded by form_class
    # success_url = reverse_lazy('heritagesites/site_list')

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = WineForm(request.POST)
        if form.is_valid():
            wine = form.save(commit=False)
            wine.save()
            for taster in form.cleaned_data['taster']:
            # for description in form.clean_description_list['description_list']:
                WineReview.objects.create(wine=wine, taster=taster)
            return redirect(wine) # shortcut to object's get_absolute_url()
            # return HttpResponseRedirect(site.get_absolute_url())
        return render(request, 'winereviews/wine_new.html', {'form': form})

    def get(self, request):
        form = WineForm()
        return render(request, 'winereviews/wine_new.html', {'form': form})

# class WineCreateView(generic.View):
#     model = Wine
#     form_class = WineForm
#     success_message = "New wine created successfully"
#     template_name = 'winereviews/wine_new.html'
#     # fields = '__all__' <-- superseded by form_class
#     # success_url = reverse_lazy('heritagesites/site_list')

#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         form = WineForm(request.POST)
#         if form.is_valid():
#             wine = form.save(commit=False)
#             wine.save()
#             for taster in form.cleaned_data['taster']:
#                 #WineReview.objects.create(wine=wine, taster=taster, description=description)
#                 WineReview.objects.create(wine=wine, taster=taster)
#             return redirect(wine) # shortcut to object's get_absolute_url()
#             # return HttpResponseRedirect(site.get_absolute_url())
#         return render(request, 'winereviews/wine_new.html', {'form': form})

#     def get(self, request):
#         form = WineForm()
#         return render(request, 'winereviews/wine_new.html', {'form': form})



@method_decorator(login_required, name='dispatch')
class WineUpdateView(generic.UpdateView):
    model = Wine
    form_class = WineForm
    # fields = '__all__' <-- superseded by form_class
    context_object_name = 'wine'
    # pk_url_kwarg = 'site_pk'
    success_message = "Wine updated successfully"
    template_name = 'winereviews/wine_update.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        wine = form.save(commit=False)
        # site.updated_by = self.request.user
        # site.date_updated = timezone.now()
        wine.save()

        # Current country_area_id values linked to site
        old_ids = WineReview.objects\
            .values_list('taster_id', flat=True)\
            .filter(wine_id=wine.wine_id)

        # New countries list
        new_taster = form.cleaned_data['taster']

        # TODO can these loops be refactored?

        # New ids
        new_ids = []

        # Insert new unmatched country entries
        for tas in new_taster:
            new_id = tas.taster_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                WineReview.objects \
                    .create(wine=wine, taster=tas)

        # Delete old unmatched country entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                WineReview.objects \
                    .filter(wine_id=wine.wine_id, taster_id=old_id) \
                    .delete()

        return HttpResponseRedirect(wine.get_absolute_url())
        # return redirect('heritagesites/site_detail', pk=site.pk)


@method_decorator(login_required, name='dispatch')
class WineDeleteView(generic.DeleteView):
    model = Wine
    success_message = "Wine deleted successfully"
    success_url = reverse_lazy('wine')
    context_object_name = 'wine'
    template_name = 'winereviews/wine_delete.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Delete HeritageSiteJurisdiction entries
        WineReview.objects \
            .filter(wine_id=self.object.wine_id) \
            .delete()

        self.object.delete()

        return redirect('wines')
        #return HttpResponseRedirect(self.get_success_url())

class WineFilterView(FilterView):
    filterset_class = WineFilter
    template_name = 'winereviews/wine_filter.html'
