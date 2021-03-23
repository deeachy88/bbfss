from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from plant import views

urlpatterns = [
    path('focal_officer_application', views.focal_officer_application, name='focal_officer_application'),
    path('oic_application', views.oic_application, name='oic_application'),
    path('inspector_application', views.inspector_application, name='inspector_application'),
    path('apply_movement_permit', views.apply_movement_permit, name='apply_movement_permit'),
    path('save_details', views.save_details, name='save_details'),
    path('save_movement_permit', views.save_movement_permit, name='save_movement_permit'),
    path('load_gewog', views.load_gewog, name='load_gewog'),
    path('load_village', views.load_village, name='load_village'),
    path('load_location', views.load_location, name='load_location'),
    path('movement_permit_app', views.movement_permit_app, name='movement_permit_app'),
    path('load_details_page', views.load_details_page, name='load_details_page'),
    path('update_application_details', views.update_application_details, name='update_details'),
    path('save', views.save, name='save'),
    path('forward_application', views.forward_application, name='forward_application'),
    path('approve_application', views.approve_application, name='approve_application'),
    path('reject_application', views.reject_application, name='reject_application'),
    path('add_details_ins', views.add_details_ins, name='add_details_ins'),
    path('save_file', views.add_file, name="save_file"),
    path('add_file_name', views.add_file_name, name='add_file_name'),
    path('delete_file', views.delete_file, name='delete_file'),

    # for import of plant and plant products
    path('apply_import_permit', views.apply_import_permit, name='apply_import_permit'),
    path('save_import', views.save_import_permit, name='save_import_permit'),
    path('load_variety', views.load_variety, name='load_variety'),
    path('save_import_agro', views.save_import_agro, name='save_import_agro'),
    path('save_import_plant', views.save_import_plant, name='save_import_plant'),
    path('view_fo_details', views.fo_app_details, name='view_fo_details'),
    path('call_for_inspection', views.call_for_inspection, name='call_for_inspection'),
    path('call_for_inspection_details', views.call_for_inspection_details, name='call_for_inspection_details'),
    path('print_imp_permit', views.print_import_details, name='print_imp_permit'),
    path('view_oic_details', views.view_oic_details, name='view_oic_details'),
    path('add_import_details_ins', views.add_import_details_ins, name='add_import_details_ins'),
    path('approve_import_application', views.approve_application, name='approve_import_application'),
    path('reject_import_application', views.reject_application, name='reject_import_application'),
    path('update_permit_details', views.update_permit_details, name='update_permit_details'),
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
    path('submit_application', views.submit_application, name='submit_application'),

    # certificate Printing
    path('certificate_print', views.certificate_print, name='certificate_print')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
