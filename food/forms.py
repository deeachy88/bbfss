from django import forms
from django.forms import Textarea

from food.models import t_food_import_permit_inspection_t2, t_food_business_registration_licensing_t5


class ImportFormFood(forms.ModelForm):
    class Meta:
        model = t_food_import_permit_inspection_t2
        fields = '__all__'
        widgets = {
            'Description': Textarea(attrs={'rows': 3}),
            'Remarks': Textarea(attrs={'rows': 3}),
        }


class FeasibilityForm(forms.ModelForm):
    class Meta:
        model = t_food_business_registration_licensing_t5
        fields = '__all__'
        exclude = ('Application_No', 'FBO_Response', 'Meeting_Type',)
        widgets = {
            'Observation': Textarea(attrs={'rows': 3}),
        }
