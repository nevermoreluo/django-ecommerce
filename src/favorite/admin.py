from django.contrib import admin

# Register your models here.
from .models import Favorite, FavoriteItem


class FavoriteItemInline(admin.TabularInline):
    model = FavoriteItem


class FavoriteAdmin(admin.ModelAdmin):
    inlines = [
        FavoriteItemInline
    ]

    class Meta:
        model = Favorite


admin.site.register(Favorite, FavoriteAdmin)
# admin.site.register(Favorite)
# admin.site.register(FavoriteItem)
