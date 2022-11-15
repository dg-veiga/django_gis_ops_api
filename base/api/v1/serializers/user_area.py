import json
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from geopandas import GeoSeries

from base.models.user_area import UserArea, DESCRIPTION_LENGTH


class GeometryFieldSerializer(serializers.Field):
    def to_representation(self, instance):
        if instance.geometry:
            instance = json.loads(instance.geometry.geojson)
        else:
            instance = None
        return instance

    def to_internal_value(self, data):
        data = str(json.dumps(data))
        meta = {"geometry": GEOSGeometry(data)}
        return meta


class UserAreaCreateSerializer(serializers.ModelSerializer):
    geometry = GeometryFieldSerializer(source='*')

    def validate(self, data):
        description = data.get('description')
        if description and len(description) > DESCRIPTION_LENGTH:
            data['description'] = (description[:DESCRIPTION_LENGTH - 3] + '...') \
                if len(description) > DESCRIPTION_LENGTH else description
        return data

    def validate_geometry(self, data):
        if data['geometry'].hasz:
            g = GeoSeries.from_wkt(data.wkt)
            g.Set3D(False)
            data['geometry'] = GEOSGeometry(g.ExportToWkt())
        return data

    class Meta:
        model = UserArea
        fields = ['id', 'user', 'code', 'description', 'geometry', 'centroid', 'area']
        read_only_fields = ['id', 'centroid', 'area']
        extra_kwargs = {
            'user': {'required': True},
            'code': {'required': True, 'allow_blank': False},
        }


class UserAreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserArea
        fields = '__all__'


class UserAreaDetailSerializer(serializers.ModelSerializer):
    # owner = OwnerDetailSerializer(read_only=True)

    class Meta:
        model = UserArea
        fields = '__all__'
        read_only_fields = ['id', 'centroid', 'area']
