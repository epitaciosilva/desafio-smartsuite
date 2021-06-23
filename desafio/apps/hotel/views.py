import re

from hotel.filters import ReserveFilter
from hotel.models import Hotel, Tax
from hotel.serializers import HotelSerializer, ReserveSerializer, TaxSerializer

from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import transaction

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

    def send_email_reserve(self, title, reserve):
        message = "Dados de confirmação: \n" \
                  "Número da reserva: {number} \n" \
                  "Nome: {name} \n" \
                  "Telefone: {telephone}\n" \
                  "Email: {email}\n" \
                  "Hotel: {hotel}\n" \
                  "Tipo de reserva: {reserve_type}\n" \
                  "Valor: R$ {valor} \n" \
                  "Período: {start} à {end}\n" \
            .format(
                number=reserve.id,
                name=reserve.name,
                telephone=reserve.telephone,
                email=reserve.email,
                hotel=reserve.hotel.name,
                reserve_type=Tax.client_type_full(reserve.client_type),
                valor=reserve.value,
                start=reserve.start.strftime("%d/%b/%Y"),
                end=reserve.end.strftime("%d/%b/%Y")
            )

        send_mail(
            title,
            message,
            None,
            [reserve.email],
            fail_silently=False
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        reserve = serializer.instance
        self.send_email_reserve(
            "Confirmação de reserva no hotel {}".format(reserve.hotel.name),
            reserve
        )

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
            if not instance.cancel:
                instance.cancel = True
                instance.save()

                self.send_email_reserve(
                    "Cancelamento da reserva no hotel {}".format(instance.hotel.name),
                    instance
                )

            return Response({
                "reserve": "Reserva cancelada com sucesso!"
            }, status=status.HTTP_200_OK)


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
