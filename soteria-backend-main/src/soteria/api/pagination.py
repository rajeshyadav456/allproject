from collections import OrderedDict

from rest_framework import pagination, status


class DefaultPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 50


class PaginatedListAPIViewMixin:
    LIST_RESULTS_KEY = "items"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def get_paginated_response(self, data):
        paginator = self.paginator
        resp_data = OrderedDict(
            [
                ("count", paginator.page.paginator.count),
                ("next", paginator.get_next_link()),
                ("previous", paginator.get_previous_link()),
                (self.LIST_RESULTS_KEY, data),
            ]
        )
        return self.success_response(resp_data, status=status.HTTP_200_OK)
