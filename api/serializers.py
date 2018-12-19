from winereviews.models import *
from rest_framework import response, serializers, status


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('country_id', 'country_name')


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = ('province_id', 'province_name', 'country_id')


class Region2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Region2
        fields = ('region2_id', 'region2_name', 'province_id')


class Region1Serializer(serializers.ModelSerializer):

    class Meta:
        model = Region1
        fields = ('region1_id', 'region1_name', 'province_id','region2_id')

class TasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Taster
        fields = ('taster_id', 'taster_name', 'taster_twitter_handle')

class VarietySerializer(serializers.ModelSerializer):

    class Meta:
        model = Variety
        fields = ('variety_id', 'variety_name')


class DescriptionSerializer(serializers.ModelSerializer):
    taster= TasterSerializer(many=False, read_only=True)

    class Meta:
        model = Description
        fields = ('description_id', 'description_text','taster_id')

class WineReviewSerializer(serializers.ModelSerializer):
    wine_id = serializers.ReadOnlyField(source='wine.wine_id')
    description_id = serializers.ReadOnlyField(source='description.description_id')

    class Meta:
        model = WineReview
        fields = ('wine_id', 'description_id')

class WineSerializer(serializers.ModelSerializer):
    wine_name= serializers.CharField(allow_blank=False, max_length=200)

    variety= VarietySerializer(many=False, read_only=True)

    variety_id=serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=Variety.objects.all(),
        source='variety'
        )

    points = serializers.IntegerField(
        allow_null=False
    )

    price=  serializers.DecimalField(
        allow_null=True,
        max_digits=10,
        decimal_places=8
    )

    region1= Region1Serializer(many=False, read_only=True)

    region1_id=serializers.PrimaryKeyRelatedField(
        allow_null=False,
        many=False,
        write_only=True,
        queryset=Region1.objects.all(),
        source='region1'
        )

    wine_review= WineReviewSerializer(
        source='wine_review_set', # Note use of _set
        many=True,
        read_only=True)

    wine_review_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Description.objects.all(),
        source='wine_review'
    )


    class Meta:
        model = Wine
        fields = ('wine_id', 'wine_name','variety','variety_id','points','price','region1','region1_id','wine_review','wine_review_ids')


    def create(self, validated_data):
        """
        This method persists a new HeritageSite instance as well as adds all related
        countries/areas to the heritage_site_jurisdiction table.  It does so by first
        removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
        data before the new HeritageSite instance is saved to the database. It then loops
        over the heritage_site_jurisdiction array in order to extract each country_area_id
        element and add entries to junction/associative heritage_site_jurisdiction table.
        :param validated_data:
        :return: site
        """

        # print(validated_data)

        countries = validated_data.pop('heritage_site_jurisdiction')
        site = HeritageSite.objects.create(**validated_data)

        if countries is not None:
            for country in countries:
                HeritageSiteJurisdiction.objects.create(
                    heritage_site_id=site.heritage_site_id,
                    country_area_id=country.country_area_id
                )
        return site

    def update(self, instance, validated_data):
        # site_id = validated_data.pop('heritage_site_id')
        site_id = instance.heritage_site_id
        new_countries = validated_data.pop('heritage_site_jurisdiction')

        instance.site_name = validated_data.get(
            'site_name',
            instance.site_name
        )
        instance.description = validated_data.get(
            'description',
            instance.description
        )
        instance.justification = validated_data.get(
            'justification',
            instance.justification
        )
        instance.date_inscribed = validated_data.get(
            'date_inscribed',
            instance.date_inscribed
        )
        instance.longitude = validated_data.get(
            'longitude',
            instance.longitude
        )
        instance.latitude = validated_data.get(
            'latitude',
            instance.latitude
        )
        instance.area_hectares = validated_data.get(
            'area_hectares',
            instance.area_hectares
        )
        instance.heritage_site_category_id = validated_data.get(
            'heritage_site_category_id',
            instance.heritage_site_category_id
        )
        instance.transboundary = validated_data.get(
            'transboundary',
            instance.transboundary
        )
        instance.save()

        # If any existing country/areas are not in updated list, delete them
        new_ids = []
        old_ids = HeritageSiteJurisdiction.objects \
            .values_list('country_area_id', flat=True) \
            .filter(heritage_site_id__exact=site_id)

        # TODO Insert may not be required (Just return instance)

        # Insert new unmatched country entries
        for country in new_countries:
            new_id = country.country_area_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                HeritageSiteJurisdiction.objects \
                    .create(heritage_site_id=site_id, country_area_id=new_id)

        # Delete old unmatched country entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                HeritageSiteJurisdiction.objects \
                    .filter(heritage_site_id=site_id, country_area_id=old_id) \
                    .delete()

        return instance