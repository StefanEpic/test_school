from rest_framework.filters import SearchFilter


class ProductTitleSearchFilter(SearchFilter):
    search_description = "Search by product title."
