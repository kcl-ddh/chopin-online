from django.conf import settings
from django.conf.urls import url
from django.db import models
from django.shortcuts import render
from django.utils.text import slugify

from model_utils.models import TimeStampedModel

from modelcluster.fields import ParentalKey

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                PageChooserPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtaildocs.models import Document
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from .behaviours import Introducable

import hashlib
import logging


logger = logging.getLogger(__name__)


def _d(str):
    return str.decode(settings.AC_ENCODING)


def _e(str):
    return str.encode(settings.AC_ENCODING)

def safe_slugify (text, model):
    """Return a slugified version of `text` that copes with the brain dead
    nature of Wagtail, which uses slugs as lookup keys and has a 50
    character limit on them."""
    slug = slugify(text)[:48]
    num = 1
    while True:
        try:
            model.objects.get(slug=slug)
            slug += '-{}'.format(num)
            num += 1
        except model.DoesNotExist:
            break
    return slug


class HomePage(Page):

    content = RichTextField()

    search_fields = Page.search_fields + (index.SearchField('content'),)
    search_name = 'Home Page'
    subpage_types = ['IndexPage', 'RichTextPage']

    class Meta:
        verbose_name = 'homepage'

HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('content', classname='full'),
]


class IndexPage(Page, Introducable):

    search_name = 'Index Page'
    search_fields = Page.search_fields + (index.SearchField('introduction'),)
    subpage_types = ['IndexPage', 'RichTextPage']

IndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
]


class LandingPageSection(Orderable):
    landing_page = ParentalKey('LandingPage', related_name='sections')
    title = models.CharField(max_length=256)
    abbreviation = models.CharField(max_length=32)
    css_class = models.CharField(max_length=64)
    introduction = RichTextField()
    image = models.ForeignKey(Image)
    page = models.ForeignKey(Page)

    panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('abbreviation', classname='full'),
        FieldPanel('css_class', classname='full'),
        FieldPanel('introduction', classname='full'),
        ImageChooserPanel('image'),
        PageChooserPanel('page', 'catalogue.HomePage')
    ]


class LandingPage(Page, Introducable):
    search_fields = Page.search_fields + (index.SearchField('introduction'),)
    search_name = 'Landing Page'
    subpage_types = ['HomePage']

LandingPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
    InlinePanel(LandingPage, 'sections', label='Sections'),
]


class RichTextPage(Page):

    content = RichTextField()

    search_fields = Page.search_fields + (index.SearchField('content'),)
    search_name = 'Rich Text Page'
    subpage_types = []

RichTextPage.content_panels += [FieldPanel('content', classname='full')]


class Country(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    panels = [
        FieldPanel('name', classname='full title'),
    ]

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return self.name

    @property
    def libraries(self):
        return Library.objects.filter(city__country=self)

    @property
    def publishers(self):
        return Publisher.objects.filter(city__country=self)

register_snippet(Country)


class City(TimeStampedModel):
    name = models.CharField(max_length=64)
    country = models.ForeignKey(Country, related_name='cities')

    panels = [
        FieldPanel('name', classname='full title'),
        SnippetChooserPanel('country', Country)
    ]

    class Meta:
        ordering = ['name']
        unique_together = ['country', 'name']
        verbose_name_plural = 'Cities'

    def __unicode__(self):
        return u'{0}'.format(self.name)

register_snippet(City)


class Library(Page):
    name = models.CharField(max_length=256)
    city = models.ForeignKey(
        City, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='libraries')
    library_url = models.URLField(blank=True, null=True)
    pdf = models.ForeignKey(Document, null=True, blank=True,
                            on_delete=models.SET_NULL, related_name='+')

    class Meta:
        ordering = ['title', 'city', 'name']
        verbose_name_plural = 'Libraries'

    def __unicode__(self):
        return u'{0}: {1}'.format(self.title, self.name)

    @property
    def impressions(self):
        return sorted(Impression.objects.filter(copies__copy__library=self),
                      key=lambda x: x.impression.work.work.sort_order +
                      float(x.impression.sort_order/1000))

Library.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('name', classname='full title'),
    SnippetChooserPanel('city', City),
    FieldPanel('library_url', classname='full'),
    DocumentChooserPanel('pdf')
]


