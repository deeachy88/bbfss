from django import forms
from django.forms import formset_factory, Textarea

from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_clearance_meat_shop_t2, \
    t_livestock_import_permit_product_inspection_t2, t_livestock_import_permit_animal_inspection_t2, \
    t_livestock_clearance_meat_shop_t5


class MeatShopClearanceFormOne(forms.ModelForm):
    class Meta:
        model = t_livestock_clearance_meat_shop_t1
        fields = '__all__'


class MeatShopClearanceFormTwo(forms.ModelForm):
    class Meta:
        model = t_livestock_clearance_meat_shop_t2
        fields = '__all__'


class ImportFormProduct(forms.ModelForm):
    class Meta:
        model = t_livestock_import_permit_product_inspection_t2
        fields = '__all__'
        widgets = {
            'Description': Textarea(attrs={'rows': 3}),
            'Remarks': Textarea(attrs={'rows': 3}),
        }


class ImportFormAnimal(forms.ModelForm):
    class Meta:
        model = t_livestock_import_permit_animal_inspection_t2
        fields = '__all__'


class MeatShopFeasibilityForm(forms.ModelForm):
    class Meta:
        model = t_livestock_clearance_meat_shop_t5
        fields = '__all__'
        exclude = ('Application_No', 'FBO_Response', 'Meeting_Type',)
        widgets = {
            'Observation': Textarea(attrs={'rows': 3}),
        }