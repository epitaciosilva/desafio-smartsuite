#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desafio.settings')

    try:
        from django.core import management
        from django.core.management import execute_from_command_line

        def get_commands():
            commands = {name: 'django.core' for name in management.find_commands(management.__path__[0])}

            if not management.settings.configured:
                return commands

            for app_config in reversed(list(management.apps.get_app_configs())):
                path = os.path.join(app_config.path, 'management')
                commands.update({name: app_config.name for name in management.find_commands(path)})

            commands.update({name: 'desafio' for name in management.find_commands(
                os.path.join(os.path.dirname(__file__), 'desafio', 'management'))})

            return commands

        # Override django get_commands to include project level commands
        management.get_commands = get_commands
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
