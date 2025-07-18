from django.views.generic import ListView, DetailView, CreateView
from shop.models import BlogModel, BlogImageModel, BlogStatusTypeModel, WishListModel, BlogTypeModel, BlogCategoryModel
from django.contrib import messages
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import UserSubscriptionModel, UserSubscriptionTypeModel
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

class BlogGridView(ListView):
    template_name="shop/blog-grid.html"
    paginate_by=9

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["categories"] = BlogCategoryModel.objects.all()
        return context

    def get_queryset(self):
        queryset =BlogModel.objects.filter(status=BlogStatusTypeModel.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)

        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)

        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)

        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                messages.error(self.request , ("خطا در وارد کردن فیلد"))

        return queryset



class BlogDetailView(DetailView):
    model=BlogModel
    template_name="shop/blog-detail.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["extra_img"] = BlogImageModel.objects.filter(blog=self.kwargs["pk"])
        if self.request.user.subscription != UserSubscriptionTypeModel.no_subscription.value:
            subscription = UserSubscriptionModel.objects.get(user=self.request.user)
            context["ramming_days"] = subscription.get_remaining_days()
        return context
    
    def dispatch(self, request, *args, **kwargs):
        blog_obj = BlogModel.objects.get(id=kwargs["pk"])
        
        if blog_obj.type == BlogTypeModel.premium.value:
            try:
                subscription = UserSubscriptionModel.objects.get(user=request.user)
                if not subscription.is_valid():
                    messages.warning(request, "مشتری گرامی برای خواندن پست های ویژه باید اشتراک تهیه کنید.")
                    return redirect("shop:blog-grid")
            except UserSubscriptionModel.DoesNotExist:
                messages.warning(request, "مشتری گرامی برای خواندن پست های ویژه باید اشتراک تهیه کنید.")
                return redirect("shop:blog-grid")

        return super().dispatch(request, *args, **kwargs)


class AddWishListView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        blog_id = request.POST.get("blog_id")
        blog_obj = BlogModel.objects.get(status=BlogStatusTypeModel.publish.value, id=blog_id)
        user = request.user
        try:
            wishlist_obj = WishListModel.objects.get(user=user, blog_id=blog_id)
            wishlist_obj.delete()
            action = "removed"
        except WishListModel.DoesNotExist:
            WishListModel.objects.create(user=user, blog=blog_obj)
            action = "added"
        return JsonResponse({"status": "success", "action": action})
