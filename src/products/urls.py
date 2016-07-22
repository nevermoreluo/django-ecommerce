# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from django.conf.urls import url
from .views import ProductDetailView, ProductListView, VariationListView

urlpatterns = [
    # Examples:
    url(r'^$', ProductListView.as_view(), name='products'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^(?P<pk>\d+)/inventory/$',
        VariationListView.as_view(), name='product_inventory'),
]
