# -*- coding: utf-8 -*-

from collections import OrderedDict

from wagtail.wagtailcore.models import Page

from catalogue.models import (AbbreviationIndexPage, AdvertIndexPage, Catalogue,
                              HomePage, IndexPage, LibraryIndexPage,
                              PublisherIndexPage, RichTextPage, STPIndexPage)


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
    'home': {
        'class': HomePage,
        'kwargs': {
            'content': 'Welcome to the ACO',
            'depth': 3,
            'numchild': 5,
            'path': '000100010001',
            'show_in_menus': True,
            'slug': 'home',
            'title': 'Home'
        }
    },
    'about': {
        'class': IndexPage,
        'kwargs': {
            'depth': 4,
            'numchild': 4,
            'path': '0001000100010001',
            'show_in_menus': True,
            'slug': 'about',
            'title': 'About',
        }
    },
    'about_introduction': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Introduction',
            'depth': 5,
            'numchild': 0,
            'path': '00010001000100010001',
            'show_in_menus': True,
            'slug': 'introduction',
            'title': 'Introducton'
        }
    },
    'about_project_narrative': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Project Narrative',
            'depth': 5,
            'numchild': 0,
            'path': '00010001000100010002',
            'show_in_menus': True,
            'slug': 'project-narrative',
            'title': 'Project Narrative'
        }
    },
    'about_people': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'People',
            'depth': 5,
            'numchild': 0,
            'path': '00010001000100010003',
            'show_in_menus': True,
            'slug': 'people',
            'title': 'People'
        }
    },
    'about_acknowledgments': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Acknowledgments',
            'depth': 5,
            'numchild': 0,
            'path': '00010001000100010004',
            'show_in_menus': True,
            'slug': 'acknowledgments',
            'title': 'Acknowledgments'
        }
    },
    'background': {
        'class': IndexPage,
        'kwargs': {
            'depth': 4,
            'numchild': 2,
            'path': '0001000100010002',
            'show_in_menus': True,
            'slug': 'background',
            'title': 'Background'
        }
    },
    'background_historical': {
        'class': IndexPage,
        'kwargs': {
            'depth': 5,
            'introduction': u'''<p>Chopin’s first editions pose major challenges to musicians and
musicologists alike because of their diversity and complex
interrelationships, not to mention the practical constraints that have
prevented the comprehensive comparison and evaluation required to
understand their creative history. Inadequate copyright protection
between the principal European countries during the early nineteenth
century led Chopin to employ different publishers in France, England
and the German states, thus giving rise to three ‘first editions’ of
most pieces. Each is unique, as a result of his idiosyncratic
editorial methods and ongoing compositional revisions. At different
stages in his career Chopin provided his publishers with various types
of Stichvorlage, including autographs, annotated proofsheets and
scribal copies. In each case, the music continually evolved as
autograph or scribal copies were prepared or proofsheets corrected,
resulting in significant differences between the multiple first
editions. Further differences arose from the interventions of house
editors and professional correctors in successive impressions which
until recently have collectively been regarded as ‘first editions’ –
an error of judgement that has undermined much Chopin
scholarship. Only now is there greater recognition of the importance
of these differences – likewise that of the first editions as a whole,
which constitute one of the principal sources of knowledge of the
composer’s music. Without thorough analysis of these sources as well
as the nineteenth-century practices that gave rise to them, Chopin’s
output cannot be understood in its historical context nor its content
accurately reproduced in any modern edition. The very identity of the
Chopin work is at stake.</p>

<p>The Annotated Catalogue begins with this survey of the publication
history of Chopin’s music within each of the countries concerned
(including Poland and Italy, where a number of Chopin editions were
produced). We also offer observations about music publishing in the
nineteenth century more generally. Although focused on the Chopin
first editions, the conclusions presented here potentially apply to
the music of contemporary composers, most of whom worked under similar
conditions and often with the same publishers.</p>''',
            'numchild': 4,
            'path': '00010001000100020002',
            'show_in_menus': True,
            'slug': 'historical-overview',
            'title': 'Historical overview'
        }
    },
    'background_legal': {
        'class': IndexPage,
        'kwargs': {
            'depth': 6,
            'introduction': u'''<p>The legislation governing publication practices and copyright
protection during Chopin’s lifetime and after his death varied
considerably between the principal European nations. This affected not
only the nature and quantity of the contractual agreements into which
the composer entered with his publishers, but also the history of
commercial sales after the music’s initial release. For example,
perusal of the Annotated Catalogue reveals striking differences in the
number of Chopin first editions published in the German states as
against those released in France or England – differences which can be
explained with reference to the respective legal frameworks in force
at the time.</p>''',
            'numchild': 3,
            'path': '000100010001000200020001',
            'show_in_menus': True,
            'slug': 'legal-contexts',
            'title': 'Legal contexts'
        }
    },
    'background_legal_france': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>French law during the first half of the nineteenth century
concerning copyright in artistic works was based on the decree of
19–24 June 1794 abolishing the royal privileges that previously had
existed. It established the exclusive right of authors, composers and
other artists throughout their lifetime to sell, provide to others to
sell, or otherwise distribute their works, or to assign their rights
to others in whole or in part. Nominated heirs or legatees benefited
from the same rights during a ten-year period following an author’s
death. This decree imposed an obligation on authors to deposit two
exemplars of their work at the Bibliothèque nationale,<a href="#_ftn1"
id="_ftnref1">[1]</a> while also setting out penalties for the
production of counterfeit or otherwise unauthorised versions.</p>

<p>Later amendments to the legislation led to changes in the number of
obligatory deposit copies as well as their place of deposit, in
addition to establishing a periodical entitled <i>Bibliographie de la
France </i>intended to announce the release of new
publications. Successive judgements from the courts helped to redress
lacunae in the legislation, notably with regard to the rights of
foreign authors whose work was published in France, as well as the
necessary conditions for the protection of works first published
outside French territory.</p>

<p>The legal situation in France during Chopin’s lifetime can
therefore be summarised as follows. For a published work to enjoy full
legal protection, an exemplar had to be deposited. A work originally
published outside France could also benefit from such protection, but
only if a copy thereof was deposited before an unauthorized edition
appeared in France (generally the latter would be a pirated version of
the original, foreign print). The registers of the Bibliothèque
nationale de France and of the <i>dépôt légal</i> reveal that copies
of Chopin’s Opp. 1, 2, 5–9, 12, 16, 17 &amp; 42, and of the <i>Grand
Duo Concertant</i> for Piano and Cello, the Mazurka dedicated to Emile
Gaillard and <i>Hexameron</i><a href="#_ftn2" id="_ftnref2">[2]</a>
were never deposited; as a result, it would have been possible for
contemporary publishers to reprint them without restriction. This was
indeed the fate of the Rondo Op. 1 and Variations Op. 2, as well as
the Polonaise Op. 3 (although its publication history is somewhat
different), all of which were released by several Paris publishers
while Chopin was still alive.<a href="#_ftn3"
id="_ftnref3">[3]</a></p>

<p>At the end of 1859 Chopin’s works entered the public domain in
France, and soon after new editions of his music started flooding the
market. They became direct competitors to the original editions, which
eventually succumbed to commercial pressures although a number
remained available into the early twentieth century.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> The name of the
Bibliothèque nationale de France (as it is known today) evolved with
the various changes of political system in France since 1789 – hence
its successive designations as ‘Bibliothèque impériale’, ‘Bibliothèque
royale’, etc.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> A collaborative set
of variations by Liszt, Thalberg, Pixis, Henri Herz, Czerny and
Chopin, composed to raise funds for Italian refugees. Liszt’s
contribution to the work was the most extensive.</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> For discussion of the
multiple French editions see ‘France’ under ‘Chopin’s publishers’.</p>
</div>''',
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000200010001',
            'show_in_menus': True,
            'slug': 'france',
            'title': 'France'
        }
    },
    'background_legal_germany': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Throughout Chopin’s lifetime the states within the Deutscher
Bund (German Confederation) had no common legislation affording
copyright protection to authors; nevertheless, the Verein der
deutschen Musikalienhändler (Union of German Music Sellers) exercised
a certain supervisory control over music publishing after its
establishment in Leipzig in May 1830.<a href="#_ftn1"
id="_ftnref1">[1]</a> The absence of legislation by no means prevented
the market from operating effectively in these states. In the case of
Chopin’s editions, apart from one suspect instance identified by
Maurice Brown (though unverified to date),<a href="#_ftn2"
id="_ftnref2">[2]</a> the German publishers behaved appropriately
towards each other.</p>

<p> The creation of the Verein was not the only initiative to be taken
with regard to the protection of authors’ rights: between 1827 and
1829, Prussia signed accords with thirty-three states within the
Confederation in order to effect reciprocal protection. It was also
the first to promulgate its own legislation in this respect. A law
from 1837 defined the conditions surrounding the protection of
artistic works, whereby copyright lasted until thirty years after the
author’s death. In 1844 Prussia extended protection to foreign authors
living outside the Confederation states themselves, provided that the
same guarantees were offered to Prussian citizens who wished to
publish works in the foreign countries in question. One concrete
outcome of this development was the treaty signed with England in
1846.</p>

<p>The fact that legal deposit was not required in the German states
markedly contrasts with the position in France and England.  German
music publishers were nevertheless obliged to provide the Verein with
a copy of their editions, to be registered in the institution’s
archives. Once this formality had been completed, the newly registered
scores were retained in the archive for one year before being returned
to their owners. The release of new editions was announced in the
musical press as well as in specialist periodicals such as the
<i>Musikalisch-literarischer Monatsbericht</i> (MlM), in essence
reproducing the content of the archive’s registers.</p>

<p>It should be pointed out that, in signing contracts with his German
publishers, Chopin ceded to them the rights to his works in all
countries except France and Great Britain.<a href="#_ftn3"
id="_ftnref3">[3]</a> Thanks to the extensive commercial foothold of
these publishers and also the especially long period of copyright
protection, the German editions held a privileged position relative to
those from other countries, thus explaining their abundance in this
catalogue.</p>

<p>The year 1879 marked the entry of Chopin’s works into the public
domain in Germany as well as the beginning of the end for the German
first editions<a href="#_ftn4" id="_ftnref4">[4]</a> of his music. The
release in 1878–80 of Breitkopf &amp; Härtel’s complete edition,
prepared by Bargiel, Brahms, Franchomme, Liszt, Reinecke and Rudorff,
precipitated the disappearance from the market of the publisher’s
Chopin first editions except that of the Sonata Op. 65. Similarly,
Carl Mikuli’s 1879 edition prompted the withdrawal from commercial
sale of Kistner’s existing Chopin material. Only Schlesinger
(R. Lienau), Hofmeister and probably also Schuberth continued to
market their original Chopin output beyond that date, but in parallel
to the new prints.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> Publishers in Austria
as well as those in Lombardy-Venetia – which until 1865 was ruled by
the Austrian Empire – also belonged to the Verein.  Apart from
2–1-HAt, the formula indicating that a given score had been registered
at the Verein’s archives can be found on the title pages of all Chopin
editions released during the composer’s lifetime in Vienna and Milan –
namely, 2–2-HAt, 3–1-ME, 43–1-RI, 44–1-ME, 45–1a-ME, 50–1-ME,
HEX–1-HAt and HEX–1-RI. On the TP of the last of these there is an
additional indication that the edition had been deposited in the
Bibliothèque impériale. As for the works published posthumously in
Milan in 1851, the TPs bear only the Habsburg coat of arms (see
4–1-RI, VGNA–1-RI). References here to ‘the German states’ include
Austria unless otherwise indicated.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> See Brown 1972:
44. Brown refers to an edition of the Polonaise Op. 3 ostensibly
released by A. M. Schlesinger in 1832, but he provides no information
about it nor does he address the rights issues that would have
surrounded the edition. Given that the work was first published in
Vienna by Mechetti, A. M. Schlesinger’s putative edition could only
have been a pirated version if it existed at all.</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> This information can
be deduced from the contracts that Chopin signed with Breitkopf &amp;
Härtel, which make particular reference to the extent of the rights
given that this publisher distributed its output to numerous European
countries via a sophisticated network of sales agents. The list of
countries can be found in von Hase and von Hase 1968: i/198.</p>
</div>

<div id="ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref4" id="_ftn4" name="_ftn4">[4]</a> We use this term to
refer to all first editions in the strict sense, later impressions
thereof (whether revised or not) and all later editions bearing the
original plate numbers. For further discussion see the Introduction as
well as the Glossary in ‘Reference material’.</p>
</div>''',
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000200010002',
            'show_in_menus': True,
            'slug': 'the-german-states',
            'title': 'The German States'
        }
    },
    'background_legal_england': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>A long history of legislation providing copyright protection to
authors exists in the case of Great Britain, and England in
particular. Although the full benefits of the legal system in
operation when Chopin was publishing his music did not extend to the
composer himself owing to his foreign citizenship and place of
residence, his English publishers did derive benefit because Chopin
assigned his rights to them.</p>

<p>For a work to gain protection, the law stipulated that it must
first be published in England, prior to release in other
countries. Furthermore, two formalities had to be undertaken no more
than one month after publication: registration at the Company of
Stationers (i.e. Stationers’ Hall), and the deposit of one exemplar at
the British Museum. Several other libraries and institutions also had
the right, upon request, to receive a copy within a period of no more
than twelve months following publication.</p>

<p>This legislation was modified on various occasions during Chopin’s
lifetime, namely in 1814, 1833 and 1842; the changes in question
largely pertained to the period during which registration was to take
place, the number of deposit copies and the period of protection. In
the case of works published between 1814 and 1842, copyright
protection lasted either twenty-eight years or until the author’s
death if it followed thereafter. For works published after 1842,
protection lasted either forty-two years or for seven years following
the author’s death, whichever was more advantageous. When the law
changed on 1 July 1842, the new period of protection was automatically
extended for works still in copyright which had been published prior
to that date, except where the rights were held by a publisher (as in
the case of Chopin’s English editions) or by another person who had
obtained them by certain means; in these cases the more limited
original period of protection continued to apply unless an extension
had been agreed between the author and the rights-holder.<a
href="#_ftn1" id="_ftnref1">[1]</a></p>

<p>The English publishers were in a favourable position compared to
their French counterparts, as they were not required to present an
exemplar at the time of registration. As a result, they benefited from
additional time in which to prepare their editions for printing and to
introduce them to the market. The dates in the Stationers’ Hall
registers therefore do not necessarily reflect the actual history of
the commercialisation of Chopin’s music in England, instead
representing the legacy of a practice intended to counteract
piracy.</p>

<p>As in France, many of Chopin’s compositions were neither registered
nor deposited in England, including Opp. 1–3, 5–12, 14–16 &amp; 20,
the <i>Grand Duo Concertant</i> and <i>Hexameron</i>. It is odd that,
despite the registration of their titles, the English editions of
Opp. 4 &amp; 21–49 and the Variations on a German National Air are
absent from the collection of the British Museum.<a href="#_ftn2"
id="_ftnref2">[2]</a> This was probably the result of negligence on
the part of the publisher.</p>

<p>Questions about the copyright protection of Chopin’s works in
England arise in two particular cases. The first concerns the editions
of the Mazurkas Op. 63 and Waltzes Op. 64. Published in 1848 by
Cramer, Beale &amp; Co.,<a href="#_ftn3" id="_ftnref3">[3]</a> these
have generally been considered to be pirated versions. In fact, these
works immediately entered the public domain in England following their
release on the continent, given that no English firm had previously
obtained the rights and registered the works as required. Like any
other English publisher, Cramer, Beale &amp; Co. was therefore in the
position of printing these works on an entirely legal basis – as
Wessel did too, with his own publication of these opuses soon after.<a
href="#_ftn4" id="_ftnref4">[4]</a> The second case is less well
documented, preceding the one just described by nearly a decade. On 20
September 1838 <i>The Musical World</i> announced the release
by Cocks of ‘Chopin’s five Mazurka’s [<i>sic</i>]’ and of ‘Three
Nocturnos’.<a href="#_ftn5" id="_ftnref5">[5]</a> The fact that no
copies have been located could mean that the editions were never
actually produced; however, because Wessel neglected not only to
register Opp. 7 &amp; 9 but also to deposit exemplars thereof, Cocks
would have been free to publish his own scores had he wished to do
so.</p>

<p>The variable periods of copyright protection arising from the
changes in legislation referred to above led to the phased entry of
Chopin’s works into the public domain in England.  Wessel and his
successors kept the original editions on the market until the
beginning of the twentieth century; meanwhile other publishing houses
began to bring out their own Chopin editions after January 1855,
though at a slower pace than in France or the German states. The
result was that only after 1900 would there be the variety of Chopin
editions in England that had existed for some decades on the
continent.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%;
text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1"
title="">[1]</a> A contemporary publication – Curtis 1847 – summarises
and elaborates on the legislation.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> To fill these gaps
the British Library has since acquired exemplars of the English first
editions, but most are later impressions rather than original
prints.</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> During this period
Chopin’s relations with Wessel broke down completely, and he therefore
sought another publisher for Opp. 63–65.  The name of the firm
‘Jullien &amp; Co.’ appears on the TP of the Brandus edition of these
works presumably because at one point it was the intended English
publisher. Negotiations were eventually abandoned, however.</p>
</div>

<div id="ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref4" id="_ftn4" name="_ftn4">[4]</a> The Waltzes Op. 64
Nos. 1 &amp; 2 were also published by Leader &amp; Cock in January
1853.</p>
</div>

<div id="ftn5">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref5" id="_ftn5" name="_ftn5">[5]</a> The latter probably
referred to Op. 9, and the former to either Op. 6 or Op. 7. The
Mazurkas edition was most likely a reprinted continental score: the
first impression of M. Schlesinger’s Op. 6 contains five mazurkas, as
does that of the second impression of Kistner’s Op. 7 (whereas, at
this time, Wessel’s editions of both opuses included four mazurkas
each).</p>
</div>''',
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000200010003',
            'show_in_menus': True,
            'slug': 'england',
            'title': 'England'
        }
    },
    'background_general': {
        'class': IndexPage,
        'kwargs': {
            'depth': 6,
            'introduction': u'''<p>The variable publication practices within each of the countries
discussed previously – i.e. France, the German states and England –
left their mark on Chopin’s first editions in important and
distinctive ways. These are summarized below in five sections
pertaining to the physical properties of the scores, the printing
methods used, and such key components as title pages, wrappers and
covers, and music text.</p>''',
            'numchild': 5,
            'path': '000100010001000200020002',
            'show_in_menus': True,
            'slug': 'general-characteristics',
            'title': 'General characteristics'
        }
    },
    'background_general_format': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>A music score published during the first half of the nineteenth
century had little in common with those on the market today. It
typically consisted of a series of folded loose bifolia (i.e. neither
stapled nor stuck to one another) starting with a title page, followed
by a number of leaves containing the music proper and possibly also
blank sheets and/or extracts from the publisher’s catalogue (situated
either between the title page and the music text or at the end); all
of this was enclosed within a loose wrapper, i.e. a folded bifolium of
coloured paper. The vast majority of Chopin’s first editions were
produced in a folio format measuring approximately 360 mm in height by
270 mm in width.<a href="#_ftn1" id="_ftnref1">[1]</a> One exception
to this norm was the first editions published in Poland, all of which
were produced in an oblong (landscape) format;<a href="#_ftn2"
id="_ftnref2">[2]</a> although close to those above, their dimensions
were of course inverted.</p>

<p>Very few of the scores described in this catalogue have been
preserved in their original state. Their size was frequently reduced
during conservation work in libraries, when changes were made to their
physical contents through the removal of blank sheets at the end and
also the systematic disposal of original wrappers in order to
economise on space and to give the semblance of continuity when
individual copies were bound in library volumes comprising disparate
scores.</p>

<p> A given edition would be made up of one or more gatherings, each
containing an odd or even number of leaves; the extent of the music
text would determine how many were required. For example, gatherings
containing ten leaves are composed of five bifolia, while those with
eleven leaves consist of five bifolia plus a further leaf (singleton)
situated either in the middle of the section (thus, leaf 6 in the case
of the hypothetical eleven-leaf gathering described here) or,
exceptionally, elsewhere (as in the thirteen-leaf 22–1b-Sm, where leaf
10 is the singleton because of the way in which the music text was
distributed). Only a few scores – including various albums and the
volumes containing the Posthumous Works (i.e. Opp. 66–73) and
Hamelle’s edition of Op. 74 – consist of multiple gatherings;
otherwise, all of Chopin’s first editions contain no more than one.<a
href="#_ftn3" id="_ftnref3">[3]</a></p>

<p> As the above comments suggest, a number of works were originally
published in volumes, of which two types can be identified: those
assembled from scores originally released as independent editions and
thus containing individual pagination and one or more blank pages (see
for example 15–1a-Sm and 45–1-ME), and those conceived as volumes from
the start, which therefore have continuous pagination and no blank
pages between works (e.g. 23–2-B&amp;H, +45–1-Sm).<a href="#_ftn4"
id="_ftnref4">[4]</a> Some of the larger volumes of this second type
contain half-titles<a href="#_ftn5" id="_ftnref5">[5]</a> whose
purpose is either to provide basic information about the volume’s
contents or to introduce one of its constituent parts. Half-titles
appear in the French and English editions of the <i>Méthode des
Méthodes</i> (see MM–0-Sm, MM–1-Sm, MM–1a-CHAP, MM–1b-CHAP), the
Posthumous Works published in Paris and Berlin (see Posth–1-MEIj,
Posth–1-Sam), and the English edition of the Songs Op. 74 (see
74–1-LW). Several volumes also possess a table of contents or ‘index’
(i.e. ‘Inhalt’, ‘Inhaltsverzeichniss’, etc.; see 23–2-B&amp;H,
33/1&amp;2–1a-B&amp;H, 45–1-ME, MM–1a-Sam, MM–1d-Sam).</p>

<p>Most of the dedications found in Chopin’s first editions are
located on the title pages. Separate dedication pages exist in only
six impressions catalogued in this volume, though they bear no
connection to Chopin or his music as such. For example, the album
published by A. M. Schlesinger contains a dedication page expressing
the publisher’s gratitude to Princess Elisabeth Luise of Prussia,<a
href="#_ftn6" id="_ftnref6">[6]</a> while the dedication page in the
<i>Hexameron</i> notes further to the information on the TP itself
that the composition was dedicated to Princess Belgiojoso and moreover
had been written for a concert organized by her (see HEX–1-RI,
HEX–1-HAt, HEX–1a-HAt, HEX–1b-Sam). A number of works lack any
dedication – i.e. Opp. 35–37, 42, 43 &amp; 59, Etudes from <i>Méthode
des Méthodes</i>, and Mazurka from <i>La France Musicale</i>.</p>

<p>Extracts from publishers’ catalogues appear in the majority of the
English editions, irrespective of their publication date; generally
these advertisements are located on a page between the TP and the
music text, or possibly on the reverse of the last page of music
text. Such extracts rarely appeared during Chopin’s lifetime in the
French and German first editions; the few exceptions include reprints
released in Paris by Pacini (see 42–1a-P) and by Chabal (see
MEG–1b-CH, MEG–1c-CH), and certain German editions published by A. M.
Schlesinger (see D-Bds copy of 32/1–1a-Sam, 32/1–1b-Sam,
32/1–1c-Sam).</p>

<p>During the second half of the nineteenth century, catalogue
extracts were included with increasing frequency in continental Chopin
editions.<a href="#_ftn7" id="_ftnref7">[7]</a> In France, they
appeared in the edition of the Posthumous Works published by
J. Meissonnier fils and his successors, the Compagnie Musicale and
E. Gérard et Cie; in Hamelle’s edition of Op. 74 (see 74–2a-H); and in
Maquet’s reprint of Op. 9 (see 9–1g-M). Advertisements of this kind
also appear in numerous publications of Breitkopf &amp; Härtel,<a
href="#_ftn8" id="_ftnref8">[8]</a> five impressions released by
Hofmeister (1–1d-HO, 1–2-HO, 5–1h-HO, 5–1i-HO, 51–1b-HO), and various
editions of Bote &amp; Bock (MEG–1b-B&amp;B), A. M. Schlesinger
(74–1d-Sam) and B. Schott’s Sohne (WaltzEm–1e-SCH). Two Polish
editions contain similar extracts: the <i>Deux Mazurkas</i> published
by Friedlein (MazG&amp;B[[composer]i]–1-FR), and the songs
<i>Wojak</i> and <i>Źyczenie</i> released by Kocipiński
(74/10&amp;1–1-KO, 74/10–1a-KO, 74/1–1a-KO).</p>

<p>The impressions of a given edition were by no means fixed either in
content or in the order of that content: considerable variation
occurred from one score to the next, especially when editions
originally comprised an odd number of leaves. Numerous examples can be
found in this volume where blank pages were added or removed, likewise
advertisements. Such changes often necessitated commensurate
adjustments to the pagination.<a href="#_ftn9"
id="_ftnref9">[9]</a></p>

<hr align="left" size="1" width="33%"/>

<div id="_ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1">[1]</a> Note however that three albums containing
Chopin’s music – i.e.  23–2-B&amp;H, 45–1-Sm and 50/1–2-Sm – were
originally smaller in size.</p>
</div>

<div id="_ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2">[2]</a> Oblong editions were considered outmoded in
the early nineteenth century and were gradually abandoned, although
the format was retained for piano-duet repertoire, to which it is well
suited.</p>
</div>

<div id="_ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3">[3]</a> In producing sizeable works such as Op. 11,
the <i>Méthode des Méthodes</i>, the album catalogued under
64/1–1a-BR, and Opp. 10 &amp; 25 (each of which was released in France
in a single volume), the publishers preferred to distribute the text
over successive individually folded bifolia. This conclusion arises
from the close study of scores which can be reconstituted in their
original form as a series of ‘mini-gatherings’ consisting in each case
of a bifolium. The assembly of music text in this way explains how two
leaves in the second F-Pn copy of 11–1a-Sm became transposed, likewise
the interposition of a Döhler etude between two of Chopin’s in the
copies classed under MM–0-Sm: that is, both problems resulted from the
folding of a bifolium in the wrong direction, as it were ‘inside
out’.</p>
</div>

<div id="_ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref4">[4]</a> Naturally these volumes have nothing to do
with the ones assembled by libraries to facilitate classification,
storage and conservation.</p>
</div>

<div id="_ftn5">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref5">[5]</a> Half-titles can frequently be found on
wrappers; for further discussion see ‘Wrappers and covers’.</p>
</div>

<div id="_ftn6">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref6">[6]</a> Two versions of this dedication page exist:
see 32/1–1-Sam and 32/1–1a-Sam (D-Bds copy). Furthermore, all of the
albums of A. M. Schlesinger contain a supplementary page designated in
the catalogue entry as ‘lith blank dedication’, the purpose of which
may have been to allow a purchaser to enter his or her own dedication
by hand, when offering the score as a gift (see 32/1–1-Sam,
32/1–1a-Sam, 32/2–1-Sam).</p>
</div>

<div id="_ftn7">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref7">[7]</a> See Appendix II for detailed information on
the evolution of the catalogue extracts.</p>
</div>

<div id="_ftn8">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref8">[8]</a> See 16–1b-B&amp;H, 17–2a-B&amp;H,
21–1d-B&amp;H, 23–1d-B&amp;H, 24–1c-B&amp;H, 26–1b-B&amp;H,
26–2-B&amp;H, 26–2b-B&amp;H, 28–1a-B&amp;H and 29–1d-B&amp;H, as well
as the separate reprints of the mazurkas, nocturnes and polonaises in
Breitkopf &amp; Härtel’s ‘pour le Pianoforte’ series.</p>
</div>

<div id="_ftn9">
<p style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref9">[9]</a> The pagination of the following
scores was modified: 12–1b-B&amp;H, 12–1c-B&amp;H, 12–1e-B&amp;H,
16–1d-B&amp;H, 20–1d-B&amp;H, 23–1h-B&amp;H, 24–2d-B&amp;H,
27–1h-B&amp;H, 27–1i-B&amp;H, 32/1–1a-Sam (i.e. Kalkbrenner piece
within D-Bds copy), 46–1d-B&amp;H, 47–1f-B&amp;H, 64/1–1c-CHAP and
70–1d-Sam.</p>
</div>''',
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000200020001',
            'show_in_menus': True,
            'slug': 'format',
            'title': 'Format'
        }
    },
    'background_general_printing': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Three different printing methods were employed by music
