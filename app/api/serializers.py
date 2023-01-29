from rest_framework.serializers import ModelSerializer
from app.models import Location, Data, RiverBasin


# Serializer for RiverBasni model

class RiverBasinSerializer(ModelSerializer):

    class Meta:
        model = RiverBasin
        fields = '__all__'
        ordering = ['updated', 'created']

    def create(self, data):
        return RiverBasin.objects.create(**data)

# Serializer for location model
class LocationSerializer(ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'
        ordering = ['updated', 'created']

    def create(self, data):
        return Location.objects.create(**data)
        

# Serializer for Data(files) model
class DataSerializer(ModelSerializer):

    class Meta:
        model = Data
        fields = '__all__'
        ordering = ['updated', 'created']

    def create(self, data):
        return Data.objects.create(**data)