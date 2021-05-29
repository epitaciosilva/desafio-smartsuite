from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.mixins import SearchMixin
from api.utils import FilterPagination


class SearchView(SearchMixin, ListAPIView, RetrieveAPIView):
    pagination_class = FilterPagination

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('id', None):
            return super(RetrieveAPIView, self).retrieve(request, *args, **kwargs)

        return super(ListAPIView, self).list(request, *args, **kwargs)
