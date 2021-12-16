from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from food import views

urlpatterns = [
    # Food Business Registration And Licensing
    path('food_business_registration_licensing', views.food_business_registration_licensing,
         name='food_business_registration_licensing'),
    path('save_food_business_registration', views.save_food_business_registration,
         name='save_food_business_registration'),
    path('update_food_business_registration', views.update_food_business_registration,
         name='update_food_business_registration'),
    path('food_business_file', views.food_business_file, name='food_business_file'),
    path('food_business_file_name', views.food_business_file_name, name='food_business_file_name'),
    path('submit_food_business_application', views.submit_food_business_application,
         name='submit_food_business_application'),
    path('delete_fbr_file', views.delete_fbr_file, name='delete_fbr_file'),
    path('save_fbr_details', views.save_fbr_details, name='save_fbr_details'),
    path('save_fh_details', views.save_fh_details, name='save_fh_details'),
    path('fbr_fo_approve', views.fbr_fo_approve, name='fbr_fo_approve'),
    path('fbr_fo_reject', views.fbr_fo_reject, name='fbr_fo_reject'),
    path('inspection_team_details', views.inspection_team_details, name='inspection_team_details'),
    path('team_details_feasibility_ins', views.team_details_feasibility_ins, name='team_details_feasibility_ins'),
    path('concern_details_feasibility_ins', views.concern_details_feasibility_ins,
         name='concern_details_feasibility_ins'),
    path('approve_feasibility_inspection', views.approve_feasibility_inspection, name='approve_feasibility_inspection'),
    path('reject_feasibility_inspection', views.reject_feasibility_inspection, name='reject_feasibility_inspection'),
    path('resubmit_feasibility_inspection', views.resubmit_feasibility_inspection,
         name='resubmit_feasibility_inspection'),
    path('fbr_factory_team_details', views.fbr_factory_team_details, name='fbr_factory_team_details'),
    path('team_details_factory_ins', views.team_details_factory_ins, name='team_details_factory_ins'),
    path('concern_details_factory_ins', views.concern_details_factory_ins,
         name='concern_details_factory_ins'),
    path('approve_factory_inspection', views.approve_factory_inspection, name='approve_factory_inspection'),
    path('reject_factory_inspection', views.reject_factory_inspection, name='reject_factory_inspection'),
    path('resubmit_factory_inspection', views.resubmit_factory_inspection,
         name='resubmit_factory_inspection'),
    path('edit_fbr_feasibility_details', views.edit_fbr_feasibility_details,
         name='edit_fbr_feasibility_details'),
    path('edit_fbr_factory_details', views.edit_fbr_factory_details,
         name='edit_fbr_factory_details'),
    path('forward_fbr_application', views.forward_fbr_application, name='forward_fbr_application'),
    path('view_factory_inspection_application', views.view_factory_inspection_application,
         name='view_factory_inspection_application'),
    path('forward_factory_application', views.forward_factory_application, name='forward_factory_application'),
    path('send_acknowledge', views.send_acknowledge, name='send_acknowledge'),
    path('fbr_submit', views.fbr_submit, name='fbr_submit'),
    path('load_outsourced_details', views.load_outsourced_details, name='load_outsourced_details'),
    path('food_handler_details', views.food_handler_details, name='food_handler_details'),
    path('load_fbr_attachment', views.load_fbr_attachment, name='load_fbr_attachment'),
    path('update_fbr_team_details_feasibility_ins', views.update_fbr_team_details_feasibility_ins,
         name='update_fbr_team_details_feasibility_ins'),
    path('update_fbr_inspection_team_details', views.update_fbr_inspection_team_details,
         name='update_fbr_inspection_team_details'),
    path('delete_fbr_fi_inspection_team_details', views.delete_fbr_fi_inspection_team_details,
         name='delete_fbr_fi_inspection_team_details'),
    path('delete_fbr_fi_team_details', views.delete_fbr_fi_team_details,
         name='delete_fbr_fi_team_details'),
    path('update_fbr_team_details_factory_ins', views.update_fbr_team_details_factory_ins,
         name='update_fbr_team_details_factory_ins'),
    path('update_fbr_factory_inspection_team_details', views.update_fbr_factory_inspection_team_details,
         name='update_fbr_factory_inspection_team_details'),
    path('delete_fbr_factory_inspection_team_details', views.delete_fbr_factory_inspection_team_details,
         name='delete_fbr_factory_inspection_team_details'),
    path('delete_fbr_factory_team_details', views.delete_fbr_factory_team_details,
         name='delete_fbr_factory_team_details'),


    # Export Of Food
    path('food_export_certificate_application', views.food_export_certificate_application,
         name='food_export_certificate_application'),
    path('save_food_export_details', views.save_food_export_details, name='save_food_export_details'),
    path('update_food_export_details', views.update_food_export_details, name='update_food_export_details'),
    path('submit_food_export_application', views.submit_food_export_application, name='submit_food_export_application'),
    path('food_export_file', views.food_export_file, name='food_export_file'),
    path('food_export_file_name', views.food_export_file_name, name='food_export_file_name'),
    path('approve_food_export', views.approve_food_export, name='approve_food_export'),
    path('reject_food_export', views.reject_food_export, name='reject_food_export'),
    path('load_fec_attachment', views.load_fec_attachment, name='load_fec_attachment'),
    path('delete_export_file', views.delete_export_file, name='delete_export_file'),


    # Licensing of Food Handler
    path('food_handler_licensing', views.food_handler_licensing,
         name='food_handler_licensing'),
    path('save_food_handler_details', views.save_food_handler_details, name='save_food_handler_details'),
    path('update_food_handler_details', views.update_food_handler_details, name='update_food_handler_details'),
    path('food_handler_file', views.food_handler_file, name='food_handler_file'),
    path('food_handler_file_name', views.food_handler_file_name, name='food_handler_file_name'),
    path('delete_fh_file', views.delete_fh_file, name='delete_fh_file'),
    path('submit_food_handler_application', views.submit_food_handler_application,
         name='submit_food_handler_application'),
    path('food_handler_forward_application', views.food_handler_forward_application,
         name='food_handler_forward_application'),
    path('reject_food_handler_application', views.reject_food_handler_application,
         name='reject_food_handler_application'),
    path('food_handler_image', views.food_handler_image, name='food_handler_image'),
    path('food_handler_image_name', views.food_handler_image_name, name='food_handler_image_name'),
    path('food_handler_image_update', views.food_handler_image_update, name='food_handler_image_update'),
    path('food_handler_image_name_update', views.food_handler_image_name_update,
         name='food_handler_image_name_update'),
    path('food_handler_update', views.food_handler_update, name='food_handler_update'),
    path('load_fh_attachment', views.load_fh_attachment, name='load_fh_attachment'),

    # import permit
    path('food_import_application', views.food_import_application, name='food_import_application'),
    path('save_food_import', views.save_food_import, name='save_food_import'),
    path('update_food_import', views.update_food_import, name='update_food_import'),
    path('save_food_import_details', views.save_food_import_details, name='save_food_import_details'),
    path('food_import_file', views.food_import_file, name='food_import_file'),
    path('food_import_file_name', views.food_import_file_name, name='food_import_file_name'),
    path('delete_import_file', views.delete_import_file, name='delete_import_file'),
    path('submit_food_import', views.submit_food_import, name='submit_food_import'),
    path('approve_fo_fip_import', views.approve_fo_fip_import, name='approve_fo_fip_import'),
    path('reject_fo_fip_import', views.reject_fo_fip_import, name='reject_fo_fip_import'),
    path('edit_food_inspector_details/<int:Record_Id>', views.edit_food_inspector_details,
         name='edit_food_inspector_details'),
    path('food_details_ins_import', views.food_details_ins_import, name='food_details_ins_import'),
    path('submit_fip_application', views.submit_fip_application, name='submit_fip_application'),
    path('update_import_details_food', views.update_import_details_food, name='update_import_details_food'),
    path('load_fip_details', views.load_fip_details, name='load_fip_details'),
    path('load_fip_attachment', views.load_fip_attachment, name='load_fip_attachment'),


    # Common
    path('food_handler_application', views.food_handler_application, name='food_handler_application'),
    path('update_batch_no', views.update_batch_no, name='update_batch_no'),
    path('result_update_list', views.result_update_list, name='result_update_list'),
    path('result_update', views.result_update, name='result_update'),
    path('update_list', views.update_list, name='update_list'),
    path('factory_inspection_list', views.factory_inspection_list, name='factory_inspection_list'),
    path('food_handler_application_details', views.food_handler_application_details,
         name='food_handler_application_details'),
    path('get_food_handler_details', views.get_food_handler_details, name='get_food_handler_details'),
    path('delete_food_handler_photo', views.delete_food_handler_photo, name='delete_food_handler_photo'),
    path('food_handler', views.food_handler, name='food_handler'),
    path('update_food_handler_status', views.update_food_handler_status, name='update_food_handler_status'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
