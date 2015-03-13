import logging
import os
import re

from django.core.files import File
from django.db import transaction
from django.utils.text import slugify

from wagtail.wagtaildocs.models import Document

from catalogue.models import Advert, City, Country, Library, STP
from catalogue.pdf_parser import PDFParser
from catalogue.work_importer import WorkImporter


logger = logging.getLogger(__name__)

def _clean_rubric (rubric):
    rubric = rubric.decode('utf-8')
    rubric = re.split(r'(\.\d{2}\.\d{2}\.\d{4}|\.v\.)',
                      rubric)[0].replace('_', ' ')
    return rubric

def _clean_publisher_name (publisher_name, fragment):
    publisher_name = publisher_name.decode('utf-8')
    return unicode(os.path.basename(publisher_name).split(fragment)[0])

@transaction.atomic
def import_adverts (advert_dir):
    logging.debug('Importing adverts')
    for root, dirs, files in os.walk(advert_dir):
        publisher_name = _clean_publisher_name(root, ' advt')
        logger.debug('publisher_name: {}'.format(publisher_name.encode('utf-8')))
        for filename in files:
            if filename.endswith('.pdf'):
                rubric = _clean_rubric(filename)
                document = Document(title=u'{}; {}'.format(
                    publisher_name, rubric))
                with open(os.path.join(root, filename), 'rb') as fh:
                    pdf_file = File(fh)
                    document.file.save(filename, pdf_file)
                document.tags.add('advert')
                advert = Advert()
                advert.publisher_name = publisher_name
                advert.rubric = rubric
                advert.pdf = document
                advert.save()
                logger.debug('rubric: {}'.format(rubric.encode('utf-8')))

def import_libraries (library_dir, index_page):
    logging.debug('Importing libraries')
    for root, dirs, files in os.walk(library_dir):
        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.abspath(os.path.join(root, filename))
                import_library(file_path, index_page)

@transaction.atomic
def import_library (file_path, index_page):
    logger.debug('Importing {}'.format(file_path))
    parser = PDFParser(file_path)
    content = parser.get_text_content()
    if not content:
        logger.debug('Found no content in the PDF')
        return

    # gets the library heading
    heading = content.split('\n')[0]
    heading_parts = heading.split('   ')

    # gets the library code, the first value before the spaces
    if len(heading_parts) < 2:
        code = content.split('\n')[1]
    else:
        code = heading_parts[0].strip()

    # the information after the spaces
    metadata = heading_parts[-1]
    metadata_parts = metadata.split(',')

    # the country name is the first element in the metadata
    country_name = metadata_parts[0].strip()
    # and the city the second
    city_name = metadata_parts[1].strip()

    # if the county is usa
    if country_name == 'United States of America':
        # the library name is after the state
        name = ','. join(metadata_parts[3:]).strip()
    else:
        # otherwise the library name comes after the city
        name = ','. join(metadata_parts[2:]).strip()

    logger.debug(u'{0} {1} {2} {3}'.format(code, country_name, city_name, name))

    # gets the country
    country = Country.objects.filter(name=country_name).first()

    # if the country is not in the db yet
    if not country:
        # creates a new country object
        country = Country(name=country_name)
        country.save()

    # gets the city
    city = City.objects.filter(name=city_name, country=country).first()

    # if the city is not in the db yet
    if not city:
        # creates a new city object
        city = City(country=country, name=city_name)
        city.save()

    # gets the library
    slug = slugify(code)[:50]
    # Use the slug for lookups, because there are case differences in
    # some references that are meant to be the same.
    library = Library.objects.filter(slug=slug).first()

    # if the library is not in the db
    if not library:
        # creates a new library
        library = Library(title=code, city=city, name=name)
        library.slug = slug
        index_page.add_child(instance=library)
    else:
        logger.warning('Duplicate library')
        # otherwise update the library
        library.city = city
        library.name = name

    # Create a Library PDF Document.
    document = Document(title=code)
    with open(file_path, 'rb') as fh:
        pdf_file = File(fh)
        document.file.save(os.path.basename(file_path), pdf_file)
    document.tags.add('library')
    library.pdf = document
    library.save()

@transaction.atomic
def import_stps (stps_dir):
    logger.debug('Importing STPs')
    for root, dirs, files in os.walk(stps_dir):
        publisher_name = _clean_publisher_name(root, ' STP')
        logger.debug('publisher_name: {}'.format(publisher_name.encode('utf-8')))
        for filename in files:
            if filename.endswith('.pdf'):
                rubric = _clean_rubric(filename)
                document = Document(title=u'{}; {}'.format(
                    publisher_name, rubric))
                with open(os.path.join(root, filename), 'rb') as fh:
                    pdf_file = File(fh)
                    document.file.save(filename, pdf_file)
                document.tags.add('STP')
                stp = STP()
                stp.publisher_name = publisher_name
                stp.rubric = rubric
                stp.pdf = document
                stp.save()
                logger.debug('rubric: {}'.format(rubric.encode('utf-8')))

def import_works (works_dir, works_page, publishers_page):
    for work_dir in os.listdir(works_dir):
        work_dir = os.path.join(works_dir, work_dir)
        try:
            import_work(work_dir, works_page, publishers_page)
        except Exception, err:
            try:
                logger.error('Failed to import {}: {}'.format(work_dir, err))
            except:
                logger.error('Failed to import {} due to error of type {}'.format(work_dir, type(err)))

@transaction.atomic
def import_work (work_dir, works_page, publishers_page):
    logger.debug('Importing work from {}'.format(work_dir))
    wi = WorkImporter(work_dir)
    wi.import_work(works_page, publishers_page)
