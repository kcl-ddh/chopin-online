from django import template

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
