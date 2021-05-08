from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from common_service import views

urlpatterns = [
    # clearance for meat shop
    path('submit_complaint', views.submit_complaint, name='submit_complaint'),
    path('load_gewog', views.load_gewog, name='load_gewog'),
    path('load_village', views.load_village, name='load_village'),
    path('complaint_app', views.complaint_app, name='complaint_app'),

    path('approve_application_cms', views.approve_application_cms, name='approve_application_cms'),
    path('reject_application_cms', views.reject_application_cms, name='reject_application_cms'),
    path('resubmit_application_cms', views.resubmit_application_cms, name='resubmit_application_cms'),

    path('co_complaint_list', views.co_complaint_list, name='co_complaint_list'),
    path('co_complaint_details', views.co_complaint_details, name='co_complaint_details'),
    path('apply_complaint_form', views.apply_complaint_form, name='apply_complaint_form'),
    path('acknowledge_complaint', views.acknowledge_complaint, name='acknowledge_complaint'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
