from hotel.serializers import (
    ClientSerializer, HotelSerializer, ReserveSerializer, TaxSerializer,
)
from hotel.models import (
    Hotel, Tax
)
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re


class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    queryset = serializer_class.Meta.model.objects.all()


class TaxViewSet(viewsets.ModelViewSet):
    serializer_class = TaxSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ReserveViewSet(viewsets.ModelViewSet):
    serializer_class = ReserveSerializer
    queryset = serializer_class.Meta.model.objects.all()


class Cheapest(APIView):
    def get(self, request):
        if not request.query_params: 
            return Response({'Query string is required.'}, status.HTTP_400_BAD_REQUEST)
        
        client_type, days = self.break_query_string(list(request.query_params.keys())[0])
        min_value = 99999999999999
        best_hotel = None
        for hotel in Hotel.objects.all():
            value = 0
            for day in days:
                tax = Tax.objects.filter(hotel=hotel, client_type=client_type, day=day).first()
                value += tax.value

            if value < min_value:
                min_value = value
                best_hotel = hotel
            elif value == min_value and best_hotel and best_hotel.stars < hotel.stars:
                best_hotel = hotel

        if not best_hotel:
            return Response({
                "cheapest": "Unregistered hotels!"
            })
        return Response({"cheapest": best_hotel.name, "value": min_value})

    def break_query_string(self, query_string):
        qs = query_string.split(": ")

        client_type = None
        if qs[0] == 'Regular':
            client_type = Tax.REGULAR
        elif qs[0] == 'Reward':
            client_type = Tax.REWARD
        else:
            raise serializers.ValidationError("Client type not found!")

        days = []
        for date in qs[1].split(", "):
            result = re.search(r"\(([a-z]+)\)", date)
            days.append(result.group(1))

        return client_type, days