publishers during the first half of the nineteenth century: engraving,
lithography and movable type. A good many editions exploited all three
techniques.</p>

<p>Most of the Polish first editions published before November 1830
(when Chopin left Warsaw in pursuit of a career as composer-pianist)
were lithographed; these include the Rondos Opp. 1 &amp; 5 (see
1–1-BRZ, 5–1-BRZ) and the Mazurka in G major
(MazG–1-KOL). Exceptionally, the Polonaise in G minor was engraved
throughout (see PolGm–1-CY), as was the collection of songs <i>Zbior
śpiewow Polskich</i>, which appeared in 1859 (see
74–1-G). <i>Wojak</i> and <i>Źyczenie</i> made use of two techniques:
engraving for the common title page and music text, and letterpress
for the extracts from Kocipiński’s catalogue (see 74/10&amp;1–1-KO,
74/10–1a-KO, 74/1–1a-KO). Post-1830 Polish first editions which were
lithographed include the Polonaise Op. 71 No. 2 (see 71/2–1-CHR), the
Mazurkas in D major, Bû major and G major, and the <i>Lento con gran
espressione</i> (see MazD,Bû,G,Lento–1-L). All other Polish first
editions from this period contain lithographed TPs and engraved music
text. Movable type was also used to prepare the pages with poetic text
in the album published by the Towarzystwo Muzyczne in Lvov (see
WaltzE–1-TM).</p>

<p>Virtually all of the French, English and Italian first editions
released during Chopin’s lifetime were engraved. Exceptions among the
French output include the lithographed scores published in the
<i>Keepsake des</i> <i>Pianistes</i> anthologies (see 45–1-Sm,
50/1–2-Sm), while the album of <i>La France Musicale</i>, which
contains a Chopin mazurka, has a lithographed album title page and
engraved music text (see MFM–1-E, MFM–1a-E). Three techniques were
employed in producing the separate volumes of posthumous works brought
out in 1855 by J. Meissonnier fils: colour lithography for the
attractive passe-partout, engraving for the music text, and movable
type for the catalogue extracts located on the verso of the last page
of music text. Movable type was also used by G. Brandus et S. Dufour
and their successors in most of the reprints produced from late 1859
onwards, namely in printing the series title page ‘ÉDITION
ORIGINALE<b>½</b>OEUVRES COMPLÈTES POUR LE
PIANO<b>½</b>DE<b>½</b>FRÉDÉRIC CHOPIN’ (hereafter
‘EO’); the music text itself was engraved or, exceptionally,
lithographed (see 9–1g-M, 34/2–2a-BR).</p>

<p>As for the Chopin first editions produced in the German states
before 1850, the vast majority have lithographed title pages and
engraved music text; exceptions include the Austrian editions of
Mechetti (Opp. 3, 50) and Tobias Haslinger (Op. 2), likewise certain
publications of Hofmeister (Op. 1, 5–1f-HO), A. M. Schlesinger
(Op. 32, <i>Grand Duo Concertant</i>) and Schuberth (Op. 43), all of
which were engraved throughout.  For the Posthumous Works published in
1855 by A. M. Schlesinger, movable type was used for the TP and Julian
Fontana’s explanatory text, and engraving for the music
text. Otherwise, the basic model described above also prevailed in
German first editions from the 1850s.</p>

<p>Almost all of the advertisements integral to an edition
(i.e. located between the TP/CTP and the music text or on the verso of
the last page of text) were printed using movable type. Only rarely
were they engraved – specifically, for two French (see 42–1a-P,
MEG–1b-CH), four German (see 32/1–1a-Sam, 32/1–1b-Sam, 32/1–1c-Sam)
and four English catalogue extracts (see 1–1-W, 2–1-W, 12–1-CRA&amp;B,
14–1-W).</p>

<p>Lithographic transfer was frequently employed during the second
half of the century, and in Chopin’s case it was first used in 1836
(see 24–1a-Sm, 26–1a-Sm). By the end of the 1850s it had become
ubiquitous throughout the German states, but not until the late 1860s
did the technique gain a similar foothold in England. Three principal
reasons explain its introduction into nineteenth-century music
publishing. First and foremost was the reduced production costs
arising from the use of lower-quality paper: whereas printing from
engraved plates required paper of sufficient thickness to withstand
high pressure from the machinery in operation, lithography could be
carried out with much lighter and thus less expensive stock. Secondly,
it effectively prolonged the life of engraved plates which, despite
their natural resistance and robustness, began to wear out after one
or two decades of heavy use.<a href="#_ftn1" id="_ftnref1">[1]</a>
Through lithographic transfer the contents of engraved plates were
easily conveyed to limestone and then reproduced on the impression
plate; the original plates thus took on the status of a back-up
copy. The third reason stems from developments within music publishing
more generally, notably the introduction of powered presses – among
them the cylindrical <i>Schnellpresse</i> (literally ‘rapid press’)
invented by Georg Sigl in 1851, which achieved greater speed and
efficiency by using a lithographic stone which was mechanically damped
and inked. At first used in the production of music periodicals,<a
href="#_ftn2" id="_ftnref2">[2]</a> machine presses such as Sigl’s
started churning out music editions towards the middle of the 1860s,
soon overtaking the production of music from engraved plates, a
technique which by contrast did not evolve and thus became outmoded.<a
href="#_ftn3" id="_ftnref3">[3]</a> It endured for the longest time in
France, where all of the reprints of Chopin’s first editions were
produced by means of this technique until c.  1880.</p>

<p>As noted above, the purpose of lithographic transfer was to obtain
a copy of the content of an engraved plate on limestone. To achieve
this an intermediate stage was required, namely the transfer of the
plate’s negative image onto special paper using slow-drying ink; then,
to obtain another negative image, the positive was immediately
transferred from the paper onto a lithographic stone. The quality of
copies thus produced often left much to be desired: details at the
edge of many pages or staves – among others slurs, ties, pagination,
plate numbers, footlines and other text at the bottom – came out
faintly or disappeared altogether. The relative frequency of
imperfections of this type can be inferred from the sheer quantity of
references to them in this catalogue, in which such ‘technical’
omissions are distinguished from deliberate modifications.<a
href="#_ftn4" id="_ftnref4">[4]</a></p>

<p>Maurice Schlesinger’s lithographic transfer of the Impromptu Op. 51
– published as a supplement to the <i>Revue et Gazette musicale de
Paris</i> of 9 July 1843 (see 51–1a-Sm) – offers a typical example of
the faults that could arise from this technique. During the transfer
process the pagination disappeared from several pages; it was then
restored directly onto each lithographic stone but with pages 3 &amp;
5 transposed. Chopin wrote to Schlesinger on 22 July 1843 complaining
that this inversion ‘renders the music incomprehensible’, and
requesting the publication of an erratum in the RGMP to alert
subscribers to the mistake. A late reprint of Hofmeister’s edition of
Op. 51 likewise contains numerous imperfections arising from
lithographic transfer: not only did the footline disappear from
several pages, but so did important elements within the music
text. Moreover, errors rectified at earlier proofreading stages
resurfaced as a consequence of the intensive use of the plates, the
previous corrections to which simply wore away (see 51–1b-HO,
51–1c-HO).</p>

<p>The edition of the Mazurkas Op. 6 classed as 6–4-KI reveals another
difficulty associated with lithographic transfer, namely the fragility
of the stone used in production. Two pages of its music text were
engraved whereas the rest were printed through lithographic transfer,
yielding a unique hybrid without parallel in this catalogue. It is
likely that pages 3 &amp; 4 of the music text were transferred along
with the rest but that the stone in question broke;<a href="#_ftn5"
id="_ftnref5">[5]</a> to save time the printer simply used the
original plates to produce these pages rather than undertaking the
transfer anew.</p>

<p>In Chopin’s first editions colour printing tends to be limited to
title pages, partly because polychrome output generally required
successive print stages using different inks.<a href="#_ftn6"
id="_ftnref6">[6]</a> Kistner’s editions of Opp.  6, 7 &amp; 9 (see
6–1-KI, 7–1-KI, 9–1-KI) have TPs printed in sepia – the earliest and
indeed simplest use of colour in the catalogued scores. A much greater
range can be found in the Mechetti prints: the TP of the Polonaise
Op. 44 exists in blue, green and black versions (see 44–1-ME,
44–1a-ME), while for the Prelude Op. 45 Mechetti variously used
reddish brown, reddish pink, blue or charcoal grey ink (see 45–1-ME,
45–1a-ME). The TP of Tobias Haslinger’s second edition of the
Variations Op. 2 is also printed in blue (see 2–2-HAt), likewise the
TPs of two late reprints of <i>Hexameron</i> published by
A. M. Schlesinger (see HEX–1b-Sam, HEX–1c-Sam). Only a single English
first edition of Chopin – the Fantasy-Impromptu Op. 66 – contains a TP
in colour, or rather in one of two colours, blue or green (see
66–1-EW).</p>

<p>Multiple colours can be found on the TPs of the Trio Op. 8 (see
8–1-KI, 8–1a-KI), Concerto Op. 11 (see +11–1-K, 11–1a-KI), Nocturne
Op. 32 No. 1 (32/1–1b-Sam) and <i>Hexameron</i> (HEX–1-HAt), all four
of which have decorative backgrounds (in blue for Opp. 8 and
<i>Hexameron</i>, in blue or green for Op. 11, and in pale green or
pink for Op. 32) over which the main text was printed in sepia in the
case of +11–1a-K, in black for 11–1a-KI, Opp. 8 &amp; 32, and in blue
and black for <i>Hexameron</i>. The TPs of Opp. 8 &amp; 11 were
lithographed in toto, whereas for those of Op. 32 No. 1 and
<i>Hexameron</i> lithography was used for the decorative background
and engraving for the text in black ink. Colour lithography was also
employed for the TP of a late impression of the Tarantella Op. 43 (see
43–2b-SCHU): the decorative frame and some of the text (e.g. printer’s
imprint and publisher’s name and address) are in violet, while the
remaining text is in black.</p>

<p>An even greater diversity of colour characterises the title pages
of the albums containing the Nocturnes Op. 32 (see 32/1–1-Sam,
32/2–1-Sam) and Prelude Op. 45 (45–1-ME), likewise those of the French
edition of the Posthumous Works (Posth–1-MEIf) and of Leitgeber’s
Polish edition of three mazurkas and the <i>Lento con gran</i>
<i>espressione</i> (MazD,Bû,G,Lento–1-L). Sumptuously decorated and
resplendent in colour, these title pages required as many separate
print models and passages under the press as there are inks on the
page.</p>

<p>This discussion of printing methods would not be complete without
reference to the techniques used to produce the wrappers and covers of
Chopin’s first editions. The front page of most wrappers and covers
was either engraved or lithographed; only exceptionally was a front
page both engraved and lithographed (see half-title of HEX–1-HAt) or
printed from movable type (18–1a-Sm, 45–1-Sm, 50/1–2-Sm, MFM–1-E,
MFM–1a-E). Letterpress printing was employed for all of the catalogue
extracts on other pages. Wrappers and covers printed in colour are
very rare: green, dark blue, ochre or gold was used for 23–2-B&amp;H,
while 32/1–1-Sam and 32/1–1a-Sam feature red and 32/2–1-Sam dark
green. The wrapper of the first Austrian edition of <i>Hexameron</i>
(HEX–1-HAt) is unique in its use of polychrome printing: the
lithographed floral motif enclosing the title is printed in dark red,
whereas the Habsburg coat of arms and the rest of the text are printed
in black.</p>

<p>Thus, taking into account each constituent element of a score, the
entire range of printing techniques employed by music publishers
during this period may well have been put to use in producing a given
first edition of Chopin. The same holds for the works of innumerable
contemporary composers.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> It is worth noting,
however, that a lithographic stone could yield many fewer copies of
high quality than an engraved plate. In general, production via a
lithographic technique was reserved for editions of limited longevity,
whereas engraving was favoured for publications intended to remain in
print over an extended period. On the other hand, numerous
lithographed TPs in the German editions of Chopin (i.e. Opp. 12, 13,
16, 20, 24, 30, 35, 39–41, 46–50, 52, 54–56 &amp; 60–63, and the
Mazurka from <i>La France Musicale</i> (separate edition)) as well as
one Austrian edition (Op. 44) remained in use over several
decades.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> The <i>Berliner
Musik-Zeitung Echo</i> was produced on a machine press from 1851
onwards.</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> Certain publishers,
among them Lemoine, nevertheless replaced their manual presses with
much more efficient mechanical ones; see
Devriès and Lesure 1988: 277.</p>
</div>

<div id="ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref4" id="_ftn4" name="_ftn4">[4]</a> Note that in the case
of Op. 74 a more sophisticated transfer technique was used with
excellent results (see, e.g., 74–1a-H).</p>
</div>

<div id="ftn5">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref5" id="_ftn5" name="_ftn5">[5]</a> Unlike metal plates,
both sides of lithographic stones were typically put to use;
furthermore, stones could be recycled simply by being sanded, whereas
plates had to be melted down and in essence made again from scratch.
The downside of lithographic stones was their fragility and the
relatively limited number of high-quality copies that they
yielded.</p>
</div>

<div id="ftn6">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref6" id="_ftn6" name="_ftn6">[6]</a> In the score of the
Mazurkas Op. 30 (see 30–1a-Sm) and the Prelude Op. 45 (see +45–1a-Sm),
a decorative orange border frames not only the TP or ATP but also all
remaining pages. These are the only known examples where colour is
used on the inner pages of a Chopin first edition.</p>
</div>''',
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000200020002',
            'show_in_menus': True,
            'slug': 'printing-methods',
            'title': 'Printing methods'
        }
    },
    'background_general_title': {
        'class': IndexPage,
        'kwargs': {
            'depth': 7,
            'introduction': u'''<p>Bibliographic analysis of a printed edition inevitably starts
with the title page, which contains essential information such as the
title of the work, name of composer, dedicatee, opus number, sale
price, publisher, and often affiliated foreign publishers and
concessionary sales agents. On many TPs the plate number and the name
or initials of the engraver or lithographer involved in the production
of the edition also appear.</p>

<p>Five different types of title page are distinguished in this
catalogue:</p>

<ol>
<li>individual title page (ITP);</li>
<li>passe-partout/series title page (STP);</li>
<li>common title page (CTP);</li>
<li>album title page (ATP);</li>
<li>half-title (HT).<a href="#_ftn1" id="_ftnref1">[1]</a></li>
</ol>

<p>The title pages of the vast majority of Chopin’s first editions
were written in French; this resulted in numerous orthographical
infelicities above all in the English publications, and to a lesser
extent in the German first editions. In relevant entries of the
<i>Annotated Catalogue</i>, these mistakes are systematically detailed
in the section on ‘Errors’.</p>

