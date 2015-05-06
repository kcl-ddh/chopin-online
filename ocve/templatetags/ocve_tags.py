from django import template

import re

register = template.Library()

@register.filter
def clean_si(html):
    """Cleans source information fields."""
    html = html.strip()
    html = re.sub(r'(<p>)?(.*)(</p>)?', '\\2', html)

    return html
