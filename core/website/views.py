from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from shop.models import BlogCategoryModel
# Create your views here.


class HomeView(TemplateView):
    template_name = "website/home.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["categories"] = BlogCategoryModel.objects.all()
        return context
class ContactView(TemplateView):
    template_name = "website/contact.html"