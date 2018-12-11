# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'country'
        ordering = ['country_name']
        verbose_name = 'Origin Country'
        verbose_name_plural = 'Origin Countries'

    def __str__(self):
        return self.country_name



class Province(models.Model):
    province_id = models.AutoField(primary_key=True)
    province_name = models.CharField(unique=True, max_length=100)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'province'
        ordering = ['province_name']
        verbose_name = 'Origin Province'
        verbose_name_plural = 'Origin Provinces'

    def __str__(self):
        return self.province_name


class Region2(models.Model):
    region2_id = models.AutoField(primary_key=True)
    region2_name = models.CharField(unique=True, max_length=100)
    province = models.ForeignKey(Province, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region2'
        ordering = ['region2_name']
        verbose_name = 'Origin Region2'
        verbose_name_plural = 'Origin Region2'

    def __str__(self):
        return self.region2_name



class Region1(models.Model):
    region1_id = models.AutoField(primary_key=True)
    region1_name = models.CharField(unique=True, max_length=100)
    province = models.ForeignKey(Province, models.DO_NOTHING, blank=True, null=True)
    region2 = models.ForeignKey('Region2', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region1'
        ordering = ['region1_name']
        verbose_name = 'Origin Region1'
        verbose_name_plural = 'Origin Region1'

    def __str__(self):
        return self.region1_name





class Taster(models.Model):
    taster_id = models.AutoField(primary_key=True)
    taster_name = models.CharField(unique=True, max_length=100)
    taster_twitter_handle = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taster'
        ordering = ['taster_name']
        verbose_name = 'Taster'
        verbose_name_plural = 'Taster'

    def __str__(self):
        return self.taster_name


class Variety(models.Model):
    variety_id = models.AutoField(primary_key=True)
    variety_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'variety'
        ordering = ['variety_name']
        verbose_name = 'Variety'
        verbose_name_plural = 'Varieties'

    def __str__(self):
        return self.variety_name


class Winery(models.Model):
    winery_id = models.AutoField(primary_key=True)
    winery_name = models.CharField(unique=True, max_length=100)


    class Meta:
        managed = False
        db_table = 'winery'
        ordering = ['winery_name']
        verbose_name = 'Winery'
        verbose_name_plural = 'Wineries'

    def __str__(self):
        return self.winery_name


class Vineyard(models.Model):
    vineyard_id = models.AutoField(primary_key=True)
    vineyard_name = models.CharField(unique=True, max_length=100)

    winery= models.ManyToManyField(Winery, through='VineyardWinery')

    class Meta:
        managed = False
        db_table = 'vineyard'
        ordering = ['vineyard_name']
        verbose_name = 'Vineyard'
        verbose_name_plural = 'Vineyards'

    def __str__(self):
        return self.vineyard_name




class VineyardWinery(models.Model):
    vineyard_winery_id = models.AutoField(primary_key=True)
    vineyard = models.ForeignKey(Vineyard, models.DO_NOTHING, blank=True, null=True)
    winery = models.ForeignKey('Winery', models.DO_NOTHING)


    class Meta:
        managed = False
        db_table = 'vineyard_winery'
        ordering = ['vineyard', 'winery']
        verbose_name = 'Vineyard _ Winery'
        verbose_name_plural = 'Vineyard _ Winery'


class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    wine_name = models.CharField(unique=True, max_length=200)
    variety = models.ForeignKey(Variety, models.DO_NOTHING)
    points = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    region1 = models.ForeignKey(Region1, models.DO_NOTHING, blank=True, null=True)
    vineyard_winery = models.ForeignKey(VineyardWinery, models.DO_NOTHING, blank=True, null=True)

    # Intermediate model (country_area -> heritage_site_jurisdiction <- heritage_site)
    taster= models.ManyToManyField(Taster, through='WineReview')

    class Meta:
        managed = False
        db_table = 'wine'

    class Meta:
        managed = False
        db_table = 'wine'
        ordering = ['wine_name']
        verbose_name = 'Wine'
        verbose_name_plural = 'Wines'

    def __str__(self):
        return self.wine_name


class WineReview(models.Model):
    wine_review_id = models.AutoField(primary_key=True)
    wine = models.ForeignKey(Wine, models.DO_NOTHING)
    taster = models.ForeignKey(Taster, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wine_review'

    class Meta:
        managed = False
        db_table = 'wine_review'
        ordering = ['wine', 'taster']
        verbose_name = 'Wine _ Review'
        verbose_name_plural = 'Wine _ Review'

