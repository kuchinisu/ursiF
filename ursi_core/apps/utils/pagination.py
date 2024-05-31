from rest_framework.pagination import PageNumberPagination
from ursi_core.apps.user.models import UserAccount


class SmallSetPagination(PageNumberPagination):
    page_query_param = 'p'
    page_size = 7
    page_size_query = 'page_size'
    max_page_size = 7

class MediumSetPagination(PageNumberPagination):
    page_query_param = 'p'
    page_size = 15
    page_size_query = 'page_size'
    max_page_size = 15

class LargeSetPagination(PageNumberPagination):
    page_query_param = 'p'
    page_size = 24
    page_size_query = 'page_size'
    max_page_size = 24
