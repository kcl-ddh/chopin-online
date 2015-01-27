from django.db import models

from wagtail.wagtailcore.fields import RichTextField


class Introducable(models.Model):
    introduction = RichTextField(blank=True)

    class Meta:
        abstract = True
