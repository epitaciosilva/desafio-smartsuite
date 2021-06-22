from hotel.models import Hotel, Tax

from django.core.management.base import BaseCommand


def create_tax(hotel, client_type, value, week_days=True):
    week = ["mon", "tues", "wed", "thur", "fri"]
    weekend = ["sat", "sun"]

    days = []
    if week_days:
        days = week
    else:
        days = weekend

    for day in days:
        Tax.objects.create(hotel=hotel, client_type=client_type, value=value, day=day)


def create_hotels():
    lakewood = Hotel.objects.create(name="Lakewood", stars=3)
    create_tax(lakewood, Tax.REGULAR, 110)
    create_tax(lakewood, Tax.REGULAR, 90, week_days=False)
    create_tax(lakewood, Tax.REWARD, 80)
    create_tax(lakewood, Tax.REWARD, 80, week_days=False)

    bridgewood = Hotel.objects.create(name="Bridgewood", stars=4)
    create_tax(bridgewood, Tax.REGULAR, 160)
    create_tax(bridgewood, Tax.REGULAR, 60, week_days=False)
    create_tax(bridgewood, Tax.REWARD, 110)
    create_tax(bridgewood, Tax.REWARD, 50, week_days=False)

    ridgewood = Hotel.objects.create(name="Ridgewood", stars=5)
    create_tax(ridgewood, Tax.REGULAR, 220)
    create_tax(ridgewood, Tax.REGULAR, 150, week_days=False)
    create_tax(ridgewood, Tax.REWARD, 100)
    create_tax(ridgewood, Tax.REWARD, 40, week_days=False)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--rollback', action='store_true', help='Delete taxs')

    def handle(self, *args, **options):
        if options.get('rollback', False):
            Hotel.objects.all().delete()
            Tax.objects.all().delete()

        create_hotels()
