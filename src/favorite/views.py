from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect, Http404
# Create your views here.
from products.models import Variation
from .models import Favorite, FavoriteItem
from orders.mixins import LoginRequiredMixin


class FavoriteView(LoginRequiredMixin, SingleObjectMixin, View):
    models = Favorite
    template_name = "favorite/favorite.html"

    def get_object(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            userFavorite, created = self.models.objects.get_or_create(
                user=self.request.user)
            return userFavorite
        else:
            return redirect('login')

    def get(self, request, *args, **kwargs):
        favorite = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        item_added = False
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            favorite_item, created = FavoriteItem.objects.get_or_create(
                favorite=favorite, variation=item_instance)
            if created:
                item_added = True
            if delete_item:
                favorite_item.delete()
            else:
                favorite_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("favorite"))

        context = {
            "object": self.get_object(),
        }
        template = self.template_name
        return render(request, template, context)
