# django imports
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# locale imports
from .serializers import ListBlogApi
from .paginations import BlogPagination
from blog.models import BlogModel
from blog.filters import BlogFilter

class ListBlogRestView(ListAPIView):
    serializer_class=ListBlogApi
    pagination_class=BlogPagination

    filter_backends=[DjangoFilterBackend,]
    filterset_class=BlogFilter


    def get_queryset(self):
        queryset= BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value).order_by("-created_date")
        return queryset
    
class CreateBlogRestView(CreateAPIView):
    serializer_class=ListBlogApi
    pagination_class=BlogPagination

    filter_backends=[DjangoFilterBackend,]
    filterset_class=BlogFilter


    def get_queryset(self):
        queryset= BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value).order_by("-created_date")
        return queryset
    
class DetailBlogRestView(UpdateAPIView):
    serializer_class=ListBlogApi
    pagination_class=BlogPagination

    filter_backends=[DjangoFilterBackend,]
    filterset_class=BlogFilter


    def get_queryset(self):
        queryset= BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value).order_by("-created_date")
        return queryset
    

class DeleteBlogRestView(DestroyAPIView):
    serializer_class=ListBlogApi
    permission_classes=[IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset= BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value).order_by("-created_date")
        return queryset