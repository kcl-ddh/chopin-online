# -*- coding: utf-8 -*-

import logging
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import unicodedata

from pyparsing import Combine, FollowedBy, Group, LineEnd, LineStart, Literal, \
    OneOrMore, Optional, SkipTo, StringEnd, StringStart, Suppress, Word

from .models import _d


class PDFParser (object):

    """Parser for PDF documents. It converts a PDF to text and provides
    access to its parsed contents."""

    logger = logging.getLogger(__name__)

    def __init__ (self, pdf_file_path):
        """Creates a new PDF to text converter for the given PDF file.

        :param pdf_file_path: File path to the PDF.

        """
        self._content = self._extract_text(os.path.abspath(pdf_file_path))
        self._g = self._define_grammar()

    def _define_grammar (self):
        g = {}
        label = Literal('Contents') | Literal('Caption title') | \
                Literal('Sub-caption') | Literal('Half-title') | \
                Literal('Footline') | Literal('Comments') | \
                Literal('Modificatons') | Literal('Errors') | \
                Literal('DMF') | Literal('ADF')
        copies_label = LineStart() + Literal('Copies')
        all_chars = u''.join(unichr(c) for c in xrange(65536)
                             if unicodedata.category(unichr(c)).startswith('L') )
        section_separator = LineEnd() + FollowedBy(label | copies_label |
                                                   StringEnd())
        section = SkipTo(section_separator)
        library = Combine(Word(all_chars) + Literal(u'-') + Word(all_chars))
        copy_separator = LineEnd() + FollowedBy(library) | \
                         LineEnd() + StringEnd() | StringEnd()
        copy = library + SkipTo(copy_separator) + Suppress(copy_separator)
        g['comments'] = Suppress('Comments') + SkipTo(section_separator)
        g['code'] = StringStart() + SkipTo(LineEnd()) + Suppress(LineEnd())
        g['title'] = Suppress(g['code']) + Suppress(LineEnd()) + section
        g['copies'] = Suppress(copies_label) + OneOrMore(Group(copy))
        return g

    def _extract_text (self, pdf_path):
        """Parses the PDF file and returns the text content."""
        # I don't know why the temporary PDF file is used; do
        # non-ASCII characters in the filename cause problems for
        # pdftotext? That seems unlikely (and is definitely not the
        # case on my Linux system).
        text = ''
        tmp_dir = tempfile.mkdtemp()
        try:
            # creates a temp pdf file without unicode characters in the name
            tmp_pdf_path = os.path.join(tmp_dir, 'tmp.pdf')
            tmp_txt_path = os.path.join(tmp_dir, 'tmp.txt')
            shutil.copyfile(pdf_path, tmp_pdf_path)

            # parses the PDF file with the pdftotext util using a subprocess
            cmd = 'pdftotext -enc UTF-8 -layout {} {}'.format(tmp_pdf_path,
                                                              tmp_txt_path)
            args = shlex.split(cmd)
            try:
                subprocess.check_call(args)
            except subprocess.CalledProcessError, err:
                self.logger.error(
                    'Failed to convert the PDF file to text: {}'.format(err))

            with open(tmp_txt_path, 'rU') as fh:
                # reads the full content of the txt file
                text = _d(fh.read().strip())
        finally:
            shutil.rmtree(tmp_dir)
        return text

    def get_comments (self):
        """Returns the text contents of the comments section."""
        matches = self._g['comments'].searchString(self._content)
        if not matches:
            self.logger.debug('No comments found.')
            matches = [['']]
        elif len(matches) > 1:
            self.logger.warning('More than one set of comments found!')
        return matches[0][0]

    def get_text_content(self):
        """Returns the text content of the PDF file."""
        return self._content

    def get_impression_code(self):
        """Returns the Impression code."""
        matches = self._g['code'].searchString(self._content)
        if not matches:
            self.logger.error('No code found.')
            matches = [['']]
        return re.sub(r'\s', '', matches[0][0], flags=re.U)

    def get_title(self):
        """Returns the Impression title."""
        matches = self._g['title'].searchString(self._content)
        if not matches:
            self.logger.error('No title found')
            matches = [['']]
        return matches[0][0]

    def get_copies(self):
        """Returns the Impression copies."""
        # Returns a dictionary keyed to the library code, with the
        # shelfmark and description as values.
        matches = self._g['copies'].searchString(self._content)
        copies = {}
        if not matches:
            self.logger.warning('No copies found')
            copies = {}
        else:
            for match in matches[0]:
                copies[match[0]] = match[1].strip()
        return copies