<p>Each of the works that Chopin published before settling in Paris
was brought out by a single firm whose name appears by itself on the
title page; it is hardly surprising that at this stage he did not
attempt the simultaneous release of multiple editions that he
routinely sought in later years in order to maximise copyright
protection and income. In the first editions brought out in Paris,
Leipzig and Berlin in 1833, the names of two publishers feature on the
title page (see Opp. 6–11, <i>Grand Duo Concertant</i>), with a
third – that of the English publisher – systematically appearing from
late 1833 onwards (see Op. 12 and subsequent publications).<a
href="#_ftn2" id="_ftnref2">[2]</a></p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> A definition of each
of these terms appears in the Glossary in ‘Reference material’.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Note however the
following exceptions: first impressions of Maurice Schlesinger’s
Op. 15 and Mechetti’s Op. 45 (names of German and English publishers
omitted, probably inadvertently); A. M. Schlesinger’s Op. 32 and first
two impressions of Brandus’ Op. 63 (name of English publisher left
blank); first impressions of Troupenas’ Opp. 35 &amp; 36, of Maurice
Schlesinger’s Opp. 44 &amp; 46–49 and second edition of the Etudes
from <i>Méthode des Méthodes</i>, of Breitkopf &amp; Härtel’s Opp. 17,
46–49 &amp; 63–65, and of Mechetti’s Opp. 44 &amp; 45, in addition to
all subsequent impressions of the latter (no English publisher
named). In the French editions of Opp. 22, 63 (third impression
onwards), 64 &amp; 65, the wrong English publisher is indicated. A
similar error in the name of the French publisher can be found on the
TPs of Breitkopf &amp; Härtel’s edition of Op. 28. Finally, in the
editions brought out by Cramer, Beale &amp; Co. and their successors,
the names of the continental publishers are missing in the copies
catalogued under 63/1–1-CRB, 64/1–1-CRB, 64/1–1a-CRB, 64/1–1c-CHAP,
64/2–1-CRB and 64/2–1a-CHAP, while that of Breitkopf &amp; Härtel is
missing from 64/1–1b-CHAP and 64/3–1-CRB.</p>
</div>''',
            'numchild': 4,
            'path': '0001000100010002000200020003',
            'show_in_menus': True,
            'slug': 'title-pages',
            'title': 'Title pages'
        }
    },
    'background_general_title_france': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>The TPs of successive French impressions of Chopin’s music
evolved to a much lesser extent than their German
counterparts. Engraved plates were used to produce the title page as
well as the music text of most French editions, and their physical
durability largely explains the relative lack of changes in later
reprints. Indeed, with only two exceptions, each and every reprint of
a French edition – even those published after a change of owner –
retained the original title page, though sometimes with minor
modifications.  The most frequent of these were increases or decreases
in price. On four title pages the dedication was re-engraved (see
Opp. 13, 52–54), while on another the number of pieces was modified
(6–1a-Sm). Other modifications include removal of the names of foreign
publishers (10–1d-LE, 12–1a-LE, 16–1b-Sm, 18–1b-LE, 25–1b-LE), the
engraver’s initials (10–1d-LE) or the copyright notice (18–1b-LE).
Certain changes in ownership resulted in updates to the publisher’s
name and address and to the plate number (10–1d-LE, 12–1a-LE,
16–1b-Sm, 17–1a-Sm, 18–1b-LE, 25–1b-LE, 28/1-12–1c-BR). After
acquiring the lists of Schlesinger and Troupenas, however, Brandus
modified the original name and address on the TPs of very few of his
predecessors’ editions,<a href="#_ftn1" id="_ftnref1">[1]</a> either
because he thought it unnecessary or owing to financial constraints.
The latter may also explain why the original TPs were recycled in
Brandus’ second edition of the Mazurkas Op. 7 and Waltz Op. 64 No. 1
(see 7–2-BR, 64–2-BRD&amp;C).  But for a reprint of the Nocturnes
Op. 9 from the early 1850s, Brandus went to the trouble of producing
an entirely new TP (9–1c-BR), as Chabal had previously done in the
case of the Mazurka dedicated to Emile Gaillard (MEG–1b-CH).</p>

<p>In certain instances a common title page was put to use for
different works or discrete parts thereof – namely, in the Preludes
Op. 28 and Nocturnes Op. 48 (divided into two volumes), and in the
Rondos Opp. 1 &amp; 5 and Variations Op. 2 published by Schonenberger
as ‘3 MORCEAUX <i>Favoris</i>’ (see 1–1-SC, 2–1-SC, 5–1-SC). A true
passe-partout exists in the Posthumous Works released by
J. Meissonnier fils (Compagnie Musicale, E. Gérard et Cie), in the
‘EO’ series created by G. Brandus et S. Dufour (G. Brandus et Cie,
Brandus et Cie, Ph. Maquet), in Hamelle’s separate editions of Op. 74
(see 74–1g-H, 74–1h-H, 74–2-H) and in Joubert’s reprint of
<i>Hexameron</i> (see HEX–1a-J).</p><p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> The change was made
in the following reprints: 3–1a-BR&amp;D, 11–1c-BR, 13–1c-BR,
14–1b-BR, 21–1c-BR, 22–1c-BR, 31–1a-BR, 37–1d-BR, MM–2a-BR.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000200030001',
            'show_in_menus': True,
            'slug': 'france',
            'title': 'France'
        }
    },
    'background_general_title_germany': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>A remarkable evolution occurred in the successive reprints of
the German first editions of Chopin’s music. First of all, over half
of the original TPs were replaced altogether, mostly to bring them up
to date stylistically but sometimes because the lithographic stone
used to produce them had worn out.<a href="#_ftn1"
id="_ftnref1">[1]</a> Modifications to TP content also occurred, in
most cases affecting the sale price. This was not the result of
inflation, however: in fact, prices stayed surprisingly stable over
several decades.<a href="#_ftn2" id="_ftnref2">[2]</a> Instead, the
principal reason concerns two key events in nineteenth-century German
monetary history: first, the introduction of the Neugroschen in 1841,
and, secondly, the birth of a new currency, the Mark, upon the
creation of the German Empire on 4 December 1871. The Neugroschen was
the result of the Thaler’s appreciation in value from 24 Groschen to
30 Neugroschen as of 1 January 1841. No transitional phase was needed
for this straightforward revaluation, whereas in the case of the Mark,
which replaced existing monetary units across the board, a period of
transition lasted until 31 December 1873. This two-year phase left its
trace on many TPs from the period, in that prices in Marks and
Pfennigs are printed next to their equivalent in old currency. After 1
January 1874, prices in Thalers and Neugroschen started disappearing,
but one can safely deduce that a given German edition was published
after this date if it bears a price in new currency only. Although
double prices can also be found on the TPs of other editions from the
first half of the nineteenth century, they refer to equivalents in
foreign currency (see e.g.  2–1-HAt, 2–2-HAt, 74–1-G, HEX–1-RI,
HEX–1-HAt)<a href="#_ftn3" id="_ftnref3">[3]</a> or to respective
values in either Groschen and silver Groschen (1–1-Sam) or Neugroschen
and ‘gute Groschen’ (6–2a-KI, 7–2-KI).</p>

<p>Several German first editions bear no sale price. In the case of
the Variations Op. 12 (see 12–1-B&amp;H) and the Bolero Op. 19
(19–1c-PE), an oversight probably occurred on the part of the
lithographer or publisher, whereas the price of the two Nocturnes
Op. 32 (see 32/1–1-Sam, 32/2–1-Sam) was deliberately omitted because
of their inclusion in albums. It is less certain why no price appears
on any of the later reprints by B. Schott’s Sohne of the E minor Waltz
and the G# minor Polonaise.</p>

<p>Changes were also made to the information printed at the bottom of
German TPs, including the names of principal and foreign publishers
and their concessionaires, the plate number, and the engraver’s or
lithographer’s imprint (e.g.  59–2a-PE). R. Lienau’s name featured on
impressions of the Posthumous Works and the Songs Op. 74 published
after the firm’s assimilation of A. M. Schlesinger, likewise on
reprints of editions originally brought out by the Austrian publisher
Haslinger, whose list had also been acquired by the Berlin
firm. Brandus’ take-over of Maurice Schlesinger similarly left its
mark on ten German title pages produced after 1845.<a href="#_ftn4"
id="_ftnref4">[4]</a> Adjustments of this sort were not carried out
systematically, however: the name of the French publisher on some
German editions either remained unchanged<a href="#_ftn5"
id="_ftnref5">[5]</a> or was otherwise inaccurate.<a href="#_ftn6"
id="_ftnref6">[6]</a></p>

<p>The fact that publishers’ addresses rarely appeared on German TPs
meant that relatively few adjustments were needed to this type of
information,<a href="#_ftn7" id="_ftnref7">[7]</a> whereas details of
their foreign sales agents changed with some frequency.<a
href="#_ftn8" id="_ftnref8">[8]</a> Often the agents’ names were
removed from later impressions because they had been commissioned to
sell a given publisher’s music for only a limited period of time (see
21–1e-B&amp;H, 22–1b-B&amp;H, 23–1c-B&amp;H, 26–2a-B&amp;H,
26–2d-B&amp;H, 27–1d-B&amp;H). Opp. 29 &amp; 30 are exceptional in
this regard: three successive versions of the Impromptu’s TP cite the
same concessionaires in St Petersburg and Warsaw, likewise two
versions of the Mazurkas (see 29–1b-B&amp;H, 29–2-B&amp;H,
30–1-B&amp;H, 30–1e-B&amp;H).</p>

<p>In the editions published by B. Schott’s Söhne, whose TPs underwent
multiple transformations, one notes the following changes in addition
to those mentioned above: removal of the Polish publisher’s name (see
PolGû–1b-SCH, WaltzEm–1b-SCH), addition or repositioning of the plate
number (PolG#m–1b-SCH, WaltzE–1a-SCH), revision or removal of
information about the publisher’s branches in other countries
(PolGû–1b-SCH, WaltzEm–1d-SCH), and excision of a reference to deposit
in France and England (PolGû–1b-SCH).</p> <p>Imprints consisting of
the name or initials of the lithographer disappeared early on from the
TPs of successive reprints. Generally small and drawn with great
delicacy, these imprints were highly susceptible to wear through
intensive use and therefore had to be removed once the quality of
reproduction became compromised (see 34/1–1a-B&amp;H,
34/2–1b-B&amp;H). Their disappearance was also necessitated by changes
in the printing firm (see 44–1b-ME, 44–1c-ME, 45–1c-ME) or, in a few
cases, for unknown reasons (see 26–1a-B&amp;H, 59–1b-ST).</p>

<p>Common title pages appear principally in editions of works divided
into two volumes (i.e. Opp. 10 &amp; 25) or published separately
(Opp. 32, 34, 64). They caused their publishers major headaches with
regard to numbering and classification. For the first impressions of
the Etudes Opp. 10 &amp; 25 and the Waltzes Op. 34, Kistner and
Breitkopf &amp; Härtel varied the number of the ‘book’ or work in
accordance with the contents of the score (thus, ‘Liv. I.’ and ‘Liv.
II.’ in the case of Opp. 10 &amp; 25’s first and second volumes
respectively), but in later impressions of these works the practice
was abandoned, as a result of which the relevant TPs invariably
feature the roman numeral ‘I’.<a href="#_ftn9" id="_ftnref9">[9]</a>
The same defect can be found in editions of the Nocturne Op. 32 No.  2
(see 32/2–1a-Sam, 32/2–1b-Sam) and the Waltzes Op. 64 Nos. 2 &amp; 3
(see 64/2–1-B&amp;H, 64/2–1a-B&amp;H, 64/3–1-B&amp;H, 64/3–1a-B&amp;H,
64/3–1c-B&amp;H). The solution that A. M. Schlesinger adopted in later
reprints of Op. 32 was to leave a space for the number of the work
within the opus (see 32/1–2a-Sam, 32/2–2-Sam), that number then being
added by hand on each printed TP. Perhaps the best solution was the
one taken when producing the four-volume version of Op. 28 (see
28–1c-B&amp;H), in which a CTP lists all four volumes and their
prices, thus eliminating the risk of confusion arising from the
production of tailormade ITPs.</p>

<p>The first passe-partout appeared relatively early in the German
editions of Chopin – initially in the Etudes Op. 25 published in
separate editions by Breitkopf &amp; Härtel in 1841. The Posthumous
Works released by A. M. Schlesinger in 1855, as well as the mazurkas,
nocturnes and polonaises brought out in separate editions by Breitkopf
&amp; Härtel from 1863, also have this type of title page.<a
href="#_ftn10" id="_ftnref10">[10]</a> Another passe-partout was used
in Hofmeister’s collection of the Chopin works in his list, entitled
<i>Altes und Neues</i>, while Bote &amp; Bock included the Mazurka
dedicated to Emile Gaillard in the series <i>Dziedzina tonów
polskich</i>, again featuring a STP of this kind.</p>

<p>It is interesting to observe the close resemblance of the TPs in
otherwise different Chopin editions, which probably resulted from the
continued involvement of an original lithographer who used the earlier
TP as a model when preparing the subsequent version. Despite their
similarity, however, these ‘identical twins’ generally can be
distinguished by minor discrepancies in decorative motifs and the size
and spacing of numbers or letters, all of which are difficult if not
impossible to convey in a standard bibliographic transcription
(compare 7–2-KI and 7–3-KI; 10/1-6–2-KI and 10/1-6–3a-KI; 10/7-12–2-KI
and 10/7-12–2a-KI). Very occasionally one notices the recycling by a
given publisher of decorative frames or borders, either in whole or in
part, on the TPs of distinct works (see 32/2–1-Sam, 45–1d-ME,
WaltzEm–1e-SCH). Similar decoration on the TPs of editions brought out
in different countries can also be found, namely in the albums
containing the Mazurka from <i>La France Musicale</i>, published in
Paris and in Mainz (see MFM–1-E, MFM–1-SCH), and in the later reprint
of the Bolero Op. 19 (19–1c-PE) produced in Leipzig, which resembles
the decorative frame on the passe-partout of certain Polish editions
(see Appendix I: KAUFMANN,
‘OEUVRES<b>½‌</b>DE<b>½‌</b>CHOPIN.<b>½‌</b>POURLE PIANO’, version
1).</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> The following
compositions nevertheless retained the original TP throughout their
commercial lifetime: Opp. 3, 12, 13, 16, 20, 24, 30, 35, 39–41, 44,
46–50, 52, 54–56 &amp; 60–63, <i>Hexameron</i>, and Mazurka from <i>La
France Musicale</i> (separate edition).</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Prices increased in
only three cases: Posthumous Works, Tarantella Op.  43 and Polonaise
Op. 44 (see Posth–1a-Sam, 43–1b-SCHU, two-hand version of 43–1d-SCHU,
and 44–1d-ME). A price decrease occurred in respect of the Rondo Op. 1
and Variations Op. 2 (1–1a-Sam, 2–2-HAt). A lower price may also have
been intended for the second edition of the Mazurkas Op. 24 from
c. 1863 (24–2–B&amp;H), the TP of which indicates an anachronistic
price of 20 Groschen rather than the correct 20 Neugroschen (compare
24–2d-B&amp;H; see also 24–1–B&amp;H).</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> Some double prices
were updated after the introduction of the Mark: see 2–2b-Sam,
74–1b-G, HEX–1a-HAt (cf. also 4–1a-Sam).</p>
</div>

<div id="ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref4" id="_ftn4" name="_ftn4">[4]</a> See 14–1b-KI,
22–1b-B&amp;H, 23–1c-B&amp;H, 26–2a-B&amp;H, 26–2d-B&amp;H,
27–1c-B&amp;H, 31–1b-B&amp;H, 33–1c-B&amp;H, 33–2a-B&amp;H and
37–1b-B&amp;H.</p>
</div>

<div id="ftn5">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref5" id="_ftn5" name="_ftn5">[5]</a> See for example the
TPs of 21–1e-B&amp;H, 29–2-B&amp;H, 34/1–1c-B&amp;H, 34/1–2a-B&amp;H
and 34/1–2b-B&amp;H, on which the name of the first French publisher
remains. The transfer of Opp. 10, 18 &amp; 25 from M. Schlesinger to
Lemoine was not taken into account on any German TP. All of Kistner’s
later reprints and new editions of the Etudes Op. 10 retain
Schlesinger’s name (see, e.g., 10/1-6–2-KI, 10/1-6–3-KI, 10/1-6–3a-KI,
10/1-6–3b-KI); Breitkopf &amp; Härtel similarly kept his name on the
TP of the Waltz Op. 18 (see 18–2d-B&amp;H), as well as that of Pleyel
on the TPs of the Mazurkas Op.  17 (see 17–1a-B&amp;H,
17–2b-B&amp;H).</p>
</div>

<div id="ftn6">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref6" id="_ftn6" name="_ftn6">[6]</a> See for example the
TPs of 25/1-6–1e-B&amp;H and 25/1-6–2a-B&amp;H, where Brandus’ name
erroneously appears. The wrong French publisher is cited on the TPs of
all Breitkopf &amp; Härtel impressions of the Preludes Op. 28 (see
28–1-B&amp;H, 28–1b-B&amp;H, 28–1c-B&amp;H, 28–1k-B&amp;H,
28–1l-B&amp;H).</p>
</div>

<div id="ftn7">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref7" id="_ftn7" name="_ftn7">[7]</a> The publisher’s
address was modified on the TP of 59–1d-F and on A. M. Schlesinger’s
STP (‘OEUVRES DE PIANO.<b>½</b>‌FRANCOIS LISZT.<b>½</b><b>‌</b>FRÉDÉRIC
CHOPIN.’ versions 3 &amp; 4, ‘OEUVRES DE
PIANO<b>½</b>‌DE<b>½</b>‌FRÉD. CHOPIN’ versions 4 &amp; 5). Although
present on the TPs of 43–2-SCHU and 43–2a-SCHU, Schuberth’s address is
absent from 43–2b-SCHU (Titelauflage).</p>
</div>

<div id="ftn8">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref8" id="_ftn8" name="_ftn8">[8]</a> Sales agents’ names
were added to the TPs of 21–1a-B&amp;H, 24–1a-B&amp;H, 27–1a-B&amp;H
and 43–1a-SCHU, and to the STP of A. M.  Schlesinger (‘OEUVRES
POSTHUMES<b>½</b>‌POUR<b>½</b>‌PIANO<b>½</b>‌DE<b>½</b>‌FRÉD. CHOPIN.’
version 3). They were either partially or entirely removed from the
TPs of PolGû–1b-SCH and PolG#m–1c-SCH, and from A. M.  Schlesinger’s
STP (‘OEUVRES
POSTHUMES<b>½</b>‌POUR<b>½</b>‌PIANO<b>½</b>‌DE<b>½</b>‌FRÉD. CHOPIN.’
version 5, ‘OEUVRES DE PIANO.<b>½</b>‌FRANCOIS LISZT.<b>½</b>‌FRÉDÉRIC
CHOPIN.’ versions 2–4).</p>
</div>

<div id="ftn9">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref9" id="_ftn9" name="_ftn9">[9]</a> Kistner nevertheless
seems to have regarded this detail as important, judging from his
efforts to ensure the accuracy of the number indicated on the TP. In
all copies of the second and third editions of volume II in Op. 10,
the second ‘I’ in ‘Liv. II’ appears to have been carefully added by
hand after printing, most likely in the workshop responsible for
producing the TPs (see comments to 10/7-12–2-KI, 10/7-12–2a-KI,
10/7-12–3a-KI). In contrast, the second ‘I’ is faintly printed on the
TPs of some of the copies catalogued under 10/7-12–1-KI, which
suggests that the title pages of both volumes were produced using the
same lithographic stone and that the missing roman numeral was added
to it prior to printing.</p>
</div>

<div id="ftn10">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref10" id="_ftn10" name="_ftn10">[10]</a> In their
successive Chopin editions these two publishers employed numerous
different STPs, some of them appearing only on wrappers. For
descriptions see Appendix I.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000200030002',
            'show_in_menus': True,
            'slug': 'the-german-states',
            'title': 'The German states'
        }
    },
    'background_general_title_england': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>It is difficult to trace the evolution of the English first
editions published between 1833 and 1840 because of major lacunae in
the surviving source material. Judging from those compositions for
which a relatively complete range of impressions exists, one observes
that the entrepreneurial Wessel was inclined to modify the title pages
of these prints with some frequency. The Polonaise Op. 3 offers a good
example of the most common changes, namely updates to the firm’s
business address, price increases and removal of redundant information
(see 3–1-W, 3–1a-W, 3–1b-W). Another representative example can be
found in the case of the Mazurkas Opp. 6 &amp; 7, whose TPs were
altered when these works were grouped into one or more
series. Originally published in a collection entitled <i>Souvenir de
la Pologne</i>, these two opuses were later assimilated into the
series <i>L’Amateur Pianiste</i>, necessitating such revisions to the
TP as the addition of references to the latter collection and
replacement of the original numbering within the series by altogether
new numbers (compare 7–1-W and 7–1a-W; see also 6–1-W).</p>

<p> Relatively few English first editions have individual title
pages. Wessel’s <i>Complete Collection of the Compositions of Frederic
Chopin</i> encompassed all of the Chopin works on his list after its
launch in June 1840, thus explaining why the Ballade Op. 38 and
subsequent publications have only a series title page (although the
latter changed considerably over time). Despite its importance, the
<i>Complete Collection</i> was not the only series marketed by Wessel
and his successors after 1840. The Etudes Op. 10 Nos. 2, 5, 7 &amp; 10
and Op. 25 Nos. 1, 2 &amp; 9 were sold in separate editions but with
adapted versions of a passe-partout (see 10/5–1d-W, 10/7–1a-W,
10/10–1a-W, 10/2–1e-W, 25/1–1d-W, 25/2–1d-W, 25/9–1g-A&amp;P).  A
similar approach was taken to the Mazurkas Op. 6 No. 1 and Op. 33
No. 4 (see 6/1–1g-W, 33/4–1f-W), as indeed to the Prelude Op. 28
No. 15 (see 28/15–1d-A&amp;P).<a href="#_ftn1" id="_ftnref1">[1]</a>
As for Chopin’s Trio Op. 8 – initially published with an ITP as part
of the <i>Series of Modern Trios</i> – it was also produced with the
STP of the <i>Collection of Grand Trios Concertante for Piano Forte,
Flute &amp; Violoncello</i> (see 8–1c-A&amp;P).</p>

<p>English first editions published with a common title page include
not only the sets of mazurkas referred to above (i.e. 6–1-W, 7–1-W,
7–1a-W), but also the Polonaises Op. 26 No. 1 and Op. 40 No. 1 (see
26/1–1d-W, 26/1–1e-W, 40/1–1f-A&amp;P), Waltzes Op. 34 (see 34/1–1-W,
34/2–1-W, 34/3–1-W) and Waltzes Op. 64 Nos. 1 &amp; 2 published by
Cramer, Beale &amp; Co. and by Chappell &amp; Co., as well as the
works released in two volumes, namely Opp. 9, 10, 25 &amp; 28 (see
9/3–1-W, 10/1-6–1-W, 10/7-12–1-W, 25/1-6–1-W, 25/7-12–1-W,
28/1-14–1-W, 28/15-24–1-W).</p> <p>Although widespread use of STPs
meant that new ITPs were rarely needed in successive impressions,
Wessel and his successors did devise tailormade title pages for the
separate editions of certain works;<a href="#_ftn2"
id="_ftnref2">[2]</a> this was also the practice of both Cramer, Beale
&amp; Co. and Chappell with regard to the Waltzes Op. 64 Nos. 1 &amp;
2, for which four different CTP designs were conceived.<a
href="#_ftn3" id="_ftnref3">[3]</a></p>

<p>The price of most English editions increased several times over
successive decades of commercial availability. The tables in Appendix
I present relevant price information for the period from 1840 to
c. 1892. Only one price decrease seems to have occurred: between 1836
and 1840, the Scherzo Op. 20 was sold for 4 shillings 6 pence, whereas
from 1840 to 1844 it cost only 4 shillings (compare versions 1–11 of
the <i>Complete Collection</i>).</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> The text of their TPs
suggests that other mazurkas and preludes from Op. 28 were sold in
this format – hence the designation of these as STPs.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Works published in
separate editions with new TPs include the following: Nocturne Op. 9
No. 2 (9/2–1e-A&amp;P), Nocturne Op. 15 No. 2 (15/2–1c-W), Andante
Spianato Op. 22 (22/Andante Spianato–1b-W), Nocturne Op. 27 No. 2
(27/2–1c-W), Nocturne Op. 32 No. 1 (32/1–1h-W), Funeral March from
Op. 35 (35/3–1a-W), Nocturne Op. 37 No. 1 (37/1–1d-A&amp;P) and
Nocturne Op. 55 No. 1 (55/1–1a-W).</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> See 64/1–1-CRB,
64/1–1a-CRB, 64/1–1b-CHAP, 64/1–1c-CHAP, 64/2–1-CRB and
64/2–1a-CHAP.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000200030003',
            'show_in_menus': True,
            'slug': 'england',
            'title': 'England'
        }
    },
    'background_general_title_poland': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>None of the Polish editions published during Chopin’s lifetime
bears a sale price; one of them was brought out anonymously (see
MazG–1-KOL). As for the Polish scores released after 1849, TP content
and design evolved along the lines of the various changes described
elsewhere under ‘Title pages’. The names of Austrian and Prussian
sales agents were added to the TP of the second impression of the
<i>Deux Valses Mélancoliques</i>; the Austrian concessionaire was then
modified in the third impression (compare 70/2&amp;69/2–1b-WI and
70/2&amp;69/2–1c-WI). A German translation of the two song titles was
added to the TP of the second impressions of <i>Wojak</i> and
<i>Źyczenie</i>, which constitute the only example within this
catalogue of Polish Chopin editions with a common title page (see
74/10–1a-KO, 74/1–1a-KO). Gebethner’s volume of the Songs Op. 74
appeared with both an ITP (see 74–1-G, 74–1a-G, 74–1c-G) and a STP
(74–1d-G). The reprint of this work in separate editions features a
STP (see 74–1b-G, 74–1e-G; compare also 74–1d-G), likewise most of
Kaufmann’s publications (see MazC–1-K, PolG#m–1a-K, WaltzEm–1-K,
WaltzEm–1a-K, WaltzEm–1b-K).</p>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000200030004',
            'show_in_menus': True,
            'slug': 'poland',
            'title': 'Poland'
        }
    },
    'background_general_wrappers': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>When originally published, most scores were contained within a
wrapper consisting of a folded bifolium of coloured paper which was
fine in quality and supple in texture.<a href="#_ftn1"
id="_ftnref1">[1]</a> As previously noted, few wrappers have survived
to the present day. This has partly to do with the delicate nature of
the stock in question, and also because wrappers were often removed
soon after purchase. Even the deposit scores held by major libraries
tend not to have original wrappers. Their loss is much to be
regretted: not only do they facilitate the dating process, but they
also offer valuable information about the period of commercial
availability of a given impression.</p>

<p>Like title pages, wrappers evolved over time but generally fall
into three broad categories:</p>

<ol>
<li>the front page consists of a replica of either the TP, a
half-title or (exceptionally) a passe-partout or ATP, while the
remaining three pages are blank;</li>

<li>as above, except that the fourth page of the wrapper contains a
catalogue extract as a form of advertising;</li>

<li>the front page consists of a replica of either the TP, a
half-title, a passe-partout or a CTP; catalogue extracts appear on
one, two or all three of the remaining pages.<a href="#_ftn2"
id="_ftnref2">[2]</a></li>
</ol>

<p>Only limited conclusions can be drawn from the few Polish and
English wrappers that survive. The two extant Polish wrappers
described in this volume contain catalogue extracts, in one case
advertising the publisher’s own output (see PolG#m–1-K), whereas the
second, printed in Berlin, includes an extract from the catalogue of
A. M. Schlesinger (74–1c-G). Of the eleven surviving English wrappers,
two are defective, lacking the first leaf (66–1-CO, 66–1a-CR). The
oldest English wrapper, dating from c. 1847, is unique in containing
no catalogue extracts (see 57–1a-W), while seven of the other
impressions with wrappers have advertisements of this kind on one page
thereof (10/1-6–1e-W, 10/1-6–1j-A&amp;P, 10/7-12–1b-W, 25/1-6–1f-W,
25/7-12–1g-A&amp;P, 28/1-14–1f-A&amp;P, 28/15-24–1f-A&amp;P) as
against two pages in the eleventh case (HEX–1-CR/M).</p>

<p>In French editions from Chopin’s lifetime the first of the three
categories predominates, although a certain number of wrappers do
contain advertisement text.<a href="#_ftn3" id="_ftnref3">[3]</a>
Around 1849 this tendency is reversed, such that wrappers of type 1
become the exception.<a href="#_ftn4" id="_ftnref4">[4]</a> As for the
German editions, the content of wrappers varies according to the
publisher. Irrespective of their publication date, all of Breitkopf
&amp; Härtel’s wrappers – of which a large number survive – include a
catalogue extract. No such advertisement text appears on the wrappers
of Kistner, Peters or Stern, whereas those of Hofmeister, Mechetti
(followed by Spina and Schreiber), A. M. Schlesinger, B.  Schott’s
Sohne and Schuberth variably include catalogue extracts. In the case
of Mechetti and A. M. Schlesinger, however, the ones without
catalogues are in a small minority.<a href="#_ftn5"
id="_ftnref5">[5]</a></p>

<p>Wrappers bearing a half-title on the front are relatively abundant,
the oldest dating from as early as 1834.<a href="#_ftn6"
id="_ftnref6">[6]</a> Although some half-titles were exclusively
intended for use on wrappers, those in the Posthumous Works serve a
double purpose: not only do they appear on the half-title pages
preceding the constituent works in the first impression of the German
volume and in all of the volumes brought out in Paris, but they also
feature on the wrappers of the successive reprints in separate
editions produced in France and Germany.<a href="#_ftn7"
id="_ftnref7">[7]</a></p>

<p>Upon close inspection the apparently identical replicas of TPs on
the front page of many wrappers turn out to be slightly different;
such wrappers may have pre- or post-dated their respective title
pages. For example, on the TP of the Mazurkas Op. 41 held by A-Wgm
(see 41–1a-B&amp;H) the price is stated in Neugroschen, whereas on
the wrapper it appears in Groschen. A similar difference exists
between the TP and wrapper of the Waltz Op. 34 No. 1
(34/1–1a-B&amp;H), where the lithographer’s signature is present on
the wrapper but missing from the TP. The publisher’s address on the
wrapper of the Mazurkas Op. 59 does not correspond to the one
indicated on the TP (see 59–1d-F), while the wrappers of the albums
classed as Posth–1b-Sam and Posth–1c-Sam diverge in several respects
from their associated STPs, having been prepared somewhat earlier than
the latter (as in the case of the three preceding examples – see
below). Variants of this sort can also be observed in some Brandus
reprints in the ‘EO’ collection.<a href="#_ftn8"
id="_ftnref8">[8]</a></p>

<p>Such discrepancies might have been caused by the production of
wrappers and scores at different printing firms and possibly at
different intervals, with assembly being carried out thereafter by the
publisher; it is equally conceivable that the latter’s stocks of
wrappers and scores were not synchronised, and that older wrappers –
of which greater quantities may well have been prepared at any one
time as they were cheaper to produce in bulk – were married up with
relatively later impressions containing updated TPs. One also should
not rule out the possibility that mistakes were made when combining
wrappers and scores at the point of sale or elsewhere; passe-partouts
used for wrappers could easily have been confused with similar ones
serving as title pages.</p>

<p>Albums constitute a special case, in that they were produced in
several versions distinguished by the type of wrapper or cover. Like
most scores, the simplest albums had a lightweight loose wrapper (see
64/1–1a-BR); a number of these were in effect softbound, with
flyleaves attached to the wrapper (see 45–1-Sm, 50<b>/</b>1–2-Sm,
Posth–1c-Sam). Catalogue extracts appeared on the back of certain
wrappers of this type (45–1-Sm, 50<b>/</b>1–2-Sm). Mid-price versions
were bound in a decorative card cover (see 23–2-B&amp;H, 32/2–1-Sam
(A-Wn copy, second D-Bds copy), 33/1&amp;2–1a-B&amp;H, +45–1-Sm,
45–1-ME (second A-Wn copy, GB-Lbl copy)), while the most expensive
albums were encased in card covered with richly embellished silk (see
15–1a-Sm, 45–1-ME (first A-Wn copy), MM–1a-CHAP (GB-Lbl copy)).<a
href="#_ftn9" id="_ftnref9">[9]</a> The last two types contained no
advertisement text for obvious reasons, given their deluxe appearance
and appeal.</p>

<p>The section on ‘Printing methods’ refers to the range of techniques
used to produce wrappers and covers.  In all of the editions surveyed
here the advertisement text was printed by means of movable
type. Where the front pages are identical to TPs, both were produced
using the same technique, whether engraving, lithography or movable
type. A half-title located on the wrapper was typically printed by the
same method as the one for the actual TP of that impression. A few
exceptions do exist, however. Movable type was employed for the
half-titles on the wrappers/covers of five different impressions,
whereas the corresponding TPs were engraved (see 18–1a-Sm, Dubois
copy), lithographed (50/1–2-Sm, MFM–1-E, MFM–1a-E) or produced via
lithographic transfer (45–1-Sm, F-Pn copy). Furthermore, the wrapper
of the <i>Album de Piano 1848</i>, in which Chopin’s Op. 64 No. 1
appeared, features an engraved half-title as against a lithographed
album title page (see 64/1–1a-BR).</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> See also ‘Format,
dimensions and physical contents’ and ‘Printing methods’ under
‘General characteristics of Chopin’s first editions’. Surviving
wrappers exist in a spectacular range of colours.  Those in white or
off-white are uncommon: see 23–2-B&amp;H, 28–1h-A&amp;P (Book 1),
40–2g-B&amp;H (D-Bds copy), 46–1-B&amp;H (US-NYpm copy), 48–1-B&amp;H
(D-Dl copy), 50–1-ME (PL-Kj copy).</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> See Appendices I
&amp; II for further information about the evolution of STPs and the
catalogue extracts printed on wrappers; see also ‘Publications of
Breitkopf &amp; Härtel’ under ‘Chopin’s publishers’.</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> Those in category 2
include 9–1a-Sm, 16–1b-Sm (US-Cu copy), 18–1a-Sm, 22–1b-Sm, 45–1-Sm,
45–2b-Sm, 50/1–2-Sm and 64/1–1a-BR, whereas 16–1a-PL, 18–1b-LE,
37–1a-TR, 63–1-BR, 63–1b-BR, 64/1–1-BR (seventh F-Pn copy), 64/2–1-BR
and 64/3–1-BR (fifth F-Pn copy) belong to category 3.</p>
</div>

<div id="ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref4" id="_ftn4" name="_ftn4">[4]</a> See 2–1a-BR, 6–1c-BR,
11–1d-BR, 16–1c-Sm, 21–1c-BR, 35–1c-BR (F-Pmounier copy), 38–1b-BR
(GB-En copy), 74–1-H, 74–1a-H, 74–1c-H, 74–1e-H, HEX–1-BR (A-Wn
copy).</p>
</div>

<div id="ftn5">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref5" id="_ftn5" name="_ftn5">[5]</a> Only one of four
complete Hofmeister wrappers contains a catalogue extract. As for the
editions of Mechetti and his successors, there are sixteen complete
wrappers, of which nine have advertisement text, likewise thirty-one
out of thirty-four complete wrappers published by A. M. Schlesinger,
four out of five released by B. Schott’s Söhne, and one out of two of
Schuberth.</p>
</div>

<div id="ftn6">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref6" id="_ftn6" name="_ftn6">[6]</a> Impressions of this
type include the following:</p>

<dl style="font-size: 9pt; line-height: 115%; text-align: justify">
<dt>French</dt>

<dd>18–1a-Sm, 28/1-12–1b-BR, 28/13-24–1b-C, 34/1–1a-Sm,
34/2–2-BRD&amp;C, 44–1-Sm, 45–2b-Sm, 46–1-Sm, 46–1a-Sm, 47–1-Sm,
47–1a-Sm, 48/1–1-Sm, 48/1–1a-Sm, 48/2–1b-Sm, 49–1b-Sm, 52–1a-Sm,
53–1a-Sm, 54–1a-Sm, 55–1a-Sm, 56–1a-Sm, 57–1-MEIj, 58–1-MEIj,
58–1a-MEIj, 74–1-H, 74–1a-H, 74–1c-H, 74–1e-H, 74–1f-H, MFM–2-BR (see
also note 7 below)</dd>

<dt>German</dt>

<dd>52–1-B&amp;H, 53–1-B&amp;H, 53–1a-B&amp;H, 54–1-B&amp;H,
57–1-B&amp;H, 58–1-B&amp;H, 58–1a-B&amp;H, 60–1-B&amp;H, 61–1-B&amp;H,
62–1-B&amp;H, 63–1-B&amp;H, 64–1-B&amp;H, 64–2-B&amp;H, 65–1-B&amp;H,
HEX–1-HAt (see also ‘Printing method’), MEG–1b-B&amp;B, PolGû–1a-SCH,
PolGû–1b-SCH, PolG#m–1a-SCH, PolG#m–1b-SCH, PolG#m–1c-SCH (see also
note 7 below)</dd>

<dt>Polish</dt>
<dd>74–1c-G, PolG#m–1-K</dd>
</dl>

<p style="font-size: 9pt; line-height: 115%; text-align:
justify">Half-titles are also present on the wrappers or covers of
certain albums: see 45–1-Sm, 50/1–2-Sm, 64/1–1a-BR, Posth–1b-GE,
MFM–1-E, MFM–1a-E.</p>
</div>

<div id="ftn7">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref7" id="_ftn7" name="_ftn7">[7]</a> In the French
editions of the Posthumous Works, no changes were made to these
half-titles after they began to appear on wrappers (compare Opp. 66–71
&amp; 73 from Posth–1-MEIf, Posth–1a-COM, Posth–1b-GE and Posth–1c-GE
with 66–1a-COM, 66–1b-GE, 66–1c-GE, 67–1c-GE, 68–1a-COM, 69–1d-GE,
70–1-MEIf, 71/1–1b-GE, 71/2–1a-GE, 71/3–1a-GE and 73–1a-GE). The
German editions present a more complex history. Certain half-titles
remained unchanged: compare Op. 70 from Posth–1-Sam with 70–1b-Sam
(D-Bds copy); likewise Op. 71 No. 1 from Posth–1-Sam with 71/1–1a-Sam
and 71/1–2-Sam (US-Wc copy). In other cases a single change was made:
compare Op. 67 from Posth–1-Sam with 67–1b-Sam (GB-Lbl copy) and
67–1c-Sam (second PL-Wn copy); Op.  68 from Posth–1-Sam with 68–1-Sam
(A-Wn copy) and 68–1b-Sam; Op. 69 from Posth–1-Sam with 69–1-Sam
(PL-Wn copy) and 69–2a-Sam (D-Bds copy); Op. 71 Nos.  2 &amp; 3 from
Posth–1-Sam with 71/2–1-Sam (PL-Kj copy), 71/2–1a-Sam (PL-Tu copy) and
71/3–1a-Sam; and Op. 72 from Posth–1-Sam with 72–1a-Sam, 72–1b-Sam and
72–1d–Sam (D-Bds, GB-Ob, US-NYp copies). Finally, in another case two
changes were made: compare Op. 66 from Posth–1-Sam with 66–1b-Sam
(PL-Tu copy), 66–2-Sam (US-Wc copy), 66–2a-Sam (D-Dl and US-Cu
copies), 66–3-Sam (PL-Kj copy), 66–4c-Sam (GB-Ob copy) and 66–4f-Sam
(D-Bds copy), as well as 66–4g-Sam (third PL-Wn copy) and
66–4i-Sam.</p>
</div>

<div id="ftn8">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref8" id="_ftn8" name="_ftn8">[8]</a> Scores with earlier
wrappers include 1–1a-BR (F-Pn copies), 3–1c-BR, 7–2a-BR, 14–1b-BR,
15–1c-BRg (first A-Wn copy), 16–1e-BR, 20–1b-BR, 23–1b-BR, 23–1c-BR,
24–1b-BR (F-Pplanes and I-Rce copies), 28/1-12–1h-BR,
28/13-24–1f-BR&amp;D, 28/13-24–1h-BR, 32–1b-BRg (second A-Wn copy),
34/1–1b-BR, 34/1–1c-BR (I-Rce copy), 34/3–1d-BR, 36–1g-BR (I-Rce
copy), 37–1e-BR&amp;D, 41–1c-BR, 48/1–1b-BR&amp;D and MFM–2b-BR. In
contrast, 35–1d-BR&amp;D has a later wrapper.</p>
</div>

<div id="ftn9">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref9" id="_ftn9" name="_ftn9">[9]</a> The sale price was
usually left off an ATP because the different versions thereof had
variable functions. That explains why a price is found on only three
copies of albums catalogued in this volume (i.e. second GB-Ob copy of
45–1-ME, second F-Pn copy of MFM–1-E, and US-Cu copy of
MFM–1a-E). Several French albums also lack a price because they were
offered to subscribers of the RGMP (see 45–1-Sm, 62/2–1-BR,
64/1–1-BR).</p>

<p style="font-size: 9pt; line-height: 115%; text-align:
justify">Information about the prices of German albums can be gleaned
from the music press and publishers’ catalogues as follows:</p>

<ul style="font-size: 9pt; line-height: 115%; text-align: justify">
<li>23–2-B&amp;H: ‘4 Thlr. Prachtausgabe 6 Thlr.’ (MlM No. 12, 1836,
p. 139)</li>

<li>32/1–1-Sam and 32/1–1a-Sam: ‘geb. 3 Thlr 18 Gr.’ (MlM No. 2, 1838,
p.  21); ‘3 Thlr 22<b style="mso-bidi-font-weight:normal">t</b> Sgr.’,
‘Prachtausgabe 7 Thlr.’ (‘MUSIKALIEN-<b
style="mso-bidi-font-weight:normal">½</b>‌VERLAGS-‌CATALOG<b
style="mso-bidi-font-weight:normal">½</b>‌der<b
style="mso-bidi-font-weight:normal">½</b>‌Schlesinger’schen Buch- &amp;
Musikhandlung<b style="mso-bidi-font-weight:normal">½</b>‌in BERLIN’,
1846, p. 10)</li>

<li>32/2–1-Sam: ‘geb. 3 Thlr 18 Gr.’ (MlM No. 12, 1838, p. 181)</li>

<li>33/1&amp;2–1a-B&amp;H: ‘cart. 3 Thlr.’, ‘Prachtausgabe 5 Thlr.’
(MlM No. 12, 1838, p. 181)</li>

<li>45–1-ME: ‘6 Fl.’, ‘Pracht-Ausgabe 10 Fl.’ (MlM No. 2, 1842,
p. 21)</li>

<li>MFM–1-SCH: ‘geb. 7 Fl. 12 Xr.’ (MlM No. 1, 1842, p. 7); ‘6
Fl. broschirt’ (<i>Intelligenz-Blatt zur Cäcilia</i> No. 81, 1842,
p. 11).</li>
</ul>
</div>''',
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000200020004',
            'show_in_menus': True,
            'slug': 'wrappers-and-covers',
            'title': 'Wrappers and covers'
        }
    },
    'background_general_music': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Each component of a Chopin first edition was subject to
