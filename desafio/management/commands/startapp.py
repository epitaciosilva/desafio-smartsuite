import os
from importlib import import_module

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    def handle(self, **options):
        if options['directory'] is None:
            directory = options['directory'] = os.path.join(settings.PROJECT_ROOT, 'apps', options['name'])

            try:
                os.makedirs(directory)
            except FileExistsError:
                raise CommandError("'%s' already exists" % directory)
            except OSError as e:
                raise CommandError(e)
        else:
            directory = options['directory']

        super().handle(**options)
        os.makedirs(os.path.join(directory, 'locale'))

    def validate_name(self, name, name_or_dir='name'):
        try:
            m = import_module(name)
        except ImportError:
            pass
        else:
            if os.listdir(list(m.__path__)[0]):
                super().validate_name(name, name_or_dir)
