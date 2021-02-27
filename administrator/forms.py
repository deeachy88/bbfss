from django import forms

from administrator.models import t_user_master, t_role_master, t_section_master, t_division_master, t_service_master, \
    t_plant_crop_master, t_plant_crop_variety_master, t_plant_chemical_master, t_plant_crop_species_master, \
    t_plant_ornamental_master, t_plant_pesticide_master, t_plant_product_master, t_plant_fodder_master, \
    t_plant_fodder_variety_master, t_field_office_master, t_location_field_office_mapping


class UserForm(forms.ModelForm):
    class Meta:
        model = t_user_master
        fields = '__all__'


class RoleForm(forms.ModelForm):
    class Meta:
        model = t_role_master
        fields = '__all__'


class SectionForm(forms.ModelForm):
    class Meta:
        model = t_section_master
        fields = '__all__'


class DivisionForm(forms.ModelForm):
    class Meta:
        model = t_division_master
        fields = '__all__'


class ServiceForm(forms.ModelForm):
    class Meta:
        model = t_service_master
        fields = '__all__'


class CropForm(forms.ModelForm):
    class Meta:
        model = t_plant_crop_master
        fields = '__all__'


class CropVarietyForm(forms.ModelForm):
    class Meta:
        model = t_plant_crop_variety_master
        fields = '__all__'


class ChemicalForm(forms.ModelForm):
    class Meta:
        model = t_plant_chemical_master
        fields = '__all__'


class CropSpeciesForm(forms.ModelForm):
    class Meta:
        model = t_plant_crop_species_master
        fields = '__all__'


class OrnamentalPlantForm(forms.ModelForm):
    class Meta:
        model = t_plant_ornamental_master
        fields = '__all__'


class PesticideForm(forms.ModelForm):
    class Meta:
        model = t_plant_pesticide_master
        fields = '__all__'


class PlantProductForm(forms.ModelForm):
    class Meta:
        model = t_plant_product_master
        fields = '__all__'


class PlantFodderForm(forms.ModelForm):
    class Meta:
        model = t_plant_fodder_master
        fields = '__all__'


class FodderVarietyForm(forms.ModelForm):
    class Meta:
        model = t_plant_fodder_variety_master
        fields = '__all__'


class FieldOfficeForm(forms.ModelForm):
    class Meta:
        model = t_field_office_master
        fields = '__all__'


class LocationFieldMappingForm(forms.ModelForm):
    class Meta:
        model = t_location_field_office_mapping
        fields = '__all__'


