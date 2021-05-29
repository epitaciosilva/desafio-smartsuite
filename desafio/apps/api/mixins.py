from collections import OrderedDict

from django.db.models import Q, TextField, Value
from django.db.models.functions import Cast, Lower, StrIndex


class SearchMixin(object):
    fields = tuple()

    def get_queryset(self):
        queryset = super(SearchMixin, self).get_queryset()
        query = self.request.GET.get('q', '')
        annotates = OrderedDict()
        order = []

        search = None

        for field in self.fields:
            search = search | Q(**{'{0}__icontains'.format(field): query}) if search is not None else \
                Q(**{'{0}__icontains'.format(field): query})

            annotates['{0}__rank'.format(field)] = StrIndex(
                Lower(Cast(field, TextField())), Value(query.lower())) + Value(2)
            order.append('{0}__rank'.format(field))

        if search:
            queryset = queryset.filter(search)

        queryset = queryset.annotate(**OrderedDict(annotates)).order_by(*order)

        for key, value in self.request.GET.items():
            if value == 'true':
                value = True
            elif value == 'false':
                value = False

            if key not in ('q', 'page'):
                if '|' in key:
                    chaves = key.split('|')
                    filtro = None

                    for c in chaves:
                        filtro = filtro | Q(**{c: value}) if filtro else Q(**{c: value})

                    queryset = queryset.filter(filtro)
                elif '__in[]' not in key:
                    queryset = queryset.filter(**{key: value})
                else:
                    try:
                        queryset = queryset.filter(**{
                            key.replace('[]', ''):
                                self.request.GET.getlist(key)
                                if len(self.request.GET.getlist(key)) > 1
                                else self.request.GET.getlist(key)[0].split(',')
                        })
                    except Exception:
                        queryset = queryset.model.objects.none()

        return queryset.distinct()
