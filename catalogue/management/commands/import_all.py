"""Command to populate an empty database with data imported from
various sources."""


import logging
import os.path

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from wagtail.wagtailcore.models import GroupPagePermission, Page, Site
from wagtail.wagtaildocs.models import Document

from catalogue.models import Abbreviation, Advert, City, Copy, Country, \
    Library, STP
from page_data import abbreviation_data, bad_library_codes, document_data, \
    page_data
from pdf_import_utils import import_adverts, import_libraries, import_stps, \
    import_works


class Command (BaseCommand):

    args = '<pdf_dir>'
    help = 'Import all data into fresh database'
    logger = logging.getLogger(__name__)

    def __init__ (self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self._pages = {}

    def handle (self, *args, **options):
        if not args or len(args) != 1:
            raise CommandError('Specify the pdf directory')
        pdf_dir = args[0]
        self._import_documents(pdf_dir)
        self._import_pages()
        self._import_snippets()
        self._import_pdfs(pdf_dir)
        self._add_permissions()
        self._tidy()

    def _add_permissions (self):
        # Allow Editors to do anything.
        editors = Group.objects.get(name='Editors')
        root_page = self._pages['root']
        for permission_type in ('edit', 'publish', 'lock'):
            permission = GroupPagePermission(group=editors, page=root_page,
                                             permission_type=permission_type)
            permission.save()
        for snippet_model in (Advert, Abbreviation, City, Copy, Country, STP):
            content_type = ContentType.objects.get_for_model(snippet_model)
            permissions = Permission.objects.filter(content_type=content_type)
            editors.permissions.add(*list(permissions))

    def _import_abbreviations (self):
        for abbreviation, description in abbreviation_data.items():
            abb = Abbreviation(abbreviation=abbreviation,
                               description=description)
            abb.save()

    def _import_documents (self, pdf_dir):
        doc_dir = os.path.join(pdf_dir, 'documents')
        for data in document_data.values():
            title = data['title']
            filename = data['file']
            self.logger.debug('Creating document {}'.format(
                title.encode('utf-8')))
            doc = Document(title=title)
            with open(os.path.join(doc_dir, filename), 'rb') as fh:
                document_file = File(fh)
                doc.file.save(filename, document_file)
            doc.save()

    def _import_pages (self):
        # Delete any existing pages.
        for page in Page.objects.all():
            page.delete()
        for page_name, info in page_data.items():
            self.logger.debug('Creating page {}'.format(page_name))
            page = info['class'](**info['kwargs'])
            page.save()
            self._pages[page_name] = page
        # Add a Wagtail Site, or nothing will appear anywhere.
        site = Site(hostname='localhost', root_page=self._pages['home'],
                    is_default_site=True)
        site.save()

    def _import_pdfs (self, pdf_dir):
        advert_dir = os.path.join(pdf_dir, 'adverts')
        import_adverts(advert_dir)
        library_dir = os.path.join(pdf_dir, 'libraries')
        import_libraries(library_dir, self._pages['library_appendix'])
        stp_dir = os.path.join(pdf_dir, 'stps')
        import_stps(stp_dir)
        work_dir = os.path.join(pdf_dir, 'works')
        import_works(work_dir, self._pages['annotated_catalogue'],
                     self._pages['reference_sigla'])

    def _import_snippets (self):
        self._import_abbreviations()

    def _tidy (self):
        for library_code in bad_library_codes:
            try:
                library = Library.objects.get(title=library_code)
                library.delete()
            except Library.DoesNotExist:
                self.logger.error(u'Whoah, missing expected bad library "{}"'.format(library_code))
