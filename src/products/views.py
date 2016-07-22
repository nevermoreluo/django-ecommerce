# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.
from random import random
from .models import Product, Variation, Category
from django.utils import timezone
from .forms import VariationInventoryFormSet
from .mixins import LoginRequiredMixin  # ,StaffRequiredMixin


class CategoryListView(ListView):

    # 子类化listview通用视图，获得产品种类视图列表
    # 也可以自己写视图函数
    # model给定一个模型类，
    # 给定model = Foo的同时指定了queryset = Foo.objects.all()，此时的objects为默认管理器
    # 即当Foo中objects被重写，或者有多个管理器时，建议需要给定一个指定的queryset
    model = Category
    # 给定一个查询集，如果没有则默认使用model返回的查询集
    queryset = Category.objects.all()
    # 给定一个视图关联的模板，
    # 默认为<appname>/<classname(不包含view，小写，中间以_链接)>.html
    template_name = "products/product_list.html"


class CategoryDetailView(DetailView):
    # 子类化DetailView通用视图，获得产品种类视图详情
    model = Category

    def get_context_data(self, *args, **kwargs):
        # 继承自django.views.generic.base.ContextMixin，
        # 重写该方法，为调用的模板以字典传递自定义参数
        # super函数返回原有的context
        context = super(CategoryDetailView, self).get_context_data(
            *args, **kwargs)

        # get_object方法继承自SingleObjectMixin
        # 方法由urls匹配回传的参数，调用queryset（没有则get_queryset()）
        # 查找pk或者slug，slug为备选
        # 从1.8开始django指定类属性query_pk_and_slug为True时，查找将执行pk和slug都满足的对象
        obj = self.get_object()
        # 通过默认的related_name可以反向查询对应关联的所有实例的查询集
        product_set = obj.product_set.all()
        # 通过指定的related_name查询，可查看Category类确认
        default_products = obj.default_category.all()
        # 两个queryset支持| 或运算，但是结果不去重，可使用distinct去重
        # 但是注意distinct不能与order_by同时使用
        products = (product_set | default_products).distinct()
        # 以字典键值形式为context传入参数
        context["products"] = products
        return context


class VariationDetailView(DetailView):
    model = Variation
    template_name = 'products/product_detail.html'

    # def get_object(self, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     variation = Variation.get_object_or_404(pk=pk)
    #     return variation

    def get_context_data(self, *args, **kwargs):
        context = super(VariationDetailView, self).get_context_data(
            *args, **kwargs)
        variation = self.get_object()
        product = variation.product
        related = sorted(
            Product.objects.get_related(product), key=lambda x: random())[:6]
        context = {'product': product,
                   'related': related,
                   'variation': variation,
                   'object': product,
                   }
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(
            *args, **kwargs)
        instance = self.get_object()
        # 注意通常情况下，下面两组实现的效果是等价的，order_by('?')方法获得一个随机的queryset
        # 但是get_related方法内使用了distinct方法，它与order_by不兼容。
        context['related'] = sorted(
            Product.objects.get_related(instance), key=lambda x: random())[:6]
        # context['related'] = Product.objects.get_related(
        #     instance).order_by('?')[:6]
        print(context)
        return context


class VariationListView(LoginRequiredMixin, ListView):

    # 继承自LoginRequiredMixin，检测用户是否登陆，如果未登陆则无法访问
    model = Variation
    template_name = 'products/variation_list.html'
    queryset = Variation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(
            *args, **kwargs)
        # 给予查询集实例化FormSet
        context['formset'] = VariationInventoryFormSet(
            queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        # 获得urls解析回的pk主键
        product_pk = self.kwargs.get('pk')
        if product_pk:
            # get_object_or_404方法按参数返回对象，如果没有返回Http404
            product = get_object_or_404(Product, pk=product_pk)
            # 返回product的所有Variation查询集
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        # is_valid方法检验表单数据是否合法并返回布尔值
        if formset.is_valid():
            # formset.save方法保存form，commit默认为True，如果设置为False表示不存储到数据库中
            formset.save(commit=False)
            for form in formset:
                # 设置commit=False，修改编辑后再保存
                new_item = form.save(commit=False)
                if new_item.title:
                    product_pk = self.kwargs.get('pk')
                    product = get_object_or_404(Product, pk=product_pk)
                    new_item.product = product
                    new_item.save()
            # messages框架的add_messages的快捷方式success，
            # 将messages的内容传递给base.html处理
            messages.success(request, 'Your inventory has been updated.')
            # 将网页重定向到products
            return redirect('products')
        # 否则返回404
        return Http404


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(
            *args, **kwargs)
        context['now'] = timezone.now()
        # 返回request.GET中的q参数，获取url内的q参数
        context['query'] = self.request.GET.get('q')
        print(context)
        return context

    def get_queryset(self, *args, **kwargs):

        # 重写类视图方法时调用super函数以获得原来的输出
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        # request.GET可以通过字典形式获取提交数据
        # 同样还有request.POST
        query = self.request.GET.get('q')
        if query:
            # icontains表示忽略大小写
            # 通过Q以及|来定义OR规则的filter查询
            qs = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs = (qs | qs2).distinct()
            except:
                pass
        return qs
