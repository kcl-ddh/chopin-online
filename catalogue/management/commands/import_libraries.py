# *-* coding: utf-8 *-*
from django.core.management.base import BaseCommand, CommandError

from wagtail.wagtailcore.models import Page

import logging
import os

from pdf_import_utils import import_library


class Command(BaseCommand):
    args = '<page_slug library_path library_path ...>'
    help = 'Imports libraries information from PDF files'

    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError('''You need to provide one parent page and at
                               least one library path''')

        slug = args[0]

        page = Page.objects.filter(slug=slug).first()

        if not page:
            self.stderr.write('Page {0} not found'.format(slug))
            return

        for library_path in args[1:]:
            # absolute path to the library file
            library_path = os.path.abspath(library_path)
            import_library(library_path, page)
