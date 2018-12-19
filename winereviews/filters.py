import django_filters
from winereviews.models import *


class WineFilter(django_filters.FilterSet):
    wine_name = django_filters.CharFilter(
        field_name='wine_name',
        label='Wine Name',
        lookup_expr='icontains'
    )

    # Add description, heritage_site_category, region, sub_region and intermediate_region filters here

    region1 = django_filters.ModelChoiceFilter(
        field_name='region1__region1_name',
        label='Region',
        queryset= Region1.objects.all().order_by('region1_name'),
        lookup_expr='exact'
    )


    

    variety = django_filters.ModelChoiceFilter(
        field_name='variety',
        label='Variety',
        queryset=Variety.objects.all().order_by('variety_name'),
        lookup_expr='exact'
    )

    points = django_filters.NumericRangeFilter(
        field_name='points',
        label='Points',
        lookup_expr='range'
    )

    price = django_filters.NumericRangeFilter(
        field_name='price',
        label='Price',
        lookup_expr='range'
    )

    

  

    # Add date_inscribed filter here


    class Meta:
        model = Wine
        # form = SearchForm
        # fields [] is required, even if empty.
        fields = []