modification throughout its commercial life, and the music text was no
exception. Indeed, many editions evolved quite significantly in this
respect. In addition to the changes resulting from lithographic
transfer (see ‘Printing methods’ under ‘General characteristics of
Chopin’s first editions’), the following modifications can be observed
within successive impressions of a given edition:</p>

<ul>

<li>
<p><i>revisions external to the music itself but on pages containing
music text</i></p>

<p>These range from elements at the top of the page (headline, caption
title, sub-caption, pagination) to those at the bottom (title,
publisher’s name and address, plate number, name of engraver and/or
printer, copyright notice, publisher’s note, advertisement text), all
of which could be added, removed, modified, re-engraved and/or
repositioned.  Such changes were made in accordance with the musical
and commercial prerogatives of individual publishers as well as the
quality of their work.</p>
</li>

<li>
<p><i>revisions to the graphic content of the music text</i></p>

<p>These did not affect the content of the music and were probably
carried out at the engraver’s discretion.</p>
</li>

<li>
<p><i>revisions intended to improve the quality of the music
text</i></p>

<p>Changes of this type were made to correct engraving errors, to
amend tempo indications, and to add accidentals, articulation marks
(staccatos, accents, etc.), pedallings (both onsets and releases),
fingerings and new variants stemming either from the composer himself
or from a house editor or professional corrector. The vast majority of
such changes were sound, though some ill-conceived revisions
attributable to an inept engraver, corrector or house editor caused
altogether new problems.</p>
</li>
</ul>

<p>Most reprints of the English editions contain numerous revisions of
the first type, i.e. external to the music itself but on pages with
music text. Indeed, a good many of the elements listed under the first
category were changed more than once – and sometimes frequently – with
the exception of the name of the publisher, which was updated by
Wessel’s successor Ashdown &amp; Parry in only three impressions
catalogued in this volume.<a href="#_ftn1" id="_ftnref1">[1]</a> In
the French and German editions, such changes also occurred regularly
but to a lesser extent,<a href="#_ftn2" id="_ftnref2">[2]</a> whereas
only three Polish editions were revised in this way (see 74–1e-G,
PolG#m–1a-K, and Polish voice part of Op. 74 No. 10 in 74/10–1a-KO,
74/1–1a-KO).</p>

<p>In just a single case – the impression of the Mazurkas Op. 6
classed as 6–2b-KI – was a revision made to the music text’s graphic
content. For some unknown reason, the engraver removed the double
strokes above and below the repeat signs which were present in the two
earlier impressions of this edition. This change – which was not the
only one in this reprint<a href="#_ftn3" id="_ftnref3">[3]</a> – was
rescinded soon after, however (see 6–2c-KI).</p>

<p><a id="1" linktype="document">Table 1 - 'First editions' with
revised music text</a></p>

<p>Revisions intended to improve the quality of the music text are the
most interesting but also the most complex.<a href="#_ftn4"
id="_ftnref4">[4]</a> Table 1 lists all of the first editions affected
in this way, divided into two broad periods. It reveals that during
Chopin’s lifetime the French first editions underwent the most
extensive revision. This is hardly surprising, given his presence in
Paris and thus his ability to refine the French prints on an ongoing
basis. By extension, it can be confidently concluded that he
instigated most of the ameliorations to the French editions. During
this period, approximately one-quarter of the English first editions
and a lesser proportion of German prints were revised. After Chopin’s
death in 1849, the situation was reversed. Apart from one
insignificant revision (see 9–1d-BR), the French editions remained
stable: the definitive texts achieved with Chopin’s input did not
change during their ensuing years on the market, even when the first
editions were reprinted by new publishers who had acquired the
original rights. In contrast, modifications were made to almost all
German and English first editions, often in great quantity. Only three
of the editions brought out posthumously in Poland changed over time;
those published before 1830 were on the market for a relatively
limited period, which explains not only the lack of corrections
therein but also their extreme rarity today. As for altogether new
editions, Table 2 identifies the second, third and later Chopin
editions retaining original plate numbers, as well as those second
editions with new plate numbers.<a href="#_ftn5"
id="_ftnref5">[5]</a></p>

<p><a id="2" linktype="document">Table 2 - Later editions</a></p>

<p>The following conclusions can be drawn about the evolution of the
music text in the Chopin editions. First of all, the vast majority of
the French scores exist in a single ‘first edition’, revised
impressions of which were often produced as described above.<a
href="#_ftn6" id="_ftnref6">[6]</a> In none of the second editions
that appeared in France (with either original or new plate numbers)
was the music text modified after publication, nor in the reprinted
first editions brought out by other publishers who had acquired the
original rights. The situation is more complex in the case of the
German prints. Here one notes two contrasting practices: replacement
of the original plates, in other words, production of a new edition;
and retention of the plates but with ongoing refinements being made to
them (i.e. the process of revision discussed above). Both methods were
adopted by Breitkopf &amp; Härtel: very few of their Chopin editions
were not revised in some way, and many were re-engraved once if not
twice. The same applies to Hofmeister, Schuberth and, to some extent,
the Austrian publishers Haslinger and Mechetti, in proportion to the
number of Chopin compositions on their respective lists. In contrast,
Kistner and A. M. Schlesinger tended not to revise their existing
editions but instead to produce altogether new, re-engraved
ones. (Indeed, very few revisions were made within successive
impressions of given Kistner editions, and almost none in the case of
A. M. Schlesinger.) That does not mean the two publishers attached
limited importance to the quality of their publications: on the
contrary, an evolution did occur in their Chopin output, but from
edition to edition rather than impression to impression. The
relatively high number of new editions that emerged is remarkable,
with as many as six editions of one work brought out by Kistner.</p>

<p>Few second editions of Chopin’s music were published in England; in
fact, during the composer’s lifetime, only one such edition appeared,
bearing the original plate number. No further new editions were
released by Wessel or his successors until the 1870s, when a more
systematic process of renovation began.<a href="#_ftn7"
id="_ftnref7">[7]</a> Nevertheless, this firm undertook an
extraordinary amount of revision and refinement of its original
editions, virtually all of which were modified at some point. In
contrast, very limited revisions were carried out to the Polish
editions identified above, i.e. <i>Źyczenie</i> (Op. 74 No. 1),
Op. 74 No. 13 and the E minor Waltz.</p>

<p>In concluding this section, it is important to emphasise that a
Chopin first edition cannot be reliably identified until each of its
components has been thoroughly scrutinised.  Moreover, rigorous and
comprehensive comparison is required of all surviving impressions of
the edition in question, given that revisions typically were made over
several decades if not longer.<a href="#_ftn8"
id="_ftnref8">[8]</a></p>

<hr align="left" size="1" width="33%"/>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" id="_ftn1">[1]</a> See 7–1k-A&amp;P, 13–1b-A&amp;P
and 33–1h-A&amp;P.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" id="_ftn2">[2]</a> Examples include the
following:</p>

<ul>
<li style="font-size: 9pt; line-height: 115%; text-align:
justify">correction, addition or displacement of caption titles or
sub-captions: 6–1a-Sm, 7–2b-KI, 15–2b-B&amp;H, 17–2c-B&amp;H,
27–1d-B&amp;H, 28–1f-B&amp;H, 30–1b-B&amp;H, 33–2a-B&amp;H,
34/3–1f-B&amp;H, 35–1a-TR, 36–1-TR, 37–1d-B&amp;H, 43–1g-SCHU,
48–1a-Sm, 48/2–1b-Sm, 48–1a-B&amp;H, 55–1c-B&amp;H, 56–1a-B&amp;H,
58–1a-MEIj, 66–3a-Sam, 68–1f-Sam, 68/4–2a-Sam, 69–2c-Sam,
70–1f-Sam</li>

<li style="font-size: 9pt; line-height: 115%; text-align:
justify">updating or addition of plate number: 12–1a-LE, 16–1b-Sm,
17–1a-Sm, 19–1a-PR, 35–1c-BR, 35/3&amp;4–2a-BR, 36–1d-BR, 37–1c-BR,
38–1b-BR, 39–1b-BR, 40–1a-BR, 41–1b-BR, 43–1b-BR</li>

<li style="font-size: 9pt; line-height: 115%; text-align:
justify">updating of publisher’s name and address: MM–2a-BR</li>

<li style="font-size: 9pt; line-height: 115%; text-align:
justify">updating of publisher’s name and address and of plate number:
10–1d-LE, 18–1b-LE, 25–1b-LE, 28/1-12–1b-BR, 28/13-24–1c-BR</li>

<li style="font-size: 9pt; line-height: 115%; text-align:
justify">addition or modification of name of publisher, engraver or
printing firm: 1–1a-BR, 3–1b-BR, 3–1c-BR, 6–4a-KI, 6–4b-KI, 7–2a-BR,
9–1f-BR, 9–3a-KI, 12–1a-LE, 20–1d-B&amp;H, 28/15–1n-B&amp;H, 29–1c-BR,
33–1c-BR, 34/1–1b-BR, 34/1–1c-BR, 34/3–1c-BR, 35–1-TR, 36–1g-BR,
36–1b-B&amp;H, 38–1a-TR, 38–1d-BR, 39–1d-B&amp;H, 40–1-TR, 40–1d-BR,
41–1-TR, 43–1a-SCHU, 43–1g-SCHU, 43–2a-SCHU, 43–2b-SCHU, 48/2–1e-BR,
53–1c-BR, 55–1c-B&amp;H, 55–1h-B&amp;H, 58–1d-B&amp;H, 64/2–1b-BR,
64/3–1a-BR, 66–1h-GE, 66–4-Sam, 66–4c-Sam, 66–4d-Sam, 66–4f-Sam,
66–4h-Sam, 67–1e-Sam, 69–1b-GE, 69–1d-GE, 71/1–2a-Sam, 71/2–1b-Sam,
71/3–1d-Sam, 72–1d-Sam, 73–1e-GE</li>

<li style="font-size: 9pt; line-height: 115%; text-align:
justify">removal of names of foreign concessionaires: 68/4–2a-Sam.</li>
</ul>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" id="_ftn3">[3]</a> The sub-caption was also
re-engraved.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref4" id="_ftn4">[4]</a> Because the original intention of
these revisions was to ‘correct’ a previous version, we refer to
impressions in which the music text has been modified as ‘corrected
reprints’. It must be stressed, however, that such changes may
themselves have amounted to errors rather than corrections as more
commonly understood. See ‘Reprint’ in the Glossary in ‘Reference
material’.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref5" id="_ftn5">[5]</a> The table comprises only those new
editions released by the original publishers or their successors, as
follows: Maurice Schlesinger → Brandus → G. Brandus, Dufour et Cie;
Stern → Friedländer; and Wessel → Ashdown &amp; Parry → Edwin
Ashdown. The numbers shown include the first impression but exclude
the multiple editions of works which had entered the public
domain. Reprinted first editions prepared using the original plates
but with new plate numbers arising from the transfer of publishing
rights from one firm to another are also excluded.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref6" id="_ftn6">[6]</a> The following works were released
in a single French edition which did not change after publication
(cf. Table 1): Opp. 4–6, 8,11, 12, 14–17, 19, 20, 22, 24, 27, 29–32,
34, 42, 43, 50, 51, 53, 59–62; Op. 64 Nos. 2 &amp; 3; Op. 65; <i>Grand
Duo Concertant</i>, Mazurka dedicated to Emile Gaillard, Mazurka from
<i>La France Musicale</i>, <i>Hexameron</i>, Variations on a German
National Air, Posthumous Works.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref7" id="_ftn7">[7]</a> Table 2 encompasses only those new
English editions which are catalogued in this volume; however,
according to Chomiński and Turło (1990: 252), new editions of all of
the nocturnes, ballades, etudes, mazurkas and waltzes were published
by Ashdown &amp; Parry or Edwin Ashdown.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref8" id="_ftn8">[8]</a> The detailed textual analysis that
we have undertaken of Chopin’s music within various albums and the
<i>Méthode des Méthodes</i> (i.e. 15–1a-Sm, 23–2-B&amp;H, 32/1–1-Sam,
32/1–1a-Sam, 32/2–1-Sam, 33/1&amp;2–1a-B&amp;H, 45–1-Sm, 45–1-ME,
50/1–2-Sm, 62/2–1a-BR, 64/1–1a-BR, MEG–1-CH, MEG–1a-CH, MFM–1-E,
MFM–1a-E, MFM–1-SCH, MM–0-Sm, MM–1-Sm, MM–1-Sam, MM–1a-Sam, MM–1b-Sam,
MM–1c-Sam, MM–1a-CHAP) has not been extended to the works therein by
other composers. Such an investigation is beyond the scope of this
catalogue, notwithstanding its potential to reveal textual
discrepancies between impressions presented here as ‘identical’, which
would necessitate a different interpretation of their identity and
respective status.</p>''',
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000200020005',
            'show_in_menus': True,
            'slug': 'music-text',
            'title': 'Music text'
        }
    },
    'background_publishers': {
        'class': IndexPage,
        'kwargs': {
            'depth': 6,
            'introduction': u'''<p>Detailed discussion follows on the publication of Chopin’s music
in the principal countries referred to previously, i.e. France, the
German states and England. The output of the most important firms is
considered, likewise that of other publishers requiring special
comment.</p>''',
            'numchild': 5,
            'path': '000100010001000200020003',
            'show_in_menus': True,
            'slug': 'chopins-publishers',
            'title': "Chopin's publishers"
        }
    },
    'background_publishers_france': {
        'class': IndexPage,
        'kwargs': {
            'depth': 7,
            'introduction': u'''<p>The Bibliothèque nationale de France (BnF) holds the world’s
most extensive collection of French first editions of Chopin; the
majority of these were acquired through the <i>dépôt légal</i>. Four
other institutions – British Library (London), Narodowy Instytut
Fryderyka Chopina (Warsaw), Österreichische Nationalbibliothek
(Vienna) and Regenstein Library (Chicago) – also possess numerous
French editions.</p>

<p><a id="3" linktype="document">Table 3 Chopin’s French publishers</a></p>

<p>Table 3 reveals that Maurice Schlesinger and his successor Brandus
were Chopin’s principal French publishers by far, followed by
Troupenas with nine Chopin works on his list. The other publishers in
the table handled Chopin’s music on a more ad hoc basis. The fact that
multiple editions of Opp. 1–3 are shown has nothing to do with a
transfer of rights between publishers; instead, these works entered
the public domain in France some years after their original
publication in Warsaw or Vienna, as a result of which French reprints
could be freely produced. Observance of the usual deposit formalities
did not secure protection for Richault’s edition of Op. 3: to remove a
work from the public domain, a publisher needed to obtain the author’s
express permission to issue a new publication, and Richault’s failure
to do this meant that Schlesinger and Schonenberger could themselves
publish Op. 3 on an entirely legal basis. Opp. 1 &amp; 2 had a similar
fate but for somewhat different reasons: although Schlesinger is
likely to have gained Chopin’s approval for a new edition, he
neglected to deposit a copy as required, and this oversight was
exploited by Schonenberger. The latter also brought out the Rondo
Op. 5, which was published first in Warsaw in 1828 and again in
Leipzig in 1839; once again, the new French publication was within the
law, although Schonenberger was the only publisher in Paris to have
any interest in this early work by the composer.</p>

<p><a id="4" linktype="document">Table 4 Changes in ownership and
acquisitions: Chopin’s French publishers</a></p>

<p>Although both Schlesinger and Brandus sought ownership of the
Chopin editions previously released by other French publishers, their
aspirations to publish the complete works of the Polish composer were
never fully realised. (See Table 4.) Schlesinger auctioned part of his
list in November 1842 to mitigate his parlous finances, enabling
Lemoine to buy Opp. 10, 18 &amp; 25. Faced with similar difficulties,
Brandus was obliged in July 1857 to sell the works of Halevy, four of
which Lemoine appears to have purchased along with Chopin’s Op. 12.<a
href="#_ftn1">[1]</a> No unequivocal information is available about
the sale of the Mazurka from <i>La France Musicale</i>; however, it is
known that in 1847 the Escudier frères had financial problems that led
to the sale of part of their list,<a href="#_ftn2">[2]</a> and
possibly the Mazurka changed hands at that time.</p>