class LibraryIndexPage(RoutablePageMixin, Page, Introducable):

    search_name = 'Library Index Page'
    subpage_urls = (
        url(r'^$', 'serve_all_libraries', name='all_libraries'),
        url(r'^libraries-by-city/$', 'serve_libraries_by_city',
            name='libraries_by_city'),
        url(r'^libraries-by-country/$', 'serve_libraries_by_country',
            name='libraries_by_country'),
    )

    class Meta:
        verbose_name = 'Library Index Page'

    @property
    def libraries(self):
        return Library.objects.all()

    def serve_all_libraries(self, request):
        """Renders all the libraries."""
        return render(request, self.get_template(request),
                      {'self': self, 'libraries': self.libraries})

    def serve_libraries_by_city(self, request):
        """Renders libraries, grouped by city."""
        return render(request, self.get_template(request),
                      {'self': self, 'cities': City.objects.all()})

    def serve_libraries_by_country(self, request):
        """Renders libraries, grouped by country."""
        return render(request, self.get_template(request),
                      {'self': self, 'countries': Country.objects.all()})

LibraryIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
]


class Publisher(Page):
    name = RichTextField(null=True, blank=True)
    abbreviation = models.CharField(max_length=256, null=True, blank=True)
    city = models.ForeignKey(
        City, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='publishers')

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        if self.name:
            return u'{0}: {1}'.format(self.title, self.name)
        else:
            return self.title

    @property
    def sorted_impressions(self):
        return sorted(self.impressions.all(),
                      key=lambda x: x.impression.work.work.sort_order +
                      float(x.impression.sort_order/1000))

    @property
    def works(self):
        works = []

        for impression in self.impressions.all():
            if impression.work not in works:
                works.append(impression.work)

        works = sorted(works, key=lambda x: x.work.sort_order)

        return works

Publisher.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('name', classname='full title'),
    FieldPanel('abbreviation', classname='full'),
    SnippetChooserPanel('city', City)
]

register_snippet(Publisher)


class PublisherIndexPage(RoutablePageMixin, Page, Introducable):

    subpage_urls = (
        url(r'^$', 'serve_all_publishers', name='all_publishers'),
        url(r'^publishers-by-city/$', 'serve_publishers_by_city',
            name='publishers_by_city'),
        url(r'^publishers-by-country/$', 'serve_publishers_by_country',
            name='publishers_by_country'),
        url(r'^(?P<p_slug>.*?)/(?P<w_slug>.*?)/$', 'serve_impressions',
            name='impressions'),
    )

    def serve_all_publishers(self, request):
        """Renders all the publishers."""
        publishers = Publisher.objects.all()

        return render(request, self.get_template(request),
                      {'self': self, 'publishers': publishers})

    def serve_publishers_by_city(self, request):
        """Renders publishers, grouped by city."""
        return render(request, self.get_template(request),
                      {'self': self, 'cities': City.objects.all(),
                       'suburl': 'publishers-by-city'})

    def serve_publishers_by_country(self, request):
        """Renders publishers, grouped by country."""
        return render(request, self.get_template(request),
                      {'self': self, 'countries': Country.objects.all()})

    def serve_impressions(self, request, p_slug, w_slug):
        """Renders impressions for the given publisher and work."""
        publisher = Publisher.objects.filter(slug=p_slug).first()
        work = Work.objects.filter(slug=w_slug).first()

        impressions = []

        for impression in publisher.sorted_impressions:
            if impression.work.work == work:
                impressions.append(impression)

        return render(request, 'catalogue/publisher.html',
                      {'self': publisher, 'publisher': publisher, 'work': work,
                       'impressions': impressions})


PublisherIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
]


class Copy(TimeStampedModel):
    library = models.ForeignKey(Library)
    description = models.TextField()

    panels = [
        PageChooserPanel('library', Library),
        FieldPanel('description', classname='full'),
    ]

    class Meta:
        verbose_name_plural = 'Copies'

    def __unicode__(self):
        return unicode(self.library)

register_snippet(Copy)


