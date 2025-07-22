from django.shortcuts import render, get_object_or_404, redirect
from .models import PaymentModel
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from idpay.api import IDPayAPI
import requests
import json

def payment_init():
    base_url = config('BASE_URL', default='http://127.0.0.1', cast=str)
    api_key = config('IDPAY_API_KEY', default='', cast=str)
    sandbox = config('IDPAY_SANDBOX', default=True, cast=bool)

    return IDPayAPI(api_key, base_url, sandbox)

def home(request):
    payments = PaymentModel.objects.all()
    return render(request, 'home.html', {'payments': payments})

def payment_start(request):
    if request.method == 'POST':

        amount = request.POST.get('amount')
        user_subs= request.POST.get("user_subs_type")
        user= request.user
        payer = {
            'phone': user.phone_number,
            'first_name': user.first_name,
        }


        record = PaymentModel(user=user, user_subscriptiontype=user_subs, amount=int(amount))
        record.save()

        idpay_payment = payment_init()
        result = idpay_payment.payment(amount, 'payment/return', payer)

        if 'id' in result:
            record.status = 1
            record.payment_id = result['id']
            record.save()

            return redirect(result['link'])

        else:
            txt = result['message']
    else:
        txt = "Bad Request"
    return render(request, 'error.html', {'txt': txt})



@csrf_exempt
def payment_return(request):
    if request.method == 'POST':

        pid = request.POST.get('id')
        status = request.POST.get('status')
        pidtrack = request.POST.get('track_id')
        amount = request.POST.get('amount')
        card = request.POST.get('card_no')
        date = request.POST.get('date')

        if Payment.objects.filter(payment_id=pid, amount=amount, status=status).count() == 1:
            idpay_payment = payment_init()

            payment = PaymentModel.objects.get(payment_id=pid, amount=amount)
            payment.status = status
            payment.date = str(date)
            payment.card_number = card
            payment.idpay_track_id = pidtrack
            payment.save()

            if str(status) == '3':
                result = idpay_payment.verify(pid, payment.order_id)

                if 'status' in result:

                    payment.status = result['status']
                    payment.bank_track_id = result['payment']['track_id']
                    payment.save()

                    return render(request, 'error.html', {'txt': result['message']})

                else:
                    txt = result['message']

            else:
                txt = "Error Code : " + str(status) + "   |   " + "Description : " + idpay_payment.get_status(status)

        else:
            txt = "Order Not Found"

    else:
        txt = "Bad Request"

    return render(request, 'error.html', {'txt': txt})



def payment_check(request, pk):

    payment = PaymentModel.objects.get(pk=pk)

    idpay_payment = payment_init()
    result = idpay_payment.inquiry(payment.payment_id, payment.order_id)

    if 'status' in result:

        payment.status = result['status']
        payment.idpay_track_id = result['track_id']
        payment.bank_track_id = result['payment']['track_id']
        payment.card_number = result['payment']['card_no']
        payment.date = str(result['date'])
        payment.save()

    return render(request, 'error.html', {'txt': result['message']})


    def inquiry(self, id):

        url = 'https://api.idpay.ir/v1.1/payment/inquiry'

        data = {
            'id': id,
        }

        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.api_key,
            'X-SANDBOX': '1' if self.sandbox else '0'
        }

        request = requests.post(url, data=json.dumps(data), headers=headers)

        if request.status_code == 200:
            response = request.json()
            response['message'] = "Status: " + str(response['status']) + " (" + self.get_status(response['status']) + ")"

            return response

        else:
            response = request.json()
            message = "Http status Code : " + str(request.status_code) + "   |   " + "Error Code : " + str(response['error_code']) + "   |   " + "Description : " + str(response['error_message'])

        return {'message': message}
    