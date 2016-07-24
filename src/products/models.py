# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils.safestring import mark_safe


DEFAULT_VARIATION_TITLE = "Default"


class ProductQuerySet(models.query.QuerySet):

    '''
    # 创建自己的数据查询规则
    '''

    def active(self):
        # 添加一个queryset规则，即查询时过滤出active为真的项(可用的项目)
        return self.filter(active=True)


class ProductManager(models.Manager):

    def get_queryset(self):
        # 重写get_queryset添加自己新增的规则
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()  # 重写all()

    def get_related(self, instance):
        # 获得一个关于iinstance同category的查询集

        # queryset对象filter方法后依旧返回queryset
        # categories__in表示过滤出category在instance中的项目,它是categories__in__exact的省略
        #################################################
        # __默认接受exact，支持多重条件选择例如:categories__in__exact
        # 它可以支持"exact", "iexact", "contains", "icontains", "gt", "gte", "lt",
        # "lte", "in", "startswith", "istartswith", "endswith", "iendswith",
        # "range", "year", "month", "day", "isnull", "search", "regex",
        # "iregex"等
        # 可以查看http://python.usyiyi.cn/django/ref/models/querysets.html#field-lookups
        ################################################
        products_one = self.get_queryset().filter(
            categories__in=instance.categories.all())
        # 获取default的queryset
        products_two = self.get_queryset().filter(default=instance.default)
        # queryset可以通过|链接，即sql执行OR语句，但是会获得重复的项目。
        # 使用distinct方法去除重复项，但是值得注意的是该方法会与order_by方法冲突
        # 必要时可以使用python内置的sort或者sorted来代替distinct，order_by等方法
        qs = (products_one | products_two).exclude(id=instance.id).distinct()
        return qs