<hr align="left" size="1" width="33%"/>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" name="_ftn1">[1]</a> See Devriès and Lesure 1988:
277; as it happens, Hérold and Halevy’s <i>Ludovic</i> – on which
Chopin’s Op. 12 was based – was not one of the four works. It is odd
that Op. 12 remained in Brandus’ catalogue until 1863 even though it
was absent from the ‘EO’ STP released in 1859, a lacuna indicating
that the work no longer belonged to Brandus at this time.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" name="_ftn2">[2]</a> See Devriès and Lesure 1988:
163.</p>''',
            'numchild': 5,
            'path': '0001000100010002000200030001',
            'show_in_menus': True,
            'slug': 'france',
            'title': 'France'
        }
    },
    'background_publishers_france_dating': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Tables 5–7 present a range of information which potentially
sheds light on when each edition was published and which impression
was truly the first.<a href="#_ftn1" id="_ftnref1">[1]</a> This
information has been compiled from the following sources:</p>

<ul>

<li><i>dépôt légal</i> registers (available from 1842 onwards; earlier
ones have been lost)</li>

<li>title pages of scores from the former Conservatoire collection (now held by the BnF)</li>

<li>BnF registers in which all scores from the <i>dépôt légal</i> were catalogued upon assimilation into the BnF’s own collection</li>

<li><i>Bibliographie de la France</i> – an official periodical established by decree on 14 October 1811</li>

<li>advertisements in the Paris musical press: <i>Revue musicale</i>
(Opp. 10, 11; <i>Grand Duo Concertant</i>), <i>Le Pianiste</i>
(Opp. 12, 19), <i>Revue et Gazette musicale de Paris</i> (Opp.  1, 2,
6–9, 13–18, 20–34, 44–65; <i>Méthode des Méthodes</i>; Mazurka
dedicated to Emile Gaillard), <i>La France Musicale</i> (Opp. 35–41,
43;<i> Hexameron</i>; Mazurka from <i>La France Musicale</i>)</li>

</ul>

<p><a id="5" linktype="document">Table 5 Works published in France
with opus number</a></p>

<p><a id="6" linktype="document">Table 6 Works published in France
without opus number</a></p>

<p><a id="7" linktype="document">Table 7 Works published posthumously
in France</a></p>

<p>Different types of information can be gleaned from the press
advertisements. Those for Opp. 1, 2 &amp; 6–9 are the first
announcements of these works, appearing some time after their initial
publication, while those for Opp. 10–19, 21–23, 25–27, 31, 32, 35–41
&amp; 43–62 proclaim the recent appearance of an edition or indicate
its imminent release. Some advertisements confirm when a work was
published either in a supplement to the RGMP (Opp. 20, 24, 29, 30, 33)
or within the albums of Maurice Schlesinger (Opp. 34, 45). The
advertisement for the Mazurkas Op. 50 anticipated the edition’s
publication by nearly ten months, whereas for Opp. 63–65 a similar
announcement appeared only weeks in advance.</p>

<p>To establish the true publication date of a French edition, one
must take all available evidence into account. In the vast majority of
cases, the information in the registers of the <i>dépôt légal</i> and
the BnF proves to be the most reliable. As for works which were not
deposited and for which press announcements either post-dated actual
publication by a long period (Opp. 1, 2, 6–9) or simply do not exist
(Opp. 5, 42), other sources such as publishers’ catalogues, Chopin’s
correspondence, the dates inscribed by the composer on title pages and
so on must be consulted, which is how some of the information under
the heading ‘Publication’ in Table 5 was derived.</p>

<p>Opp. 22, 23, 26, 37, 41, 63 &amp; 64 were deposited twice. It is
noteworthy that more than seven months elapsed between the second
registration of Opp. 63 &amp; 64 and deposit of the scores,<a
href="#_ftn2" id="_ftnref2">[2]</a> and furthermore that on the TPs of
the BnF scores from this second deposit the stamp ‘1847’ can be
found. Examination of the BnF’s registers confirms that a persistent
error affected a sizeable number of scores (nos. 459–501 in the
registers), which, despite having been catalogued in late 1848, all
bear the same incorrect date stamp.</p>

<p id="ftn1" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref1" name="_ftn1">[1]</a> Tables 3, 5–8,
10–12, 14–15, 17 &amp; 19 cite only those editions presumed to have
appeared first or which were published more or less simultaneously
with the former. The abbreviated dates in all of the tables and
throughout the entire Annotated Catalogue Online appear in one of two
formats: either day/month/year (e.g. 26/4/1834) or month/year
(e.g. 4/1834). A range of months within a given year takes the form
‘y–z/18XX’, where y and z represent the months in question.</p>

<p id="ftn2" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref2" name="_ftn2">[2]</a> The titles were
registered on 23 March 1848, whereas the copies themselves were
deposited on 13 November that year. Curiously, the TP and music text
of the deposit copy of the Mazurkas Op. 63 are earlier versions of
those in the first deposit copy.</p>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300010001',
            'show_in_menus': True,
            'slug': 'dating-the-french-editions',
            'title': 'Dating the French editions'
        }
    },
    'background_publisher_france_schlesinger': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Between 1833 and 1845, Chopin brought out the majority of his
works with this important Paris music publisher, on only two occasions
taking his business elsewhere. A quarrel alienated the two men in
1839–40, whereupon Chopin succumbed to Camille Pleyel’s promise of
better conditions which in fact never materialised. As his
correspondence reveals,<a href="#_ftn1" id="_ftnref1">[1]</a> Chopin
regretted forsaking Schlesinger at this time, and once the two were
reconciled he remained committed to him until his eventual retirement
from music publishing.</p>

<p>The editions of this firm are well represented in the <i>Annotated
Catalogue</i>, despite the lack of deposit copies in several cases.
The resultant lacunae were nevertheless redressed thanks in large part
to the BnF’s acquisition of the former collections of Camille
Dubois-O’Meara and Jane Stirling.</p>

<p>As noted above, the music text of numerous Schlesinger editions of
Chopin was refined subsequent to their initial publication, in each
case in a single ‘corrected reprint’ that almost certainly was
initiated at Chopin’s behest. The works in question include a
significant proportion of those shown in Table 1, i.e. Opp. 9, 10, 13,
18, 21, 23, 25, 26, 33, 44, 46–49, 52 and 54–56, and the Etudes from
<i>Méthode des Méthodes</i>. Altogether new engravings were undertaken
only in the case of works which had initially been published in either
an album (Op.  45, Op. 50 No. 1) or an anthology (Etudes from
<i>Méthode des Méthodes</i>).</p>

<p>A sizeable number of impressions – namely of Opp. 24, 26, 29, 30,
33 &amp; 51 – were produced by means of lithographic transfer for the
subscribers to Schlesinger’s journal; lithography (or possibly
lithographic transfer) was also used to prepare two albums published
in quantity (see 45–1-Sm, 50/1–2-Sm). Colour appears in two of
Schlesinger’s Chopin editions: Op. 45 (see +45–1-Sm) and a special
impression of Op. 30 (see 30–1a-Sm) which most likely was released in
the <i>Album du Pianiste 1838</i>, of which no surviving copies have
been traced. Nor has it been possible to locate two other anthologies
which contained works by Chopin and which are known only through press
announcements or similar evidence: <i>Album des Pianistes 1833
</i>(Nocturnes Op. 9) and <i>Album des Pianistes 1836</i> (Mazurkas
Op. 24).<a href="#_ftn2" id="_ftnref2">[2]</a></p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> See Chopin’s letter to Fontana of 10 August 1839 in KFC 1955: i/353–354.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Publication of the albums of 1836 and 1838 was announced in the RGMP.
The ostensible existence of the album of 1833 was asserted by Brown (1972: 59).
According to Fuld (1995: 392, 611), Alan Tyson owned copies of the 1833 and
1839 albums, but his collection – acquired after
his death by GB-Lbl and GB-Ob – does not include them. Tyson did possess a
defective copy of the 1834 album, currently located at GB-Lbl (see 15–1a-Sm). A
copy of the 1839 album belonging to the collection of Robert Commagère is
described under 34/1–1-Sm.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300010002',
            'show_in_menus': True,
            'slug': 'publications-of-maurice-schlesinger',
            'title': 'Publications of Maurice Schlesinger'
        }
    },
    'background_publishers_france_troupenas': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Chopin’s strained relations with Schlesinger and Pleyel left him
in the awkward position of having no French publisher just when he
needed one in order to keep pace with the German editions of several
works then being prepared in Leipzig. Under pressure of time he turned
to Troupenas, ceding the rights to Opp. 35–41 in March 1840 and to the
Tarantella Op. 43 a few months later. It is hardly surprising that in
these circumstances the French editions of Opp. 35–37 were hastily
produced; indeed, Troupenas barely had time to engrave the music text
between signing the contract in late March<a href="#_ftn1"
id="_ftnref1">[1]</a> and depositing a copy of each in mid-May. His
solution was to deposit uncorrected proofs of Opp. 35 &amp; 37 rather
than finished copies, while Op. 36, registered at the same time, was
in a more advanced state but still far from definitive. The fact that
Opp. 38, 40 &amp; 41 were also deposited at proof stage is harder to
explain, given that in principle Troupenas had more than five months
to prepare these editions – unless Chopin was late in submitting his
manuscripts to the publisher.<a href="#_ftn2"
id="_ftnref2">[2]</a></p>

<p>All of this helps to explain the relatively poor state of the music
text in Troupenas’ first impressions and thus the need for their
ongoing refinement, a process that can be discerned from successive
entries within this catalogue. One corrected reprint each of the
Scherzo Op. 39 and the Polonaises Op. 40 appeared on the market, while
the editions of the Impromptu Op. 36, Nocturnes Op. 37, Ballade Op. 38
and Mazurkas Op. 41 were twice revised. As for the Sonata Op. 35, no
fewer than three stages of correction occurred between the proofs and
the definitive version of the edition. Only Troupenas’ score of the
Tarantella Op. 43 remained unchanged after its initial
publication. Shortly after Chopin’s death Troupenas brought out newly
engraved versions of the third and fourth movements of the Sonata
Op. 35. No copies of his <i>Hexameron</i> edition have been located.<a
href="#_ftn3" id="_ftnref3">[3]</a></p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> In a letter of 23 April 1840, Chopin informed Fontana of the recent
acquisition by Troupenas of Opp. 35–41;
see KFC 1955: ii/8. Probst confirmed
as much in his letter to Breitkopf &amp; Härtel of 25 March 1840; see Lenneberg
1990: 73.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Apart from the proof copies deposited by Troupenas (see above), only
two other proofs of Chopin first editions
can be located at present: see 10/2–0-Sm
and 42–0-P.</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a>
Copies of the reprint issued by Brandus after
1850 are nevertheless available (see HEX–1-BR).</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300010003',
            'show_in_menus': True,
            'slug': 'publications-of-troupenas',
            'title': 'Publications of Troupenas'
        }
    },
    'background_publishers_france_brandus': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>As the successor to Maurice Schlesinger, Brandus published the
last seven opuses released during Chopin’s lifetime, three of which he
also offered to the subscribers of the RGMP in keeping with the
practice of his predecessor (see 59/2–1a-BR, 62/2–1a-BR,
64/1–1a-BR). Lithographic transfer was used to produce the three works
in question; two of them – the Nocturne Op. 62 No. 2 and Waltz Op. 64
No. 1 – appeared in albums with beautiful title pages in colour. The
reprint of Op. 34 No. 2 brought out by this firm shortly before its
demise is another example of the use of this technique (see
34/2–2a-BR).</p>

<p>After buying the Preludes Op. 28 from Catelin, the Mazurka from
<i>La France Musicale </i>and Troupenas’ list, Brandus possessed a
vast proportion of Chopin’s music, and this allowed him to launch the
‘ÉDITION ORIGINALE<b>½</b>‌OEUVRES COMPLÈTES POUR LE
PIANO<b>½</b>‌DE<b>½</b>‌FRÉDÉRIC CHOPIN’ late in 1859 even though a
good many works were missing from his catalogue, namely Opp. 5, 10,
18, 19, 25, 42, 57 &amp; 58 and the Mazurka dedicated to Emile
Gaillard. Brandus therefore set about producing new editions of
Opp. 18, 42 &amp; 57, which were published by 1859,<a href="#_ftn1"
id="_ftnref1">[1]</a> whereas nearly twenty years elapsed before he
released Opp. 5, 19 &amp; 58.<a href="#_ftn2" id="_ftnref2">[2]</a>
Despite this output, the series remained incomplete, given the absence
of the Variations Op. 12 and possibly also of Op. 10, Op. 25 and the
Mazurka dedicated to Emile Gaillard, no copies of which have been
located to date.<a href="#_ftn3" id="_ftnref3">[3]</a></p>

<p>After 1859 Brandus continued to publish Chopin’s music
independently of his main series, for example in the three volumes
entitled <i>Succès universels</i> (Op. 10 Nos. 3 &amp; 4, Op. 18,
Funeral March and Presto from Op. 35)<a href="#_ftn4"
id="_ftnref4">[4]</a> and within an anthology of more than 250 pages
containing a wide range of works.<a href="#_ftn5"
id="_ftnref5">[5]</a> It goes without saying that these amounted to
new Chopin editions rather than reprints prepared from the original
engravings.</p>

<p>Financial difficulties caused a dramatic reduction in the output of
this publisher from 1873 onwards. In 1874 a loan was negotiated to
settle the most urgent debts, and as collateral Brandus deposited
nearly 50,000 engraved plates with the printer Jean Thierry. Among
them were numerous Chopin works, thus explaining the presence of the
name of the firm Buttner-Thierry at the bottom of the music text of
many late reprints brought out in the ‘EO’ series.<a href="#_ftn6"
id="_ftnref6">[6]</a> After Louis Brandus’ suicide in 1887, control of
the firm passed to his associate Philippe Maquet; then, in 1899, the
Brandus/Maquet works were acquired by Celestin Joubert. Only two
first-edition reprints released after 1887 have been catalogued in
this volume: Maquet’s Nocturnes Op. 9 (see 9–1g-M) and Joubert’s
<i>Hexameron</i> (see HEX–1a-J).<a href="#_ftn7"
id="_ftnref7">[7]</a></p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> Each of the known exemplars of Op. 18 (plate no. B. D. 10.192,
available at US-Cu: M32.C54 W395) and Op. 42 (B. et D. 10195.; US-Cu: M32.C54
W471) has an ITP, whereas that of Op. 57 (B. et D. 10.197; F-Pn: Vm<sup>12</sup>
5504) was sold with a STP.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Respectively, Op. 5 (plate no. B. et Cie 12,409, available at F-Pn: Vm<sup>12</sup>
5558), Op. 19 (B. et Cie 12408; F-Pn: Vm<sup>12</sup> 5509), Op. 58 (B. et Cie
12.405; F-Pn: Vm<sup>12</sup> 5567). According to the plate numbers, these date
from as late as 1877. Two other works belonging to Brandus but originating in
Troupenas’ list were released in a second edition within the ‘EO’ series: Op.
37 (B. et CA 6481; F-Pn: Vm<sup>12</sup> 5544) and Op. 43 (B. et CA 6480; F-Pn: Vm<sup>12</sup> 5568).</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> Opp. 10 &amp; 25 appeared in Brandus’ catalogue from July 1868, and the
<i>Deux
Mazurkas</i> in the one from July 1869. Nevertheless, the fact that
Opp. 5, 19 &amp; 58, which were not published for another ten years, also
appear in these catalogues casts doubt over their credibility. Moreover, the
Mazurka dedicated to Emile Gaillard is not included within the score catalogued
under MFM–2b-BR, despite the presence on the STP of the title ‘Deux Mazurkas en
<i>la</i> mineur’, whereas on versions 5 &amp; 6 of the ‘EO’ STP, the title was
changed to ‘Mazurka en <i>la</i> mineur’ (see description
in Appendix I). Both of these observations indicate that the mazurka in
question was never published by Brandus. It is noteworthy that even after 1860 certain works by Chopin were
reprinted with an ITP rather than a STP; these include the US-Cu scores of Op.
16 and Op. 64 No. 1 classed respectively under 16–1c-Sm
and 64/1–2-BRD&amp;C, the F-Pmounier copies under 24–1-Sm and 64/3–1-BR, the
US-Wc copy under 33–1b-Sm, and the copies of the Etudes from <i>Méthode des Méthodes</i> under MM–2a-BR.</p>
</div>

<div id="ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref4" id="_ftn4" name="_ftn4">[4]</a> See F-Pn: L 1421 (1-2) and Vm<sup>7</sup> 3868.</p>
</div>

<div id="ftn5">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref5" id="_ftn5" name="_ftn5">[5]</a>
Entitled <i>Oeuvres
choisies pour piano</i> and published in 1875,
the volume is available at F-Pn: Vm<sup>7</sup> 2423.</p>
</div>

<div id="ftn6">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref6" id="_ftn6" name="_ftn6">[6]</a> See 1–1a-BR, 1–1b-BR, 2–1d-BR, 3–1c-BR, 7–2a-BR, 7–2b-BR, 9–1f-BR,
9–1g-M, 11–1e-BR, 14–1b-BR, 15–1d-BR, 17–1b-BR, 20–1b-BR, 22–1e-BR, 23–1c-BR, 26–1e-BR,
27–1d-BR, 28/1-12–1h-BR, 28/13-24–1h-BR, 29–1c-BR, 31–1b-BR, 32–1c-BR,
33–1c-BR, 34/1–1b-BR, 34/1–1c-BR, 34/2–2a-BR, 34/2–2b-BR, 34/3–1c-BR,
34/3–1d-BR, 35–1e-BR, 36–1g-BR, 38–1d-BR, 40–1d-BR,
40–1e-BR, 41–1c-BR, 48/2–1e-BR, 50–1b-BR, 53–1c-BR, 64/2–1b-BR, 64/3–1a-BR,
MFM–2b-BR and MM–2a-BR.</p>
</div>

<div id="ftn7">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref7" id="_ftn7" name="_ftn7">[7]</a> A Joubert catalogue from c. 1900 in the F-Pn collection confirms that virtually all of the Chopin
editions previously brought out by Brandus were also available from Joubert.
This indicates that Maquet kept the original plates of his predecessor.
Furthermore, the printer’s imprint in the FL on p. 13 of 9–1g-M confirms that Maquet upheld the arrangement
made between Brandus and Jean Thierry in 1874. Note that one work absent from
Joubert’s catalogue – the <i>Grand Duo Concertant</i> –
most likely formed part of the lot bought by Benoît aîné in April 1894 (see the
Benoît aîné catalogue held by F-Pn; see also Devriès and Lesure 1988: 50).</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300010004',
            'show_in_menus': True,
            'slug': 'publications-of-brandus',
            'title': 'Publications of Brandus'
        }
    },
    'background_publishers_france_meissonier': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Chopin turned to Jean Meissonnier in mid-1845 when his principal
Paris publisher, Maurice Schlesinger, was winding up his business
affairs, and it was for this reason that the former brought out the
<i>Berceuse</i> Op. 57 and Sonata Op. 58. A decade later, in 1855,
Meissonnier’s son similarly took charge of the publication of Chopin’s
Posthumous Works after Brandus withdrew from the project. His edition
– which remained on the market for over thirty years<a href="#_ftn1"
id="_ftnref1">[1]</a> – was sold both as a volume and as separate
works; it featured no fewer than fourteen versions of the same STP, of
which the first eight were in colour. In April 1887 the Posthumous
Works were acquired by Heugel, who rapidly released a corrected
version printed from the original plates but with new plate numbers
(H. 8329–H. 8336) within Marmontel’s <i>Edition classique</i>
series. One or more posthumous pieces were also published in the
<i>Album des pianistes</i> released by the Compagnie Musicale in 1859,
of which no copies have been traced to date.<a href="#_ftn2"
id="_ftnref2">[2]</a></p>

<p>Lithographic transfer was used in the case of only two
works published by Meissonnier’s successors, namely Opp. 66 &amp; 69 (see the
impressions from 66–1b-GE to 66–1h-GE, as well as 69–1d-GE).</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> In the 1880s the Posthumous Works were the subject of a lawsuit filed by Gérard against Breitkopf &amp;
Härtel, which had tried to sell these pieces in France through the machinations
of their agent Durdilly. Gérard attempted to gain control of this edition in a
legal process that lasted several years, including an appeal; he died, however,
before a final judgement was reached.
The ultimate decision, pronounced on 22 November 1888, confirmed that protection of Opp. 66–73
would continue until June 1891.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Publication of this album was announced in the RGMP (25 December 1859, p. 436).</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300010005',
            'show_in_menus': True,
            'slug': 'publications-of-meissonier-and-successors',
            'title': 'Publications of Meissonier and successors'
        }
    },
    'background_publishers_germany': {
        'class': IndexPage,
        'kwargs': {
            'depth': 7,
            'introduction': u'''<p>The Chopin first editions published in Vienna (Austria), Leipzig
(Saxony), Berlin (Prussia), Mainz (Grand Duchy of Hesse and by Rhine)
and Hamburg (a free city during this period) constitute the largest
proportion of scores in this catalogue. They are well represented in
most European and American collections apart from the BnF, which has
only four such scores. Chopin’s principal publisher in the German
states was Breitkopf &amp; Härtel, followed by A. M. Schlesinger and
then Kistner (with thirteen and eight editions respectively); the
other publishers listed in Table 8 dealt with Chopin on a more
marginal basis. In addition to the usual patterns of succession within
a given country, one notes the transfer of the Austrian publications
to such German firms as Lienau (Berlin) and Cranz (Hamburg). (See
Table 9.) The appointment in 1860 of Julius Friedländer as the head of
C. F. Peters explains the change in the designated publisher on the TP
of Chopin’s Op. 59 (compare 59–2-FR and 59–2a-PE). A single work by
Chopin – Rondo Op. 1 – was brought out by two firms, A. M. Schlesinger
and Hofmeister. </p>

<p><a id="8" linktype="document">Table 8 Chopin’s German/Austrian publishers</a></p>

