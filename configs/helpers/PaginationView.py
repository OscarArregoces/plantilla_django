from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 5
    page_query_param = 'page'


class ViewPagination(APIView):
    pagination_class = CustomPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


# class DecoratorPaginateView(ViewPagination, object):

#     def __init__(self, func):
#         self.func = func

#     def __call__(self, *args, **kwargs):
#         self.request = args[0]
#         response = self.func(request=self.request, *args, **kwargs)

#         resulst = self.paginate_queryset(response)
#         paginate_data = self.get_paginated_response(resulst).data

#         if paginate_data is None:
#             return Response("error", status.HTTP_400_BAD_REQUEST)

#         return Response(paginate_data, status.HTTP_200_OK)
    

class DecoratorPaginateView(ViewPagination, object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.request = args[0]
        response = self.func(request=self.request, *args, **kwargs)

        if isinstance(response, Response):  # Verificar si la respuesta es una instancia de Response
            queryset = response.data
            paginated_queryset = self.paginate_queryset(queryset)
            paginated_response = self.get_paginated_response(paginated_queryset)
            return Response(paginated_response.data, status=status.HTTP_200_OK)
        else:
            paginated_response = self.paginate_queryset(response)
            return Response(paginated_response, status=status.HTTP_200_OK)