class Product(models.Model):
    # CharField存储字符串文本类型，必须接受一个max_length参数规定最大文本长度
    title = models.CharField(max_length=120)
    # TextField相当于一个存储更大数据的CharField。
    # 这里blank是Field的可选参数，blank默认为False，设置为True表示可以用空值储存。
    # 对应的的null默认为False，设置为True表示当django以空值存储数据时，数据库将以null存储，
    # 但是TextField和CharField为空时，建议使用默认的空字符存储，而不是设置null为True。
    # 让空值存储文本时数据类型依旧保持一致。
    description = models.TextField(blank=True, null=True)
    # DecimalField两个必填参数
    # max_digits位数总数（包含小数位，即必须大于等于decimal_places），
    # decimal_places 小数位
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True)
    # BooleanField接受一个default参数表示默认的勾选状态，如果不填则默认值为None
    active = models.BooleanField(default=True)

    # Product与Category多对多关联，并允许为空
    categories = models.ManyToManyField('Category', blank=True)
    # 默认一对多关系,
    # model之间建立关联时，需要一个
    # 通常会指定一个默认的related_name=<classname>_set
    # 当与一个类同时建立多种关系需要指定不一样的related_name
    default = models.ForeignKey(
        'Category', related_name='default_category', null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        # 重载__str__方法,py2可使用 __unicode__
        # 类以实例的标题显示
        return self.title

    def get_absolute_url(self):
        # 给视图以及模板提供更恰当的url返回，防止硬编码
        # reverse逆向解析url，这里返回www.ex.com/products/pk/
        # 即pk以传参的方式逆向传回urls里的"product_detail"解析
        return reverse("product_detail", kwargs={"pk": self.pk})

    def get_image_url(self):
        # productimage_set是默认ProductImage的反向查询名称，设置related_name可以更改。
        # first返回Queryset的第一个对象，如果没有返回None
        img = self.productimage_set.first()
        if img:
            # 调用ImageField的url属性返回image的链接地址
            return img.image.url
        # return img

    def get_defualt_variation_pk(self):
        variation = self.variation_set.first()
        if variation:
            return variation.pk


class Variation(models.Model):
    # 商品规格
    # 与商品建立一对多关联，即一个商品有多种规格
    product = models.ForeignKey(Product)
    # 规格名称
    title = models.CharField(max_length=120)
    # 价格
    price = models.DecimalField(decimal_places=2, max_digits=20)
    # 销售价格，可以为空，
    sale_price = models.DecimalField(
        decimal_places=2, max_digits=20, null=True, blank=True)
    # 是否可用，默认为可用
    active = models.BooleanField(default=True)
    # 库存
    inventory = models.IntegerField(default="0", null=True, blank=True)

    def __str__(self):
        return self.title

    def get_price(self):
        # 销售价格为空时，读取商品价格
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_absolute_url(self):
        # 返回链接为商品链接一致
        return reverse("variation", kwargs={"pk": self.pk})

    def get_html_price(self):
        # 获取price，编写函数方便模板中调用
        if self.sale_price is not None:
            html_text = ("<span class='sale-price'>%s</span>"
                         " <span class='og-price'>原价:%s</span>") % (
                self.sale_price, self.price)
        else:
            html_text = "<span class='price'>%s</span>" % (self.price)
        # mark_safe将富文本以合理的方式显示于网页中
        return mark_safe(html_text)

    def add_to_cart(self):
        return "%s?item=%s&qty=1" % (reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" % (reverse("cart"), self.id)

    def get_title(self):
        return "%s - %s" % (self.product.title, self.title)

def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    # 截获表单save事件，
    # 即当保存product时(不论新旧)，检测是否有Variation
    # 如果没有自动为其添加一个名为default的Variation
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = DEFAULT_VARIATION_TITLE
        new_var.price = product.price
        new_var.sale_price = product.sale_price
        new_var.save()
    else:
        # 如果存在default则保持default的price和product的价格始终一致
        # 即始终将product的价格同步给default
        default = product.variation_set.filter(
            title=DEFAULT_VARIATION_TITLE).first()
        if default:
            default.price = product.price
            default.sale_price = product.sale_price
            default.save()

# save事件的槽函数，接受post_save信号时，调用自定义product_post_saved_receiver函数
post_save.connect(product_post_saved_receiver, sender=Product)


def image_upload_to(instance, filename):
    # 为image的存储，指定一个规定路径下的名称，便于管理
    title = instance.product.title
    # 将title转换为友善与django的字符串
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return 'products/%s/%s' % (slug, new_filename)


class ProductImage(models.Model):
    # 建立一个一对多关联，一个产品可以有多张图片
    product = models.ForeignKey(Product)
    # ImageField需求PIL，如果有特殊原因无法使用，可用FileField替代
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.product.title


class Category(models.Model):
    # 产品种类,
    # Field.unique参数表示该数据在表中的唯一性，
    # 即试图存储一个已存在的值时，会抛出django.db.IntegrityError
    title = models.CharField(max_length=120, unique=True)
    # 短标题，SlugField类似CharField但是它只接受ascii码以及-和_。默认max_length为50
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    # 记录category第一次被创建的时间,
    # auto_now_add第一次被创建时自动设置时间
    # auto_now 每次保存时自动记录时间
    # auto_now_add，auto_now，default相互排斥，并均由 TIME_ZONE的default timezone决定
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})


def image_upload_to_featured(instance, filename):
    # 填写一个和image_upload_to类似的函数
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "products/%s/featured/%s" % (slug, new_filename)


class ProductFeatured(models.Model):
    # 为home页面设置标题样式
    product = models.ForeignKey(Product)
    # 背景图片
    image = models.ImageField(upload_to=image_upload_to_featured)
    title = models.CharField(max_length=120, null=True, blank=True)
    # 简介
    text = models.CharField(max_length=220, null=True, blank=True)
    # 简介是否靠右
    text_right = models.BooleanField(default=False)
    # 字体颜色
    text_css_color = models.CharField(max_length=6, null=True, blank=True)
    # 是否显示价格
    show_price = models.BooleanField(default=False)
    # 是否设置为背景图片
    make_image_background = models.BooleanField(default=False)
    # 是否可用
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title
