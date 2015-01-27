# -*- coding: utf-8 -*-

from django.test import TestCase
from catalogue.pdf_parser import PDFParser
from catalogue.models import _d


class TestPDFToText(TestCase):

    def setUp(self):
        file_path = 'catalogue/tests/docs/Opus 1/1–1-BRZ.v.1.pdf'
        self.parser = PDFParser(file_path)
        self._expected_code = u'1–1-BRZ'

    def test_get_text_content(self):
        content = self.parser.get_text_content()
        expected_content = _d('''1–1-BRZ

RONDEAUcomposé pour lePIANOFORTEet dédiéà M de LindePARFREDERIC CHOPINProprieté de l’editeur
à Varsovie chez A. Brzezina

Contents           6 leaves: p. [1] lith ITP, pp. 2–11 lith text, p. [12] blank.
Sub-caption        p. 2: Rondo.

Comments           PFE published without plate number, printed on grey paper. PD: 2/6/1825 (KW No. 129). No price appears on TP
                   but, according to advt in KW, cost was 3 złp.
Errors             TP: ‘Proprieté’, ‘l’editeur’.

Copies

D-Dl       Mus. 5565-T-530 – 274 x 342 mm.
PL-Wn      Mus.III.127.998 Cim.  237 x 324 mm (v). TP: signature ‘Helena Turno1830’.
PL-Wnifc   D/508 – 243 x 323 mm. TP: stamp ‘a Leopol [illegible]’. Reduction in size resulted in loss of pagination on pp. 2, 5, 6, 10, 11.
'''.strip())
        self.assertEqual(content, expected_content)

    def test_get_impression_code(self):
        expected = self._expected_code
        impression_code = self.parser.get_impression_code()
        self.assertEqual(expected, impression_code)

    def test_get_title(self):
        title = self.parser.get_title()
        expected_title = _d('''RONDEAUcomposé pour lePIANOFORTEet dédiéà M de LindePARFREDERIC CHOPINProprieté de l’editeur
à Varsovie chez A. Brzezina''')
        self.assertEqual(title, expected_title)

    def test_get_comments(self):
        comments = self.parser.get_comments()
        expected_comments = _d('''PFE published without plate number, printed on grey paper. PD: 2/6/1825 (KW No. 129). No price appears on TP
                   but, according to advt in KW, cost was 3 złp.''')
        self.assertEqual(comments, expected_comments)

    def test_get_copies(self):
        copies = self.parser.get_copies()
        expected_copies = {
            u'D-Dl': u'Mus. 5565-T-530 – 274 x 342 mm.',
            u'PL-Wn': u'Mus.III.127.998 Cim.  237 x 324 mm (v). TP: signature ‘Helena Turno1830’.',
            u'PL-Wnifc': u'D/508 – 243 x 323 mm. TP: stamp ‘a Leopol [illegible]’. Reduction in size resulted in loss of pagination on pp. 2, 5, 6, 10, 11.'
        }
        self.assertEqual(copies, expected_copies)
