from django import forms
from django.forms import formset_factory

from plant.models import t_plant_movement_permit_t1, \
    t_plant_movement_permit_t2, t_plant_movement_permit_t3, t_file_attachment, t_plant_import_permit_t1, \
    t_plant_import_permit_t2, t_plant_import_permit_inspection_t3


class ImportFormOne(forms.ModelForm):
    class Meta:
        model = t_plant_movement_permit_t1
        fields = '__all__'


class ImportFormTwo(forms.ModelForm):
    Quantity = forms.CharField(disabled=True)
    Import_Category = forms.CharField(disabled=True)
    Unit = forms.CharField(disabled=True)

    class Meta:
        model = t_plant_import_permit_t2
        fields = ['Quantity', 'Import_Category', 'Unit', 'Quantity_Released', 'Remarks']


class ImportFormThree(forms.ModelForm):
    class Meta:
        model = t_plant_import_permit_inspection_t3
        fields = ['Current_Observation', 'Decision_Conformity']


class FileAttachmentForm(forms.ModelForm):
    class Meta:
        model = t_file_attachment
        fields = ['attachment']
