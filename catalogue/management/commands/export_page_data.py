from collections import OrderedDict
import cPickle
import logging

from django.core.management.base import BaseCommand, CommandError

from wagtail.wagtailcore.models import Page

from catalogue import models


class Command (BaseCommand):

    args = '<output_file>'
    help = 'Exports all page content into a file that can be then used by import_all.'
    logger = logging.getLogger(__name__)

    def __init__ (self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle (self, *args, **options):
        if not args or len(args) != 1:
            raise CommandError('Specify the output file')
        output_filename = args[0]
        page_data = {
            'root': {
                'class': Page,
                'kwargs': {
                    'depth': 1,
                    'numchild': 1,
                    'path': '0001',
                    'title': 'Root'
                }
            },
            'aco': {
                'class': Page,
                'kwargs': {
                    'depth': 2,
                    'numchild': 1,
                    'path': '00010001',
                    'title': 'Annotated Catalogue Online'
                }
            },
        }
        export_models = [models.HomePage, models.IndexPage, models.RichTextPage,
                         models.PublisherIndexPage, models.AbbreviationIndexPage,
                         models.STPIndexPage, models.LibraryIndexPage,
                         models.Catalogue, models.AdvertIndexPage]
        for model in export_models:
            logging.debug('Exporting instances of {0}'.format(model))
            for page in model.objects.all():
                key = '{0}-{1}'.format(page.title.encode('UTF-8'), page.path)
                page_data[key] = {
                    'class': page._meta.model,
                    'kwargs': {
                        'depth': page.depth,
                        'numchild': page.numchild,
                        'path': page.path,
                        'show_in_menus': page.show_in_menus,
                        'slug': page.slug,
                        'title': page.title
                    }
                }
                try:
                    page_data[key]['kwargs']['content'] = page.content
                except AttributeError:
                    pass
                try:
                    page_data[key]['kwargs']['introduction'] = page.introduction
                except AttributeError:
                    pass
        page_data = OrderedDict(sorted(page_data.items(),
                                       key=lambda t: t[1]['kwargs']['path']))
        with open(output_filename, 'w') as fh:
            cPickle.dump(page_data, fh)