<p><a id="9" linktype="document">Table 9 Changes in ownership and acquisitions: Chopin’s Greman/Austrian publishers</a></p>''',
            'numchild': 8,
            'path': '0001000100010002000200030002',
            'show_in_menus': True,
            'slug': 'the-german-states',
            'title': 'The German States'
        }
    },
    'background_publishers_germany_dating': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Reference can be made to a large body of documentary
evidence to determine the publication dates of these first editions:</p>

<ul>
<li><i>Allgemeine musikalische Zeitung</i> (AmZ) – Leipzig’s leading
music periodical</li>

<li><i>Musikalisch-literarischer Monatsbericht</i> (MlM)<a
href="#_ftn1" id="_ftnref1">[1]</a> – periodical established by the
Verein der deutschen Musikalienhändler</li>

<li><i>Musikalischer Monatanzeiger aller im Jahre 1840 neu
erscheinenden Musikalien</i> – similar to preceding periodical,
providing supplementary information about the dates of Opp. 35–42</li>

<li><i>Wiener Zeitung</i><a href="#_ftn2" id="_ftnref2">[2]</a> – Austrian
periodical in which the publication of Opp. 2, 3, 44, 45 &amp; 50 and
of <i>Hexameron</i> was announced</li>

<li>books by Niecks (1888, R1902), Brown (1972), and Chomiński and
Turło (1990). Many of the dates proposed by these authors diverge from
those indicated in the press.</li>
</ul>

<p>Publishers in Germany and Austria used the musical press not only
to announce the release of their editions but also, quite frequently,
to inform readers that they had acquired certain works. It is
essential to distinguish between acquisition advertisements and
publication advertisements (respectively ‘AA’ and ‘PA’ in Tables 10
&amp; 11) and above all not to confuse the dates of first publicity
notices with those of actual publication. The fact that advertisements
such as these were not produced systematically means that significant
gaps occur within any chronology constructed on the basis thereof. A
fuller picture of publication dates can be gained by referring to the
review sections of the AmZ, i.e. ‘Kurze Anzeige’ and ‘Rezensionen’
(respectively abbreviated ‘KA’ and ‘R’ in Table 10).  The abbreviation
‘IB’ in Table 10 indicates a date emanating from the
<i>Intelligenz-Blatt</i>, published as a supplement to the AmZ. For a
short time in 1842–43, the AmZ printed a summary list of those
editions released during the week or fortnight before the appearance
of the journal itself; dates listed in Tables 10 &amp; 11 which come
from these summaries are marked with an asterisk.<a href="#_ftn3"
id="_ftnref3">[3]</a> Comments are provided in note 88 for dates
followed by a dagger (†).<a href="#_ftn4" id="_ftnref4">[4]</a></p>

<p>It is important to consider which information most reliably
reflects the actual dates of publication. In general, dates taken from
MlM are both extremely accurate and more or less complete, thanks to
their likely provenance from and correspondence with the dates
inscribed in the registers in the archives of the Verein der deutschen
Musikalienhandler, which unfortunately have not survived. Compared to
the AmZ’s dates, those from MlM sometimes follow by one month (see
Opp. 40–42) but rarely longer (Opp. 59, 60–62). Cross-reference
between the MlM’s dates and asterisked ones from the AmZ leads to two
conclusions: editions published in the second half of the month
appeared in the next month’s MlM, whereas for those editions published
in the first half of the month the two sources’ dates are
identical.</p>

<p><a id="10" linktype="document">Table 10 Works published in the
German states with opus number</a></p>

<p><a id="11" linktype="document">Table 11 Works published in the
German states without opus number or posthumously</a></p>

<p>No press advertisements appear to exist for A. M. Schlesinger’s
edition of the Rondo Op. 1; therefore, a choice is required between
the date proposed by Brown as well as Chomiński and Turło (December
1835), versus the more general one indicated in this catalogue (1835;
see 1–1-Sam). As for the Polonaise Op. 3, the advertisement in the
Leipzig press appears to have been released long after the edition
itself (cf.  3–1-ME), again necessitating a choice. In the case of the
Posthumous Works, a noteworthy discrepancy exists between the dates in
MlM and the ‘4 JU 55’ stamped on the volume registered by
A. M. Schlesinger at Stationers’ Hall to gain copyright protection in
England (see ‘England’ under ‘Legal contexts’; see also note 4 under
‘Publications of A. M. Schlesinger and successor (Robert Lienau)’).
This deposit demonstrates that the German edition was ready for
release some time before the date announced in the Hofmeister
periodical.</p>

<hr align="left" size="1" width="33%"/>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref1" name="_ftn1">[1]</a> As its name suggests, MlM
normally appeared on a monthly basis, but occasionally it spanned a
two-month period – including the issues containing announcements of
Chopin’s Opp. 2, 3, 6–19, 25–27, 32, 37 &amp; 74, <i>Grand Duo
Concertant</i>, and <i>Hexameron</i>.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" name="_ftn2">[2]</a> The dates attributed to this
periodical derive from Weinmann 1966 and 1980.</p>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref3" name="_ftn3">[3]</a> These include the following:</p>

<ul style="font-size: 9pt; line-height: 115%; text-align: justify">
<li>5/1/1842: publications from 15/12/1841 to 4/1/1842 (Op. 43, ‘Notre
Temps’ album including the Mazurka from <i>La France Musicale</i>)</li>

<li>2/2/1842: publications from 26/1/1842 to 1/2/1842 (Op. 44,
‘Album-Beethoven’ containing Op. 45, Opp. 46–49)</li>

<li>9/2/1842: publications from 2/2/1842 to 8/2/1842 (separate edition
of Mazurka from <i>La France Musicale</i>)</li>

<li>31/8/1842: publications from 23/8/1842 to 29/8/1842 (Op. 50)</li>

<li>26/4/1843: publications from 18/4/1842 to 24/4/1843 (Op. 51)</li>

<li>1/5/1843: publications from 2/5/1843 to 8/5/1843 (separate edition
of Op. 45)</li>

<li>22/11/1843: publications from 14/11/1843 to 20/11/1843
(Opp. 52–54).</li>
</ul>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref4" name="_ftn4">[4]</a> Further comment is needed in the
following cases:</p>

<ul style="font-size: 9pt; line-height: 115%; text-align: justify">
<li>Op. 2: the actual publication date appears to coincide with the one
stipulated by Chomiński and Turło (1990). In successive letters to Tytus
Woyciechowski dating from 27 March, 27 April, 15 May and 5 June 1830, Chopin
refers to the publication of these variations; thus there is little doubt that
Haslinger brought them out in 1830 on the occasion of the Oster-Messe (Easter
Fair) in Leipzig.</li>

<li>Op. 3: the advertisement appeared in the <i>Intelligenz-Blatt</i>
accompanying the AmZ from August 1836 (No. 10), though bearing the
date ‘Wien, im Juli 1836’.</li>

<li>Opp. 13, 14: because an unusually extended interval elapsed
between the acquisition advertisement and actual publication, Kistner
placed an updated version of the advertisement in the
<i>Intelligenz-Blatt</i> of December 1833.</li>
</ul>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300020001',
            'show_in_menus': True,
            'slug': 'dating-the-german-and-austrian-editions',
            'title': 'Dating the Garman and Austrian editions'
        }
    },
    'background_publishers_german_haslinger': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Tobias Haslinger was Chopin’s first foreign publisher. The two
became acquainted during the young composer’s trip to Vienna in 1829,
when Haslinger was presented with manuscripts of the Variations Op. 2,
Sonata Op. 4 and Variations on a German National Air. Op. 2 was
released in April 1830, whereas the other two works were not engraved
until 1840. Only after Chopin’s death were they actually brought out,
however: their earlier publication was suspended as a result of the
composer’s own misgivings.<a href="#_ftn1" id="_ftnref1">[1]</a></p>


<p>The title page of Op. 2 exists in two slightly different versions:
the first refers to the orchestral accompaniment, while the second –
intended for the solo piano market – makes no mention of the version
with orchestra. Haslinger published a second edition of this work
relatively early, only nine years after the first. Its TP – like the
wrapper, TP and dedication page of <i>Hexameron</i> (published at the
beginning of the same year) – is distinguishable by the use of
colour.</p>

<p>Haslinger employed lithographic transfer only once, when producing
a late reprint of <i>Hexameron</i> in 1872–73 (see HEX–1a-HAt). In
contrast, his successor Schlesinger (Lienau) used this technique quite
frequently.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> See his letters to Fontana of 12 September 1841 and to his family of 1 August
1845 in KFC 1955: ii/34, 145–146.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300020002',
            'show_in_menus': True,
            'slug': 'haslinger',
            'title': 'Haslinger'
        }
    },
    'background_publishers_germany_mechetti': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Chopin’s correspondence reveals that he made initial contact
with Pietro Mechetti during his second and more extended stay in
Vienna in 1830–31. Just before embarking for Paris in July 1831,<a
href="#_ftn1" id="_ftnref1">[1]</a> he gave Mechetti the Polonaise
Op. 3, which was published in November that year. Only after a lengthy
delay did the <i>Musikalisch-literarischer Monatsbericht</i> refer to
its appearance, in the issue of May/June 1832. In July 1836, an
arrangement for piano and violin of Op. 3 was released, and on this
occasion the publisher amended the TP to refer to this new format
while also taking the opportunity to make numerous corrections to the
music text of both the piano and the cello parts (see
3–1a-ME). Publication of the new version was promptly announced in
both MlM and the local press.</p>

<p>Some years later Chopin entrusted three other compositions to
Mechetti, namely Opp. 44, 45 &amp; 50. The TPs of the first two opuses
were printed in a range of different colours. The first impression of
Op. 45 was included in an album intended to raise funds for the
construction of the Beethoven monument in Bonn; a later reprint (see
45–1d-ME) has a title page skilfully combining elements from the
original one and that of Op. 44.</p>

<p>After Mechetti’s death, the firm changed hands three times. The
modification of Op. 3’s plate number to ‘11048’ was probably
undertaken by Spina between 1855 and 1857,<a href="#_ftn2"
id="_ftnref2">[2]</a> i.e. just after the first change of owner. This
can be inferred from the impression released by Alwin Cranz<a
href="#_ftn3" id="_ftnref3">[3]</a> around 1877, which happens to be
the only known example of a lithographic transfer of a Chopin edition
originally published by Mechetti himself. Spina also brought out
second editions of Op. 44 in c. 1868 and Op. 50 in c. 1861.</p>

<p>In October 1873, MlM announced Spina’s publication of a collective
edition containing Opp. 44, 45 &amp; 50. As no trace can be found of
this volume, it is impossible to determine whether the three works
were newly engraved or simply reprinted from existing plates.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> See the letter to his family of 16 July 1831 in KFC 1955: i/181.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> See Deutsch 1961: 12.</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> Located at US-Wc – shelfmark M3.3 .C55 no. 2 Case. A Cranz catalogue
extract appears on the verso of the last page of music text (piano part).</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300020003',
            'show_in_menus': True,
            'slug': 'mechetti',
            'title': 'Mechetti'
        }
    },
    'background_publishers_germany_kistner': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>This Leipzig firm brought out eight Chopin opuses, including
editions of the Mazurkas Opp. 6 &amp; 7 and the Nocturnes Op. 9 which
were re-engraved with unusual frequency because of their
popularity. In effect Kistner published several distinct editions of
Opp. 6, 7, 9, 10 &amp; 13, even though many of these retained their
original plate numbers. From 1858, however, a new plate number was
assigned to each successive edition; initially this was added next to
the original plate number (i.e. in Opp. 8, 10 &amp; 11)<a
href="#_ftn1" id="_ftnref1">[1]</a> before eventually supplanting it
altogether (in Opp. 6, 7 &amp; 9).<a href="#_ftn2"
id="_ftnref2">[2]</a></p>

<p>Kistner’s editions of Op. 9 pose unique challenges of
identification. The second nocturne in the set was also released
separately and was re-engraved on numerous occasions, to an even
greater extent than Nos. 1 &amp; 3 were. Indeed, no fewer than
eighteen individual catalogue entries are needed to encompass all
known impressions of Op. 9, the evolution of which was extraordinarily
complex (see 9–1-KI and subsequent prints). In general, however, few
changes to the music text were made in the successive reprints of most
editions; notable exceptions include Op. 10 (Book 2 of third
edition)<a href="#_ftn3" id="_ftnref3">[3]</a> and Opp. 11 &amp;
13.</p>

<p>Colour was introduced by Kistner in several early impressions of
Opp. 6, 7 &amp; 11 the title pages of which are in sepia, while the
TPs of Opp. 8 &amp; 11 feature a decorative blue or green
background. Later editions of Opp. 6, 7 &amp; 9 were produced using
lithographic transfer, as were the reprints of Opp. 13 &amp; 14 dating
from the late 1860s and the editions of Opp. 8, 10 &amp; 11 with
double plate numbers (see notes 1–3).</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> Plate numbers as follows:</p>

<ul style="font-size: 9pt; line-height: 115%; text-align: justify">
<li>second edition of Op. 8,
published in 4/1872 (MlM): 3778<b>½</b>‌999 (copy available at A-Wn)</li>

<li>fourth edition of Op. 10, published in 1865: in Book 1,
1018.2961.–1018.2966. (engraved copy available at A-Wn; lithographic transfer
copies available at A-Wgm, D-Bds, D-Bs, GB-Lam, GB-Lbl); in Book 2,
1019.2967.–1019.2972. (lithographic transfer copies available at D-Bs, D-Mbs,
GB-Lam, GB-Lbl)</li>

<li>second edition of Op. 11, published in 1858: 2340<b>½</b>‌1020.
1021. 1022 (engraved copies available at A-Wgm, A-Wn, D-LEm,
D-Mbs, PL-Wn, PL-Wnifc, US-NYp; lithographic transfer copies available at
PL-Wnifc).</li>
</ul>

<p style="font-size: 9pt; line-height: 115%; text-align: justify">Note that the fourth edition of Op.  10 was also released in
separate editions, the publication of which was announced in AmZ
(11/10/1865) and MlM (11/1865). US-Cu holds a copy of the fifth
edition (1868) with plate number 3581 and ‘2<u><sup>ME</sup></u>
EDITION’ on the TP (see <a
href="http://chopin.lib.uchicago.edu/gsdl/cgi-bin/library?a=d&amp;c=chopin&amp;d=CHOP423.1">M25.C54E712
c.1</a>).</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Plate numbers as follows:</p>

<ul style="font-size: 9pt; line-height: 115%; text-align: justify">
<li>fifth edition of Op. 6 and seventh edition of
Op. 7, published in single volume in 12/1872 (MlM): 3615 (copy available at
D-Mbs)</li>

<li>fourth edition of Op. 9 Nos. 1
&amp; 3 and sixth edition of Op. 9 No. 2, also published in 12/1872: 3616 (copy
available at US-Cu).</li>
</ul>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> The later reprints of the third edition of Book 2 are not included in
the catalogue because they already contain the double plate numbers 2967<b>½</b>‌1019
➛ 2972<b>½</b>‌1019, which are similar to the fourth edition’s (see note 1 above). In
an A-Wn copy (shelfmark M.S. 88171-4<sup>o</sup>), the music text is identical
to that of 10/7-12–3-KI and 10/7-12–3a-KI, whereas variants exist in an A-Wgm
copy (shelfmark VII 23955; see, e.g., b. 11 of Op. 10 No. 7).</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300020004',
            'show_in_menus': True,
            'slug': 'kistner',
            'title': 'Kistner'
        }
    },
    'background_publishers_germany_schlesinger': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>It is possible that Chopin met Adolph Martin Schlesinger in 1828
during a trip to Berlin.<a href="#_ftn1" id="_ftnref1">[1]</a> In
collaboration with his son Maurice (based in Paris), Schlesinger
published the <i>Grand Duo Concertant</i>, Nocturnes Op.  32, Rondo
Op. 1 and <i>Méthode des Méthodes</i>; he also brought out the
posthumous editions of Opp.  66–73 and Op. 74 in 1855 and 1859
respectively. Schlesinger’s successor Robert Lienau eventually
acquired five additional Chopin works from Friedländer/Peters and
Haslinger.<a href="#_ftn2" id="_ftnref2">[2]</a></p>

<p>It should be noted that the opus numbers generally used to refer to
the posthumous works are attributable not to their editor, Julian
Fontana, but to the publisher.<a href="#_ftn3" id="_ftnref3">[3]</a>
The latter also appears to have held the English rights to these
works, in that a copy of Schlesinger’s first impression of Opp. 66–73
was deposited at Stationers’ Hall in keeping with Article II of the
1846 treaty between Prussia and England, as explicitly stated on two
of the half-titles of the volume in question.<a href="#_ftn4"
id="_ftnref4">[4]</a> Schlesinger re-engraved his Chopin editions with
some frequency, first and foremost Op. 32 No. 1 and Op. 66, each of
which appeared in four distinct editions, while three engravings of
Op. 32 No. 2 were made. Op. 71 No. 1, the Etudes from <i>Méthode des
Méthodes</i> and the Songs Op. 74 all came out in two editions, in the
latter two cases with the new plate numbers S. 2423 (see MM–2-Sam),
S. 6669 (version of Op. 74 for soprano or tenor) and S. 6670 (version
of Op. 74 for alto or baritone).<a href="#_ftn5" id="_ftnref5">[5]</a>
A more selective approach was taken with the Waltzes Op. 69: in the
first impression of the second edition, three pages were produced
using the original plates (see 69–2-Sam), whereas in the following
impression only two original pages remain (see 69–2a-Sam).</p>

<p>The evolution of the music text within the Schlesinger prints was
often extensive, above all in the successive editions of Op. 32. An
especially bold revision was made to Op. 32 No. 1: in all editions
subsequent to the first, the piece ends in B major rather than the
original B minor – an editorial intervention without philological or
musical justification.<a href="#_ftn6" id="_ftnref6">[6]</a></p>

<p>Numerous Schlesinger title pages warrant discussion. The scores of
Opp. 1 &amp; 32 and the Etudes from <i>Méthode des Méthodes</i> were
initially available with individual TPs and then with three different
STPs, each of which exists in several versions. The Posthumous Works
originally contained a unique STP, but from the mid-1860s they were
assimilated into larger collections with correspondingly different
title pages. Chopin and Liszt have equal status on one of them
(‘OEUVRES DE PIANO.<b>½</b>‌FRANCOIS LISZT.<b>½</b>‌FRÉDÉRIC
CHOPIN.’). A list of all of the Chopin compositions published by
Schlesinger (Lienau) appears on the STP
‘OEUVRES<b>½</b>‌DE<b>½</b>‌FRÉDÉRIC CHOPIN.’, including not only the
original versions but also copious transcriptions. The first
incarnation of this title page was in c. 1874, i.e. prior to
acquisition of the Haslinger scores, although all but one of the
latter appear on the following two versions of the STP.<a
href="#_ftn7" id="_ftnref7">[7]</a></p>

<p>Schlesinger also published separate editions of the constituent
works within the multipartite opuses on his Chopin list. The Nocturnes
Op. 32 were originally released individually and only later came out
in a single edition.<a href="#_ftn8" id="_ftnref8">[8]</a> The
opposite approach was taken in the case of the Etudes from <i>Méthode
des Méthodes</i> and Opp. 59, 67–70 &amp; 72, each of which was
initially published in a volume containing the entire opus, as against
the separate editions sold from 1871.<a href="#_ftn9"
id="_ftnref9">[9]</a> As for the Songs Op. 74, these were produced
both separately and in a single volume from the start, likewise the
Polish first edition published by Gebethner, for which Schlesinger’s
firm prepared the plates (see ‘Poland’ under ‘Chopin’s
publishers’).</p>

<p>Colour was used by Schlesinger for only one ITP (see 32/1–1b-Sam)
in addition to the title pages and wrappers of the albums containing
the Nocturnes Op. 32 (32/1–1-Sam, 32–1a-Sam, 32/2–1-Sam). Lithographic
transfer was regularly employed for the reprints published from 1865
onwards.</p>

<p>Versions 2 &amp; 3 of the STP ‘OEUVRES<b>½‌</b>DE<b>½‌</b>FRÉDÉRIC
CHOPIN.’ as well as Schlesinger’s 1890 catalogue (held by the
Bayerische Staatsbibliothek in Munich) confirm that reprints of the
Variations on a German National Air were published after 1874,
although no copies thereof have been located. The 1890 catalogue also
reveals that after 1879 Lienau continued to market all of the Chopin
first editions originally released by Schlesinger and Haslinger.<a
href="#_ftn10" id="_ftnref10">[10]</a> A number of these might have
been commercially available even after the turn of the century.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> Nevertheless, in a letter to his family of 16 September 1828 (KFC 1955:
i/82), Chopin wrote: ‘I would have preferred to spend the morning at
Schlesinger’s [shop] rather than stroll through the thirteen rooms of the
zoological exhibition. The exhibition is of course a delight, but the
music-shop I’ve referred to would have been of greater use to me.’ The regret
expressed here leads one to surmise that before leaving Berlin Chopin may not
have seen Schlesinger. (All translations are ours unless otherwise indicated.)</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> Reprints of the edition of Op. 59 acquired from Peters bear a new plate
number, S. 6071, whereas those of the editions from the Haslinger list – Opp. 2
&amp; 4, <i>Hexameron</i> and (probably) the Variations on a German National Air – preserve their
original plate numbers. Lienau also retained the original name of the firm, adding his own alongside it in round
brackets; thus the TPs of the editions acquired from Haslinger refer to
Schlesinger even though he himself had no role in their publication.</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a> Previously, in 1834, Schlesinger had taken the initiative without consulting
Chopin to assign an opus number (i.e. ‘Op. 15’) to the <i>Grand Duo Concertant </i>(see GDC–1a-Sam). In the 1846 catalogue cited in note 52 the Etudes from
<i>Méthode
des Méthodes</i> are designated as Op. 32a.</p>
</div>

<div id="ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref4" id="_ftn4" name="_ftn4">[4]</a> See Posth–1-Sam (half-titles of Op. 70 and Op. 71 No. 1) and also the
wrappers of the later reprints classified
under 70–1b-Sam (D-Bds copy),
71/1–1a-Sam and 71/1–2-Sam (US-Wc copy). Note that the TPs of several other
editions produced in Germany also refer to registration at Stationers’ Hall
(see 74–1-G, 74–1-Sam, MEG–1-B&amp;B, MazC–1-SCH, PolG-–1-SCH,
PolG#m–1-SCH, WaltzEm–1d-SCH and their consecutive reprints),
despite which it appears that copies of these were never actually deposited, in
that none of the exemplars held by the British Library was obtained through
legal deposit (indeed, all were acquired at a much later date).</p>
</div>

<div id="ftn5">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref5" id="_ftn5" name="_ftn5">[5]</a> These two volumes of Op. 74, produced in octavo format, were part of a
larger-scale repackaging of various Schlesinger editions. Note for example the
three volumes published in 11–12/1872 (MlM): Opp. 67–70 (plate number S. 6666);
Opp. 1, 71 &amp; 73, and Op. 74 No. 17 (for solo piano; plate number S. 6667);
and Opp. 32 &amp; 66, Funeral March Op. 72, Etudes from <i>Méthode des Méthodes</i> (plate number S. 6668); similarly the new versions of Op. 74 with Polish
and English texts which were released in March 1880 (MlM), once again in octavo
format.</p>
</div>

<div id="ftn6">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref6" id="_ftn6" name="_ftn6">[6]</a>
This inventive ‘correction’ was taken up in later reprints of the English
edition (see 32/1–1h-W, 32–1i-A&amp;P, 32/1–1j-A&amp;P).</p>
</div>

<div id="ftn7">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref7" id="_ftn7" name="_ftn7">[7]</a> <i>Hexameron</i> was omitted. For further
information about the Schlesinger STPs see Appendix I.</p>
</div>

<div id="ftn8">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref8" id="_ftn8" name="_ftn8">[8]</a> The price of the volume is already present on the TPs of 32/1–1e-Sam
and 32/2–1b-Sam, although no copies have been located of the entire opus
comprising the first editions of each
nocturne. The oldest complete set catalogued here contains their respective
second editions (see 32–1-Sam, 32–1a-Sam); 32–2-Sam is based on their third
editions, while 32–3-Sam combines the fourth engraving of No. 1 and the third
of No. 2. Each of these versions forms a rather eclectic whole in terms of the
CTs and pagination.</p>
</div>

<div id="ftn9">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref9" id="_ftn9" name="_ftn9">[9]</a>
In August 1871 MlM announced the publication in separate editions of Opp. 67–70
&amp; 72.</p>
</div>

<div id="ftn10">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref10" id="_ftn10" name="_ftn10">[10]</a> In the early 1880s Schlesinger (Lienau) released another edition of
Chopin’s music, in 13 volumes: <i>Friedrich Chopin’s Werke. Instructive Ausgabe mit erlauternden
Anmerkungen und Fingersatz von Dr. Theodor KULLAK</i>.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300020005',
            'show_in_menus': True,
            'slug': 'am-schlesinger',
            'title': 'AM Schlesinger'
        }
    },
    'background_publishers_germany_bh': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Founded in 1719 and still commercially active, Breitkopf &amp;
Härtel<a href="#_ftn1" id="_ftnref1">[1]</a> produced an especially
large number of Chopin first editions which pose greater challenges of
description and chronological classification than those of any other
firm.  B&amp;H’s Chopin output has three principal features: numerous
new engravings, ongoing refinement of the music text (often over
extended periods), and frequent revision or replacement of title
pages.</p>

<p>Tables 1 &amp; 2 provide an overview of those compositions for
which multiple editions were published, in addition to those whose
music text changed over time. Further relevant information concerns
the large number of editions published with different title pages –
namely Op. 34 (five versions) and Opp. 18, 25, 29, 57 &amp; 64 (three
versions) – as well as those brought out with a single title page and
engraved only once (Opp. 12, 16, 20, 35, 39, 46–49, 52, 54, 55, 56,
60, 61).<a href="#_ftn2" id="_ftnref2">[2]</a></p>

<p>Like Kistner, Breitkopf &amp; Härtel released various new editions
with revised plate numbers. The first was the Funeral March from
Op. 35, published in 1853 with plate number 8728. Four more editions
of this type appeared in 1858 – Op. 18 (plate number 9618), Op.  31
(9671), Op. 34 No. 1 (9620) and Op. 64 No. 1 (9619) – while two
further ones date from 1861: Op. 64 No. 2, with plate number ‘10097
(7716)’, and Op. 64 No.  3, with plate number ‘10098 (7717)’.<a
href="#_ftn3" id="_ftnref3">[3]</a> It is difficult to date two other
re-engraved editions because their plate numbers are anomalous: Op. 25
(Book 1 – plate number 961; Book 2 – no plate number) and Op.  55
(362).<a href="#_ftn4" id="_ftnref4">[4]</a> Oddly, their title pages
were respectively based on either 25/1-6–1e-B&amp;H or
25/1-6–1f-B&amp;H and 55–1-B&amp;H, on which the original plate
numbers appear.</p>

<p>Breitkopf &amp; Härtel also brought out three collections of
Chopin’s music organised by genre – mazurkas, nocturnes and polonaises
– which were based on previous editions of individual opuses although
each piece within the collections was separately published with the
relevant STP (see Appendix I).<a href="#_ftn5" id="_ftnref5">[5]</a>
The Mazurkas appeared in August 1863 and the Nocturnes three months
later, while the Polonaises were published in February 1864. They
remained on the market for about fifteen years, during which similar
changes were made to their respective title pages (see the
descriptions in Appendix I) as well as their pagination, which in
several reprints was modified in favour of individual pagination for
every work.<a href="#_ftn6" id="_ftnref6">[6]</a></p>

<p>Select Chopin pieces featured in five other collections issued by
Breitkopf &amp; Härtel. From 1841 to the late 1870s, Op. 25 belonged
to a series that also included separate editions of studies by Henselt
and Thalberg (e.g. 25/1-6(sep)–1c-B&amp;H) and, eventually, Liszt’s
<i>Etudes d’exécution transcendante</i>
(e.g. 25/1-6(sep)–2e-B&amp;H). The collection of <i>Perles
Musicales</i><a href="#_ftn7" id="_ftnref7">[7]</a> that was launched
in early 1865 united smaller-scale works intended for performance in
either the concert hall or more domestic settings; it contained five
Preludes from Op. 28, namely Nos. 13 &amp; 15 (released in October
1865; see 28/15–1n-B&amp;H)<a href="#_ftn8" id="_ftnref8">[8]</a> and
Nos. 6, 8 &amp; 11 (from February 1867).<a href="#_ftn9"
id="_ftnref9">[9]</a> A similar collection was published for cello and
piano with the name <i>Lyrische Stucke</i>; among other pieces, it
included the third movement of Chopin’s Sonata Op. 65 and a
transcription of the Prelude Op. 28 No. 15 (see 65/3–1e-B&amp;H). A
version of the Sonata Op. 65 for violin and piano was also released in
<i>Breitkopf &amp; Härtel’s Violin-Bibliothek</i> (see
65–1f-B&amp;H). The fifth such collection containing reprints of
Chopin first editions was the series released between 1866 and 1869
under the title <i>Classische und moderne Pianoforte-Musik</i>, which
comprised six volumes of various composers’ music.<a href="#_ftn10"
id="_ftnref10">[10]</a></p>

<p>In contrast to the other collections described here, the original
plate numbers were not retained in this series: in order to underscore
the integrity of the respective volumes, the publisher assigned a new
plate number to each one, corresponding to the date of
publication.</p>

<p>The original wrappers of an unusually large number of Breitkopf
&amp; Härtel Chopin editions have survived, and their content
facilitates the dating of the relevant scores while also revealing an
evolution in the wrappers themselves. Three principal stages can be
discerned. From 1833 to the mid-1850s, the wrappers reproduced either
the TP or the half-title.<a href="#_ftn11" id="_ftnref11">[11]</a>
During the ten years from c. 1855 to the middle of 1865, the wrappers
of the ballades, impromptus, mazurkas, nocturnes, polonaises and
waltzes featured a STP or CTP listing the Breitkopf &amp; Härtel
editions of these genres. Finally, between 1865 and 1879, a different
STP with the heading ‘OEUVRES DE
PIANO<b>½</b>‌DE<b>½</b>‌FRÉD. CHOPIN’ was regularly used;
seven variants exist,<a href="#_ftn12" id="_ftnref12">[12]</a> each
listing the publisher’s entire Chopin catalogue. The presence or
absence of Breitkopf &amp; Härtel’s oval logo needs to be considered
when identifying individual Chopin scores. For example, numerous
copies detailed in this catalogue feature a printed B&amp;H ‘stamp’
centred at the bottom of the TP; in this respect such stamps differ
from ordinary ones applied by hand, which rarely are centred even
though most are similarly located at the bottom of the TP.<a
href="#_ftn13" id="_ftnref13">[13]</a> The fact that the printed logo
appears only on the TP of impressions released from c. 1865 makes it
possible to date given scores more or less precisely on the basis of
this symbol alone.<a href="#_ftn14" id="_ftnref14">[14]</a></p>

<p>The relative quality of Breitkopf &amp; Härtel’s Chopin output can
be attributed in large part to the firm’s house editors and
professional correctors, most of whom have never been identified.
Nevertheless, despite their musical knowledge and vigilance, numerous
engraving errors can be found in the earliest impressions and many
subsequent ones as well; moreover, it is astonishing to discover a few
passages where the correct music text was unnecessarily and wrongly
modified (e.g. 25/1-6–1g-B&amp;H, 53–1a-B&amp;H, 53–1b-B&amp;H).<a
href="#_ftn15" id="_ftnref15">[15]</a></p>

<p>Detailed information about the preparation of certain B&amp;H
editions can be gleaned from sources such as Clara Schumann’s
correspondence, which describes the preparation and in particular her
participation in the correction of Opp. 60, 61 &amp; 63–65 (probably
also Op. 62).<a href="#_ftn16" id="_ftnref16">[16]</a> Her letters<a
href="#_ftn17" id="_ftnref17">[17]</a> also reveal the important fact
that between 1866 and 1867, at the request of Hermann Härtel, she
undertook a large-scale review of all of the firm’s Chopin output,
using contemporary B&amp;H first-edition reprints as the basis of the
exercise. The extent of her editorial emendations was such that the
publisher incorporated them not only in the new series for which
Clara’s assistance had been commissioned in the first place,<a
href="#_ftn18" id="_ftnref18">[18]</a> but also in later impressions
of the editions that she had used in the course of her work. This can
be seen in the case of numerous editions brought out in the late
1860s.<a href="#_ftn19" id="_ftnref19">[19]</a></p>

<p>Attention also needs to be drawn to two other late reprints of
Breitkopf &amp; Härtel’s Chopin editions. Between 1873 and 1875, the
latter were regrouped into eight volumes, each of which contained a
plate number corresponding to its publication date.<a href="#_ftn20"
id="_ftnref20">[20]</a> In addition there are corrected reprints of
the Sonata Op. 65 (original scoring and version for piano and violin)
with plate numbers from the late nineteenth-century
<i>Volksausgabe</i> series;<a href="#_ftn21" id="_ftnref21">[21]</a>
these constitute the only B&amp;H first edition still marketed after
1879.</p>

<p>None of the Breitkopf &amp; Härtel Chopin editions listed in this
catalogue features a title page in colour. Two albums published by the
firm include works by Chopin (see 23–2-B&amp;H,
33/1&amp;2–1a-B&amp;H). Lithographic transfer was used for the vast
majority of the B&amp;H Chopin scores released after 1860, although
printing from engraved plates was not completely abandoned: a few late
reprints were prepared in this way, among them 22–2b-B&amp;H,
25/7-12(sep)–2g-B&amp;H and 28–1l-B&amp;H.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> Lenneberg 1990 contains invaluable information not only about the
negotiations between Chopin and Breitkopf &amp; Härtel but also concerning the
transmission of manuscripts and French proofsheets to Leipzig.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a>
The point applies to Op. 35 as a whole but not to the separate editions of the
Funeral March.</p>
</div>

<div id="ftn3" style="mso-element:footnote">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref3" id="_ftn3" name="_ftn3" style="mso-footnote-id:ftn3">[3]</a> Successive corrections were also made to these editions, one of which –
the Funeral March – was re-engraved twice. Copies are relatively abundant and
can be found in numerous libraries.</p>
</div>

<div id="ftn4">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref4" id="_ftn4" name="_ftn4">[4]</a>
Copies can be found at GB-Lbl (Op. 25 – h. 473.b.(5.); Op. 55 – h.471.r.(7.)).
These editions probably came out in the late 1850s.</p>
</div>

<div id="ftn5">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref5" id="_ftn5" name="_ftn5">[5]</a> Chopin’s name and the opus number were added above the first system of the music text so that each
piece could be sold separately. The fact that these caption titles also appear
in reprinted editions of complete opuses outside the series provides a useful
tool in dating the later impressions thereof, in that any score with these two
elements necessarily appeared after
1863. However, in the later reprints of Opp. 41, 48 &amp; 63 – likewise in 26–3h-B&amp;H,
37–1h-B&amp;H and 55–1e-B&amp;H – caption titles of this type can be found only
in the first piece within each opus
and not in the subsequent works. This suggests that such elements were
introduced during an advanced stage of lithographic transfer, and specifically for the series of separate editions
described above.</p>
</div>

<div id="ftn6">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref6" id="_ftn6" name="_ftn6">[6]</a>
See 15–2g-B&amp;H, 15–2i-B&amp;H, 17–2g-B&amp;H, 27–1h-B&amp;H, 27–1j-B&amp;H,
33–2b-B&amp;H, 33–2e-B&amp;H and 55–1d-B&amp;H.</p>
</div>

<div id="ftn7">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref7" id="_ftn7" name="_ftn7">[7]</a> The STP of this collection existed in at least four versions: the first – as yet unlocated – appeared within
the 1865 edition and probably comprised some thirty-five items; the second, from 1867, is described in note 114; for
the third, from 1874, see 28/15–1n-B&amp;H; and the fourth, which featured
ninety-five items, is reproduced as
plate 46 in Chomiński and Turło 1990. The catalogue extract ‘Verlag von
Breitkopf &amp; Härtel in Leipzig.<b style="mso-bidi-font-weight:normal">½</b>‌PERLES MUSICALES’ indicates that this collection was also available as a
volume containing the first fifty
pieces.</p>
</div>

<div id="ftn8">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref8" id="_ftn8" name="_ftn8">[8]</a> See the advertisement in AmZ No. 40 (4 October 1865). To date no copies
of the first impressions of these two
preludes have been located. The impression classed under 28/15–1n-B&amp;H dates
from c. 1874 and was produced using the original plates, likewise the print of
Op. 28 No. 13.</p>
</div>

<div id="ftn9">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref9" id="_ftn9" name="_ftn9">[9]</a> See MlM, February 1867, p. 22. A copy of the Preludes Op. 28 Nos. 6
&amp; 11 with the same STP (on which sixty-one pieces are listed) and with
common plate number 11275 is held by GB-Eu (shelfmark D 6114). No. 6 was
printed from the original plate, whereas a new engraving was prepared in the
case of No. 11. As for Op. 28 No. 8, which was published at the same time, this
too had to be newly engraved because the original page layout was unsuitable
for separate publication; its plate number would have followed consecutively
from the one for Nos. 6 &amp; 11.</p>
</div>

<div id="ftn10">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref10" id="_ftn10" name="_ftn10">[10]</a> The Chopin works included Op. 16 (vol. 1), Op. 25 No. 1 (vol. 2), Op.
33 No. 2 and Op. 17 No. 1 (vol. 5), and Op. 63 No. 1 and Op. 57 (vol. 6). Their
publication was announced as follows: vol. 1 – AmZ No. 7 (21 February 1866);
vols. 2 &amp; 3 – AmZ No. 41 (12 October 1866); and vol. 5 – AmZ No. 26 (26
June 1867). Judging from its plate number – 11579 – the sixth volume,
containing a partial reprint of 63–2c-B&amp;H and 57–2f-B&amp;H, dated from
1869.</p>
</div>

<div id="ftn11">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref11" id="_ftn11" name="_ftn11">[11]</a>
See ‘Wrappers and covers’, note 6, under ‘General characteristics
of Chopin’s first editions’.</p>
</div>

<div id="ftn12">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref12" id="_ftn12" name="_ftn12">[12]</a>
The variants are described in Appendix I.</p>
</div>

<div id="ftn13">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref13" id="_ftn13" name="_ftn13">[13]</a> At least thirteen different
B&amp;H stamps have been identified;
for details see Platzman 2003: 303–304. The stamp that corresponds to the logo
is referred to by Platzman as ‘BH/I’. Note that in the first edition of his catalogue, Platzman (1997) distinguished
between the logo and other stamps. The logo is also present on the front pages
of certain wrappers, and notably on the following STPs: versions 3 &amp; 4 of ‘MAZURKAS<b style="mso-bidi-font-weight:
normal">½</b>‌FÜR DAS PIANOFORTE<b>½</b>VON<b>½</b>‌FR.
CHOPIN.’, ‘NOTTURNOS<b>½</b>‌FÜR DAS PIANOFORTE<b>½</b>‌VON<b>½</b>‌FR. CHOPIN.’ and ‘POLONAISES<b>½</b>‌FÜR DAS PIANOFORTE<b>½</b>‌VON<b>½</b>‌FR.
CHOPIN.’; version 2 of ‘CHOPIN, HENSELT, LISZT, THALBERG.<b>½</b>‌ETÜDEN<b>½</b>‌FÜR<b>½</b>‌DAS
PIANOFORTE.’; and versions 2–4, 6
&amp; 7 of ‘OEUVRES DE PIANO<b>½</b>‌DE<b>½</b>‌FRÉD. CHOPIN.’. For details see
Appendix I.</p>
</div>

<div id="ftn14">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref14" id="_ftn14" name="_ftn14">[14]</a> The logo was not added systematically: it appears on none of the copies
of Opp. 12, 16, 23, 30, 38, 39, 41, 42, 49, 52, 54, 56 &amp; 58 catalogued in this volume, nor on
the ITPs of Opp. 17, 22 &amp; 33. In the case of Op. 25, it can be found on
only three reprints: 25/7-12–2a-B&amp;H, 25/1-6(sep)–2h-B&amp;H and 25/7-12(sep)–2g-B&amp;H.</p>
</div>

<div id="ftn15">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref15" id="_ftn15" name="_ftn15">[15]</a> Engraving errors that remained at later publication stages include
those in the first edition of the
Funeral March from Op. 35 (see 35/3–1a-B&amp;H), which reappear in the second
edition (see 35/3–1b-B&amp;H) as well as the third (with plate number 8728).
Only in the fourth edition (the plate number of which is identical to the third
edition’s) were the errors in question eliminated. Similarly, several errors
within the original print of the Waltz Op. 34 No. 1 (34/1–1-B&amp;H) were
reproduced in both the second edition (34/1–2-B&amp;H) and the third edition
(plate number 9620). It was not until the late 1860s that these were corrected. The
erroneous modifications within Op. 53
appear to have resulted from the re-engraving of two minuscule bits of text
located at the edge of the plates, i.e. where distortion or fissures are more likely to occur. In
53–1a-B&amp;H, having repaired the damaged plate as required, the engraver
re-engraved the last RH note in b. 96, accidentally transposing it by a third.
(The slur at the end of this bar was largely effaced
at the same time.) Similarly, in 53–1b-B&amp;H, a superfluous note was added in the last two LH chords in b. 61. As for
Op. 25 No. 6, it is impossible to determine what motivated the intervention in
question.</p>
</div>

<div id="ftn16">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref16" id="_ftn16" name="_ftn16">[16]</a> See the letters of 9 October 1846, 27 October 1846, 31 October 1846, 14
September 1847, 22 September 1847, 9 October 1847 and 28 November 1847 in
Steegmann 1997. According to the letter of 14 September 1847, Robert Schumann
helped to revise the Op. 63 proofs.</p>
</div>

<div id="ftn17">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref17" id="_ftn17" name="_ftn17">[17]</a> See the letters of 4 October 1866, 8 January 1867 and 28 August 1867 in
Steegmann 1997. In the second of these, Clara asked for her name not to appear
on the TPs of this edition.</p>
</div>

<div id="ftn18">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref18" id="_ftn18" name="_ftn18">[18]</a> This series consisted of eight volumes in octavo format: Waltzes (plate
number 11349); Polonaises (11460); Nocturnes (11477); Mazurkas (11485);
Ballades, Berceuse, Barcarolle (11625); Preludes, Scherzos, Impromptus (11638);
Sonatas, Opp. 12, 16, 46, 49 (11652); Etudes Op. 25 (12281). These were
respectively published in 8/1867, 1/1868, 5/1868, 7/1868, 11/1868, 12/1868,
1/1869 and 12/1870 (MlM).</p>
</div>

<div id="ftn19">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref19" id="_ftn19" name="_ftn19">[19]</a> On the whole Clara Schumann’s work resulted in major improvements to
Breitkopf &amp; Härtel’s Chopin editions. To her may also be attributed the
introduction of an authentic variant in Op. 34 No. 2 (see 34/2–3c-B&amp;H) as
well as the restoration of the original text in Op. 64 No. 3 (see 64–2b-B&amp;H). But it is also likely that she
was responsible for the (incorrect)
standardisation of the rhythm in Op. 28 No. 1 and for erroneous changes to both
Op. 28 No. 23 (see 28–1h-B&amp;H) and Op. 15 No. 3 (see 15–2d-B&amp;H). The mistake in Op. 28 No. 23 was quickly rectified, however (see 28–1i-B&amp;H).</p>
</div>

<div id="ftn20">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref20" id="_ftn20" name="_ftn20">[20]</a> Waltzes (plate number 13177, published 4/1873); Polonaises (13358,
published 10/1873); Nocturnes (13359, published 11/1873); Mazurkas (13360,
published 12/1873); Preludes, Scherzos, Impromptus (13740, published 11/1874);
Ballades, Berceuse, Barcarolle, Bolero (13757, published 11/1874); Sonatas,
Opp. 12, 16, 46, 49 (13741, published 2/1875); Etudes Op. 25 (published 9/1875
with unknown plate number – i.e. no copy has been located). These volumes
contain reprints of altogether new editions of Op. 18, Op. 31 and Op. 34 No. 1.
A comment printed on the bottom of the first
page of Op. 19 confirms that Breitkopf
&amp; Härtel had obtained permission from Peters to publish it. Note that Op.
33 No. 4, Op. 38, Op. 40 No. 1, Op. 48 No. 1, Op. 52, Op. 54 and Op. 56 No. 3
were partially re-engraved in order to improve the
layout. For example, the rather dense music text on the first page of 38–2a-B&amp;H was spread over two pages in the new
volume, whereas the first three pages
of 54–1c-B&amp;H were confined to only
two pages in the latter.</p>
</div>

<div id="ftn21">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref21" id="_ftn21" name="_ftn21">[21]</a> The plate number of the reprint of 65–1f-B&amp;H (for piano and violin)
is V.A. 1200 (copies available at D-Bds: DMS 19447 (1, 2), GB-En: Mus.Box.
423.11. and GB-Lbl: g.553.aa.(7.)), as against V.A. 1201 for the piano/cello
version (copies available at D-Bds: DMS 14446 (1, 2) and F-Prt: TV. 864). The <i>Lyrische Stücke</i> series was also reprinted in a volume with plate number V.A. 378 (copy
available at D-Dl: Mus 2<sup>o</sup> 7421).</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300020006',
            'show_in_menus': True,
            'slug': 'bh',
            'title': 'B&H'
        }
    },
    'background_publishers_germany_hofmeister': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Hofmeister’s name appears twice in Chopin’s correspondence: in
1831 the composer’s sister Ludwika informed him that the Leipzig
publisher wished to market the editions belonging to G. Sennewald
(Brzezina’s successor),<a href="#_ftn1" id="_ftnref1">[1]</a> and some
eleven years later Chopin wrote to Breitkopf &amp; Härtel explaining
why he had sold a work to one of the latter’s chief rivals.<a
href="#_ftn2" id="_ftnref2">[2]</a> Hofmeister published Opp.  1, 5
&amp; 51. Classifying the editions of the first two opuses is not
straightforward in that their title pages give pride of place to the
Polish publisher, thus creating confusion as to which one brought out
the piece in question.<a href="#_ftn3" id="_ftnref3">[3]</a> In fact,
an unusual arrangement may have been made between the two firms which
Chopin presumably would have approved. It is possible that Hofmeister
prepared his editions on the basis of scores sent to him from Warsaw;
in exchange for the rights, and without further payment, Sennewald
accordingly would have been able to bring out newly engraved and
corrected publications replacing the poorly lithographed, highly
flawed earlier editions.</p>

<p>The evolution of the music text in Hofmeister’s editions is also
noteworthy. Alongside the usual corrections (of which Op. 1 offers a
good example), a much less common process of revision can be observed
in the case of Op. 5 whereby the plates were gradually renewed in
successive impressions (see 5–1a-HO, 5–1b-HO, 5–1c-HO, 5–1d-HO,
5–1e-HO, 5–1g-HO) or partially reengraved (see 5–1h-HO). In 1877–78,
Hofmeister also published a new edition, revised by Zschocher, of all
of the Chopin works in his possession; these preserved the original
plate numbers but were released as part of the collection <i>Altes und
Neues</i>.</p>

<p>None of Hofmeister’s Chopin editions uses colour. All of the later
impressions were prepared by means of lithographic transfer; the
defects resulting from this technique (for example in 51–1b-HO) are
described under ‘Printing methods’.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a>
See the letter of 27 November 1831 in KFC 1955: i/195.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a> See the letter of 15 December 1842 in KFC 1955: ii/356. The rather
formal way in which Chopin cites Hofmeister’s name suggests that they were not
personally acquainted. Hofmeister obtained Op. 51 through the intercession of
his Paris agent Leopold Louis Sina, who, in a letter dated 4 January 1841 (see
KFC 1955: ii/335), insisted on meeting Chopin to discuss works in progress
which he clearly wished to acquire for his Leipzig employer. (For further
information about Sina’s activity in Paris, see Probst’s letter to Breitkopf
&amp; Härtel of 10 March 1838 in Lenneberg 1990: 37.)</p>
</div>

<div id="ftn3">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref3" id="_ftn3" name="_ftn3">[3]</a>
Tomaszewski (1992a: 170, 186) classifies
these as Polish editions.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300020007',
            'show_in_menus': True,
            'slug': 'hofmeister',
            'title': 'Hofmeister'
        }
    },
    'background_publishers_germany_schuberth': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>A vast amount of source material exists for the one Chopin
edition brought out by this publisher – the Tarantella Op. 43.<a
href="#_ftn1" id="_ftnref1">[1]</a> Two different engravings were
produced, and each was revised several times. A review published in
the AmZ of 9 February 1842 referred to a number of errors and thus
inspired the first phase of correction (see 43–1a-SCHU). Further
improvements to the first edition were effected by Schuberth in three
subsequent stages, the last of which was carried out by an editor
whose name appears on the TP (see 43–1g- SCHU). Still dissatisfied,
Schuberth then enlisted the aid of Hans von Bulow,<a href="#_ftn2"
id="_ftnref2">[2]</a> who corrected a late impression of the second
edition (see 43–2b-SCHU).</p>

<p>The title pages of both editions of the Tarantella changed
considerably over time. Of the four versions that have been
identified, three experienced multiple transformations which are fully
detailed under the relevant catalogue entries.  Colour was used for
one version. Another more original feature is the decorative border
surrounding the music text. Lithographic transfer was used for later
reprints of the first edition and for the full range of second-edition
impressions. All of the reprints after 43–1d-SCHU contain an
unauthorised addition attributable to Schuberth, i.e. the name of an
inauthentic dedicatee.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> Frequent reference is made to this composition in the 1841
correspondence, most notably in Chopin’s letter to Schuberth of 29 July 1841
(KFC 1955: ii/340), in which he requested the correction of two mistakes made
by the copyist of his manuscript.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a>
Von Bulow also prepared other Chopin editions, notably the volumes of
impromptus and etudes published by J. Aibl during the 1880s.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300020008',
            'show_in_menus': True,
            'slug': 'schuberth',
            'title': 'Schuberth'
        }
    },
    'background_publishers_england': {
        'class': IndexPage,
        'kwargs': {
            'depth': 7,
            'introduction': u'''<p>Compared with their French and German counterparts, relatively
