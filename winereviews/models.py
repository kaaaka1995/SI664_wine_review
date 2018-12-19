# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse
from django.db.models import  F


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
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True)

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
    province = models.ForeignKey(Province, on_delete=models.PROTECT, blank=True, null=True)

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
    province = models.ForeignKey(Province, on_delete=models.PROTECT, blank=True, null=True)
    region2 = models.ForeignKey('Region2', on_delete=models.PROTECT, blank=True, null=True)

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


# class Winery(models.Model):
#     winery_id = models.AutoField(primary_key=True)
#     winery_name = models.CharField(unique=True, max_length=100)


#     class Meta:
#         managed = False
#         db_table = 'winery'
#         ordering = ['winery_name']
#         verbose_name = 'Winery'
#         verbose_name_plural = 'Wineries'

#     def __str__(self):
#         return self.winery_name


# class Vineyard(models.Model):
#     vineyard_id = models.AutoField(primary_key=True)
#     vineyard_name = models.CharField(unique=True, max_length=100)

#     winery= models.ManyToManyField(Winery, through='VineyardWinery')

#     class Meta:
#         managed = False
#         db_table = 'vineyard'
#         ordering = ['vineyard_name']
#         verbose_name = 'Vineyard'
#         verbose_name_plural = 'Vineyards'

#     def __str__(self):
#         return self.vineyard_name




# class VineyardWinery(models.Model):
#     vineyard_winery_id = models.AutoField(primary_key=True)
#     vineyard = models.ForeignKey(Vineyard, on_delete=models.PROTECT, blank=True, null=True)
#     winery = models.ForeignKey('Winery', on_delete=models.PROTECT)


#     class Meta:
#         managed = False
#         db_table = 'vineyard_winery'
#         ordering = ['vineyard', 'winery']
#         verbose_name = 'Vineyard _ Winery'
#         verbose_name_plural = 'Vineyard _ Winery'

class Description(models.Model):
    description_id = models.AutoField(primary_key=True)
    description_text = models.TextField(blank=True, null=True)
    taster = models.ForeignKey('Taster', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'description'
        ordering = ['description_text']
        verbose_name = 'Description'
        verbose_name_plural = 'Description'

    def __str__(self):
        return self.description_text


class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    wine_name = models.CharField(unique=True, max_length=200)
    variety = models.ForeignKey(Variety, on_delete=models.PROTECT)
    points = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    region1 = models.ForeignKey(Region1, on_delete=models.PROTECT, blank=True, null=True)
    #vineyard_winery = models.ForeignKey(VineyardWinery, on_delete=models.PROTECT, blank=True, null=True)

    # Intermediate model (country_area -> heritage_site_jurisdiction <- heritage_site)
    #taster= models.ManyToManyField(Taster, through='WineReview')
    description= models.ManyToManyField(Description, through='WineReview')

    

    class Meta:
        managed = False
        db_table = 'wine'
        ordering = ['wine_name']
        verbose_name = 'Wine'
        verbose_name_plural = 'Wines'

    def __str__(self):
        return self.wine_name

    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('wine_detail', kwargs={'pk': self.pk})

    @property
    def descriptions(self):
        """
        Returns a list of UNSD countries/areas (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with a country/area (e.g., Old City
        Walls of Jerusalem). In such cases the Queryset will return as <QuerySet [None]> and the
        list will need to be checked for None or a TypeError (sequence item 0: expected str
        instance, NoneType found) runtime error will be thrown.
        :return: string
        """
        des = self.description.select_related('taster').order_by('description_text')
        tasters = self.description.select_related('taster').values(taster_name=F('taster__taster_name'),twitter=F('taster__taster_twitter_handle'),).order_by('taster__taster_name')


        names = []
        for d in des:
            name = d.description_text
            if name is None:
                continue
            
            if name not in names:
                names.append(name)


        tlist = []

        for taster in tasters:
            name = taster['taster_name']
         
            if name is None:
                continue
            taster_twitter = taster['twitter']
            if taster_twitter is None:
                taster_twitter='None'

            name_and_code = ''.join([name, ' (', taster_twitter, ')'])
            if name_and_code not in tlist :
                tlist.append(name_and_code)

        finallist=[]
        for i in range(len(names)):
            if i <= len(tlist)-1:
                finallist.append([names[i],tlist[i]])
            else:
                finallist.append([names[i],'None'])

        return finallist

    # @property
    # def taster_names(self):
       
    #     tasters = self.taster.order_by('taster_name')

    #     names = []
    #     for taster in tasters:
    #         name = taster.taster_name
         
    #         if name is None:
    #             continue
    #         taster_twitter = taster.taster_twitter_handle

    #         name_and_code = ''.join([name, ' (', taster_twitter, ')'])
    #         if name_and_code not in names:
    #             names.append(name_and_code)


    #     return names[0]

    # @property
    # def descriptions(self):
       
    #     descriptions = self.description.order_by('description_text')

    #     names = []
    #     for description in descriptions:
    #         name = description.description_text
         
    #         if name is None:
    #             continue
           
    #         if name not in names:
    #             names.append(name)


    #     return names[0]

    # @property
    # def descriptions(self):
       
    #     des =  self.description.order_by('description_text')

    #     text_list = []
    #     for text in des:
    #         temp = text.description_text
         
    #         if temp is None:
    #             continue
              
            
    #         if temp not in text_list:
    #             text_list.append(temp)

    #     tasters = self.taster.order_by('taster_name')

    #     names = []

    #     for taster in tasters:
    #         name = taster.taster_name
         
    #         if name is None:
    #             continue
    #         taster_twitter = taster.taster_twitter_handle
    #         if taster_twitter is None:
    #             taster_twitter='None'

    #         name_and_code = ''.join([name, ' (', taster_twitter, ')'])
    #         if name_and_code not in names:
    #             names.append(name_and_code)

    #     finallist=[]
    #     for i in range(len(text_list)):
    #         if i <= len(names)-1:
    #             finallist.append([text_list[i],names[i]])
    #         else:
    #             finallist.append([text_list[i],'None'])



    #     return finallist



 



class WineReview(models.Model):
    wine_review_id = models.AutoField(primary_key=True)
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    #taster = models.ForeignKey(Taster, on_delete=models.CASCADE)
    #description0 = models.TextField(blank=True, null=True)
    description = models.ForeignKey(Description, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'wine_review'

    class Meta:
        managed = False
        db_table = 'wine_review'
        ordering = ['wine', 'description']
        verbose_name = 'Wine _ Review'
        verbose_name_plural = 'Wine _ Review'

