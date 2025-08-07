import django_filters
from django import forms
from .models import BlogModel, BlogCategoryModel
from django.db.models import Q

class BlogFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    IMAGE_CHOICES = [
        ('A', 'عکس دار'),
    ]
    IS_SALE_CHOICES = [
        ('A', 'تخفیف دار'),
    ]
    image = django_filters.MultipleChoiceFilter(
        choices=IMAGE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        method='filter_image'
    )
    is_sale = django_filters.MultipleChoiceFilter(
        choices=IS_SALE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        method='filter_is_sale'
    )

    class Meta:
        model= BlogModel
        fields= ["title", "price__lt", "price__gt", "category", "type", "image", "is_sale"]

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.form.fields['title'].widget.attrs.update({'class': 'form-control p-1', 'placeholder': 'جستجو ..'})
            self.form.fields['category'].widget.attrs.update({'class': 'form-control p-1'})
            self.form.fields['type'].widget.attrs.update({'class': 'form-control p-1'})
            self.form.fields['price__lt'].widget.attrs.update({'class': 'form-control p-1', 'placeholder': 'تا ۰ تومان'})
            self.form.fields['price__gt'].widget.attrs.update({'class': 'form-control p-1', 'placeholder': 'از ۰ تومان'})

    def filter_image(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(image__isnull=False) & ~Q(image='blogs/image.jpg') |  # تصویر اصلی غیر پیش‌فرض باشد
                Q(blogimagemodel__isnull=False)
            ).distinct()
        return queryset

    def filter_is_sale(self, queryset, name, value):
        if value:
            return queryset.filter(discount_percent__gt=0)
        return queryset