few English first editions have survived to the present day. Whether
this is the result of low demand within the local market,<a
href="#_ftn1">[1]</a>
limited distribution at home and abroad, and/or other factors is
difficult to say. The English scores were even less widely
disseminated on the continent than in England itself, and the fact
that they made little headway in Europe after Chopin’s works entered
the public domain may explain why so few copies are now held by
continental and American libraries<a href="#_ftn2">[2]</a> and why the most
significant collections of English prints are located in their country
of origin.</p>

<p><a id="12" liktype="document">Table 12 Chopin’s English publishers</a></p>

<p>As Table 12 reveals, multiple English editions of several works
appeared on the market; in the case of Op. 63 No. 1 and Op. 64, this
had to do with the factors discussed under ‘Legal contexts’. The
<i>Deux Valses Mélancoliques</i> also came out in multiple editions
published by Wessel and less than a year later by Ewer. Both were
based on the somewhat earlier edition released in Cracow by Wildt,
which did not benefit from copyright protection in England. The
circumstances surrounding the Fantasy-Impromptu Op. 66 were more
remarkable: at least four<a href="#_ftn3">[3]</a> London publishers
rushed to bring out this composition despite the fact that they were
in clear breach of copyright.<a href="#_ftn4">[4]</a></p>

<p><a id="13" linktype="document">Table 13 Changes in ownership,
acquisitions and reprints: Chopin’s English publishers</a></p>

<p>Although this section focuses primarily on normal patterns of
succession, reference should also be made to known first-edition
reprints released by other firms. (See Table 13.) Details of four such
works preserving their original plate numbers are provided in the
catalogue (see 64/1–1b-CHAP, 64/1–1c-CHAP, 64/2–1a-CHAP,
66–1a-CR). Another edition of this type which lacks a plate number – a
reprint of Chappell’s edition of the Etudes from <i>Méthode des
Méthodes</i> – was released by Jullien &amp; Co. in the series
<i>MACFARREN’S Universal Library of Piano Forte Music</i>.<a
href="#_ftn5">[5]</a></p>

<hr align="left" size="1" width="33%"/>

<p id="ftn1" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref1" name="_ftn1">[1]</a> Notwithstanding the
difficulty and stylistic novelty of Chopin’s music, the following
remark of Liszt’s probably overstates the case: ‘On the subject of
Publisher, Wessel, who has brought out the collection of Chopin’s
works and lost more than 200 Louis from it, came to ask me to play
some of his pieces in order to make them known here. As yet no one has
dared risk it... I will play his Etudes, Mazurkas and Nocturnes – all
of which are virtually unknown in London. That will encourage Wessel
to buy other manuscripts from him. The poor Publisher is a bit tired
of publishing without selling.’ (Letter of 29 May 1840; see original
French text in Franz Liszt and Marie d’Agoult, <i>Correspondance</i>,
ed. Serge Gut and Jacqueline Bellas (Paris: Fayard, 2001),
p. 609.)</p>

<p id="ftn2" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref2" name="_ftn2">[2]</a> The Chopin first
editions in these institutions largely come from private
collections. Particularly significant Chopin collectors have included
Anthony van Hoboken, Arthur Hedley, Alan Tyson, James Fuld and George
W. Platzman, whose individual efforts spawned greater general
knowledge of these important sources.</p>

<p id="ftn3" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref3" name="_ftn3">[3]</a> I.e. Ewer, Ashdown
&amp; Parry, Lamborn Cock, and Cramer. Other editions from the period
not catalogued in this volume were published by Robert Cocks in 1866
(No. 6 of H. B. Richards’ <i>The Pianist’s Library</i>; GB-Lbl:
h.1392.(1.)), by Chappell in 1869 (Charles Halle’s edition; GB-Lbl:
h.474.(29.)) and by Hutchings &amp; Romer in 1871 (No. 34 of A.
Gilbert’s <i>Classics of the Pianoforte</i>; GB-Lbl: h.1340.a.).</p>

<p id="_ftn4" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref4" name="_ftn4">[4]</a> A. M. Schlesinger
possessed the rights in England thanks to the 1846 treaty discussed in
‘The German States’ under ‘Legal contexts’ and in ‘Publications of
A. M. Schlesinger and successor (Robert Lienau)’ under ‘Chopin’s
publishers’. The score of the Posthumous Works catalogued here under
Posth–1-Sam was in fact the deposit copy that Schlesinger registered
at Stationers’ Hall.</p>

<p id="ftn5" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref5" name="_ftn5">[5]</a> Copy available at
GB-Lbl with shelfmark h.1420.(5.).</p>''',
            'numchild': 2,
            'path': '0001000100010002000200030003',
            'show_in_menus': True,
            'slug': 'england',
            'title': 'England'
        }
    },
    'background_publishers_england_dating': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>The English Chopin editions pose certain difficulties because
the registration dates at Stationers’ Hall frequently do not coincide
with actual publication dates for the reasons discussed earlier. It is
therefore essential to compare registration dates with those from the
musical press and as inscribed on individual scores at the time of
deposit in the British Museum. Inferences about publication dates
based solely on the registers of the Stationers’ Hall tend to lack
historical validity and to oversimplify the chronology of the English
publications adumbrated in Tables 14 &amp; 15.</p>

<p>All but two of the dates from the musical press in Table 14 come
from respective first publication announcements<a href="#_ftn1"
id="_ftnref1">[1]</a> in <i>The Musical World</i>; given the relative
dearth of other sources prior to 1836,<a href="#_ftn2"
id="_ftnref2">[2]</a> the exceptions are the date proposed for Op. 11,
which appears in a review published in <i>The Musical Magazine</i>,
and that for Op. 15, taken from <i>The New Music Magazine</i>. Where
lacunae occur in the Stationers’ Hall registers, the British Museum
(i.e. British Library) collection or the musical press, recourse has
been made to the dates in Brown (1960, 1972)<a href="#_ftn3"
id="_ftnref3">[3]</a> and Chomiński and Turło (1990). Commentary is
provided in the main body of the catalogue about several especially
problematic dates (see, e.g., 1–1-W, 5–1-W, 28/1-14–1-W).</p>

<p><a id="14" linktype="document">Table 14 Works published in England
with opus number</a></p>

<p><a id="15" linktype="document">Table 15 Works published in England
without opus number or posthumously</a></p>

<hr align="left" size="1" width="33%"/>

<p id="ftn1" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref1" name="_ftn1">[1]</a> A handful of
acquisition advertisements appeared in <i>The Musical World </i>as
follows:</p>

<ul style="font-size: 9pt; line-height: 115%; text-align: justify">
<li>26 September 1839: Op. 28</li>

<li>27 January 1842: Opp. 44–49,
with the indication ‘In the Press’ but no sale price. Wessel thus gave notice
of the forthcoming publication of six new Chopin works of which four were
mentioned by name (Opp. 45 &amp; 48 are absent from the list).</li>

<li>11 August 1842: Op. 50, with the
indication ‘In the Press’ but no sale price</li>

<li>1 August 1846: Opp. 60–62, with the indication ‘Now Publishing’
but no sale price.</li>
</ul>

<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a
href="#_ftnref2" name="_ftn2">[2]</a> The earlier periodical referred
to by Brown, i.e. <i>The Musical Library</i> (see Brown 1972: xiii,
note 2), contains no relevant information.</p>

<p id="ftn3" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref3" name="_ftn3">[3]</a> Brown (1972)
specifies when the editions of Opp. 52–56 were first advertised –
hence the references to ‘first publication announcement’ (i.e. FPA) in
Table 14.</p>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300030001',
            'show_in_menus': True,
            'slug': 'dating-the-english-editions',
            'title': 'Dating the English editions'
        }
    },
    'background_publishers_england_wessel': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>It is likely that Chopin and his principal English publisher
first made contact in 1833, although the exact circumstances remain
obscure. The earliest record of their interaction is the date
‘Nov. 1833’ added to the sales contract for Opp. 13–17 (signed on 4
April 1836). But if the publication dates proposed by Brown for
Opp. 6–10 are correct – i.e.  June–August 1833 – Chopin and Wessel
would have been in touch by no later than April or May that year. Be
that as it may, their initial meeting took place in July 1837 during
Chopin’s first trip to England, and the second one occurred when
Wessel visited Paris in May 1845.<a href="#_ftn1"
id="_ftnref1">[1]</a> There is no evidence that they met while Chopin
was next in London (i.e. April–August and November 1848), nor is it
likely that Chopin sought an encounter then given that their relations
had been strained from late 1841 onwards.<a href="#_ftn2"
id="_ftnref2">[2]</a></p>

<p>Wessel’s Chopin output encompassed more or less the entire oeuvre
of the composer and was distinctive in a number of key respects.
First of all, a significant number of the Wessel Chopin editions were
marketed in series such as <i>Album des Pianistes de Premiere
Force</i> (Opp.  2, 11, 13, 14, 21, 22), <i>L’Amateur Pianiste</i>
(Opp. 1, 6, 7, 9, 15–20, 23, 24, 26, 27), <i>Le Pianiste Moderne</i>
(Opp. 5 &amp; 29–34, solo piano version of Op. 3), <i>Les Agremens au
Salon</i> (Opp. 35, 36, 38–41) and <i>Modern Trios</i> (Op. 8).<a
href="#_ftn3" id="_ftnref3">[3]</a> Furthermore, all of the mazurkas
up to Op. 59 were released with the subtitle <i>Souvenir(s) de
Pologne</i>, which in essence functioned as a series title. Among
other things, the creation of a complete collection of Chopin’s
nocturnes confirms that Wessel’s successors took a similar approach to
the marketing of his music (see 27/2–2-Ae, 27/1–2-Ae, 55/2–2-Ae).</p>

<p>The clearest indication of Wessel’s tendency to classify and
systematise can be seen in the launch in 1840 of the <i>Complete
Collection of the Compositions of Frederic Chopin</i>, which, as its
name suggests, was exclusively reserved for the Polish composer’s
music. Throughout its long lifespan extending over some sixty years,
the series title page experienced an extraordinary evolution whose
different stages are outlined in Appendix I. The transcriptions for
piano four hands were also packaged in different ways: initially in
two series organised by genre;<a href="#_ftn4" id="_ftnref4">[4]</a>
then, from 1840 to 1851, in the <i>Complete Collection</i> (along with
the original versions);<a href="#_ftn5" id="_ftnref5">[5]</a> and
finally in an independent collection of twenty pieces with its own
title page.<a href="#_ftn6" id="_ftnref6">[6]</a></p>

<p>The approach taken by Wessel and his successors to refining the
music text of their Chopin editions was no less distinctive. The first
such initiative was carried out by Chopin’s friend Julian Fontana, to
whom Wessel entrusted the correction of Opp. 1, 3, 5, 10 &amp; 11
(either before or after initial publication) during his stay in London
from 1834 to 1837. Fontana did not limit himself to the simple
rectification of engraving errors, however: he also added fingerings
to the editions of Opp. 10 &amp; 11. In recognition of his role Wessel
displayed Fontana’s name on the title pages of the five
editions. Editorial review of this kind was exceptional prior to
1849,<a href="#_ftn7" id="_ftnref7">[7]</a> whereas in the late 1850s
and throughout the following decade Wessel and then Ashdown &amp;
Parry undertook a wholesale revision of their Chopin output (see Table
1). The unknown person(s) in charge of this work must have held the
German first editions in high regard, given that a multitude of
readings from the scores published by Breitkopf &amp; Härtel, Kistner
and A. M. Schlesinger made their way into the corrected English
reprints.<a href="#_ftn8" id="_ftnref8">[8]</a></p>

<p>The constant presence of catalogue extracts is yet another
distinctive feature of the Wessel editions. In the French and German
first editions, this form of publicity appeared only rarely, whether
within the score or on the reverse of the last page of music text; in
the English prints, however, they regularly occupied one or both of
these positions. Many editions go so far as to advertise other Chopin
works on the TP or at the bottom of the last page of music text (see
Opp. 3, 11, 13, 16, 17). This creative use of what would otherwise be
empty space can be explained by the fact that, unlike Maurice
Schlesinger or Breitkopf &amp; Härtel, Wessel did not own a music
journal and thus lacked similar opportunities to promote his output
free of charge.</p>

<p>Most of the numerous publicity pages exist in several versions,<a
href="#_ftn9" id="_ftnref9">[9]</a> and classification of the ones
found in scores from the <i>Complete Collection</i> parallels in
virtually all cases that of the respective STP. The Prelude Op. 45 is
exceptional in this regard, because each of the four copies listed
under 45–1-W&amp;S contains version 3 of the STP as against version 2
of ‘Page E’.  Although this inconsistency challenges the
classification of the relevant STP and advertisement, it must be
remembered that Wessel’s publicity extracts at that time were produced
separately from the rest of the score and by different means:
advertisements were printed using movable type, whereas engraving was
used for the rest of an edition. Analysis of the prices of Chopin’s
music in the first two versions of Page E leads to the conclusion that
they date from the very beginning of the <i>Complete Collection</i>:
they appear only in copies containing version 1 of the STP, apart from
the four copies of Op. 45 referred to above. On the other hand,
version 3 of Page E, which certainly post-dated versions 1 &amp; 2, is
present in only one score containing the original STP of the
<i>Complete Collection</i> (i.e. 42–1-W has version 1 of the STP and
version 3 of Page E), and thereafter principally in scores containing
versions 2 &amp; 4–7 of the latter (e.g. 48/1–1-W&amp;S features
version 2 of the STP and version 3 of Page E). In the light of all
this, it seems likely that, in the production of Op. 45, the publisher
made use of a stock of paper which had been mislaid or put to one
side, and on which version 2 of Page E had previously been
printed. For there to be consistency between the four copies cited
above and the classification scheme that we have proposed, these
scores would have had to contain version 3 of Page E rather than
version 2.</p>

<p>A good many Wessel scores and some of those published by his
successors have survived in an incomplete state, i.e. without their
title pages. For reasons of economy, the bulk have been catalogued
here along with complete scores but only when the descriptive elements
of the defective copies (e.g. titles or subtitles in the header,
printed text at the bottom of relevant pages, and DMFs) correspond in
every particular to those of their complete counterparts.<a
href="#_ftn10" id="_ftnref10">[10]</a> Thanks to the advertisements
within the imperfect copies, it is generally possible to establish
their approximate publication dates and even to infer which versions
of the TP might have been present when the volume in question first
came out. Because these conclusions are speculative and cannot be
confirmed on the basis of existing evidence, they appear in Table 16
rather than within the catalogue proper.<a href="#_ftn11"
id="_ftnref11">[11]</a></p>

<p><a id="16" linktype="document">Table 16 Possible TPs and
publication dates of defective English Chopin editions as inferred
from advertisements</a></p>

<p>To date it has not been possible to locate a significant number of
Wessel’s first editions of Chopin, among them the very first
impressions of Opp. 1, 3, 6, 10 &amp; 11 and Op. 9 Nos. 1 &amp; 2. In
the case of Opp. 5, 14, 19, 21, 45, 46, 48, 50–52 &amp; 54, only the
first and last impressions have been available for cataloguing, while
for other editions – namely, Op. 34 No. 3, Mazurka from <i>La France
Musicale</i>, and Opp. 38, 42, 56, 59 &amp; 63 – the later impressions
have disappeared, likewise the edition of Op. 33 No. 3 separately
published in July 1842.<a href="#_ftn12" id="_ftnref12">[12]</a> These
lacunae may be filled one day, and only then will the particularly
rich history of the Wessel output be more fully understood.<a
href="#_ftn13" id="_ftnref13">[13]</a> </p>

<p>No usage of colour can be attributed to Wessel, who did however
employ lithographic transfer prior to 1860 when producing two reprints
(see 18–1d-W, 34/1–1f-W). The latter technique was exploited more
generally by Ashdown &amp; Parry from the late 1860s onwards.</p>

<hr align="left" size="1" width="33%"/>

<p id="ftn1" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref1" name="_ftn1">[1]</a> See MW (29 May
1845), p. 263. Wessel also travelled to the continent in 1839 (see MW,
26 September 1839, p. 346); although he stopped in Paris to meet
Chopin, the composer was at Nohant, having gone there directly upon
returning from Majorca.</p>

<p id="ftn2" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref2" name="_ftn2">[2]</a> See Chopin’s letter
to Breitkopf &amp; Härtel of 3 December 1841 in KFC 1955: ii/343.</p>

<p id="ftn3" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref3" name="_ftn3">[3]</a> For individual work
numbers see the catalogue entries for the first impressions of each
opus. The transcription for solo piano of Op. 3, which is not
catalogued here, was number 50 in <i>Le Pianiste Moderne</i>.</p>

<p id="ftn4" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref4" name="_ftn4">[4]</a> The first series
contained the Nocturnes Opp. 9, 15, 27 &amp; 32, which were brought
out with the same STP; the second combined four mazurka opuses
(Opp. 6, 7, 17, 24) and similarly utilised a single
passe-partout. Copies of Opp. 6 &amp; 9 are held by D-Dl (respective
shelfmarks Mus. 5565-T-546 and Mus. 5565-T-547).</p>

<p id="ftn5" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref5" name="_ftn5">[5]</a> See Op. 34 Nos. 1
&amp; 2 and Op. 42, which featured STP version 21 (GB-Lbl: h.472.(16.,
17., 20.)), whereas Op. 34 No. 3 was published with STP version 22
(GB-Lbl: h.472.(18.)).</p>

<p id="ftn6" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref6" name="_ftn6">[6]</a> See the GB-Lbl copy
of Op. 29 (shelfmark h.473.(9.)).</p>

<p id="ftn7" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref7" name="_ftn7">[7]</a> Ignaz Moscheles may
have participated in the correction of the English first editions of
Opp. 44–49, although at the behest not of Wessel but of Maurice
Schlesinger in an unusual arrangement brokered by the latter.  For
details see Kallberg 1996: 210–213.</p>

<p id="ftn8" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref8" name="_ftn8">[8]</a> For example, 9–1b-W,
23–1e-A&amp;P and 32/1–1h-W are three English editions containing
revisions derived from their German counterparts; refer to the
respective DMF entries for details.</p>

<p id="ftn9" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref9" name="_ftn9">[9]</a> These are described
in Appendix II.</p>

<p id="ftn10" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref10" name="_ftn10">[10]</a> Differences
within the publicity extracts have not been singled out as a criterion
for classification within this catalogue; for discussion see
‘Classification criteria’ under ‘Explaining the <i>Annotated
Catalogue</i>’.</p>

<p id="ftn11" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref11" name="_ftn11">[11]</a> The TPs of the
following defective scores would have been identical to those of the
complete scores classified under the same edition/impression codes:
17–1b-W (GB-Lbl copy), 24–1-W (US-NYp copy), 29–1c-W (GB-En copy),
30–1a-W (GB-Lbl copy), 44–1-W&amp;S (GB-Lbl copy), 53–1-W (US-NYpm
copy) and 53–1a-W (PL-Pglensk copy). This conclusion is based on the
presence of the same catalogue extracts in the respective copies. In
contrast, one cannot infer the TPs of the copies classed under
10/7-12–1d-A&amp;P (GB-Bu copy), 19–1c-W, 28/15-24–1d-A&amp;P
(PL-Wnifc copy) and 55–1-W (first GB-En copy) because these contain no
such advertisements. As for the defective copy catalogued under
32/1–2-Ae, it probably contained the first version of the STP
‘EIGHTEEN NOCTURNES<b>½</b>‌FOR THE<b>½</b>‌Pianoforte’ – an inference
that results from close comparison with the complete copies shown
under 27/2–2-Ae and 55/1–2-Ae. Finally, the defective copy of <i>Deux
Valses Mélancoliques</i>, classed under 70/2&amp;69/2–1a-W, was
published with ITP similar to that of 70/2&amp;69/2–1-W, but with
updated publisher’s address.</p>

<p id="ftn12" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref12" name="_ftn12">[12]</a> The piece was
entitled ‘Madame Oury’s favorite Mazurka’ in this edition. See MW (21
July 1842), p. 231.</p>

<p id="ftn13" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref13" name="_ftn13">[13]</a> Consider for
example the two arrangements of the Polonaise Op. 3. The one for piano
and tenor – as yet unlocated – is known only through a press
advertisement in MW (4 October 1838, p. 75), whereas the transcription
for piano and flute, prepared by Sedlatzek and published by Wessel in
1840 (see MW, 6 August 1840, p. 95), does exist but only in a later
reprint from 1856–60 (see 3–1c-W).</p>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300030002',
            'show_in_menus': True,
            'slug': 'wessel',
            'title': 'Wessel'
        }
    },
    'background_publishers_poland': {
        'class': IndexPage,
        'kwargs': {
            'depth': 7,
            'introduction': u'''<p>Although copies of the Polish first editions are extremely rare
