
from cart.models import Cart
from products.models import Product
from django import template
from random import choice, random

register = template.Library()


@register.assignment_tag
def get_cart_items(request, *args, **kwargs):
    cart_id = request.session.get("cart_id")
    if request.user.is_authenticated():
        userCart, created = Cart.objects.get_or_create(user=request.user)
        # cart_items = userCart.cartitem_set.all()
        return userCart
    if cart_id:
        cart = Cart.objects.get(id=cart_id)
        # cart_items = cart.cartitem_set.all()
        return cart


@register.assignment_tag
def get_random_items(cart, *args, **kwargs):
    if cart:
        if cart.cartitem_set.count():
            item = choice(cart.cartitem_set.all())
            instance = item.item.product
            related_items = sorted(Product.objects.get_related(instance), key=lambda x: random())[:4]
            return related_items
    return Product.objects.order_by('?')[:4]
