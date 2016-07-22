from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from .models import Cart, CartItem
from products.models import Variation
from orders.models import UserCheckout
from orders.mixins import CartOrderMixin
from orders.forms import GuestCheckoutForm


class ItemCountView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id is None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                # print(dir(cart))
                count = cart.items.count()
                # cart_items = cart.cartitem_set.all()
                print('count:', count)
                # print(cart_items[0].pk, type(cart_items[0]), dir(cart_items[0]))
            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "cart/view.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(5 * 60 * 60)  # 300 = 5 minutes
        cart_id = self.request.session.get("cart_id")
        print('get_objecct', cart_id)
        if self.request.user.is_authenticated():
            userCart, created = Cart.objects.get_or_create(
                user=self.request.user)
        else:
            userCart = None
        if cart_id is None and userCart:
            cart = userCart
        elif cart_id is None and not userCart:
            cart = Cart()
            cart.tax_percentage = 0.075
            cart.save()
            print('new', cart.id)
        elif cart_id is not None and userCart:
            # guestCart = Cart.objects.get(id=cart_id)
            # guset_items = guestCart.cartitem_set.all()
            # user_items = userCart.cartitem_set.all()
            # for item in guset_items:
            #     if item not in user_items:
            #         c, cre = Cart.objects.get_or_create(items=item)
            #         userCart.save()
            cart = userCart
        else:
            cart = Cart.objects.get(id=cart_id)
        self.request.session["cart_id"] = cart.id
        return cart

    def _try(self, a, b=None):
        try:
            return eval(a)
        except:
            return b

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        flash_message = ""
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, item=item_instance)
            if created:
                flash_message = "Successfully added to the cart"
                item_added = True
            if delete_item:
                flash_message = "Item removed successfully."
                cart_item.delete()
            else:
                if not created:
                    flash_message = "Quantity has been updated successfully."
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("cart"))
                # return cart_item.cart.get_absolute_url()

        if request.is_ajax():
            # total = self._try('cart_item.line_item_total')
            try:
                total = cart_item.line_item_total
            except:
                total = None
            # subtotal = self._try('cart_item.cart.subtotal')
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None
            # cart_total = self._try('cart_item.cart.total')
            try:
                cart_total = cart_item.cart.total
            except:
                cart_total = None
            # tax_total = self._try('cart_item.cart.tax_total')
            try:
                tax_total = cart_item.cart.tax_total
            except:
                tax_total = None
            # total_items = self._try('cart_item.cart.items.count()', 0)
            try:
                total_items = cart_item.cart.items.count()
            except:
                total_items = 0

            data = {
                "deleted": delete_item,
                "item_added": item_added,
                "line_total": total,
                "subtotal": subtotal,
                "cart_total": cart_total,
                "tax_total": tax_total,
                "flash_message": flash_message,
                "total_items": total_items
            }

            return JsonResponse(data)
        context = {
            "object": self.get_object(),
        }
        template = self.template_name
        return render(request, template, context)


class CheckoutView(CartOrderMixin, FormMixin, DetailView):
    model = Cart
    template_name = "cart/checkout_view.html"
    form_class = GuestCheckoutForm

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart is None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get("user_checkout_id")
        if self.request.user.is_authenticated():
            user_can_continue = True
            user_checkout, created = UserCheckout.objects.get_or_create(
                email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.save()
            # context["client_token"] = user_checkout.get_client_token()
            self.request.session["user_checkout_id"] = user_checkout.id
        elif user_check_id is None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        else:
            pass


        if user_check_id:
            user_can_continue = True
        #     if not self.request.user.is_authenticated():  # GUEST USER
        #         user_checkout_2 = UserCheckout.objects.get(id=user_check_id)
        #         context["client_token"] = user_checkout_2.get_client_token()

        # if self.get_cart() is not None:
        context["order"] = self.get_order()
        context["user_can_continue"] = user_can_continue
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_checkout, created = UserCheckout.objects.get_or_create(
                email=email)
            request.session["user_checkout_id"] = user_checkout.id
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart == None:
            return redirect("cart")
        new_order = self.get_order()
        user_checkout_id = request.session.get("user_checkout_id")
        if user_checkout_id is not None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if new_order.billing_address == None or new_order.shipping_address == None:
                return redirect("order_address")
            new_order.user = user_checkout
            new_order.save()
        return get_data
