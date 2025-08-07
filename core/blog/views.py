# Django Imports

from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

# Third Party
from accounts.models import UserSubscriptionModel, UserSubscriptionTypeModel
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
        context=super().get_context_data(**kwargs)
        context["extra_img"] = BlogImageModel.objects.filter(blog=self.kwargs["pk"])
        if self.request.user.is_authenticated:
            user_subscription= UserSubscriptionModel.objects.filter(user=self.request.user).exists()
            if user_subscription is True:
                subscription = UserSubscriptionModel.objects.get(user=self.request.user)
                context["ramming_days"] = subscription.get_remaining_days()
            else:
                context["ramming_days"] = "بدون اشتراک"
            context["reviews"]= ReviewModel.objects.filter(status=ReviewModel.ReviewStatusModel.accepted.value, blog__id=self.kwargs["pk"]).order_by("-created_date")
        return context
    
    def dispatch(self, request, *args, **kwargs):
        blog_obj = BlogModel.objects.get(id=kwargs["pk"])
        
        if blog_obj.type == BlogModel.BlogTypeModel.premium.value:
            try:
                subscription = UserSubscriptionModel.objects.get(user=request.user)
                if not subscription.is_valid():
                    messages.warning(request, "مشتری گرامی برای خواندن پست های ویژه باید اشتراک تهیه کنید.")
                    return redirect("blog:blog-grid")
            except UserSubscriptionModel.DoesNotExist:
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
        context["filter"] = BlogFilter(self.request.GET, queryset=BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value))
        return context


class WishListBlogPageView(ListView):
    model=WishListModel
    template_name="blog/blog_wishlist.html"
    paginate_by=9
    
    def get_queryset(self):
        queryset= self.model.objects.filter(user=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["filter"] = BlogFilter(self.request.GET, queryset=BlogModel.objects.filter(status=BlogModel.BlogStatusTypeModel.publish.value))
        return context