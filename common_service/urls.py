from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from common_service import views

urlpatterns = [
    # inspection_and_monitoring
    path('inspection_and_monitoring', views.inspection_and_monitoring, name='inspection_and_monitoring'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)