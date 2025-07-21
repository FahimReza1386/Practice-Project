from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from shop.models import BlogCategoryModel
from accounts.models import User, UserSubscriptionTypeModel, UserSubscriptionModel
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.


class HomeView(TemplateView):
    template_name = "website/home.html"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["categories"] = BlogCategoryModel.objects.all()
        return context
    
class ContactView(TemplateView):
    template_name = "website/contact.html"

class SubscriptionsView(TemplateView):
    template_name= "website/subscriptions.html"

class AcceptedRequestBuy(View):
    
    def get(self, request, *args, **kwargs):
        id=self.kwargs["pk"]

        if id ==1:
            user=User.objects.get(id=self.request.user.id)
            user.subscription = UserSubscriptionTypeModel.month_1.value
            user.save()

            UserSubscriptionModel.objects.create(user=user, subs_type=UserSubscriptionTypeModel.month_1.value, start_date=timezone.now(), end_date=timezone.now() + timedelta(days=30))
            messages.success(request, "خرید شما با موفقیت انجام شد ...")
            return redirect(reverse_lazy("website:home"))


        elif id==2:
            user=User.objects.get(id=self.request.user.id)
            user.subscription = UserSubscriptionTypeModel.month_3.value
            user.save()

            UserSubscriptionModel.objects.create(user=user, subs_type=UserSubscriptionTypeModel.month_3.value, start_date=timezone.now(), end_date=timezone.now() + timedelta(days=60))
            messages.success(request, "خرید شما با موفقیت انجام شد ...")
            return redirect(reverse_lazy("website:home"))


        elif id==3:
            user=User.objects.get(id=self.request.user.id)
            user.subscription = UserSubscriptionTypeModel.month_3.value
            user.save()

            UserSubscriptionModel.objects.create(user=user, subs_type=UserSubscriptionTypeModel.month_3.value, start_date=timezone.now(), end_date=timezone.now() + timedelta(days=90))
            messages.success(request, "خرید شما با موفقیت انجام شد ...")
            return redirect(reverse_lazy("website:home"))

        return HttpResponse({"detail" :"انجام شد .."})