from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext as _


class Hotel(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    stars = models.PositiveSmallIntegerField(_('Stars'), default=0)
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        ordering = ('-stars', 'name',)

    def __str__(self):
        return self.name


# class Client(models.Model):
#     name = models.CharField(_("Name"), max_length=255)
#     email = models.EmailField(_("Email"), max_length=254)
#     telefone = models.CharField(_("Telefone"), max_length=11, validators=[MinValueValidator(11)])
#     created_at = models.DateTimeField('Created At', auto_now_add=True)
#     updated_at = models.DateTimeField('Updated At', auto_now=True)

#     class Meta:
#         verbose_name = 'Client'
#         verbose_name_plural = 'Clients'
#         ordering = ('name',)

#     def __str__(self):
#         return self.name


class Tax(models.Model):
    REGULAR = 1
    REWARD = 2

    CLIENT_TYPES = (
        (REGULAR, 'Regular'),
        (REWARD, 'Reward')
    )

    DAYS = (
        ("mon", "Monday"),
        ("tues", "Tuesday"),
        ("wed", "Wednesday"),
        ("thur", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday")
    )

    hotel = models.ForeignKey(Hotel, verbose_name=_("Hotel Tax"), on_delete=models.CASCADE)
    client_type = models.PositiveSmallIntegerField(_("Client Type"), choices=CLIENT_TYPES)
    day = models.CharField(_("Day"), max_length=4, choices=DAYS)
    value = models.FloatField(_("Value"))
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ('hotel', 'client_type', 'day',)

    def __str__(self):
        return f'{self.hotel.name} - {self.client_type} - {self.day} - {self.value}'

    @staticmethod
    def client_type_full(client_type):
        return Tax.CLIENT_TYPES[client_type - 1][1]


class Reserve(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_("Email"), max_length=254)
    telephone = models.CharField(_("Telefone"), max_length=11, validators=[MinLengthValidator(11)])
    hotel = models.ForeignKey(Hotel, verbose_name=_("Hotel"), on_delete=models.CASCADE)
    client_type = models.PositiveSmallIntegerField(_("Client Type"), choices=Tax.CLIENT_TYPES)
    start = models.DateField(_("Entrance"))
    end = models.DateField(_("Exit"))
    value = models.FloatField(_("Value of reserve"))
    cancel = models.BooleanField(_("Cancel"), default=False)
    observations = models.TextField(_("Observations"), blank=True, null=True)

    class Meta:
        verbose_name = 'Reserve'
        verbose_name_plural = 'Reserves'
        ordering = ('hotel', 'name',)

    def __str__(self):
        return f'{self.hotel.name} - {self.client.name} - {self.value}'
