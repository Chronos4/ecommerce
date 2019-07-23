from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                # clear the cart
                cart.clear()
                # launch asynchronous task
                order_created.delay(order.id)  # set the order in the session
                # redirect to the payment
                request.session["order_id"] = order.id
        return render(request,
                      'orders/order/created.html',
                      {'order': order})
    else:
        form = OrderForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})
