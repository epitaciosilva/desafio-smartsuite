from rest_framework.exceptions import ValidationError

from django.db import models
from django.utils.translation import gettext as _


class Status(models.Model):
    ACTIVE = 'A'
    INACTIVE = 'I'

    STATUS_CHOICE = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    )

    status = models.CharField(_('Status'), max_length=1, choices=STATUS_CHOICE)

    class Meta:
        abstract = True


class Hotel(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    classification = models.PositiveSmallIntegerField(_('Classification'))

    clients = models.ManyToManyField(
        'hotel_chain.client',
        through='hotel_chain.HotelClient',
        verbose_name=_('Hotel Clients')
    )

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        ordering = ('-classification', 'name',)

    def __str__(self):
        return self.name


class ClientType(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'))

    class Meta:
        verbose_name = 'Client Type'
        verbose_name_plural = 'Client Types'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('Email'), max_length=255)
    telephone = models.CharField(_('Telephone'), max_length=11)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ('name',)

    def __str__(self):
        return self.name


class HotelClient(models.Model):
    client = models.ForeignKey(Client, verbose_name=_('Client Reserve'), on_delete=models.PROTECT)
    hotel = models.ForeignKey(Hotel, verbose_name=_('Hotel'), on_delete=models.PROTECT)

    client_type = models.ForeignKey(
        ClientType,
        verbose_name=_('Client Type'),
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Hotel Client'
        verbose_name_plural = 'Hotel Clients'
        unique_together = ('client', 'hotel', 'client_type')

    def __str__(self):
        return f'{self.hotel.name} - {self.client.name}'


class Rate(Status):
    WEEK_RATE = 'WEK'
    WEEKEND_RATE = 'WEN'

    RATE_TYPE_CHOICES = (
        (WEEKEND_RATE, 'Weekend Rate'),
        (WEEK_RATE, 'Week Rate')
    )

    value = models.FloatField(_('Value'))
    rate_type = models.CharField(_('Rate Type'), max_length=3, choices=RATE_TYPE_CHOICES)
    hotel = models.ForeignKey(Hotel, verbose_name=_('Hotel Rate'), on_delete=models.CASCADE)

    client_type = models.ForeignKey(
        ClientType,
        verbose_name=_('Client Type'),
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.hotel.name} - {self.rate_type} - {self.client_type.name} - {self.value}'

    def save(self, *args, **kwargs):
        if self.status == Rate.ACTIVE:
            current_rate = Rate.objects.filter(
                client_type=self.client_type,
                rate_type=self.rate_type,
                status=Rate.ACTIVE
            ).esclude(id=self.id)

            if current_rate:
                raise ValidationError(_('Hotel cannot have two rate active for the same client type and rate type.'))

        return super(Rate, self).save(*args, **kwargs)


class Reserve(Status):
    hotel_client = models.ForeignKey(
        HotelClient,
        verbose_name=_('Hotel Client'),
        on_delete=models.PROTECT
    )

    rate = models.ForeignKey(
        Rate,
        verbose_name=_('Rate Reserve'),
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Reserve'
        verbose_name_plural = 'Reserves'
        ordering = ('hotel_client', 'status')
