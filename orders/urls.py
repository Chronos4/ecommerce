from django.urls import path
from .views import order_create, admin_order_detail


app_name = "order"

urlpatterns = [
    path("create", order_create, name="create"),
    path("admin/order/<order_id>", admin_order_detail, name="admin_order_detail"),
    #path("admin/order/<order_id>/pdf/",admin_order_pdf, name="admin_order_pdf")
]
