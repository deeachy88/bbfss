from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from certification import views

urlpatterns = [
    # clearance for meat shop
    path('organic_certificate', views.organic_certificate, name='organic_certificate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)