from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product

"""A list of all the products that are available 
if we have a category slug then we will have the products of that category"""


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, "shop/product/list.html", {
        "category": category,
        "categories": categories,
        "products": products
    })


"""The detail view that has the informations about a product"""


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_form = CartAddProductForm()
    return render(request, "shop/product/detail.html", {
        "product": product,
        "cart_product_form": cart_form
    })
