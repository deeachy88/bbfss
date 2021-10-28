from datetime import date, datetime, timedelta

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils import formats

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_location_field_office_mapping, \
    t_user_master, t_field_office_master, t_plant_crop_master, t_plant_pesticide_master, t_plant_crop_variety_master
from food.models import t_food_export_certificate_t1, t_food_licensing_food_handler_t1, t_food_import_permit_t1, \
    t_food_business_registration_licensing_t1
from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_ante_post_mortem_t1, \
    t_livestock_movement_permit_t1, t_livestock_import_permit_product_t1, t_livestock_import_permit_animal_t1, \
    t_livestock_export_certificate_t1

from plant.models import t_workflow_details, t_plant_movement_permit_t2, t_plant_movement_permit_t1, \
    t_plant_movement_permit_t3, t_file_attachment, t_plant_import_permit_t1, t_plant_import_permit_t2, \
    t_plant_import_permit_inspection_t3, t_plant_export_certificate_plant_plant_products_t1, \
    t_plant_clearence_nursery_seed_grower_t1, t_plant_clearence_nursery_seed_grower_t2, t_plant_seed_certification_t1, \
    t_plant_seed_certification_t2, t_plant_seed_certification_t3, t_payment_details
from certification.models import t_certification_gap_t1, t_certification_gap_t2, t_certification_gap_t3, \
    t_certification_gap_t4, t_certification_gap_t5, t_certification_gap_t6, t_certification_gap_t7, \
    t_certification_gap_t8, t_certification_food_t1, t_certification_food_t2, t_certification_food_t3, \
    t_certification_food_t4, t_certification_food_t5, t_certification_organic_t1, t_certification_organic_t2, \
    t_certification_organic_t3, t_certification_organic_t4, t_certification_organic_t5, \
    t_certification_organic_t6, t_certification_organic_t7, t_certification_organic_t8, t_certification_organic_t9, \
    t_certification_organic_t10, t_certification_organic_t11
from administrator.models import t_service_master

def certificate_report_form(request):
    field_office = t_field_office_master.objects.all()
    return render(request, 'certificate_report_form.html')

def permit_report_form(request):
    field_office = t_field_office_master.objects.all()
    return render(request, 'permit_report_form.html')

def view_certificate_list(request):
    fromDate = request.GET.get('from_date')
    toDate = request.GET.get('to_date')
    serviceId = request.GET.get('service_id')
    service_name = t_service_master.objects.filter(Service_Id=serviceId)
    if serviceId == '16':
        certificate_details = t_certification_gap_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)
    elif serviceId == '17':
        certificate_details = t_certification_organic_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)
    elif serviceId == '18':
        certificate_details = t_certification_food_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)

    return render(request, 'certificate_list.html', {'certificate_details': certificate_details, 'service_name': service_name})

def view_permit_list(request):
    fromDate = request.GET.get('from_date')
    toDate = request.GET.get('to_date')
    serviceId = request.GET.get('service_id')
    service_name = t_service_master.objects.filter(Service_Id=serviceId)
    dzongkhag = t_dzongkhag_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    if serviceId == '1':    # List of Movement Permit For Plant And Products Issued
        permit_details = t_plant_movement_permit_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '2':  # List of Import Permit For Plant And Plant Products Issued
        permit_details = t_plant_import_permit_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '3':  # List of Export Permit For Plant And Plant Products Issued
        permit_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '4':  # List of Nurseries/Seed Growers Registered
        permit_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '5':  # List of Seed Certification Issued
        permit_details = t_plant_seed_certification_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '6':  # List of Meat Shop License Issued
        permit_details = t_livestock_clearance_meat_shop_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)
    elif serviceId == '7':  # List of Ante Mortem And Post Mortem Certificate Issued
        permit_details = t_livestock_ante_post_mortem_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '8':  # List of Movement Permit For Livestock Issued
        permit_details = t_livestock_movement_permit_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '9':  # List of Import Permit for Livestock Products Issued
        permit_details = t_livestock_import_permit_product_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)
    elif serviceId == '10':     # List of Import Permit For Live Animal And Fish Issued
        permit_details = t_livestock_import_permit_animal_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)
    elif serviceId == '11':     # List of Export Certificate for Animal and Animal Products Issued
        permit_details = t_livestock_export_certificate_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)
    elif serviceId == '12':     # List of Export Certificate for Food Products Issued
        permit_details = t_food_export_certificate_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '13':     # List of Food Handler Certificate Issued
        permit_details = t_food_licensing_food_handler_t1.objects.filter(Approved_Date__gte=fromDate, Approved_Date__lte=toDate)
    elif serviceId == '14':     # List of Import Permit for Food Products Issued
        permit_details = t_food_import_permit_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)
    elif serviceId == '15':     # List of Food Business Registered And License Issued
        permit_details = t_food_business_registration_licensing_t1.objects.filter(Approve_Date__gte=fromDate, Approve_Date__lte=toDate)

    return render(request, 'permit_list.html', {'permit_details': permit_details, 'service_name': service_name,
                                                'location':location})
