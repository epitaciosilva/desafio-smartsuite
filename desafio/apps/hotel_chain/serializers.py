from rest_framework import serializers

from hotel_chain.models import (
    Client, ClientType, Hotel, HotelClient, Rate, Reserve,
)


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class ClientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientType
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class HotelClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelClient
        fields = '__all__'


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'
