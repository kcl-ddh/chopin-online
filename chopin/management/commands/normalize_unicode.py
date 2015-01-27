from catalogue.models import Advert, Library, Publisher, STP

from django.core.management.base import NoArgsCommand

from unicodedata import normalize as _n

from wagtail.wagtailcore.models import Page


class Command(NoArgsCommand):
    help = """Normalizes UNICODE data in text fields, it replaces combining
    character with UNICODE character."""

    def handle_noargs(self, **options):
        norm = 'NFKC'

        for l in Library.objects.all():
            l.name = _n(norm, l.name)
            l.save()

        for p in Publisher.objects.all():
            if p.name:
                p.name = _n(norm, p.name)
                p.save()

        for s in STP.objects.all():
            s.publisher_name = _n(norm, s.publisher_name)
            s.rubric = _n(norm, s.rubric)
            s.save()

        for a in Advert.objects.all():
            a.publisher_name = _n(norm, a.publisher_name)
            a.rubric = _n(norm, a.rubric)
            a.save()

        for p in Page.objects.all():
            p = p.specific
            p.title = _n(norm, p.title)

            if hasattr(p, 'content'):
                p.content = _n(norm, p.content)

            if hasattr(p, 'introduction'):
                p.introduction = _n(norm, p.introduction)

            p.save()
