from django import forms
from .models import ReviewModel
from shop.models import BlogModel, BlogStatusTypeModel

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
            BlogModel.objects.get(id=blog.id, status=BlogStatusTypeModel.publish.value)
        except BlogModel.DoesNotExist:
            return forms.ValidationError("پست انتخاب شده پیدا نشد .")

        return cleaned_data