# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.files import File
from django.utils.text import slugify

from lxml import etree

from models import (_d, Copy, Impression, ImpressionCopy, ImpressionPDF,
                    Library, Publisher, Work, WorkPDF, safe_slugify)

from pdf_parser import PDFParser

from wagtail.wagtailcore.models import Page

import glob
import logging
import os
import zipfile


class WorkImporter(object):
    """Imports work information from Word documents and PDF files. The Word
    documents have the order of the impressions of a Work, and the PDF files
    are the impressions of a Work."""

    NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    logger = logging.getLogger(__name__)

    def __init__(self, work_path):
        """Create a new Work importer class for the given path.

        :param work_path: path to the Work files.
        """
        self._work_path = os.path.abspath(work_path)
        self._work_code = os.path.basename(self._work_path)
        self._order_of_impressions = []
        self._impressions = []

    def import_work(self, works_page, publishers_page):
        """Imports a Work: gets the work name and heading; gets the order of
        impressions; walks through the work directory and creates an
        impression object for each PDF file."""
        work = Work()
        work.code = self._work_code

        if work.code.find('Opus') >= 0:
            work.has_opus = True

            try:
                opus_n = int(work.code.split()[1].strip())
            except ValueError:
                opus_n = 66

            work.is_posthumous = (opus_n >= settings.POSTHUMOUS_WORKS_WITH_OPUS)
            work.sort_order = opus_n
        else:
            work.has_opus = False
            work.is_posthumous = (
                work.code in settings.POSTHUMOUS_WORKS_WITHOUT_OPUS)
            work.sort_order = settings.ALL_WORKS_WITHOUT_OPUS.index(work.code) + 74
        self.logger.debug('Work sort order: {}'.format(work.sort_order))
        # Heading filename.
        heading_filename = glob.glob(os.path.join(self._work_path,
                                                  '*.heading.pdf'))[0]
        work.heading = self._import_heading(heading_filename)
        work.title = work.heading.split('  ')[0].strip()
        work.slug = safe_slugify(work.title, Work)

        # Create a WorkPDF Document.
        document = WorkPDF(title=work.title)
        with open(heading_filename, 'rb') as fh:
            pdf_file = File(fh)
            document.file.save(os.path.basename(heading_filename), pdf_file)
        document.tags.add('work')
        work.pdf = document

        # gets the order of impressions
        self._order_of_impressions = self._import_order_of_impressions()
        self.logger.debug(self._order_of_impressions)
        works_page.add_child(instance=work)
        self._import_impressions(work, publishers_page)

    def _import_impressions (self, work, publishers_page):
        # walks through the work directory to convert the PDF files
        for root, dirs, files in os.walk(self._work_path):
            # loops through all the files
            for f in files:
                # checks it is an impression PDF
                if f.endswith('.pdf') and not(f.endswith('.heading.pdf')):
                    f_path = _d(os.path.abspath(os.path.join(self._work_path, f)))
                    self._import_impression(work, publishers_page, f_path)

    def _import_impression (self, work, publishers_page, f_path):
        # creates a new PDFParser to get the impression
        self.logger.debug('Parsing {}'.format(f_path.encode('utf-8')))
        parser = PDFParser(f_path)
        code = parser.get_impression_code()
        if code:
            self.logger.debug('Impression: ' + code)

            # Create an ImpressionPDF Document.
            document = ImpressionPDF(title=code)
            with open(f_path, 'rb') as fh:
                pdf_file = File(fh)
                document.file.save(os.path.basename(f_path), pdf_file)
            document.tags.add('impression')

            # creates a new impression
            impression = Impression()
            impression.title = code
            impression.impression_title = parser.get_title()
            impression.content = parser.get_text_content()
            impression.pdf = document
            try:
                sort_order = self._order_of_impressions.index(code)
            except Exception:
                self.logger.error(
                    u'{0} missing from order of impressions'.format(code))
                sort_order = 999
            impression.sort_order = sort_order
            impression.slug = safe_slugify(impression.title,
                                           Impression)
            impression.comments = parser.get_comments()
            self._import_copies(impression, parser, code)
            publisher_code = impression.title.split('-')[-1]
            publisher = Publisher.objects.filter(title=publisher_code).first()
            if not publisher:
                publisher = Publisher(title=publisher_code)
                publisher.slug = slugify(publisher_code)
                publishers_page.add_child(instance=publisher)
            impression.publisher = publisher
            work.add_child(instance=impression)

    def _import_copies(self, impression, parser, code):
        # adds the copies to the impression
        copies = parser.get_copies()
        # Special case some that are known not to work.
        if not copies:
            if code == u'32–1a-Sm':
                copies = {u'F-Pn': u'Ac.p. 2682 \u2013 333 x 251 mm (v). TP: annotation \u2018D\xe9pos\xe9 \xe0 la Direction\uf0bdN         1837 - No 197\u2019.'}
            elif code == u'74–1-H':
                copies = {u'F-Pn': u'4 O. 408 \uf02d 277 x 195 mm. TP: publisher\u2019s oval stamp. Wrapper (fawn): p. [1] \u2018F. CHOPIN.\uf0bdM\xe9lodies Polonaises\uf0bd - in\xe9dites en France -\uf0bdOp. 74.\uf0bdPo\xe9sies\n             Fran\xe7aises\uf0bdde VICTOR WILDER.\uf0bdPrix net. 5 Fr.\uf0bdParis, Maison J. MAHO, Editeur\uf0bdJ. Hamelle, Successeur\uf0bd25 faudourg [sic] Saint-Honor\xe9 25.\u2019, p. [2]\n             blank, pp. [3, 4] blank.',
                          u'US-Cu': u'M1619.S46 \uf02d 270 x 190 mm. TP: publisher\u2019s oval stamp, stamp \u2018SCHOTT FR\xc8RES\uf0bdBRUXELLES\u2019.'}
        keys = copies.keys()
        keys.sort()
        for key in keys:
            slug = slugify(key)
            library = Library.objects.filter(slug=slug).first()

            if not library:
                library = Library(title=key)
                library.slug = slug
                library_index_page = Page.objects.filter(
                    slug='iii').first()
                library_index_page.add_child(instance=library)

            copy = Copy()
            copy.library = library
            copy.description = copies[key]
            copy.save()

            impression.copies.add(
                ImpressionCopy(impression=impression,
                               copy=copy))

    def _import_heading(self, heading_filename):
        """Imports the heading information about the Work."""
        self.logger.debug('_import_heading {0}'.format(heading_filename))

        # creates a new PDFParser to read the contents of the heading file
        parser = PDFParser(heading_filename)

        # gets the content of the PDF file
        heading = parser.get_text_content()

        return heading

    def _import_order_of_impressions(self):
        """Imports the order of the impressions in the Work."""
        order_of_impressions = []

        # gets the first Word document
        f = glob.glob(os.path.join(self._work_path, '*.docx'))[0]

        # opens the Word document
        doc = zipfile.ZipFile(f)

        # gets the XML content of the Word document
        xml_content = doc.read('word/document.xml')

        # creates an XML element from the XML content
        root = etree.fromstring(xml_content)

        # the following code to read the docx content was adapted from
        # https://github.com/mikemaccana/python-docx/blob/master/docx.py

        # compile a list of all paragraph (p) elements
        p_list = root.xpath('//w:p', namespaces=self.NS)

        # since a single sentence might be spread over multiple text elements,
        # iterate through each paragraph, appending all text (t) children to
        # that paragraphs text
        for p in p_list:
            p_text = u''

            # loop through each paragraph
            for element in p.iter():
                # t (text) elements
                if element.tag == '{' + self.NS['w'] + '}t':
                    if element.text:
                        p_text = p_text + element.text
                # sym (symbol) elements
                elif element.tag == '{' + self.NS['w'] + '}sym':
                    # converts the symbol to unicode character
                    char = unichr(int(
                        element.get('{' + self.NS['w'] + '}char'), 16))
                    p_text = p_text + char

            # add our completed paragraph text to the list of paragraph text
            if len(p_text) > 0:
                order_of_impressions.append(p_text)

        return order_of_impressions
