from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url


def whitelister_element_rules():
    return {
        'a': attribute_rule({'href': check_url, 'id': True}),
        'span': attribute_rule({'class': True}),
    }

hooks.register('construct_whitelister_element_rules',
               whitelister_element_rules)
