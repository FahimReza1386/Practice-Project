# Third Party Imports
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer


# Django Imports
from django.utils.translation import gettext_lazy as _


class ObtainPairTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data =super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"detail": "user is not verified ."})
        validated_data["user_id"] = self.user.id
        return validated_data