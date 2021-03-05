from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


from plant import views

urlpatterns = [
    path('apply_movement_permit', views.apply_movement_permit, name='apply_movement_permit'),
    path('save_details', views.save_details, name='save_details'),
    path('load_gewog', views.load_gewog, name='load_gewog'),
    path('load_village', views.load_village, name='load_village'),
    path('load_location', views.load_location, name='load_location'),
    path('movement_permit_app', views.movement_permit_app, name='movement_permit_app'),
    path('load_details_page', views.load_details_page, name='load_details_page'),
    path('update_application_details', views.update_application_details, name='update_details'),
    path('save', views.save, name='save'),
    path('save_movement_permit', views.save_movement_permit, name='save_movement_permit'),
    path('oic_app', views.oic_app, name='movement_permit_app_oic'),
    path('ins_app', views.ins_app, name='movement_permit_app_ins'),
    path('view_app_details', views.view_app_details, name='get_application_details'),
    path('forward_application', views.forward_application, name='forward_application'),
    path('view_app_details_ins', views.view_app_details_ins, name='view_app_details_ins'),
    path('approve_application', views.approve_application, name='approve_application'),
    path('reject_application', views.reject_application, name='reject_application'),
    path('add_details_ins', views.add_details_ins, name='add_details_ins'),
    path('save_file', views.add_file, name="save_file"),
    path('add_file_name', views.add_file_name, name='add_file_name')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
