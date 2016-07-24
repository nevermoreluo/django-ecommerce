from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
# Create your models here.
from products.models import Variation


class FavoriteItem(models.Model):
    favorite = models.ForeignKey("Favorite")
    variation = models.ForeignKey(Variation)
    old_price = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.variation.get_title()

    def get_price(self):
        return self.variation.get_price()


def variation_post_save_receiver(sender, instance, created, *args, **kwargs):
    variation = instance
    if not created and variation.favoriteitem_set.count():
        price = int(variation.get_price())
        old = int(variation.favoriteitem_set.first().old_price)
        if price < old:
            favorites = variation.favorite_set.all()
            if favorites:
                for fav in favorites:
                    print('got one ', fav.user.username)


post_save.connect(variation_post_save_receiver, sender=Variation)


class Favorite(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    favoriteItem = models.ManyToManyField(Variation, through=FavoriteItem)

    def __str__(self):
        return self.user.username + "'s favorite"
