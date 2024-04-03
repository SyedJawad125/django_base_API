from rest_framework.serializers import ModelSerializer
from .models import Make, Vechile


class VechileSerializer(ModelSerializer):
    class Meta:
        model = Vechile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["make"] = MakeListingSerializer(instance.make).data
        return data


class MakeSerializer(ModelSerializer):
    class Meta:
        model = Make
        fields = '__all__'


class MakeListingSerializer(ModelSerializer):
    class Meta:
        model = Make
        exclude = ['created_at', 'updated_at']
