# Django Imports

from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

# Locale Imports

from .models import PaymentModel
from subscriptions.models import Subs_Buy, Subscriptions
from .zarinpal_client import ZarinPalSandBox
 
class StartPaymentView(View):
    def post(self, request, *args, **kwargs):
        amount = request.POST.get("amount")
        subs_id = request.POST.get("subs_id")
        user = request.user
        subscriptions = Subscriptions.objects.get(id=subs_id)
        
        active_subscription = Subs_Buy.objects.filter(user=user, is_active=True).exists()
        
        if active_subscription:
            messages.error(request, "مشتری گرامی شما اشتراک فعال دارید در صورت تمام شدن میتوانید مجدد خرید کنید..")
            return redirect(reverse_lazy("dashboard:home"))
        
        zarinpal = ZarinPalSandBox()
        response = zarinpal.payment_request(float(amount))
        
        if not response.get("data") or "authority" not in response["data"]:
            messages.error(request, "خطا در ایجاد درخواست پرداخت")
            return redirect(reverse_lazy("dashboard:home"))
            
        data = response["data"]
        authority = data["authority"]
        
        PaymentModel.objects.create(
            authority_id=authority,
            amount=amount,
            user_subscriptiontype=subscriptions
        )
        
        payment_url = zarinpal.generate_payment_url(authority=authority)
        return HttpResponseRedirect(payment_url)


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
            user_subs= Subs_Buy.objects.create(user=request.user, subscription=payment_obj.user_subscriptiontype, start_date=timezone.now(), end_date=timezone.now() + timedelta(days=payment_obj.user_subscriptiontype.days), is_active=True)
            user_subs.save()
            messages.success(request, "مشتری گرامی پرداخت شما با موفقیت انجام شد و شما دسترسی های لازم رو دارد.")
            return redirect(reverse_lazy("dashboard:home"))
        else:
            payment_obj.status= PaymentModel.PaymentStatusModel.failed.value
            payment_obj.save()
            messages.success(request, "مشتری گرامی درخواست شما ناموفق بود بار دیگر تلاش کنید.")
            return redirect(reverse_lazy("dashboard:home"))