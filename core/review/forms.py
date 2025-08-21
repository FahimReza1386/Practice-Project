# Django Imports
from django import forms

# Locale Imports

from blog.models import BlogModel
from .models import ReviewModel

class CreateReviewForm(forms.ModelForm):
    class Meta:
        model= ReviewModel
        fields=("blog", "description", "rate")
        error_messages={
            'description' : {
                'required' : "فیلد توضیحات اجباری است",
            }
        }

    def clean(self):
        cleaned_data= super().clean()
        blog= cleaned_data.get("blog")

        try:
            BlogModel.objects.get(id=blog.id, status=BlogModel.BlogStatusTypeModel.publish.value)
        except BlogModel.DoesNotExist:
            return forms.ValidationError("پست انتخاب شده پیدا نشد .")

        return cleaned_data

class ReplyReviewForm(forms.ModelForm):
    class Meta:
        model= ReviewModel
        fields=("blog", "description", "rate", "parent")
        error_messages={
            'description' : {
                'required' : "فیلد توضیحات اجباری است",
            }
        }

    def clean(self):
        cleaned_data= super().clean()
        blog= cleaned_data.get("blog")

        try:
            BlogModel.objects.get(id=blog.id, status=BlogModel.BlogStatusTypeModel.publish.value)
        except BlogModel.DoesNotExist:
            return forms.ValidationError("پست انتخاب شده پیدا نشد .")

        return cleaned_data