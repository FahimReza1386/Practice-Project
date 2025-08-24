# Third Party Imports
from rest_framework import serializers

# Locale Imports
from subscriptions.models import Subscriptions

class ApiListSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subscriptions
        fields=("id", "name", "price", "discount_percent", "days", "type")