from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from livestock import views

urlpatterns = [
    # clearance for meat shop
    path('apply_clearance_meat_shop', views.apply_clearance_meat_shop, name='apply_clearance_meat_shop'),
    path('save_meat_shop_clearance', views.save_meat_shop_clearance, name='save_meat_shop_clearance'),
    path('load_gewog', views.load_gewog, name='load_gewog'),
    path('load_village', views.load_village, name='load_village'),
    path('load_location', views.load_location, name='load_location'),
    path('meat_shop_clearance_app', views.meat_shop_clearance_app, name='meat_shop_clearance_app'),
    path('load_application_details', views.load_application_details, name='load_application_details'),
    path('load_attachment_details', views.load_attachment_details, name='load_attachment_details'),
    path('save_meat_shop_file', views.save_meat_shop_file, name="save_meat_shop_file"),
    path('add_meat_shop_file_name', views.add_meat_shop_file_name, name='add_meat_shop_file_name'),
    path('delete_meat_shop_file', views.delete_meat_shop_file, name='delete_meat_shop_file'),
    path('submit_details', views.submit_details, name='submit_details'),
    path('details_ins_CMS', views.details_ins_cms, name='details_ins_CMS'),
    path('approve_application_cms', views.approve_application_cms, name='approve_application_cms'),
    path('reject_application_cms', views.reject_application_cms, name='reject_application_cms'),
    path('resubmit_application_cms', views.resubmit_application_cms, name='resubmit_application_cms'),

    # import permit for live animal and fish
    path('import_permit', views.import_permit, name='import_permit'),
    path('save_import_la_fish', views.save_import_la_fish, name='save_import_la_fish'),
    path('import_permit_details', views.import_permit_la_details, name='import_permit_details'),
    path('add_liv_permit_file', views.add_la_permit_file, name='add_liv_permit_file'),
    path('add_permit_file_name', views.add_la_file_name, name='add_permit_file_name'),
    path('submit_import_application', views.submit_import_application, name='submit_import_application'),
    path('edit_la_inspector_details/<int:Record_Id>', views.edit_la_inspector_details, name='edit_la_inspector_details'),
    path('submit_la_application', views.submit_la_application, name='submit_la_application'),

    # import permit for livestock products and animal feed
    path('import_permit_application', views.import_permit_application, name='import_permit_application'),
    path('save_import_lp', views.save_import_lp, name='save_import_lp'),
    path('import_livestock_product_details', views.import_livestock_product_details,
         name='import_livestock_product_details'),
    path('add_livestock_product_file', views.add_livestock_product_file, name='add_livestock_product_file'),
    path('add_livestock_product_name', views.add_livestock_product_name, name='add_livestock_product_name'),
    path('submit_livestock_product_application', views.submit_livestock_product_application,
         name='submit_livestock_product_application'),
    path('approve_fo_lp_import', views.approve_fo_lp_import, name='approve_fo_lp_import'),
    path('reject_fo_lp_import', views.reject_fo_lp_import, name='reject_fo_lp_import'),
    path('edit_lp_inspector_details/<int:Record_Id>', views.edit_lp_inspector_details, name='edit_lp_inspector_details'),
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

    # movement permit for animal, animal products and animal feed apply_movement_permit
    path('movement_permit_application', views.movement_permit_application, name='movement_permit_application'),
    path('save_movement_permit_application', views.save_movement_permit_application,
         name='save_movement_permit_application'),
    path('save_movement_permit_details', views.save_movement_permit_details, name='save_movement_permit_details'),
    path('add_lmp_file', views.add_lmp_file, name='add_lmp_file'),
    path('add_lmp_file_name', views.add_lmp_file_name, name='add_lmp_file_name'),
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
    path('reject_application_apm', views.reject_application_apm, name='reject_application_apm')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
