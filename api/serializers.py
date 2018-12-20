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


# class DescriptionSerializer(serializers.ModelSerializer):
#     taster= TasterSerializer(many=False, read_only=True)

#     class Meta:
#         model = Description
#         fields = ('description_id', 'description_text','taster_id')

class WineReviewSerializer(serializers.ModelSerializer):
    wine_id = serializers.ReadOnlyField(source='wine.wine_id')
    taster_id = serializers.ReadOnlyField(source='taster.taster_id')

    class Meta:
        model = WineReview
        fields = ('wine_id', 'taster_id')

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
        queryset=Taster.objects.all(),
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

        wines = validated_data.pop('wine_review')
        wine = Wine.objects.create(**validated_data)

        if tasters is not None:
            for taster in tasters:
                WineReview.objects.create(
                    wine_id=wine.wine_id,
                    taster_id=taster.taster_id
                )
        return wine

    def update(self, instance, validated_data):
        # site_id = validated_data.pop('heritage_site_id')
        wine_id = instance.wine_id
        new_tasters = validated_data.pop('wine_review')

        instance.wine_name = validated_data.get(
            'wine_name',
            instance.wine_name
        )
        instance.variety_id = validated_data.get(
            'variety_id',
            instance.variety_id
        )

        instance.region1_id = validated_data.get(
            'region1_id',
            instance.region1_id
        )
        instance.points = validated_data.get(
            'points',
            instance.justification
        )
        instance.price = validated_data.get(
            'price',
            instance.date_inscribed
        )
        
        instance.save()

        # If any existing country/areas are not in updated list, delete them
        new_ids = []
        old_ids = WineReview.objects \
            .values_list('taster_id', flat=True) \
            .filter(wine_id__exact=wine_id)

        # TODO Insert may not be required (Just return instance)

        # Insert new unmatched country entries
        for taster in new_tasters:
            new_id = taster.taster_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                WineReview.objects \
                    .create(wine_id=wine_id, taster_id=new_id)

        # Delete old unmatched country entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                WineReview.objects \
                    .filter(wine_id=wine_id, taster_id=old_id) \
                    .delete()

        return instance