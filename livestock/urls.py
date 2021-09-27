from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from livestock import views

urlpatterns = [
    # clearance for meat shop
    path('meat_shop_registration_licensing', views.meat_shop_registration_licensing,
         name='meat_shop_registration_licensing'),
    path('save_meat_shop_registration', views.save_meat_shop_registration,
         name='save_meat_shop_registration'),
    path('meat_shop_file', views.meat_shop_file, name='meat_shop_file'),
    path('meat_shop_file_name', views.meat_shop_file_name, name='meat_shop_file_name'),
    path('submit_meat_shop_application', views.submit_meat_shop_application,
         name='submit_meat_shop_application'),
    path('delete_meat_shop_fh_file', views.delete_meat_shop_fh_file, name='delete_meat_shop_fh_file'),
    path('save_meat_item_details', views.save_meat_shop_details, name='save_meat_item_details'),
    path('save_meat_shop_fh_details', views.save_meat_shop_fh_details, name='save_meat_shop_fh_details'),
    path('meat_shop_fo_approve', views.meat_shop_fo_approve, name='meat_shop_fo_approve'),
    path('meat_shop_fo_reject', views.meat_shop_fo_reject, name='meat_shop_fo_reject'),
    path('meat_shop_inspection_team_details', views.meat_shop_inspection_team_details,
         name='meat_shop_inspection_team_details'),
    path('meat_shop_team_details_feasibility_ins', views.meat_shop_team_details_feasibility_ins,
         name='meat_shop_team_details_feasibility_ins'),
    path('meat_shop_concern_details_feasibility_ins', views.meat_shop_concern_details_feasibility_ins,
         name='meat_shop_concern_details_feasibility_ins'),
    path('approve_meat_shop_feasibility_inspection', views.approve_meat_shop_feasibility_inspection,
         name='approve_meat_shop_feasibility_inspection'),
    path('reject_meat_shop_feasibility_inspection', views.reject_meat_shop_feasibility_inspection,
         name='reject_meat_shop_feasibility_inspection'),
    path('resubmit_meat_shop_feasibility_inspection', views.resubmit_meat_shop_feasibility_inspection,
         name='resubmit_meat_shop_feasibility_inspection'),
    path('meat_shop_team_details_factory_ins', views.meat_shop_team_details_factory_ins,
         name='meat_shop_team_details_factory_ins'),
    path('meat_shop_concern_details_factory_ins', views.meat_shop_concern_details_factory_ins,
         name='meat_shop_concern_details_factory_ins'),
    path('approve_meat_shop_factory_inspection', views.approve_meat_shop_factory_inspection,
         name='approve_meat_shop_factory_inspection'),
    path('reject_meat_shop_factory_inspection', views.reject_meat_shop_factory_inspection,
         name='reject_meat_shop_factory_inspection'),
    path('resubmit_meat_shop_factory_inspection', views.resubmit_meat_shop_factory_inspection,
         name='resubmit_meat_shop_factory_inspection'),
    path('edit_meat_shop_feasibility_details', views.edit_meat_shop_feasibility_details,
         name='edit_meat_shop_feasibility_details'),
    path('edit_meat_shop_factory_details', views.edit_meat_shop_factory_details,
         name='edit_meat_shop_factory_details'),
    path('forward_meat_shop_application', views.forward_meat_shop_application, name='forward_meat_shop_application'),
    path('view_meat_shop_factory_inspection_application', views.view_meat_shop_factory_inspection_application,
         name='view_meat_shop_factory_inspection_application'),
    path('forward_meat_shop_factory_application', views.forward_meat_shop_factory_application,
         name='forward_meat_shop_factory_application'),
    path('send_meat_shop_acknowledge', views.send_meat_shop_acknowledge, name='send_meat_shop_acknowledge'),
    path('meat_shop_submit', views.meat_shop_submit, name='meat_shop_submit'),

    # import permit for live animal and fish
    path('import_permit', views.import_permit, name='import_permit'),
    path('save_import_la_fish', views.save_import_la_fish, name='save_import_la_fish'),
    path('import_permit_details', views.import_permit_la_details, name='import_permit_details'),
    path('add_la_permit_file', views.add_la_permit_file, name='add_la_permit_file'),
    path('add_la_file_name', views.add_la_file_name, name='add_la_file_name'),
    path('delete_la_file', views.delete_la_file, name='delete_la_file'),
    path('submit_import_application', views.submit_import_application, name='submit_import_application'),
    path('edit_la_inspector_details/<int:Record_Id>', views.edit_la_inspector_details,
         name='edit_la_inspector_details'),
    path('submit_la_application', views.submit_la_application, name='submit_la_application'),
    path('approve_fo_la_import', views.approve_fo_la_import, name='approve_fo_la_import'),
    path('reject_fo_la_import', views.reject_fo_la_import, name='reject_fo_la_import'),
    path('update_details_la', views.update_details_la, name='update_details_la'),

    # import permit for livestock products and animal feed
    path('import_permit_application', views.import_permit_application, name='import_permit_application'),
    path('save_import_lp', views.save_import_lp, name='save_import_lp'),
    path('import_livestock_product_details', views.import_livestock_product_details,
         name='import_livestock_product_details'),
    path('add_livestock_product_file', views.add_livestock_product_file, name='add_livestock_product_file'),
    path('add_livestock_product_name', views.add_livestock_product_name, name='add_livestock_product_name'),
    path('delete_lp_file', views.delete_lp_file, name='delete_lp_file'),
    path('submit_livestock_product_application', views.submit_livestock_product_application,
         name='submit_livestock_product_application'),
    path('approve_fo_lp_import', views.approve_fo_lp_import, name='approve_fo_lp_import'),
    path('reject_fo_lp_import', views.reject_fo_lp_import, name='reject_fo_lp_import'),
    path('update_details_lp', views.update_details_lp, name='update_details_lp'),
    path('submit_lp_application', views.submit_lp_application, name='submit_lp_application'),

    # export certificate for animal and animal products
    path('export_certificate_application', views.export_certificate_application, name='export_certificate_application'),
    path('save_livestock_export', views.save_livestock_export, name="save_livestock_export"),
    path('save_liv_export_details', views.save_liv_export_details, name='save_liv_export_details'),
    path('add_liv_export_file', views.add_liv_export_file, name='add_liv_export_file'),
    path('add_ec_file_name', views.add_ec_file_name, name='add_ec_file_name'),
    path('submit_ec_details', views.submit_ec_details, name='submit_ec_details'),
    path('approve_application_export', views.approve_application_export, name='approve_application_export'),
    path('reject_application_export', views.reject_application_export, name='reject_application_export'),
    path('delete_ec_file', views.delete_ec_file, name='delete_ec_file'),

    # movement permit for animal, animal products and animal feed apply_movement_permit
    path('movement_permit_application', views.movement_permit_application, name='movement_permit_application'),
    path('save_movement_permit_application', views.save_movement_permit_application,
         name='save_movement_permit_application'),
    path('save_movement_permit_details', views.save_movement_permit_details, name='save_movement_permit_details'),
    path('add_lmp_file', views.add_lmp_file, name='add_lmp_file'),
    path('add_lmp_file_name', views.add_lmp_file_name, name='add_lmp_file_name'),
    path('delete_lmp_file', views.delete_ec_file, name='delete_lmp_file'),
    path('submit_lmp_details', views.submit_lmp_details, name='submit_lmp_details'),
    path('details_ins_lmp', views.details_ins_lmp, name='details_ins_lmp'),
    path('approve_application_lmp', views.approve_application_lmp, name='approve_application_lmp'),
    path('reject_application_lmp', views.reject_application_lmp, name='reject_application_lmp'),

    # Ante Mortem And Post Mortem
    path('application_form', views.application_form, name='application_form'),
    path('save_application_form', views.save_application_form, name='save_application_form'),
    path('save_mortem_details', views.save_mortem_details, name='save_mortem_details'),
    path('add_mortem_file', views.add_mortem_file, name='add_mortem_file'),
    path('add_mortem_file_name', views.add_mortem_file_name, name='add_mortem_file_name'),
    path('submit_mortem_details', views.submit_mortem_details, name='submit_mortem_details'),
    path('approve_application_apm', views.approve_application_apm, name='approve_application_apm'),
    path('reject_application_apm', views.reject_application_apm, name='reject_application_apm'),
    path('delete_mortem_file', views.delete_mortem_file, name='delete_mortem_file'),
    path('load_gewog', views.load_gewog, name='load_gewog'),
    path('load_village', views.load_village, name='load_village'),
    path('load_location', views.load_location, name='load_location'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
