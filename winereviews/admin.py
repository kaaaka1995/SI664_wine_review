from django.contrib import admin

import winereviews.models as models


@admin.register(models.Wine)
class WineAdmin(admin.ModelAdmin):
    fields = [
        'wine_name',
        (
            'variety',
            'region1'
        ),
        'points',
        'price'
    ]

    list_display = [
        'wine_name',
        'variety',
        'region1',
        'points',
        'price'
    ]

    list_filter = ['variety', 'points', 'price', 'region1']

# admin.site.register(models.CountryArea)


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    fields = ['country_name']
    list_display = ['country_name']
    ordering = ['country_name']



@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    fields = ['province_name', 'country']
    list_display = ['province_name', 'country']
    ordering = ['province_name']


@admin.register(models.Region2)
class Region2Admin(admin.ModelAdmin):
    fields = ['region2_name', 'province']
    list_display = ['region2_name', 'province']
    ordering = ['region2_name']
# admin.site.register(models.IntermediateRegion)


@admin.register(models.Region1)
class Region1Admin(admin.ModelAdmin):
    fields = [
        'region1_name',
        (
            'province',
            'region2'
        )
    ]

    list_display = [
        'region1_name',
        'province',
        'region2'
    ]

    list_filter = ['province', 'region2']

@admin.register(models.Taster)
class TasterAdmin(admin.ModelAdmin):
    fields = ['taster_name','taster_twitter_handle']
    list_display = ['taster_name','taster_twitter_handle']
    ordering = ['taster_name']

@admin.register(models.Variety)
class VarietyAdmin(admin.ModelAdmin):
    fields = ['variety_name']
    list_display = ['variety_name']
    ordering = ['variety_name']


@admin.register(models.Winery)
class WineryAdmin(admin.ModelAdmin):
    fields = ['winery_name']
    list_display = ['winery_name']
    ordering = ['winery_name']
# admin.site.register(models.Region)

@admin.register(models.Vineyard)
class VineyardAdmin(admin.ModelAdmin):
    fields = ['vineyard_name']
    list_display = ['vineyard_name']
    ordering = ['vineyard_name']

