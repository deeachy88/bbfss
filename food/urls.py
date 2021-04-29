from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from food import views

urlpatterns = [
    # Food Business Registration And Licensing
    path('food_business_registration_licensing', views.food_business_registration_licensing,
         name='food_business_registration_licensing'),
    path('food_export_certificate_application', views.food_export_certificate_application,
         name='food_export_certificate_application'),
    path('save_food_export_details', views.save_food_export_details, name='save_food_export_details'),
    path('submit_food_export_application', views.submit_food_export_application, name='submit_food_export_application'),
    path('food_export_file', views.food_export_file, name='food_export_file'),
    path('food_export_file_name', views.food_export_file_name, name='food_export_file_name'),
    path('approve_food_export', views.approve_food_export, name='approve_food_export'),
    path('reject_food_export', views.reject_food_export, name='reject_food_export'),


    # Licensing of Food Handler
    path('food_handler_licensing', views.food_handler_licensing,
         name='food_handler_licensing'),
    path('save_food_handler_details', views.save_food_handler_details, name='save_food_handler_details'),
    path('food_handler_file', views.food_handler_file, name='food_handler_file'),
    path('food_handler_file_name', views.food_handler_file_name, name='food_handler_file_name'),
    path('submit_food_handler_application', views.submit_food_handler_application,
         name='submit_food_handler_application'),
    path('food_handler_forward_application',views.food_handler_forward_application,
         name='food_handler_forward_application'),
    path('reject_food_handler_application', views.reject_food_handler_application,
         name='reject_food_handler_application'),

    # Common
    path('food_handler_application', views.food_handler_application, name='food_handler_application'),
    path('update_batch_no', views.update_batch_no, name='update_batch_no'),
    path('result_update_list', views.result_update_list, name='result_update_list'),
    path('result_update', views.result_update, name='result_update')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)