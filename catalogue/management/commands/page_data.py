# -*- coding: utf-8 -*-

from collections import OrderedDict


# The documents are referenced by page content, via the database IDs,
# so these must be ordered.
document_data = {
    1: {
        'file': 'Table 1.pdf',
        'title': "Table 1 'First editions' with revised music text"
    },
    2: {
        'file': 'Table 2.pdf',
        'title': 'Table 2 Later editions'
    },
    3: {
        'file': 'Table 3.pdf',
        'title': u'Table 3 Chopin’s French publishers'
    },
    4: {
        'file': 'Table 4.pdf',
        'title': u'Table 4 Changes in ownership and acquisitions: Chopin’s French publishers'
    },
    5: {
        'file': 'Table 5.entire.pdf',
        'title': 'Table 5 Works published in France with opus number'
    },
    6: {
        'file': 'Table 6.pdf',
        'title': 'Table 6 Works published in France without opus number'
    },
    7: {
        'file': 'Table 7.pdf',
        'title': 'Table 7 Works published posthumously in France'
    },
    8: {
        'file': 'Table 8.pdf',
        'title': u'Table 8 Chopin’s German/Austrian publishers'
    },
    9: {
        'file': 'Table 9.pdf',
        'title': u'Table 9 Changes in ownership and acquisitions: Chopin’s German/Austrian publishers'
    },
    10: {
        'file': 'Table 10.entire.pdf',
        'title': 'Table 10 Works published in the German states with opus number'
    },
    11: {
        'file': 'Table 11.pdf',
        'title': 'Table 11 Works published in the German states without opus number or posthumously'
    },
    12: {
        'file': 'Table 12.pdf',
        'title': u'Table 12 Chopin’s English publishers'
    },
    13: {
        'file': 'Table 13.pdf',
        'title': u'Table 13 Changes in ownership, acquisitions and reprints: Chopin’s English publishers'
    },
    14: {
        'file': 'Table 14.entire.pdf',
        'title': 'Table 14 Works published in England with opus number'
    },
    15: {
        'file': 'Table 15.pdf',
        'title': 'Table 15 Works published in England without opus number or posthumously'
    },
    16: {
        'file': 'Table 16.pdf',
        'title': 'Table 16 Possible TPs and publication dates of defective English Chopin editions as inferred from advertisements'
    },
    17: {
        'file': 'Table 17.pdf',
        'title': u'Table 17 Chopin’s Polish publishers'
    },
    18: {
        'file': 'Table 18.pdf',
        'title': u'Table 18 Changes in ownership: Chopin’s Polish publishers'
    },
    19: {
        'file': 'Table 19.pdf',
        'title': 'Table 19 Italian publisher'
    }
}

document_data = OrderedDict(sorted(document_data.items(), key=lambda t: t[0]))

abbreviation_data = {
    u'AA': u'acquisition advertisement',
    u'ADF': u'Additional Distinguishing Feature(s)',
    u'advt(s)': u'advertisement(s)',
    u'AFE': u'Austrian first edition',
    u'AmZ': u'<i>Allgemeine musikalische Zeitung</i>',
    u'ATP': u'album title page',
    u'b.': u'bar',
    u'BnF': u'Bibliotheque nationale de France',
    u'bs': u'bars',
    u'c.': u'circa',
    u'CFC': u'<i>Correspondance de Frédéric Chopin</i> (see <a id="20" linktype="page">Bibliography</a>)',
    u'Ch&T': u'Chomiński and Turło, <i>Katalog dzieł Fryderyka Chopina</i> (see <a id="20" linktype="page">Bibliography</a>)',
    u'col.': u'column',
    u'cols.': u'columns',
    u'CP': u'cover page',
    u'CT': u'caption title',
    u'CTP': u'common title page',
    u'DF': u'Distinguishing Feature(s)',
    u'DMF': u'Distinguishing Musical Feature(s)',
    u'edn': u'edition',
    u'EFE': u'English first edition',
    u'engr': u'engraved',
    u'EO': u"STP of u'ÉDITION ORIGINALE| OEUVRES COMPLÈTES POUR LE PIANO|DE|FRÉDÉRIC CHOPIN (...)' published by G. Brandus et S. Dufour→G. Brandus et Cie→Brandus et Cie→Ph. Maquet",
    u'FFE': u'French first edition',
    u'Fl.': u'Florin(s)',
    u'FL': u'footline',
    u'Florp.': u'floren polski (i.e. Polish florin(s))',
    u'FPA': u'first publication announcement',
    u'GFE': u'German first edition',
    u'gGr.': u'gute Groschen',
    u'GMP': u'<i>Gazette musicale de Paris</i>',
    u'Gr.': u'Groschen',
    u'GW': u'<i>Gazeta Warszawska</i>',
    u'HL': u'headline',
    u'HT': u'half-title',
    u'IB': u'<i>Intelligenz-Blatt</i> (in AmZ)',
    u'IFE': u'Italian first edition',
    u'ITP': u'individual title page',
    u'KA': u'<i>Kurze Anzeige</i> (in AmZ)',
    u'KFC': u'<i>Korespondencja Fryderyka Chopina</i> (see <a id="20" linktype="page">Bibliography</a>)',
    u'Kop.': u'kopeck(s)',
    u'Kr.': u'Kreutzer(s)',
    u'KW': u'<i>Kurjer Warszawski</i>',
    u'LH': u'left hand',
    u'lith': u'lithographed',
    u'MIM': u'<i>Musikalisch-literarischer Monatsbericht</i>',
    u'Mk.': u'Mark(s)',
    u'mm': u'millimetre(s)',
    u'mvt(s)': u'movement(s)',
    u'MW': u'<i>Musical World</i>',
    u'Ngr.': u'Neugroschen',
    u'p.': u'page',
    u'PA': u'publication advertisement',
    u'PD': u'publication date',
    u'Pf.': u'Pfennig(s)',
    u'PFE': u'Polish first edition',
    u'pp.': u'pages',
    u'R': u'<i>Rezensionen</i> (in AmZ)',
    u'RD': u'registration date',
    u'RGMP': u'<i>Revue et Gazette musicale de Paris</i>',
    u'RH': u'right hand',
    u'RH/LH': u'right and left hands (used to describe a musical feature in both parts)',
    u'Rs.': u'srebrny rubel (i.e. silver rouble(s))',
    u'SC': u'sub-caption',
    u'sep.': u'separate',
    u'Sgr.': u'Silbergroschen',
    u'STP': u'series title page',
    u'Thlr.': u'Thaler(s)',
    u'TP': u'title page',
    u'vol.': u'volume',
    u'vols.': u'volumes',
    u'WP': u'wrapper page',
    u'WZ': u'<i>Wiener Zeitung</i>',
    u'złp., Złtp.': u'złoty polski',
}

bad_library_codes = [
    u'Buch-u',
    u'EDITEURS-COMMISSIORES',
    u'Fantaisie-Transcription',
    u'Fantasy-Impromptu',
    u'Half-title',
    u'I-A',
    u'Instrumenten-u',
    u'MUSIKALIEN-LEIHANSTALT',
    u'PIANOFORTE-WERKE',
    u'PUITS-GAILLOT',
    u'quasi-oval',
    u'reddish-brown',
    u'Saint-Honoré',
    u'Sub-caption',
    u'Zaleska-Rosengardt',
]
