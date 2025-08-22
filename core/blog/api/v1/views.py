# django imports
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
# locale imports
from .serializers import ListBlogApi
from .paginations import BlogPagination
from blog.models import BlogModel
from blog.filters import BlogFilter

class ListBlogRestView(ListCreateAPIView):
    serializer_class=ListBlogApi
    pagination_class=BlogPagination

    filter_backends=[DjangoFilterBackend,]
    filterset_class=BlogFilter


    def get_queryset(self):
        queryset= BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value).order_by("-created_date")
        return queryset
    

class RetrieveBlogRestView(RetrieveUpdateDestroyAPIView):
    serializer_class=ListBlogApi
    
    def get_queryset(self):
        queryset= BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value).order_by("-created_date")
        return queryset