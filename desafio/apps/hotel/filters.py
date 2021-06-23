from hotel.models import Reserve, Tax

import rest_framework_filters as filters


class ReserveFilter(filters.FilterSet):
    reserve_type = filters.CharFilter(method='filter_reserve_type')

    class Meta:
        model = Reserve
        fields = {
            "hotel": ['exact'],
        }

    def filter_reserve_type(self, qs, name, value):
        client_type = Tax.REGULAR
        if value.lower() == 'reward':
            client_type = Tax.REWARD
        return qs.filter(client_type=client_type)
