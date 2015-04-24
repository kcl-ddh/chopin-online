from django import template
from django.conf import settings
from ocve.bartools import toGeos
from ocve.models_generic import BarCollection


register = template.Library()

@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]

@register.filter(name='get_collections')
def get_collections(user):
	if user.is_authenticated():
		collections = BarCollection.objects.select_related().filter(user=user)
	else:
		collections = None
			
	return collections
