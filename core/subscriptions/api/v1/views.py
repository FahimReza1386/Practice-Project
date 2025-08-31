# Third Party Imports
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

# Locale Imports
from .serializers import ApiListSubscriptionsSerializer
from subscriptions.models import Subscriptions
from blog.filters import SubscriptionsFilter


class ApiListSubscriptionView(ListAPIView):
    serializer_class = ApiListSubscriptionsSerializer
    filter_backends=[DjangoFilterBackend,]
    filterset_class=SubscriptionsFilter

    def get_queryset(self):
        queryset= Subscriptions.objects.filter(type=Subscriptions.SubscriptionType.publish.value)
        return queryset
    
class ApiCreateSubscriptionView(CreateAPIView):
    serializer_class = ApiListSubscriptionsSerializer
    filter_backends=[DjangoFilterBackend,]
    filterset_class=SubscriptionsFilter

    def get_queryset(self):
        queryset= Subscriptions.objects.filter(type=Subscriptions.SubscriptionType.publish.value)
        return queryset
    

class ApiDetailSubscriptionView(UpdateAPIView):
    permission_classes=[IsAuthenticated, IsAdminUser]
    serializer_class = ApiListSubscriptionsSerializer
    
    def get_queryset(self):
        queryset= Subscriptions.objects.filter(type=Subscriptions.SubscriptionType.publish.value)
        return queryset
    
class ApiDeleteSubscriptionView(DestroyAPIView):
    permission_classes=[IsAuthenticated, IsAdminUser]
    serializer_class = ApiListSubscriptionsSerializer
    
    def get_queryset(self):
        queryset= Subscriptions.objects.filter(type=Subscriptions.SubscriptionType.publish.value)
        return queryset