class ImpressionCopy(Orderable, TimeStampedModel):
    impression = ParentalKey('Impression', related_name='copies')
    copy = models.ForeignKey(Copy)

    panels = [
        SnippetChooserPanel('copy', Copy)
    ]

    class Meta:
        ordering = ['sort_order']
        unique_together = ('impression', 'copy')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.impression, self.copy)


class Impression(Page):
    code_hash = models.CharField(max_length=32, editable=False)
    impression_title = models.TextField()
    publisher = models.ForeignKey(Publisher, blank=True, null=True,
                                  on_delete=models.SET_NULL,
                                  related_name='impressions')
    comments = models.TextField()
    content = models.TextField()
    sort_order = models.PositiveIntegerField()
    pdf = models.ForeignKey(Document, null=True, blank=True,
                            on_delete=models.SET_NULL, related_name='+')

    search_fields = (
        index.SearchField('title', boost=10),
        index.SearchField('impression_title', partial_match=True, boost=10),
        index.SearchField('content', partial_match=True)
    )
    search_name = 'Impression'

    class Meta:
        verbose_name = 'Impression'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.code_hash = hashlib.md5(_e(self.title)).hexdigest()
        super(Impression, self).save(*args, **kwargs)

    @property
    def work(self):
        return self.get_parent()

Impression.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('impression_title', classname='full title'),
    PageChooserPanel('publisher', Publisher),
    FieldPanel('content', classname='full'),
    FieldPanel('comments', classname='full'),
    FieldPanel('sort_order'),
    DocumentChooserPanel('pdf'),
    InlinePanel(Impression, 'copies', label='Copies'),
]


class Work(Page):
    code = models.CharField(max_length=32)
    heading = models.TextField()
    has_opus = models.BooleanField(default=False)
    is_posthumous = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField()
    pdf = models.ForeignKey(Document, null=True, blank=True,
                            on_delete=models.SET_NULL, related_name='+')

    search_fields = Page.search_fields + (
        index.SearchField('heading', partial_match=True),
    )
    search_name = 'Work'
    subpage_types = ['Impression']

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Work'

    def __unicode__(self):
        return self.title

    @property
    def impressions(self):
        return self.get_children()

Work.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('code', classname='full'),
    FieldPanel('has_opus'),
    FieldPanel('is_posthumous'),
    FieldPanel('sort_order'),
    FieldPanel('heading', classname='full'),
    DocumentChooserPanel('pdf')
]


class Catalogue(RoutablePageMixin, Page, Introducable):
    search_name = 'Catalogue'
    subpage_types = ['Work']

    subpage_urls = (
        url(r'^$', 'serve_all_works', name='all_works'),
        url(r'^works-with-opus/$', 'serve_works_with_opus',
            name='works_with_opus'),
        url(r'^posthumous-works-with-opus/$',
            'serve_posthumous_works_with_opus',
            name='posthumous_works_with_opus'),
        url(r'^works-without-opus-numbers/$', 'serve_works_without_opus',
            name='works_without_opus'),
        url(r'^posthumous-works-without-opus/$',
            'serve_posthumous_works_without_opus',
            name='posthumous_works_without_opus'),
    )

    class Meta:
        verbose_name = 'Catalogue'

    @property
    def works(self):
        return self.get_children()

    def serve_all_works(self, request):
        """Renders all the works."""
        works = self.works

        return render(request, self.get_template(request),
                      {'self': self, 'works': works})

    def serve_works_with_opus(self, request):
        """Renders all the works that have opus number."""
        works = self.works.filter(work__has_opus=True,
                                  work__is_posthumous=False)

        return render(request, self.get_template(request),
                      {'self': self, 'works': works,
                       'subtitle': 'Works with opus numbers',
                       'suburl': 'works-with-opus'})

    def serve_posthumous_works_with_opus(self, request):
        """Renders all the posthumous works with opus number."""
        works = self.works.filter(work__has_opus=True,
                                  work__is_posthumous=True)

        return render(request, self.get_template(request),
                      {'self': self, 'works': works,
                       'subtitle': 'Posthumous works with opus numbers',
                       'suburl': 'posthumous-works-with-opus'})

    def serve_works_without_opus(self, request):
        """Renders all the works that don't have opus number."""
        works = self.works.filter(work__has_opus=False,
                                  work__is_posthumous=False)

        return render(request, self.get_template(request),
                      {'self': self, 'works': works,
                       'subtitle': 'Works without opus numbers',
                       'suburl': 'works-without-opus'})

    def serve_posthumous_works_without_opus(self, request):
        """Renders all the posthumous works without opus number."""
        works = self.works.filter(work__has_opus=False,
                                  work__is_posthumous=True)

        return render(request, self.get_template(request),
                      {'self': self, 'works': works,
                       'subtitle': 'Posthumous works without opus numbers',
                       'suburl': 'posthumous-works-without-opus'})

