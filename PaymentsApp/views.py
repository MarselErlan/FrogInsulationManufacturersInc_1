# from django.http import HttpResponse
# from django.shortcuts import render, get_object_or_404
# from MainWepSite.models import Product
# from PaymentsApp.models import Transaction
# from paypal.standard.forms import PayPalPaymentsForm
# from django.conf import settings
# import uuid
# from django.urls import reverse
#
#
# def CheckOut(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     # Создание уникального ID транзакции
#     transaction_id = str(uuid.uuid4())
#
#     transaction = Transaction.objects.create(
#         user=request.user,
#         product=product,
#         amount=product.price,
#         transaction_id=transaction_id,
#         status='Initiated'
#     )
#
#     host = request.get_host()
#
#     paypal_checkout = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': product.price,
#         'item_name': product.name,
#         'invoice': transaction_id,
#         'currency_code': 'USD',
#         'notify_url': f"http://{host}{reverse('paypal-ipn')}",
#         'return_url': f"http://{host}{reverse('payment-success', kwargs={'product_id': product.id, 'transaction_id': transaction_id})}",
#         'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'product_id': product.id, 'transaction_id': transaction_id})}",
#     }
#
#     paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
#
#     context = {
#         'product': product,
#         'paypal': paypal_payment
#     }
#
#     return render(request, 'templates_for_payment/checkout.html', context)

#
# def PaymentSuccessful(request, product_id, transaction_id):
#     product = get_object_or_404(Product, id=product_id)
#     transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
#
#     transaction.status = 'Completed'
#     transaction.updated_by = request.user
#     transaction.save()
#
#     return render(request, 'templates_for_payment/payment-success.html', {'product': product})
#
#
# def paymentFailed(request, product_id, transaction_id):
#     product = get_object_or_404(Product, id=product_id)
#     transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
#
#     transaction.status = 'Failed'
#     transaction.updated_by = request.user
#     transaction.save()
#
#     return render(request, 'templates_for_payment/payment-failed.html', {'product': product})
#
#
#
# from django.views.decorators.csrf import csrf_exempt
# from paypal.standard.ipn.signals import valid_ipn_received
#
# @csrf_exempt
# def paypal_ipn_listener(request):
#     def update_transaction(sender, **kwargs):
#         ipn_obj = sender
#         transaction = Transaction.objects.get(transaction_id=ipn_obj.invoice)
#         if ipn_obj.payment_status == 'Completed':
#             transaction.status = 'Completed'
#         else:
#             transaction.status = 'Failed'
#         transaction.save()
#
#     valid_ipn_received.connect(update_transaction)
#     return HttpResponse('OK')
