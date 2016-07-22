from django.contrib import admin

# Register your models here.
from .models import Product, Variation, ProductImage, Category, ProductFeatured


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 10


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0
    max_num = 10


class ProductAdmin(admin.ModelAdmin):
    # list_display可以设置，为admin内的添加标题列的内容
    list_display = ['__str__', 'price']
    # inlines接受inlines列表（TabularInline以及StackedInline两类）
    inlines = [
        ProductImageInline,
        VariationInline,
    ]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

# admin.site.register(ProductImage)

# admin.site.register(Category)

admin.site.register(ProductFeatured)
