from catalogue.views import FacetedSearchView

from django.conf.urls import patterns, include, url

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

from wagtail.wagtailcore import urls as wagtail_urls

sqs = SearchQuerySet().order_by(
    '-_score').order_by('sort_order').facet('document')

urlpatterns = patterns('',
                       url(r'^search/',
                           FacetedSearchView(form_class=FacetedSearchForm,
                                             load_all=True,
                                             searchqueryset=sqs),
                           name='haystack_search'),
                       )
