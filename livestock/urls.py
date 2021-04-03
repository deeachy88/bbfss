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


    # import permit for live animal and fish


    # import permit for livestock products and animal feed


    # export certificate for animal and animal products


    # movement permit for animal, animal products and animal feed apply_movement_permit


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
