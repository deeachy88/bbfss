from django.conf.urls import url

from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='index'),
    url(r'^login/$', views.login, name='login'),
    path('register', views.register, name='register'),
    path('user', views.user, name='user_page'),
    path('edit_user/<int:Login_Id>', views.edit_user, name='edit_user'),
    path('role', views.role_manage, name='role_page'),
    path('edit_role/<int:Role_Id>', views.edit_role, name='edit_role'),
    path('section', views.section_manage, name='section_page'),
    path('edit_section/<int:Section_Id>', views.edit_section, name='edit_section'),
    path('division', views.division_manage, name='division'),
    path('edit_division/<int:Division_Id>', views.edit_division, name='edit_division'),
    path('service', views.service_manage, name='service_page'),
    path('edit_service/<int:Service_Id>', views.edit_service, name='edit_service'),
    path('crop_category', views.crop_category_manage, name='crop_category'),
    path('edit_crop_category/<int:Crop_Category_Id>', views.edit_crop_category, name='edit_crop_category'),
    path('delete_crop_category/<int:Crop_Category_Id>', views.delete_crop_category, name='delete_crop_category'),
    path('crop', views.crop_manage, name='crop_page'),
    path('edit_crop/<int:Crop_Id>', views.edit_crop, name='edit_crop'),
    path('crop_variety', views.crop_variety_manage, name='crop_variety_page'),
    path('edit_crop_variety/<int:Crop_Variety_Id>', views.edit_crop_variety, name='edit_crop_variety'),
    path('chemical', views.chemical_manage, name='chemical_page'),
    path('edit_chemical/<int:Chemical_Id>', views.edit_chemical, name='edit_chemical'),
    path('crop_species', views.crop_species_manage, name='plant_crop_species_page'),
    path('edit_crop_species/<int:Crop_Species_Id>', views.edit_crop_species, name='edit_crop_species'),
    path('ornamental_plant', views.ornamental_plant_manage, name='ornamental_plant_page'),
    path('edit_ornamental/<int:Ornamental_Plant_Id>', views.edit_ornamental_plant, name='edit_ornamental'),
    path('pesticide', views.pesticide_manage, name='pesticide_page'),
    path('edit_pesticide/<int:Pesticide_Id>', views.edit_pesticide, name='edit_pesticide'),
    path('plant_product', views.plant_product_manage, name='plant_product'),
    path('edit_product/<int:Plant_Product_Id>', views.edit_plant_product, name='edit_product'),
    path('plant_fodder', views.plant_fodder_manage, name='plant_fodder_page'),
    path('edit_plant_fodder/<int:Fodder_Id>', views.edit_plant_fodder, name='edit_plant_fodder'),
    path('plant_fodder_variety', views.plant_fodder_variety_manage, name='plant_fodder_variety'),
    path('edit_fodder_variety/<int:Fodder_Variety_Id>', views.edit_fodder_variety, name='edit_fodder_variety'),
    path('field_office', views.field_office_page_manage, name='field_office'),
    path('edit_field_office/<int:Field_Office_Id>', views.edit_field_office, name='edit_field_office'),
    path('location_field', views.location_field_manage, name='location_field'),
    path('edit_location_field/<int:Location_Code>', views.edit_location_field, name='edit_location_field'),
    path('delete_role/<int:Role_Id>', views.delete_role, name='delete_role'),
    path('delete_division/<int:Division_Id>', views.delete_division, name='delete_division'),
    path('delete_crop/<int:Crop_Id>', views.delete_crop, name='delete_crop'),
    path('delete_section/<int:Section_Id>', views.delete_section, name='delete_section'),
    path('delete_crop_variety/<int:Crop_Variety_Id>', views.delete_crop_variety, name='delete_crop_variety'),
    path('delete_chemical/<int:Chemical_Id>', views.delete_chemical, name='delete_chemical'),
    path('delete_crop_species/<int:Crop_Species_Id>', views.delete_plant_species, name='delete_crop_species'),
    path('delete_ornamental/<int:Ornamental_Plant_Id>', views.delete_ornamental, name='delete_ornamental'),
    path('delete_pesticide/<int:Pesticide_Id>', views.delete_pesticide, name='delete_pesticide'),
    path('delete_product/<int:Plant_Product_Id>', views.delete_product, name='delete_product'),
    path('delete_plant_fodder/<int:Fodder_Id>', views.delete_plant_fodder, name='delete_plant_fodder'),
    path('delete_fodder_variety/<int:Fodder_Variety_Id>', views.delete_fodder_variety, name='delete_fodder_variety'),
    path('delete_field_office/<int:Field_Office_Id>', views.delete_field_office, name='delete_field_office'),
    path('delete_location_field/<int:Location_Code>', views.delete_location_mapping, name='delete_location_field'),
    path('reg_clients', views.new_registration, name='new_registration'),
    path('registered_clients', views.registered_clients, name='registered_clients'),
    path('accept_registration/<str:Email_Id>/<str:Name>/', views.accept_registration, name='accept_registration'),
    path('reject_registration/<str:Email_Id>/<str:Name>/', views.reject_registration, name='reject_registration'),
    path('reset_client_password/<str:Email_Id>/<str:Name>/', views.reset_client_password, name='reset_client_password'),
    path('deactivate_client/<str:Email_Id>/<str:Name>/', views.deactivate_client, name='deactivate_client'),
    path('load_gewog', views.load_gewog, name='load_gewog'),
    path('load_village', views.load_village, name='load_village'),
    path('load_section', views.load_section, name='load_section'),
    path('password_update', views.password_update, name='password_update'),
    path('payment_details', views.payment_list, name='payment_details'),
    path('update_payment_details', views.update_payment_details, name='update_payment_details'),
    path('livestock_species', views.livestock_species_manage, name='livestock_species_page'),
    path('edit_livestock_species/<int:Species_Id>', views.edit_livestock_species, name='edit_livestock_species'),
    path('delete_livestock_species/<int:Species_Id>', views.delete_livestock_species, name='delete_livestock_species'),
    path('livestock_species_breed', views.livestock_species_breed_manage, name='livestock_species_breed_page'),
    path('edit_livestock_species_breed/<int:Species_Breed_Id>', views.edit_livestock_species_breed, name='edit_livestock_species_breed'),
    path('delete_livestock_species_breed/<int:Species_Breed_Id>', views.delete_livestock_species_breed, name='delete_livestock_species_breed'),
    path('livestock_product', views.livestock_product_manage, name='livestock_product_page'),
    path('edit_livestock_product/<int:Product_Id>', views.edit_livestock_product, name='edit_livestock_product'),
    path('delete_livestock_product/<int:Product_Id>', views.delete_livestock_product, name='delete_livestock_product'),
]