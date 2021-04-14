from django import forms
from django.forms import formset_factory

from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_clearance_meat_shop_t2


class MeatShopClearanceFormOne(forms.ModelForm):
    class Meta:
        model = t_livestock_clearance_meat_shop_t1
        fields = '__all__'


class MeatShopClearanceFormTwo(forms.ModelForm):

    class Meta:
        model = t_livestock_clearance_meat_shop_t2
        fields = '__all__'

