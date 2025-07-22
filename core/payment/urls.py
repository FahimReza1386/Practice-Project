from django.urls import path
from . import views

app_name="payment"
urlpatterns = [
    path('', views.StartPaymentView.as_view(), name='request-payment'),
    path('verify', views.PaymentVerifyView.as_view(), name='verify-payment'),
]