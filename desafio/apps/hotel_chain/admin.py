from django.contrib import admin

from . import models


class HotelAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'classification')
    list_filter = ('id', 'name', 'classification')
    raw_id_fields = ('clients',)
    search_fields = ('name',)


class ClientTypeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description')
    list_filter = ('id', 'name', 'description')
    search_fields = ('name',)


class ClientAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'email', 'telephone')
    list_filter = ('id', 'name', 'email', 'telephone')
    search_fields = ('name',)


class HotelClientAdmin(admin.ModelAdmin):

    list_display = ('id', 'client', 'hotel', 'client_type')
    list_filter = (
        'client',
        'hotel',
        'client_type',
        'id',
        'client',
        'hotel',
        'client_type',
    )


class RateAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'status',
        'value',
        'rate_type',
        'hotel',
        'client_type',
    )
    list_filter = (
        'hotel',
        'client_type',
        'id',
        'status',
        'value',
        'rate_type',
        'hotel',
        'client_type',
    )


class ReserveAdmin(admin.ModelAdmin):

    list_display = ('id', 'status', 'hotel_client', 'rate')
    list_filter = (
        'hotel_client',
        'rate',
        'id',
        'status',
        'hotel_client',
        'rate',
    )


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Hotel, HotelAdmin)
_register(models.ClientType, ClientTypeAdmin)
_register(models.Client, ClientAdmin)
_register(models.HotelClient, HotelClientAdmin)
_register(models.Rate, RateAdmin)
_register(models.Reserve, ReserveAdmin)
