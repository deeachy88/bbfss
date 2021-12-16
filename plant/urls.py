from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from plant import views

urlpatterns = [
    path('focal_officer_application', views.focal_officer_application, name='focal_officer_application'),
    path('oic_application', views.oic_application, name='oic_application'),
    path('inspector_application', views.inspector_application, name='inspector_application'),
    path('complain_officer_application', views.complain_officer_application, name='complain_officer_application'),
    path('chief_application', views.chief_application, name='chief_application'),

    # movement permit
    path('apply_movement_permit', views.apply_movement_permit, name='apply_movement_permit'),
    path('save_details', views.save_details, name='save_details'),
    path('save_movement_permit', views.save_movement_permit, name='save_movement_permit'),
    path('load_gewog', views.load_gewog, name='load_gewog'),
    path('load_village', views.load_village, name='load_village'),
    path('load_location', views.load_location, name='load_location'),
    path('to_gewog_list', views.to_gewog_list, name='to_gewog_list'),
    path('movement_permit_app', views.movement_permit_app, name='movement_permit_app'),
    path('load_details_page', views.load_details_page, name='load_details_page'),
    path('agro_details_page', views.agro_details_page, name='agro_details_page'),
    path('update_application_details', views.update_application_details, name='update_details'),
    path('save_details_movement', views.save_details_movement, name='save_details_movement'),
    path('forward_application', views.forward_application, name='forward_application'),
    path('approve_application', views.approve_application, name='approve_application'),
    path('reject_movement_application', views.reject_movement_application, name='reject_movement_application'),
    path('add_details_ins', views.add_details_ins, name='add_details_ins'),
    path('save_file', views.add_file, name="save_file"),
    path('add_file_name', views.add_file_name, name='add_file_name'),
    path('save_movement_file', views.save_movement_file, name="save_movement_file"),
    path('movement_agro_file_name', views.movement_agro_file_name, name='movement_agro_file_name'),
    path('delete_file', views.delete_file, name='delete_file'),
    path('update_movement_details', views.update_movement_permit, name='update_movement_details'),
    path('mov_plant_details', views.mov_plant_details, name='mov_plant_details'),
    path('mov_plant_attachment', views.mov_plant_attachment, name='mov_plant_attachment'),
    path('mov_agro_attachment', views.mov_agro_attachment, name='mov_agro_attachment'),
    path('get_unit_master', views.get_unit_master, name='get_unit_master'),
    path('load_to_location', views.load_to_location, name='load_to_location'),
    path('update_movement_permit', views.update_movement_permit, name='update_movement_permit'),


    # for import of plant and plant products
    path('apply_import_permit', views.apply_import_permit, name='apply_import_permit'),
    path('save_import', views.save_import_permit, name='save_import_permit'),
    path('load_variety', views.load_variety, name='load_variety'),
    path('save_import_agro', views.save_import_agro, name='save_import_agro'),
    path('save_import_plant', views.save_import_plant, name='save_import_plant'),
    path('view_fo_details', views.fo_app_details, name='view_fo_details'),
    path('print_imp_permit', views.print_import_details, name='print_imp_permit'),
    path('view_oic_details', views.view_oic_details, name='view_oic_details'),
    path('add_import_details_ins', views.add_import_details_ins, name='add_import_details_ins'),
    path('approve_import_application', views.approve_import_application, name='approve_import_application'),
    path('reject_import_application', views.reject_import_application, name='reject_import_application'),
    path('add_plant_import_file', views.add_plant_import_file, name="add_plant_import_file"),
    path('add_agro_import_file', views.add_agro_import_file, name="add_agro_import_file"),
    path('add_plant_attach', views.add_plant_attach, name='add_plant_attach'),
    path('add_agro_attach', views.add_agro_attach, name='add_agro_attach'),
    path('delete_plant_file', views.delete_plant_file, name='delete_plant_file'),
    path('delete_agro_file', views.delete_agro_file, name='delete_agro_file'),
    path('save_details_import', views.save_details_import, name='save_details_import'),
    path('fo_approve', views.fo_approve, name='fo_approve'),
    path('fo_reject', views.fo_reject, name='fo_reject'),
    path('assign_to_inspector', views.assign_to_inspector, name='assign_to_inspector'),
    path('edit_inspector_details/<int:Record_Id>', views.edit_inspector_details, name='edit_inspector_details'),
    path('add_details_ins_import', views.add_details_ins_import, name='add_details_ins_import'),
    path('edit_decision/<int:Record_Id>', views.edit_decision, name='edit_decision'),
    path('view_application_details', views.view_application_details, name='view_application_details'),
    path('approve_clearance_application', views.approve_clearance_application, name='approve_clearance_application'),
    path('load_import_details', views.load_import_details, name='load_import_details'),
    path('agro_details_permit', views.load_import_details_agro, name='agro_details_permit'),
    path('permit_attachment_plant', views.permit_attachment_plant, name='permit_attachment_plant'),
    path('permit_attachment_agro', views.permit_attachment_agro, name='permit_attachment_agro'),
    path('details_plant', views.details_plant, name='details_plant'),
    path('details_agro', views.details_agro, name='details_agro'),
    path('plant_import_update', views.plant_import_update, name='plant_import_update'),
    path('agro_import_update', views.agro_import_update, name='agro_import_update'),
    path('update_details_plant', views.update_details_plant, name='update_details_plant'),
    path('update_details_agro', views.update_details_agro, name='update_details_agro'),
    path('update_import_permit', views.update_import_permit, name='update_import_permit'),
    path('load_plant_import_details', views.load_plant_import_details, name='load_plant_import_details'),
    path('load_plant_import_attachment', views.load_plant_import_attachment, name='load_plant_import_attachment'),

    # certificate Printing
    path('certificate_print', views.certificate_print, name='certificate_print'),
    path('view_certificate_details', views.view_certificate_details, name='view_certificate_details'),
    path('get_certificate_details', views.get_certificate_details, name='get_certificate_details'),

    # Export Permit
    path('apply_export_certificate', views.apply_export_permit, name='apply_export_certificate'),
    path('submit_export', views.submit_export, name='submit_export'),
    path('add_file_phyto', views.add_file_phyto, name='add_file_phyto'),
    path('add_file_name_phyto', views.add_file_name_phyto, name='add_file_name_phyto'),
    path('add_file_cordyceps', views.add_file_cordyceps, name='add_file_cordyceps'),
    path('add_file_name_cordyceps', views.add_file_name_cordyceps, name='add_file_name_cordyceps'),
    path('export_complete', views.export_complete, name='export_complete'),
    path('permit_plant_details', views.permit_plant_details, name='permit_plant_details'),
    path('permit_agro_details', views.permit_agro_details, name='permit_agro_details'),
    path('update_nursery_details', views.update_nursery_details, name='update_nursery_details'),
    path('plant_file_details', views.plant_file_details, name='plant_file_details'),
    path('cordyceps_file_details', views.cordyceps_file_details, name='cordyceps_file_details'),
    path('save_export_permit', views.save_export_permit, name='save_export_permit'),
    path('delete_file_export', views.delete_file_export, name='delete_file_export'),
    path('delete_file_phyto', views.delete_file_phyto, name='delete_file_phyto'),
    path('update_export', views.update_export, name='update_export'),

    # Registration Of Nursery/Seed Growers
    path('registration_application', views.registration_application, name='registration_application'),
    path('save_nursery_reg', views.save_nursery_reg, name='save_nursery_reg'),
    path('add_file_reg', views.add_file_reg, name="add_file_reg"),
    path('add_file_name_reg', views.add_file_name_reg, name='add_file_name_reg'),
    path('add_reg_details', views.add_reg_details, name='add_reg_details'),
    path('submit_nursery_details', views.submit_nursery_details, name='submit_nursery_details'),
    path('approve_nursery_application', views.approve_nursery_application, name='approve_nursery_application'),
    path('reject_nursery_application', views.reject_nursery_application, name='reject_nursery_application'),
    path('resubmit_nursery_application', views.resubmit_nursery_application, name='resubmit_nursery_application'),
    path('add_details_nursery', views.add_details_nursery, name='add_details_nursery'),
    path('load_nursery_details', views.load_nursery_details, name='load_nursery_details'),
    path('update_nursery_details', views.update_nursery_details, name='update_nursery_details'),
    path('load_details', views.load_details, name='load_details'),
    path('load_file_details', views.load_file_details, name='load_file_details'),
    path('load_location_nursery', views.load_location_nursery, name='load_location_nursery'),
    path('nursery_client_resubmit', views.nursery_client_resubmit, name='nursery_client_resubmit'),
    path('delete_file_nursery', views.delete_file_nursery, name='delete_file_nursery'),
    path('update_nursery_reg', views.update_nursery_reg, name='update_nursery_reg'),
    path('load_nursery_attachment', views.load_nursery_attachment, name='load_nursery_attachment'),

    # Seed Certification
    path('seed_certificate_application', views.seed_certificate_application, name='seed_certificate_application'),
    path('save_certificate', views.save_seed_cert, name='save_certificate'),
    path('add_file_certificate', views.add_file_certificate, name="add_file_certificate"),
    path('add_file_name_certificate', views.add_file_name_certificate, name='add_file_name_certificate'),
    path('add_certificate_details', views.add_certificate_details, name='add_certificate_details'),
    path('submit_certificate_details', views.submit_certificate_details, name='submit_certificate_details'),
    path('approve_certificate_application', views.approve_certificate_application,
         name='approve_certificate_application'),
    path('reject_certificate_app', views.reject_certificate_application, name='reject_certificate_app'),
    path('resubmit_seed_application', views.resubmit_seed_application, name='resubmit_seed_application'),
    path('add_details_ins_certificate', views.add_details_ins_certificate, name='add_details_ins_certificate'),
    path('add_recommendation_details', views.add_recommendation_details, name='add_recommendation_details'),
    path('load_certificate_details', views.load_certificate_details, name='load_certificate_details'),
    path('update_certificate_details', views.update_certificate_details, name='update_certificate_details'),
    path('certificate_details', views.certificate_details, name='certificate_details'),
    path('certificate_file_details', views.certificate_file_details, name='certificate_file_details'),
    path('load_seed_variety', views.load_seed_variety, name='load_seed_variety'),
    path('seed_certification_client_resubmit', views.seed_certification_client_resubmit,
         name='seed_certification_client_resubmit'),
    path('delete_file_seed', views.delete_file_seed, name='delete_file_seed'),
    path('update_seed_certificate', views.update_seed_certificate, name='update_seed_certificate'),

    # Common Details
    path('application_status', views.application_status, name='application_status'),
    path('resubmit_application', views.resubmit_application, name='resubmit_application'),
    path('call_for_inspection', views.call_for_inspection, name='call_for_inspection'),
    path('call_for_inspection_details', views.call_for_inspection_details, name='call_for_inspection_details'),
    path('update_inspection_call_details', views.update_inspection_call_details, name='update_inspection_call_details'),
    path('resubmit_app_details', views.resubmit_app_details, name='resubmit_app_details'),
    path('update_resubmit_details', views.update_resubmit_details, name='update_resubmit_details'),
    path('get_variety', views.get_variety, name='get_variety'),
    path('get_crop', views.get_crop, name='get_crop'),
    path('validate_receipt_no', views.validate_receipt_no, name='validate_receipt_no'),
    path('get_citizen_details', views.get_citizen_details, name='get_citizen_details'),
    path('delete_details', views.delete_details, name='delete_details'),
    path('update_edit_details', views.update_edit_details, name='update_edit_details'),
    path('view_complain_officer_details', views.view_complain_officer_details, name='view_complain_officer_details'),
    path('view_chief_details', views.view_chief_details, name='view_chief_details'),
    path('member_audit_plan', views.member_audit_plan, name='member_audit_plan'),
    path('client_audit_plan', views.client_audit_plan, name='client_audit_plan'),
    path('view_audit_plan', views.view_audit_plan, name='view_audit_plan'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
