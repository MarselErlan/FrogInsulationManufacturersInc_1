# from django.urls import path
# from PaymentsApp.views import CheckOut, PaymentSuccessful, paymentFailed, paypal_ipn_listener
#
# urlpatterns = [
#     path('checkout/<int:product_id>/', CheckOut, name='checkout'),
#     path('payment-success/<int:product_id>/<uuid:transaction_id>/', PaymentSuccessful, name='payment-success'),
#     path('payment-failed/<int:product_id>/<uuid:transaction_id>/', paymentFailed, name='payment-failed'),
#     path('paypal-ipn/', paypal_ipn_listener, name='paypal-ipn'),
# ]
