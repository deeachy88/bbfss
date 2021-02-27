from django import forms
from django.forms import formset_factory

from plant.models import t_plant_movement_permit_t1, \
    t_plant_movement_permit_t2, t_plant_movement_permit_t3, t_file_attachment


class ImportFormOne(forms.ModelForm):
    class Meta:
        model = t_plant_movement_permit_t1
        fields = '__all__'


class ImportFormTwo(forms.ModelForm):
    class Meta:
        model = t_plant_movement_permit_t2
        fields = '__all__'


class ImportFormThree(forms.ModelForm):
    class Meta:
        model = t_plant_movement_permit_t3
        fields = '__all__'


class FileAttachmentForm(forms.ModelForm):
    class Meta:
        model = t_file_attachment
        fields = '__all__'


