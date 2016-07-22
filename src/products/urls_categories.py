# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from django.conf.urls import url

from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    # Examples:
    # url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^$', CategoryListView.as_view(), name='categories'),
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(),
        name='category_detail'),
]
