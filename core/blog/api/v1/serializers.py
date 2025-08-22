# third party imports
from rest_framework import serializers

# locale imports
from blog.models import BlogModel

class ListBlogApi(serializers.ModelSerializer):
    
    class Meta:
        model=BlogModel
        fields=("id", "title", "description", "type", "status", "price", "discount_percent", "image", "category", "created_date", "updated_date")