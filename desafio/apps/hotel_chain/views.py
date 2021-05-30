from rest_framework import viewsets

from hotel_chain.serializers import (
    ClientSerializer, ClientTypeSerializer, HotelClientSerializer,
    HotelSerializer, RateSerializer, ReserveSerializer,
)


class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ClientTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClientTypeSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClientSerializer
    queryset = serializer_class.Meta.model.objects.all()


class HotelClientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelClientSerializer
    queryset = serializer_class.Meta.model.objects.all()


class RateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RateSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ReserveViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReserveSerializer
    queryset = serializer_class.Meta.model.objects.all()
