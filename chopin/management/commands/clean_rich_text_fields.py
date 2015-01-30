from bs4 import BeautifulSoup

from django.core.management.base import NoArgsCommand

from catalogue.models import IndexPage, RichTextPage

import logging
import re


class Command(NoArgsCommand):
    help = """Cleans the rich text fields that were copied and pasted from word
    documents"""

    logger = logging.getLogger(__name__)

    def handle_noargs(self, **options):
        for page in IndexPage.objects.all():
            if page.introduction:
                self.logger.debug(u'Cleaning {0}'.format(page.title))
                page.introduction = self._add_footnote_ids(page.introduction)
                page.introduction = self._annotate_characters(
                    page.introduction)
                page.save()

        for page in RichTextPage.objects.all():
            if page.content:
                self.logger.debug(u'Cleaning {0}'.format(page.title))
                page.content = self._add_footnote_ids(page.content)
                page.content = self._annotate_characters(
                    page.content)
                page.save()

    def _add_footnote_ids(self, html):
        soup = BeautifulSoup(html)
        links = soup.find_all('a')

        for link in links:
            if link.has_attr('href'):
                if re.findall(r'_ftn\d+', link['href']):
                    if not link.has_attr('id'):
                        link['id'] = '_ftnref{0}'.format(
                            re.findall(r'\d+', link['href'])[0])

            if link.has_attr('href'):
                if re.findall(r'_ftnref\d+', link['href']):
                    if not link.has_attr('id'):
                        link['id'] = '_ftn{0}'.format(
                            re.findall(r'\d+', link['href'])[0])

        return str(soup)