Catalogue.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
]


class STP(TimeStampedModel):
    publisher = models.ForeignKey(Publisher, blank=True, null=True,
                                  related_name='stps')
    publisher_name = models.CharField(max_length=256)
    publisher_name_slug = models.CharField(max_length=256, editable=False)
    rubric = RichTextField()
    rubric_slug = models.CharField(max_length=256, editable=False)
    pdf = models.ForeignKey(Document, blank=True, null=True,
                            on_delete=models.SET_NULL, related_name='+')

    class Meta:
        ordering = ['publisher_name', 'rubric']
        verbose_name = 'Series Title Page'

    def __unicode__(self):
        return u'{0}: {1}'.format(self.publisher_name, self.rubric)

    @property
    def url(self):
        index_page = Page.objects.filter(slug='i').first()
        stp_index_page = index_page.get_children().filter(
            slug='publishers').first()

        return '{0}{1}/{2}/'.format(stp_index_page.url,
                                    self.publisher_name_slug, self.rubric_slug)

    def save(self, *args, **kwargs):
        self.publisher_name_slug = slugify(self.publisher_name)
        self.rubric_slug = slugify(self.rubric)
        super(STP, self).save(*args, **kwargs)

STP.panels = [
    FieldPanel('rubric', classname='full title'),
    FieldPanel('publisher_name', classname='full'),
    SnippetChooserPanel('publisher', Publisher),
    DocumentChooserPanel('pdf')
]

register_snippet(STP)


class STPIndexPage(RoutablePageMixin, Page):
    introduction = RichTextField(blank=True)

    search_name = 'STP Index Page'

    subpage_urls = (
        url(r'^$', 'serve_all_publishers', name='all_publishers'),
        url(r'^(?P<pn_slug>.*?)/(?P<r_slug>.*?)/$', 'serve_rubric',
            name='rubric'),
        url(r'^(?P<slug>.*?)/$', 'serve_rubrics', name='rubrics'),
    )

    class Meta:
        verbose_name = 'Series Title Page Index Page'

    def serve_all_publishers(self, request):
        """Renders all the publishers."""
        publishers = STP.objects.values(
            'publisher_name', 'publisher_name_slug').distinct().order_by(
            'publisher_name')

        return render(request, self.get_template(request),
                      {'self': self, 'publishers': publishers})

    def serve_rubrics(self, request, slug):
        """Renders rubrics for publisher."""
        stps = STP.objects.filter(publisher_name_slug=slug)

        return render(request, self.get_template(request),
                      {'self': self, 'stps': stps})

    def serve_rubric(self, request, pn_slug, r_slug):
        """Renders rubric."""
        stp = STP.objects.filter(publisher_name_slug=pn_slug,
                                 rubric_slug=r_slug).first()

        return render(request, self.get_template(request),
                      {'self': self, 'stp': stp})

STPIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
]


class Advert(TimeStampedModel):
    publisher = models.ForeignKey(Publisher, blank=True, null=True,
                                  related_name='adverts')
    publisher_name = models.CharField(max_length=256)
    publisher_name_slug = models.CharField(max_length=256, editable=False)
    rubric = RichTextField()
    rubric_slug = models.CharField(max_length=256, editable=False)
    pdf = models.ForeignKey(Document, null=True, blank=True,
                            on_delete=models.SET_NULL, related_name='+')

    class Meta:
        ordering = ['publisher_name', 'rubric']

    def __unicode__(self):
        return u'{0}: {1}'.format(self.publisher_name, self.rubric)

    @property
    def url(self):
        index_page = Page.objects.filter(slug='ii').first()
        stp_index_page = index_page.get_children().filter(
            slug='publishers').first()

        return '{0}{1}/{2}/'.format(stp_index_page.url,
                                    self.publisher_name_slug, self.rubric_slug)

    def save(self, *args, **kwargs):
        self.publisher_name_slug = slugify(self.publisher_name)
        self.rubric_slug = slugify(self.rubric)
        super(Advert, self).save(*args, **kwargs)

