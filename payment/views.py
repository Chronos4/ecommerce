from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEICER_EMAIL,
        "ammount": '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
        "item_name": f"Order {order.id}",
        "invoice": str(order.id),
        "currency_code": "EUR",
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return_url": f"http://{host}{reverse('payment:done')}",
        "cancel_return": f"http://{host}{reverse('payment:canceled')}"
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "payment/process.html", {"order": order, "form": form})


@csrf_exempt
def payment_done(request):
    return render(request, "payment/done.html")


@csrf_exempt
def payment_canceled(request):
    return render(request, "payment/canceled.html")
