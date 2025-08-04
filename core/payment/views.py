# Django Imports

from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

# Third Party

from .models import PaymentModel
from accounts.models import UserSubscriptionModel
from .zarinpal_client import ZarinPalSandBox



class StartPaymentView(View):

    def post(self, request, *args, **kwargs):
        amount= request.POST.get("amount")
        subs_type= request.POST.get("subs_type")
        user = request.user
        user_subscription= UserSubscriptionModel.objects.filter(user=user).exists()
        if user_subscription is not True:
            zarinpal= ZarinPalSandBox()
            response= zarinpal.payment_request(float(amount))
            data= response["data"]
            authority= data["authority"]
            PaymentModel.objects.create(authority_id=authority, amount=amount, user_subscriptiontype=subs_type)
            payment_url = zarinpal.generate_payment_url(authority=authority)
            return HttpResponseRedirect(payment_url)
        else:
            messages.error(request, "مشتری گرامی شما اشتراک فعال دارید در صورت تمام شدن میتوانید مجدد خرید کنید..")
            return redirect(reverse_lazy("dashboard:home"))
    
class PaymentVerifyView(View):
    def get(self, request, *args, **kwargs):
        authority_id= request.GET.get("Authority")
        payment_obj= get_object_or_404(PaymentModel, authority_id=authority_id)
        zarinpal= ZarinPalSandBox()
        response= zarinpal.payment_verify(int(payment_obj.amount), payment_obj.authority_id)
        data= response["data"]

        if data["code"] == 100 or data["code"] == 101:
            payment_obj.ref_id= data["ref_id"]
            payment_obj.response_code= data["code"]
            payment_obj.status= PaymentModel.PaymentStatusModel.success.value
            payment_obj.save()
            user_subs= UserSubscriptionModel.objects.create(user=self.request.user, subs_type=payment_obj.user_subscriptiontype, start_date=timezone.now(), is_active=True)
            user_subs.save()
            messages.success(request, "مشتری گرامی پرداخت شما با موفقیت انجام شد و شما دسترسی های لازم رو دارد.")
            return redirect(reverse_lazy("dashboard:home"))
        else:
            payment_obj.status= PaymentModel.PaymentStatusModel.failed.value
            payment_obj.save()
            messages.success(request, "مشتری گرامی درخواست شما ناموفق بود بار دیگر تلاش کنید.")
            return redirect(reverse_lazy("dashboard:home"))