Advert.panels = [
    FieldPanel('rubric', classname='full title'),
    FieldPanel('publisher_name', classname='full'),
    SnippetChooserPanel('publisher', Publisher),
    DocumentChooserPanel('pdf')
]

register_snippet(Advert)


class AdvertIndexPage(RoutablePageMixin, Page, Introducable):

    subpage_urls = (
        url(r'^$', 'serve_all_publishers', name='all_publishers'),
        url(r'^(?P<pn_slug>.*?)/(?P<r_slug>.*?)/$', 'serve_rubric',
            name='rubric'),
        url(r'^(?P<slug>.*?)/$', 'serve_rubrics', name='rubrics'),
    )

    class Meta:
        verbose_name = 'Publishers\' Advertisements Index Page'

    def serve_all_publishers(self, request):
        """Renders all the publishers."""
        publishers = Advert.objects.values(
            'publisher_name', 'publisher_name_slug').distinct().order_by(
            'publisher_name')

        return render(request, self.get_template(request),
                      {'self': self, 'publishers': publishers})

    def serve_rubrics(self, request, slug):
        """Renders rubrics for publisher."""
        adverts = Advert.objects.filter(publisher_name_slug=slug)

        return render(request, self.get_template(request),
                      {'self': self, 'adverts': adverts})

    def serve_rubric(self, request, pn_slug, r_slug):
        """Renders rubric."""
        advert = Advert.objects.filter(publisher_name_slug=pn_slug,
                                       rubric_slug=r_slug).first()

        return render(request, self.get_template(request),
                      {'self': self, 'advert': advert})

AdvertIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('introduction', classname='full'),
]


class Abbreviation(TimeStampedModel):
    abbreviation = models.CharField(max_length=32, unique=True)
    description = RichTextField()
    slug = models.CharField(max_length=256, editable=False)

    class Meta:
        ordering = ['abbreviation']

    def __unicode__(self):
        return u'{0}: {1}'.format(self.abbreviation, self.description)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.abbreviation)
        super(Abbreviation, self).save(*args, **kwargs)

Abbreviation.panels = [
    FieldPanel('abbreviation', classname='full title'),
    FieldPanel('description', classname='full')
]

register_snippet(Abbreviation)


class AbbreviationIndexPage(RoutablePageMixin, Page, Introducable):

    subpage_urls = (
        url(r'^$', 'serve_all_abbreviations', name='all_abbreviations'),
    )

    def serve_all_abbreviations(self, request):
        """Renders all the abbreviations."""
        abbreviations = Abbreviation.objects.all()

        return render(request, self.get_template(request),
                      {'self': self, 'abbreviations': abbreviations})

AbbreviationIndexPage.content_panels = [
    FieldPanel('title', classname='title full'),
    FieldPanel('introduction', classname='full')
]


class GlossaryItem (TimeStampedModel):

    title = models.CharField(max_length=32, unique=True)
    description = RichTextField()
    slug = models.CharField(max_length=256, editable=False)

    class Meta:
        ordering = ['title']

    def save (self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(GlossaryItem, self).save(*args, **kwargs)

GlossaryItem.panels = [
    FieldPanel('title', classname='title full'),
    FieldPanel('description', classname='full')
]

register_snippet(GlossaryItem)


class GlossaryIndexPage (RoutablePageMixin, Page, Introducable):

    subpage_urls = (
        url(r'^$', 'serve_all_glossary_items', name='all_glossary_items'),
    )

    def serve_all_glossary_items (self, request):
        '''Renders all glossary items.'''
        glossary_items = GlossaryItem.objects.all()
        return render(request, self.get_template(request),
                      {'self': self, 'glossary_items': glossary_items})

GlossaryIndexPage.content_panels = [
    FieldPanel('title', classname='title full'),
    FieldPanel('introduction', classname='full')
]