and thus have a limited presence in this catalogue, they are
nevertheless highly significant, particularly in the case of the early
works for which no manuscript sources survive. The posthumously
published Polish editions are also of interest, given that some were
based on sources other than the ‘official’ version prepared by Julian
Fontana and brought out in Paris and Berlin. (See Tables 17 &amp;
18.)</p>

<p><a id="17" linktype="document">Table 17 Chopin’s Polish
publishers</a></p>

<p><a id="18" linktype="document">Table 18 Changes in ownership:
Chopin’s Polish publishers</a></p>

<p>Polish editions of two works have not been located: the Mazurka in
Bû major published by Kolberg (cf. MazG–1-KOL), and the Polonaise in
Gû major brought out by Kaufmann. Chopin biographies also refer to a
Military March of which no trace can be found.<a href="#_ftn1"
id="_ftnref1">[1]</a> One of relatively few compositions published in
Poland during Chopin’s lifetime – the popular Mazurka Op. 7 No. 1 –
was issued on three separate occasions by Ignacy Klukowski, in January
1835 and March 1842, and by C. A. Simon in 1837.<a
href="#_ftn2" id="_ftnref2">[2]</a></p>

<p>The editions of Gebethner, Kocipiński and Chaberski as well as
Kaufmann’s of the Polonaise in G# minor were all engraved and printed
by foreign firms.  This hybrid provenance makes it difficult to
classify Gebethner’s two impressions of the Songs Op. 74,<a
href="#_ftn3" id="_ftnref3">[3]</a> in which the publisher’s name was
removed from the TP and replaced by that of A. M. Schlesinger, which
was made more prominent into the bargain. In view of this
modification, and according to conventional music-bibliographic
practice regarding attribution, these impressions should be listed
under Schlesinger’s name; however, to avoid confusion with the
reprints of the German edition published by Schlesinger, the original
attribution is maintained within the respective edition/impression
codes (i.e. 74–1d-G, 74–1e-G). It is interesting to speculate about
the reasons behind Gebethner’s apparent disinterest in this
publication. Most likely, having taken the decision to bring out a
wholly independent edition of the Songs (released in 1879),<a
href="#_ftn4" id="_ftnref4">[4]</a> Gebethner abandoned any active
marketing of the original edition for which Schlesinger’s assistance
had been enlisted, thereby giving the latter an opportunity to
distribute the score exclusively under his own name.<a href="#_ftn5"
id="_ftnref5">[5]</a></p>

<hr align="left" size="1" width="33%"/>

<p id="ftn1" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref1" name="_ftn1">[1]</a> This supposedly was
offered by Chopin to the Grand Duke Constantine and was anonymously
published around 1820; see Kobylańska 1977: i/356–357.</p>

<p id="ftn2" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref2" name="_ftn2">[2]</a> These publications
are not catalogued in this volume. Both Klukowski editions – based on
the Kistner edition – were probably unauthorised. The 1835 score is
available at PL-Kj (shelfmark 407 III Mus.), while the 1842 one –
which contains no indication of the publisher – can be found at PL-Wp
(shelfmark Mus. Cim. 10886). As for the Simon edition (for which a
publication announcement appeared in MlM in March/April 1837), the
exemplar belonging to a private collector in Poland contains numerous
imperfections and omissions compared with the Kistner and Klukowski
editions. These flaws make it difficult to identify the relevant
<i>Stichvorlage</i>, which could be either a somewhat careless copy of
one of the earlier prints or possibly a manuscript unlikely to have
emanated from Chopin himself, the location of which is currently
unknown.</p>

<p id="ftn3" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref3" name="_ftn3">[3]</a> The same problem
arises with two other editions – namely, those of the Rondos Opp. 1
&amp; 5 which in this catalogue are classified under Hofmeister’s
name. For further discussion see ‘Publications of Hofmeister’.</p>

<p id="ftn4" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref4" name="_ftn4">[4]</a> Gebethner published
virtually all of Chopin’s music between 1863 and 1873, but in 1882 he
brought out a new Chopin edition revised by Jan Kleczyński.</p>

<p id="ftn5" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref5" name="_ftn5">[5]</a> As noted in the
preface to the German edition, A. M. Schlesinger held the worldwide
rights to this work. Although details of the agreement between
Gebethner and Schlesinger with regard to the Polish edition are not
known, it is clear that the proofs of this edition were corrected in
Warsaw. In a letter to Gebethner of 9 November 1859, Fontana expressed
considerable dissatisfaction with the modifications introduced by
Polish proofreaders subsequent to the corrections that he himself had
made in January 1859 while in Berlin. See Hoesick 1912:
439–441.</p>''',
            'numchild': 1,
            'path': '0001000100010002000200030004',
            'show_in_menus': True,
            'slug': 'poland',
            'title': 'Poland'
        }
    },
    'background_publishers_poland_dating': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>Documentary evidence concerning the publication of the Polish
first editions is basically limited to press advertisements and the
composer’s correspondence. A single source – <i>Pamiętnik
Warszawski</i> – announced the release of the Polonaise in G minor,
while the publication of one of the mazurkas lithographed in Warsaw
(see MazG–1-KOL) was mentioned in a letter from Chopin to Jan
Białobłocki.<a href="#_ftn1" id="_ftnref1">[1]</a> As for the Rondos
Opp. 1 &amp; 5, the proposed dates come from the <i>Kurjer
Warszawski</i>. Other Polish Chopin editions were advertised in the
Leipzig periodical <i>Musikalisch-literarischer</i>
<i>Monatsbericht</i>, from which one can also glean the publication
dates of the <i>Deux Valses Mélancoliques</i> (see 70/2&amp;69/2–1-WI)
and the second Polish editions of the <i>Deux Mazurkas</i> (see
MazG&amp;Bû–1-FR) and the Waltz in E major (see WaltzE–1-CHA).</p>

<p>Different release dates have been proposed for the Songs Op. 74 as
follows: 1/1859 (Chomiński and Turło 1990), 9/1859 (GW, No. 238) and
1/1860 (MlM). The first of these, which evidently was based on the
printed date below Fontana’s preface in 74–1-G and 74–1a-G, preceded
the edition’s actual release, whereas the date in MlM followed it. In
fact, Fontana’s letter of 9 November 1859 from Paris to Gebethner in
Warsaw, noting receipt of the Polish edition of Op. 74 a few days
before, confirms the date given by the <i>Gazeta Warszawska</i>.<a
href="#_ftn2" id="_ftnref2">[2]</a> The dates of all other Polish
editions derive from those cited by Chomiński and Turło.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> KFC 1955: i/74–75.</p>
</div>

<div id="ftn2">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref2" id="_ftn2" name="_ftn2">[2]</a>
See Hoesick 1912: 439–441.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300040001',
            'show_in_menus': True,
            'slug': 'dating-the-polish-editions',
            'title': 'Dating the Polish editions'
        }
    },
    'background_publishers_italy': {
        'class': IndexPage,
        'kwargs': {
            'depth': 7,
            'introduction': u'''<p>Most of the Chopin editions published in Italy<a href="#_ftn1"
id="_ftnref1">[1]</a> during the composer’s lifetime recycled the
music text of editions from other countries, almost certainly without
the original publisher’s consent.<a href="#_ftn2"
id="_ftnref2">[2]</a> Because they therefore do not constitute primary
material, the Italian sources have not been catalogued apart from two
editions published before 1849 and two posthumous ones, which have
been included for reasons explained below. All four were brought out
by the same publisher (see Table 19) and two have direct links to
Italian music,<a href="#_ftn3" id="_ftnref3">[3]</a> which partly
explains the high level of interest in these works within Italy
itself.</p>

<p><a id="19" linktype="document">Table 19 Italian publisher</a></p>

<p>By all appearances, Ricordi’s edition of <i>Hexameron</i> was the
first of the four original publications of this work, thus warranting
its presence in this catalogue. According to Gastone Belotti,<a
href="#_ftn4" id="_ftnref4">[4]</a> it preceded by four weeks the
edition of Haslinger and by more than two years that of Troupenas. It
similarly anticipated the English edition, which dates from the first
six months of 1840.</p>

<p>The edition of the Tarantella Op. 43 appears to have resulted from
an arrangement between Ricordi and Troupenas of which no details are
known. What is clear is that the former prepared his edition on the
basis of the French print, while for his part Troupenas added the name
of the Milanese firm to the TP of Op. 43’s second impression (see
43–1a-TR).<a href="#_ftn5" id="_ftnref5">[5]</a> Chopin would have
been informed about the publication of this fourth ‘first edition’ of
the work. Ricordi’s editions of the Sonata Op. 4 and Variations on a
German National Air (both of which appeared in 1851) reflect a truly
international effort. The fact that the title pages of the French and
Austrian first editions refer to him as an associate editor (see
4–1-R, 4–1-HAc, VGNA–1-R, VGNA–1-HAc)<a href="#_ftn6"
id="_ftnref6">[6]</a> shows that Ricordi was a partner from the start
and that his publications are ‘official’ Chopin first editions along
with the others.</p>

<hr align="left" size="1" width="33%"/>

<p id="ftn1" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref1" name="_ftn1">[1]</a> Like Poland, Italy
did not exist as an independent nation during much of the nineteenth
century. Between 1815 and 1859, Milan – where all of the Italian
editions of Chopin were published – belonged to the Kingdom of
Lombardy-Venetia which itself was under Austrian domination.</p>

<p id="ftn2" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref2" name="_ftn2">[2]</a> These include the
following:</p>

<ul style="font-size: 9pt; line-height: 115%; text-align: justify">
<li>Ricordi: Opp. 9, 18, 34 (1839); Opp. 35–37, 42 (1840); <i>Méthode
des Méthodes</i> (1841)</li>

<li>Artaria: Op. 9 (1836); Opp. 15, 18 (1837)</li>

<li>Lucca: Opp. 9, 10, 12, 14, 16, 18–20, 22, 23, 27 (1836); Op. 25
(1837); Op. 28 (1839); <i>Méthode des Méthodes</i> (c. 1841); Op. 30
(1843)</li>

<li>Canti: Op. 27 (1840).</li>
</ul>

<p style="font-size: 9pt; line-height: 115%; text-align: justify">This
information is taken from Belotti 1977: 419–451 and Chomiński and
Turło 1990: 272–273, except for the publication date of the two
editions of the <i>Méthode des Méthodes</i>, which has been deduced
from the plate numbers. To the above list can be added the editions of
Opp. 15, 30, 34, 37 &amp; 42 published around 1840 by C. Pozzi, a firm
of Italian origin located in Medrisio in Switzerland.</p>

<p id="ftn3" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref3" name="_ftn3">[3]</a> <i>Hexameron</i> was
based on a theme by Bellini and was first performed at a concert
organised by Princess Belgiojoso for the benefit of Italian
refugees. (See ‘France’, note 2, under ‘Legal contexts’.)  The
Tarantella Op. 43 was inspired by a dance of the same name originating
in southern Italy.</p>

<p id="ftn4" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref4" name="_ftn4">[4]</a> See Belotti 1977:
447.</p>

<p id="ftn5" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref5" name="_ftn5">[5]</a> This mention of the
Italian firm on the TP of Op. 43 is the only such reference in all of
the ‘official’ Chopin editions published before 1850. It should be
recalled that Chopin generally assigned rights to his German
publishers in all countries save France and England. His contracts
with Troupenas and Schuberth do not survive, but given that Chopin
demanded 500 francs from the latter (see his letter to Fontana of 20
June 1841, in Chopin 1962: 196), it is likely that the conditions
under which he sold the rights of other works were broadly similar if
not identical. Ricordi would thus have had to negotiate with Schuberth
rather than Troupenas.</p>

<p id="ftn6" style="font-size: 9pt; line-height: 115%; text-align:
justify"><a href="#_ftnref6" name="_ftn6">[6]</a> The TPs of the
Austrian editions also give the name of a Leipzig
concessionaire. Oddly, the English edition indicates neither
continental publisher (see 4–1-COC, VGNA–1-COC).</p>''',
            'numchild': 1,
            'path': '0001000100010002000200030005',
            'show_in_menus': True,
            'slug': 'italy',
            'title': 'Italy'
        }
    },
    'background_publishers_italy_dating': {
        'class': RichTextPage,
        'kwargs': {
            'content': u'''<p>The publication dates indicated for the first editions of the
Tarantella Op. 43 and <i>Hexameron </i>derive from Belotti.<a
href="#_ftn1" id="_ftnref1">[1]</a> For the two posthumous editions,
scrutiny of the Italian press, especially the <i>Gazzetta Musicale</i>
<i>di Milano</i>, allows one to deduce the exact dates of release.</p>

<hr align="left" size="1" width="33%"/>

<div id="ftn1">
<p style="font-size: 9pt; line-height: 115%; text-align: justify"><a href="#_ftnref1" id="_ftn1" name="_ftn1">[1]</a> See notes 2 &amp; 4
above.</p>
</div>''',
            'depth': 8,
            'numchild': 0,
            'path': '00010001000100020002000300050001',
            'show_in_menus': True,
            'slug': 'dating-the-italian-editions',
            'title': 'Dating the Italian editions'
        }
    },
    'background_explaining': {
        'class': IndexPage,
        'kwargs': {
            'depth': 5,
            'numchild': 5,
            'path': '00010001000100020003',
            'show_in_menus': True,
            'slug': 'explaining-the-annotated-catalogue',
            'title': 'Explaining the Annotated Catalogue'
        }
    },
    'background-classification-critera': {
        'class': IndexPage,
        'kwargs': {
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000200030001',
            'show_in_menus': True,
            'slug': 'classification-criteria',
            'title': 'Classification criteria'
        }
    },
    'background-descriptive-method': {
        'class': IndexPage,
        'kwargs': {
            'depth': 6,
            'numchild': 16,
            'path': '000100010001000200030002',
            'show_in_menus': True,
            'slug': 'descriptive-method',
            'title': 'Descriptive method'
        }
    },
    'background_descriptive_general_information': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020001',
            'show_in_menus': True,
            'slug': 'general-information',
            'title': 'General Information'
        }
    },
    'background_description_edition': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020002',
            'show_in_menus': True,
            'slug': 'edition-impression-code',
            'title': 'Edition / Impression code'
        }
    },
    'background_description_title': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020003',
            'show_in_menus': True,
            'slug': 'title-page-transcription',
            'title': 'Title page transcription'
        }
    },
    'background_description_contents': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020004',
            'show_in_menus': True,
            'slug': 'contents',
            'title': 'Contents'
        }
    },
    'background_description_dedication': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020005',
            'show_in_menus': True,
            'slug': 'dedication',
            'title': 'Dedication'
        }
    },
    'background_description_half_title': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020006',
            'show_in_menus': True,
            'slug': 'half-title',
            'title': 'Half-title'
        }
    },
    'background_description_headline': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020007',
            'show_in_menus': True,
            'slug': 'headline',
            'title': 'Headline'
        }
    },
    'background_description_caption': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020008',
            'show_in_menus': True,
            'slug': 'caption-title',
            'title': 'Caption title'
        }
    },
    'background_description_sub_caption': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '0001000100010002000300020009',
            'show_in_menus': True,
            'slug': 'sub-caption',
            'title': 'Sub-caption'
        }
    },
    'background_description_footline': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '000100010001000200030002000A',
            'show_in_menus': True,
            'slug': 'footline',
            'title': 'Footline'
        }
    },
    'background_description_comments': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '000100010001000200030002000B',
            'show_in_menus': True,
            'slug': 'comments',
            'title': 'Comments'
        }
    },
    'background_description_modifications': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '000100010001000200030002000C',
            'show_in_menus': True,
            'slug': 'modifications',
            'title': 'Modifications'
        }
    },
    'background_description_errors': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '000100010001000200030002000D',
            'show_in_menus': True,
            'slug': 'errors',
            'title': 'Errors'
        }
    },
    'background_description_dmfs': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '000100010001000200030002000E',
            'show_in_menus': True,
            'slug': 'dmfs',
            'title': 'DMFs'
        }
    },
    'background_description_adfs': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '000100010001000200030002000F',
            'show_in_menus': True,
            'slug': 'adfs',
            'title': 'ADFs'
        }
    },
    'background_description_copies': {
        'class': RichTextPage,
        'kwargs': {
            'depth': 7,
            'numchild': 0,
            'path': '000100010001000200030002000G',
            'show_in_menus': True,
            'slug': 'copies',
            'title': 'Copies'
        }
    },
    'background_cross_references': {
        'class': IndexPage,
        'kwargs': {
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000200030003',
            'show_in_menus': True,
            'slug': 'cross-references-and-abbreviated-descriptions',
            'title': 'Cross-references and abbreviated descriptions'
        }
    },
    'background_policies': {
        'class': IndexPage,
        'kwargs': {
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000200030004',
            'show_in_menus': True,
            'slug': 'policies-on-quasi-facsimile-transcription',
            'title': 'Policies on quasi-facsimile transcription'
        }
    },
    'background_dating': {
        'class': IndexPage,
        'kwargs': {
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000200030005',
            'show_in_menus': True,
            'slug': 'dating-the-editions',
            'title': 'Dating the editions'
        }
    },
    'annotated_catalogue': {
        'class': Catalogue,
        'kwargs': {
            'depth': 4,
            'path': '0001000100010003',
            'show_in_menus': True,
            'slug': 'annotated-catalogue',
            'title': 'Annotated catalogue'
        }
    },
    'appendices': {
        'class': IndexPage,
        'kwargs': {
            'depth': 4,
            'numchild': 4,
            'path': '0001000100010004',
            'show_in_menus': True,
            'slug': 'appendices',
            'title': 'Appendices'
        }
    },
    'stp_appendix': {
        'class': IndexPage,
        'kwargs': {
            'depth': 5,
            'numchild': 3,
            'path': '00010001000100040004',
            'show_in_menus': True,
            'slug': 'i',
            'title': 'I. Series title pages'
        }
    },
    'stp_introduction': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Introduction',
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000400040001',
            'show_in_menus': True,
            'slug': 'introduction',
            'title': 'Introduction'
        }
    },
    'stp_descriptive_method': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Descriptive method',
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000400040002',
            'show_in_menus': True,
            'slug': 'descriptive-method',
            'title': 'Descriptive method'
        }
    },
    'stp_publishers': {
        'class': STPIndexPage,
        'kwargs': {
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000400040003',
            'show_in_menus': True,
            'slug': 'publishers',
            'title': 'Publishers',
        }
    },
    'advert_appendix': {
        'class': IndexPage,
        'kwargs': {
            'depth': 5,
            'numchild': 3,
            'path': '00010001000100040005',
            'show_in_menus': True,
            'slug': 'ii',
            'title': "II. Publishers' advertisements"
        }
    },
    'advert_introduction': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Introduction',
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000400050001',
            'show_in_menus': True,
            'slug': 'introduction',
            'title': 'Introduction'
        }
    },
    'advert_descriptive_method': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Descriptive method',
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000400050002',
            'show_in_menus': True,
            'slug': 'descriptive-method',
            'title': 'Descriptive method'
        }
    },
    'advert_index': {
        'class': AdvertIndexPage,
        'kwargs': {
            'depth': 6,
            'numchild': 0,
            'path': '000100010001000400050003',
            'show_in_menus': True,
            'slug': 'publishers',
            'title': 'Publishers'
        }
    },
    'library_appendix': {
        'class': LibraryIndexPage,
        'kwargs': {
            'depth': 5,
            'path': '00010001000100040006',
            'show_in_menus': True,
            'slug': 'iii',
            'title': 'III. Libraries and private collections: sigla and holdings'
        }
    },
    'appendix_uncatalogued': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Uncatalogued works',
            'depth': 5,
            'numchild': 0,
            'path': '00010001000100040007',
            'show_in_menus': True,
            'slug': 'iv',
            'title': 'IV. Uncatalogued works'
        }
    },
    'reference_material': {
        'class': IndexPage,
        'kwargs': {
            'depth': 4,
            'numchild': 3,
            'path': '0001000100010005',
            'show_in_menus': True,
            'slug': 'reference-material',
            'title': 'Reference material'
        }
    },
    'reference_abbreviations': {
        'class': AbbreviationIndexPage,
        'kwargs': {
            'depth': 5,
            'numchild': 0,
            'path': '00010001000100050006',
            'show_in_menus': True,
            'slug': 'list-abbreviations',
            'title': 'List of abbreviations'
        }
    },
    'reference_sigla': {
        'class': PublisherIndexPage,
        'kwargs': {
            'depth': 5,
            'path': '00010001000100050007',
            'show_in_menus': True,
            'slug': 'sigla-publishers',
            'title': 'Sigla of publishers'
        }
    },
    'reference_glossary': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Glossary',
            'depth': 5,
            'numchild': 0,
            'path': '00010001000100050008',
            'show_in_menus': True,
            'slug': 'glossary',
            'title': 'Glossary'
        }
    },
    'reference_bibliography': {
        'class': RichTextPage,
        'kwargs': {
            'content': 'Bibliography',
            'depth': 5,
            'numchild': 0,
            'path': '00010001000100050009',
            'show_in_menus': True,
            'slug': 'bibliography',
            'title': 'Bibliography'
        }
    }
}

page_data = OrderedDict(sorted(page_data.items(),
                               key=lambda t: t[1]['kwargs']['path']))

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
