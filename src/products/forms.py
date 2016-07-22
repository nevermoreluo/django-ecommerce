# !/usr/bin/env python
# _*_ coding: utf-8 _*_

from django import forms

from django.forms.models import modelformset_factory

from .models import Variation


class VariationInventoryForm(forms.ModelForm):

    class Meta:
        model = Variation
        # 设置表单内的项目，必须是model的属性之一
        fields = [
            'price',
            'sale_price',
            'inventory',
            'active',
        ]

# modelformset_factory返回一个FormSet，参数model接受传入的模型类
# form接受一个ModelForm设定了fields
# extra指定默认给予额外的form数量
VariationInventoryFormSet = modelformset_factory(
    Variation, form=VariationInventoryForm, extra=0)
