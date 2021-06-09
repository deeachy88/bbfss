from django import forms
from django.forms import Textarea

from certification.models import t_certification_gap_t8, t_certification_food_t5, t_certification_organic_t11


class GapForm(forms.ModelForm):
    class Meta:
        model = t_certification_gap_t8
        fields = '__all__'
        exclude = ('Application_No',)
        widgets = {
            'Non_Conformity_Description': Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
            'Corrective_Action_Proposed_Auditee': Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
        }


class FpcForm(forms.ModelForm):
    class Meta:
        model = t_certification_food_t5
        fields = '__all__'
        exclude = ('Application_No',)
        widgets = {
            'Non_Conformity_Description': Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
            'Corrective_Action_Proposed_Auditee': Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
        }


class OCForm(forms.ModelForm):
    class Meta:
        model = t_certification_organic_t11
        fields = '__all__'
        exclude = ('Application_No',)
        widgets = {
            'Non_Conformity_Description': Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
            'Corrective_Action_Proposed_Auditee': Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
        }
