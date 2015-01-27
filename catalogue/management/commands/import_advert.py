from django.core.management.base import BaseCommand, CommandError

from .pdf_import_utils import import_adverts


class Command(BaseCommand):
    args = '<path path ...>'
    help = 'Imports adverts'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('''You need to provide at least one path to the
                               directories containing adverts''')

        for path in args:
            import_adverts(path)
