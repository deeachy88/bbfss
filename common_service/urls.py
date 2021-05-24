from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from common_service import views

urlpatterns = [
    # Complaint service
    path('submit_complaint', views.submit_complaint, name='submit_complaint'),
    path('load_gewog', views.load_gewog, name='load_gewog'),
    path('load_village', views.load_village, name='load_village'),
    path('co_complaint_list', views.co_complaint_list, name='co_complaint_list'),
    path('investigation_complaint_list', views.investigation_complaint_list, name='investigation_complaint_list'),
    path("investigation_complaint_details", views.investigation_complaint_details, name="investigation_complaint_details"),
    path('co_complaint_details', views.co_complaint_details, name='co_complaint_details'),
    path('apply_complaint_form', views.apply_complaint_form, name='apply_complaint_form'),
    path('complaint_details', views.complaint_details, name='complaint_details'),
    path('acknowledge_complaint', views.acknowledge_complaint, name='acknowledge_complaint'),
    path('forward_complaint_by_co', views.forward_complaint_by_co, name='forward_complaint_by_co'),
    path('forward_complaint_to_co', views.forward_complaint_to_co, name='forward_complaint_to_co'),
    path('investigation_report_list', views.investigation_report_list, name='investigation_report_list'),
    path('investigation_report_details', views.investigation_report_details, name='investigation_report_details'),
    path('close_complaint', views.close_complaint, name='close_complaint'),

    path('inspection_and_monitoring_form', views.inspection_and_monitoring_form,
         name='inspection_and_monitoring_form'),
    path('save_sample_details', views.save_sample_details, name='save_sample_details'),
    path('save_item_details', views.save_item_details, name='save_item_details'),
    path('save_owner_manager_details', views.save_owner_manager_details, name='save_owner_manager_details'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
