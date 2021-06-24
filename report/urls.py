from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from common_service import views

urlpatterns = [
    # Complaint service
    path('certificate_reportForm', views.certificate_reportForm, name='certificate_reportForm'),
    path('permit_reportFrom', views.permit_reportFrom, name='permit_reportFrom'),
    path('view_certificateList', views.view_certificateList, name='view_certificateList'),
    path('view_permitList', views.view_permitList, name='view_permitList'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
