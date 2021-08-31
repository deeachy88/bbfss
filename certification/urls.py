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
    path('gap_audit_team_details', views.gap_audit_team_details, name='gap_audit_team_details'),
    path('gap_for_acceptance', views.gap_for_acceptance, name='gap_for_acceptance'),
    path('gap_application_team_leader', views.gap_application_team_leader,
         name='gap_application_team_leader'),
    path('gap_audit_team_accept', views.gap_audit_team_accept, name='gap_audit_team_accept'),
    path('gap_farm_input_observation', views.gap_farm_input_observation, name='gap_farm_input_observation'),
    path('gap_audit_plan_acceptance', views.gap_audit_plan_acceptance, name='gap_audit_plan_acceptance'),
    path('gap_audit_plan_resubmit', views.gap_audit_plan_resubmit, name='gap_audit_plan_resubmit'),
    path('gap_conform_observation', views.gap_conform_observation, name='gap_conform_observation'),
    path('forward_application_head_office', views.forward_application_head_office,
         name='forward_application_head_office'),
    path('approve_gap_application', views.approve_gap_application, name='approve_gap_application'),
    path('save_gap_audit_plan', views.save_gap_audit_plan, name='save_gap_audit_plan'),
    path('save_gap_audit_plan_name', views.save_gap_audit_plan_name, name='save_gap_audit_plan_name'),
    path('resubmit_nc_details', views.resubmit_nc_details, name='resubmit_nc_details'),
    path('edit_nc_details/<int:Record_Id>', views.edit_nc_details, name='edit_nc_details'),
    path('gap_nc_response', views.gap_nc_response, name='gap_nc_response'),


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
    path('send_audit_plan_resubmit', views.send_audit_plan_resubmit, name='send_audit_plan_resubmit'),
    path('approve_application', views.approve_application, name='approve_application'),
    path('farm_input_observation', views.farm_input_observation, name='farm_input_observation'),
    path('conform_observation', views.conform_observation, name='conform_observation'),
    path('audit_team_accept', views.audit_team_accept, name='audit_team_accept'),
    path('forward_application_team_leader', views.forward_application_team_leader,
         name='forward_application_team_leader'),
    path('approve_oc_application', views.approve_oc_application, name='approve_oc_application'),
    path('oc_application_team_leader', views.oc_application_team_leader, name='oc_application_team_leader'),
    path('save_oc_audit_plan', views.save_oc_audit_plan, name='save_oc_audit_plan'),
    path('save_oc_audit_plan_name', views.save_oc_audit_plan_name, name='save_oc_audit_plan_name'),
    path('resubmit_oc_nc_details', views.resubmit_oc_nc_details, name='resubmit_oc_nc_details'),
    path('edit_oc_nc_details/<int:Record_Id>', views.edit_oc_nc_details, name='edit_oc_nc_details'),
    path('oc_nc_response', views.oc_nc_response, name='oc_nc_response'),


    # Food Product certificate
    path('food_product_certificate', views.food_product_certificate, name='food_product_certificate'),
    path('save_food_product_certificate', views.save_food_product_certificate,
         name='save_food_product_certificate'),
    path('food_product_certificate_file', views.food_product_certificate_file, name='food_product_certificate_file'),
    path('food_product_certificate_file_name', views.food_product_certificate_file_name,
         name='food_product_certificate_file_name'),
    path('submit_food_product_certificate', views.submit_food_product_certificate,
         name='submit_food_product_certificate'),
    path('fpc_audit_team_details', views.fpc_audit_team_details, name='fpc_audit_team_details'),
    path('fpc_for_acceptance', views.fpc_for_acceptance, name='fpc_for_acceptance'),
    path('fpc_application_team_leader', views.fpc_application_team_leader,
         name='fpc_application_team_leader'),
    path('fpc_audit_team_accept', views.fpc_audit_team_accept, name='fpc_audit_team_accept'),
    path('fpc_farm_input_observation', views.fpc_farm_input_observation, name='fpc_farm_input_observation'),
    path('fpc_audit_plan_acceptance', views.fpc_audit_plan_acceptance, name='fpc_audit_plan_acceptance'),
    path('fpc_audit_plan_resubmit', views.fpc_audit_plan_resubmit, name='fpc_audit_plan_resubmit'),
    path('fpc_conform_observation', views.fpc_conform_observation, name='fpc_conform_observation'),
    path('approve_fpc_application', views.approve_fpc_application, name='approve_fpc_application'),
    path('save_fpc_audit_plan', views.save_fpc_audit_plan, name='save_fpc_audit_plan'),
    path('save_fpc_audit_plan_name', views.save_fpc_audit_plan_name, name='save_fpc_audit_plan_name'),
    path('resubmit_fpc_nc_details', views.resubmit_fpc_nc_details, name='resubmit_fpc_nc_details'),
    path('edit_fpc_nc_details/<int:Record_Id>', views.edit_fpc_nc_details, name='edit_fpc_nc_details'),
    path('fpc_nc_response', views.fpc_nc_response, name='fpc_nc_response'),


    # Common
    path('certificate_pending_list', views.certificate_pending_list, name='certificate_pending_list'),
    path('view_certificate_draft_details', views.view_certificate_draft_details, name='view_certificate_draft_details'),
    path('update_food_product_form', views.update_food_product_form, name='update_food_product_form'),
    path('update_oc_form', views.update_oc_form, name='update_oc_form'),
    path('update_gap_form', views.update_gap_form, name='update_gap_form'),
    path('date_month', views.date_month, name='date_month'),
    path('delete_audit_team', views.delete_audit_team, name='delete_audit_team'),
    path('delete_farm_details', views.delete_farm_details, name='delete_farm_details'),
    path('update_nc_response', views.update_nc_response, name='update_nc_response'),
    path('delete_farmers_group', views.delete_farmers_group, name='delete_farmers_group'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
