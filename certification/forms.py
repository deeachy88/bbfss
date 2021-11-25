from django import forms
from django.forms import Textarea

from certification.models import t_certification_gap_t8, t_certification_food_t5, t_certification_organic_t11


class GapForm(forms.ModelForm):
    class Meta:
        model = t_certification_gap_t8
        fields = '__all__'
        exclude = ('Application_No',)
        labels = {
            "Corrective_Action_Verified_Auditor": "Auditors Remarks",
            "Corrective_Action_Proposed_Auditee": "Response To NC"
        }
        widgets = {
            'Non_Conformity_Description': Textarea(attrs={'rows': 3}),
            'Corrective_Action_Verified_Auditor': Textarea(attrs={'rows': 3}),
            'Corrective_Action_Proposed_Auditee': Textarea(attrs={'rows': 3}),
        }


class FpcForm(forms.ModelForm):
    class Meta:
        model = t_certification_food_t5
        fields = '__all__'
        exclude = ('Application_No',)
        labels = {
            "Corrective_Action_Verified_Auditor": "Auditors Remarks",
            "Corrective_Action_Proposed_Auditee": "Response To NC"
        }
        widgets = {
            'Non_Conformity_Description': Textarea(attrs={'rows': 3}),
            'Corrective_Action_Verified_Auditor': Textarea(attrs={'rows': 3}),
            'Corrective_Action_Proposed_Auditee': Textarea(attrs={'rows': 3}),
        }


class OCForm(forms.ModelForm):
    class Meta:
        model = t_certification_organic_t11
        fields = '__all__'
        exclude = ('Application_No',)
        labels = {
            "Corrective_Action_Verified_Auditor": "Auditors Remarks",
            "Corrective_Action_Proposed_Auditee": "Response To NC"
        }
        widgets = {
            'Non_Conformity_Description': Textarea(attrs={'rows': 3}),
            'Corrective_Action_Verified_Auditor': Textarea(attrs={'rows': 3}),
            'Corrective_Action_Proposed_Auditee': Textarea(attrs={'rows': 3}),
        }
