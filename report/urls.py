from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path

urlpatterns = [
    path('certificate_report_form', views.certificate_report_form, name='certificate_report_form'),
    path('permit_report_form', views.permit_report_form, name='permit_report_form'),
    path('view_certificate_list', views.view_certificate_list, name='view_certificate_list'),
    path('view_permit_list', views.view_permit_list, name='view_permit_list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
