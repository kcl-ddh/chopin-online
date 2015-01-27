from django.conf import settings as s


def settings(request):
    title = s.PROJECT_TITLE
    base_url = ''

    for key in s.SITE_TITLE:
        if key in request.path:
            title = s.SITE_TITLE[key]
            base_url = key
            break

    return {'BASE_URL': base_url,
            'CFEO_BASE_URL': s.CFEO_BASE_URL,
            'OCVE_BASE_URL': s.OCVE_BASE_URL,
            'PROJECT_TITLE': title}
