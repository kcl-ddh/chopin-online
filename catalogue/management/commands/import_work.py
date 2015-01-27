from catalogue.models import _e, Work
from pdf_import_utils import import_work

from django.core.management.base import BaseCommand, CommandError

from wagtail.wagtailcore.models import Page

import logging
import os

class Command(BaseCommand):
    args = '<page_slug work_path work_path ...>'
    help = 'Imports works from PDF files'

    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError(
                'You need to provide one page and at least one work path')

        slug = args[0]

        page = Page.objects.filter(slug=slug).first()

        if not page:
            self.stderr.write('Page {0} not found.'.format(slug))
            return

        publisher_index_page = Page.objects.filter(
            slug='sigla-publishers').first()

        if not publisher_index_page:
            self.stderr.write('Page {0} not found.'.format('sigla-publishers'))
            return

        for work_path in args[1:]:
            code = os.path.basename(work_path)
            work = Work.objects.filter(code=code).first()

            if not work:
                self.stdout.write('Importing ' + work_path)

                try:
                    import_work(work_path, page, publisher_index_page)
                except Exception as e:
                    self.logger.error('E: Failed to import {0} {1}'.format(
                        work_path, _e(e.message)))
                    self.stderr.write('E: Failed to import {0} {1}'.format(
                        work_path, _e(e.message)))
