from __future__ import unicode_literals

from django import template

from django.utils.safestring import mark_safe
from json import dumps
import re

register = template.Library()


@register.filter
def clean_si(html):
    """Cleans source information fields."""
    html = html.strip()

    return html


@register.assignment_tag()
def has_printing_method(source_information):
    for pm in source_information.printingmethod.all():
        if pm and pm.method and pm.method.lower() != 'unspecified':
            return True

    return False


@register.filter
def pick(a_list, attribute):
    return [getattr(i, attribute) for i in a_list]


@register.filter
def index_by(a_list, attribute):
    """ this tag creates an index of a list of objects
        by a specific attribute

        e.g.
        a_list = [{'id': 1, 'value': 'a'}, {'id': 2, 'value': 'b'}]

        index_by(a_list, 'value') => {'a': {'id': 1, 'value': 'a'},
                                      'b': {'id': 2, 'value': 'b'}}

    """
    return dict([(unicode(getattr(i, attribute)), i) for i in a_list])


@register.filter
def join_and_quote(a_list, separator=','):
    return mark_safe(separator.join(['"{}"'.format(i) for i in a_list]))


@register.filter
def to_json(an_object):
    """ this tag turns a simple object into json
    Note that it does not work with complex django models, querysets etc.
    """
    return mark_safe(dumps(an_object))
