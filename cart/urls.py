from django.urls import path
from .views import cart_add, cart_detail, cart_remove

app_name = "cart"

urlpatterns = [
    path("", cart_detail, name="detail"),
    path("add/<product_id>", cart_add, name="add"),
    path("remove/<product_id>", cart_remove, name="remove")
]
