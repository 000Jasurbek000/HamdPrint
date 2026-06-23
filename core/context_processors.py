from catalog.views import get_book_categories
from .contact_info import CONTACT_INFO, JOURNAL_URL
from .home_page import HOME_INDEX_CATEGORIES


def site_context(request):
    is_home = (
        request.resolver_match
        and request.resolver_match.url_name == 'home'
        and request.resolver_match.namespace == 'core'
    )
    return {
        'site_name': 'BUKHARA HAMD PRINT',
        'contact': CONTACT_INFO,
        'is_home': is_home,
        'book_categories': get_book_categories(),
        'home_index_categories': HOME_INDEX_CATEGORIES,
        'journal_url': JOURNAL_URL,
    }
