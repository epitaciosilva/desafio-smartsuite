import re

from hotel.filters import ReserveFilter
from hotel.models import Hotel, Tax
from hotel.serializers import HotelSerializer, ReserveSerializer, TaxSerializer

from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist

from api.utils import Schema


class HotelViewSet(viewsets.ModelViewSet):
    serializer_class = HotelSerializer
    queryset = serializer_class.Meta.model.objects.all()


class TaxViewSet(viewsets.ModelViewSet):
    serializer_class = TaxSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ReserveViewSet(viewsets.ModelViewSet):
    serializer_class = ReserveSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filter_class = ReserveFilter
    schema = Schema()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"reserve": serializer.data['number']}, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk):
        try:
            pk = int(pk)
            instance = self.get_queryset().get(pk=pk)
        except ValueError as e:
            raise serializers.ValidationError(e)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Reserve not found!")
        else:
            instance.cancel = True
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)


class Cheapest(APIView):
    def __break_query_string(self, query_string):
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

    def get(self, request):
        if not request.query_params:
            return Response({'Query string is required.'}, status.HTTP_400_BAD_REQUEST)

        client_type, days = self.__break_query_string(list(request.query_params.keys())[0])

        min_value = float("inf")
        best_hotel = None

        for hotel in Hotel.objects.all():
            value = 0

            # faz a soma da taxa para todos os dias
            for day in days:
                tax = Tax.objects.filter(hotel=hotel, client_type=client_type, day=day).first()
                value += tax.value

            # fazendo a verificação se o valor é o menor
            # se der empate, então o critério de desempate é a classificação
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
