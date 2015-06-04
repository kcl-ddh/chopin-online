from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls

# Signal handlers
from wagtail.wagtailsearch.signal_handlers import register_signal_handlers as \
    wagtailsearch_register_signal_handlers
wagtailsearch_register_signal_handlers()

from ddhldap.signal_handlers import register_signal_handlers as \
    ddhldap_register_signal_handlers
ddhldap_register_signal_handlers()

import chopin.signal_handlers
import os.path

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )

try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += patterns('',
                                url(r'^__debug__/',
                                    include(debug_toolbar.urls)),
                                )
except ImportError:
    pass

urlpatterns += patterns('',
                        url(r'^aco/', include('catalogue.urls')),
                        url(r'^ocve/', include('ocve.urls')),
                        url(r'^cfeo/', include('ocve.cfeourls')),

                        url(r'^tinymce/', include('tinymce.urls')),

                        url(r'^frontend/search/',
                            include(wagtailsearch_frontend_urls)),
                        url(r'wagtail/', include(wagtailadmin_urls)),
                        url(r'^documents/', include(wagtaildocs_urls)),

                        url(r'', include(wagtail_urls)),
                        )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))

urlpatterns += static(settings.MEDIA_URL + 'documents/',
                      document_root=os.path.join(settings.MEDIA_ROOT,
                                                 'documents'))
