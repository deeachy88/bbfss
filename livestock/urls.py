from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from livestock import views

urlpatterns = [
    # clearance for meat shop
    path('apply_clearance_meat_shop', views.apply_clearance_meat_shop, name='apply_clearance_meat_shop'),



    # import permit for live animal and fish


    # import permit for livestock products and animal feed


    # export certificate for animal and animal products


    # movement permit for animal, animal products and animal feed apply_movement_permit


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
