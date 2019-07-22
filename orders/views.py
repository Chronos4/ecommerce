from django.shortcuts import render
from .forms import OrderForm
from .tasks import order_created

def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order,
                                         product=item["product"],
                                         price=item["price"],
                                         quantity=item["quantity"])
                # clear the cart
                cart.clear()
                # launch asynchronous task
                order_created.delay(order.id)
        return rendre(request, "orders/order/created.html", {"order": order})
    else:
        form = OrderForm()
    return render(request, "orders/order/create.html", {"cart": cart, "form": form})
