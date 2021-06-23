from datetime import timedelta

from hotel.models import Hotel, Reserve, Tax

from rest_framework import serializers


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'


class ReserveSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField()
    cancel = serializers.ReadOnlyField()

    hotel = HotelSerializer(read_only=True)
    hotel_id = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Reserve
        fields = ('id', 'name', 'email', 'telephone', 'client_type', 'hotel_id', 'hotel', 'start', 'end', 'value',
                  'cancel', 'observations')

    def calculate_value(self, start, end, hotel, client_type):
        delta = end - start
        days = [start + timedelta(days=i) for i in range(delta.days + 1)]
        value = 0
        for day in days:
            tax = Tax.objects.filter(
                hotel=hotel,
                client_type=client_type,
                day=Tax.DAYS[day.weekday()][0]
            ).first()
            value += tax.value
        return value

    def create(self, validated_data):
        validated_data['value'] = self.calculate_value(
            validated_data['start'],
            validated_data['end'],
            validated_data['hotel_id'],
            validated_data['client_type']
        )
        validated_data['hotel_id'] = validated_data['hotel_id'].id
        return super(ReserveSerializer, self).create(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['number'] = ret['id']

        if ret['client_type'] == Tax.REGULAR:
            ret['client_type'] = 'Regular'
        else:
            ret['client_type'] = 'Reward'

        return ret
