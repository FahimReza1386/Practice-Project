# Django Imports

from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

# Third Party
from subscriptions.models import Subs_Buy, Subscriptions
from review.models import ReviewModel
from jalali_date import datetime2jalali, date2jalali
from blog.models import BlogModel, BlogImageModel, WishListModel, BlogCategoryModel
from blog.filters import BlogFilter


class BlogGridView(ListView):
    template_name="blog/blog-grid.html"
    paginate_by=9

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["categories"] = BlogCategoryModel.objects.all()
        context["filter"] = BlogFilter(self.request.GET, queryset=BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value))
        return context

    def get_queryset(self):
        queryset =BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value)
        return queryset



class BlogDetailView(DetailView):
    model=BlogModel
    template_name="blog/blog-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_img"] = BlogImageModel.objects.filter(blog=self.kwargs["pk"])
    
        context["reviews"] = ReviewModel.objects.filter(
            status=ReviewModel.ReviewStatusModel.accepted.value,
            blog__id=self.kwargs["pk"],
            parent=None
        ).order_by("-created_date")
    
        return context
        
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "برای دسترسی به این بخش باید وارد شوید.")
            return redirect("blog:blog-grid")
        
        try:
            blog_obj = BlogModel.objects.get(id=kwargs["pk"])
        except BlogModel.DoesNotExist:
            messages.warning(request, "پست مورد نظر یافت نشد.")
            return redirect("blog:blog-grid")
        
        if blog_obj.type == BlogModel.BlogTypeModel.premium.value:
            if not Subs_Buy.objects.filter(user=request.user, is_active=True).exists():
                messages.warning(request, "مشتری گرامی برای خواندن پست های ویژه باید اشتراک تهیه کنید.")
                return redirect("blog:blog-grid")
        
        return super().dispatch(request, *args, **kwargs)

class AddWishListView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        blog_id = request.POST.get("blog_id")
        blog_obj = BlogModel.objects.get(status=BlogModel.BlogStatusTypeModel.publish.value, id=blog_id)
        user = request.user
        try:
            wishlist_obj = WishListModel.objects.get(user=user, blog_id=blog_id)
            wishlist_obj.delete()
            action = "removed"
        except WishListModel.DoesNotExist:
            WishListModel.objects.create(user=user, blog=blog_obj)
            action = "added"
        return JsonResponse({"status": "success", "action": action})

class CategoriesView(ListView):
    template_name="blog/categories.html"
    model=BlogModel
    paginate_by=9

    def get_queryset(self):
        queryset = self.model.objects.filter(category=self.kwargs["pk"])

        return queryset
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filtered_queryset = BlogFilter(self.request.GET, queryset=queryset)
        context['object_list'] = filtered_queryset.qs
        context['filter'] = filtered_queryset
        return context


class WishListBlogPageView(ListView):
    model=BlogModel
    template_name="blog/blog_wishlist.html"
    paginate_by=9
    
    def get_queryset(self):
        blog_ids = WishListModel.objects.filter(user=self.request.user).values_list('blog_id', flat=True)
        queryset = self.model.objects.filter(
            id__in=blog_ids,
            status=BlogModel.BlogStatusTypeModel.publish.value
        )
        return queryset
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filtered_queryset = BlogFilter(self.request.GET, queryset=queryset)
        context['object_list'] = filtered_queryset.qs
        context['filter'] = filtered_queryset
        return context