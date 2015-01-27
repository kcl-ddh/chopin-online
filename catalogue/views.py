from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import haystack.views


class FacetedSearchView(haystack.views.FacetedSearchView):

    def build_page(self):
        # Override Haystack's pagination logic so that invoking a
        # facet that reduces the number of pages of results below the
        # current page does not result in a 404.
        #
        # This is essentially the same code as Django 1.4's pagination
        # example.
        paginator = Paginator(self.results, self.results_per_page)
        page_number = self.request.GET.get('page')
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return (paginator, page)
