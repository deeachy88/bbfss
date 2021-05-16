from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from certification import views

urlpatterns = [
    # GAP
    path('gap_certificate', views.gap_certificate, name='gap_certificate'),
    path('save_gap_certificate', views.save_gap_certificate,
         name='save_gap_certificate'),
    path('gap_certificate_file', views.gap_certificate_file, name='gap_certificate_file'),
    path('gap_certificate_file_name', views.gap_certificate_file_name, name='gap_certificate_file_name'),
    path('submit_gap_certificate', views.submit_gap_certificate,
         name='submit_gap_certificate'),
    path('gap_farmers_group_details', views.gap_farmers_group_details, name='gap_farmers_group_details'),
    path('gap_crop_production_details', views.gap_crop_production_details, name='gap_crop_production_details'),
    path('add_pack_house_details', views.add_pack_house_details, name='add_pack_house_details'),

    # Organic certificate
    path('organic_certificate', views.organic_certificate, name='organic_certificate'),
    path('save_organic_certificate', views.save_organic_certificate, name='save_organic_certificate'),
    path('organic_certificate_file', views.organic_certificate_file, name='organic_certificate_file'),
    path('organic_certificate_file_name', views.organic_certificate_file_name, name='organic_certificate_file_name'),
    path('save_farmers_group_details', views.save_farmers_group_details, name='save_farmers_group_details'),
    path('save_crop_production_details', views.save_crop_production_details, name='save_crop_production_details'),
    path('save_wild_collection_details', views.save_wild_collection_details, name='save_wild_collection_details'),
    path('save_animal_husbandry_details', views.save_animal_husbandry_details, name='save_animal_husbandry_details'),
    path('save_aquaculture_details', views.save_aquaculture_details, name='save_aquaculture_details'),
    path('save_api_culture_details', views.save_api_culture_details, name='save_api_culture_details'),
    path('save_processing_unit_details', views.save_processing_unit_details, name='save_processing_unit_details'),
    path('submit_organic_certificate', views.submit_organic_certificate,
         name='submit_organic_certificate'),
    path('send_acknowledge', views.send_acknowledge, name='send_acknowledge'),
    path('send_for_acceptance', views.send_for_acceptance, name='send_for_acceptance'),
    path('add_audit_team_details', views.add_audit_team_details, name='add_audit_team_details'),
    path('send_audit_plan_acceptance', views.send_audit_plan_acceptance, name='send_audit_plan_acceptance'),
    path('approve_application', views.approve_application, name='approve_application'),
    path('resubmit_application', views.resubmit_application, name='resubmit_application'),
    path('farm_input_observation', views.farm_input_observation, name='farm_input_observation'),
    path('conform_observation', views.conform_observation, name='conform_observation'),
    path('audit_team_accept',views.audit_team_accept, name='audit_team_accept'),


    # Food Product certificate
    path('food_product_certificate', views.food_product_certificate, name='food_product_certificate'),
    path('save_food_product_certificate', views.save_food_product_certificate,
         name='save_food_product_certificate'),
    path('food_product_certificate_file', views.food_product_certificate_file, name='food_product_certificate_file'),
    path('food_product_certificate_file_name', views.food_product_certificate_file_name,
         name='food_product_certificate_file_name'),
    path('submit_food_product_certificate', views.submit_food_product_certificate,
         name='submit_food_product_certificate'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
