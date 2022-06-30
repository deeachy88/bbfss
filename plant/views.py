from datetime import date, datetime, timedelta

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max, Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
import requests
import numpy as np
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from zeep import Client
from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_location_field_office_mapping, \
    t_user_master, t_field_office_master, t_plant_crop_master, t_plant_pesticide_master, t_plant_crop_variety_master, \
    t_service_master, t_country_master, t_plant_crop_category_master, t_unit_master, t_section_master, \
    t_inspection_type_master, t_livestock_species_master, t_livestock_species_breed_master
from administrator.views import dashboard
from bbfss import settings
from bbfss.settings import MEDIA_ROOT, MEDIA_URL
from common_service.models import t_common_complaint_t1
from food.models import t_food_export_certificate_t1, t_food_licensing_food_handler_t1, t_food_import_permit_t1, \
    t_food_import_permit_t2, t_food_import_permit_inspection_t1, t_food_import_permit_inspection_t2, \
    t_food_business_registration_licensing_t1, t_food_business_registration_licensing_t2, \
    t_food_business_registration_licensing_t5, t_food_business_registration_licensing_t4, \
    t_food_business_registration_licensing_t3, t_food_business_registration_licensing_t6, \
    t_food_import_permit_inspection_t3, t_food_business_registration_licensing_t7, \
    t_food_business_registration_licensing_t8
from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_ante_post_mortem_t2, \
    t_livestock_ante_post_mortem_t1, t_livestock_movement_permit_t1, t_livestock_movement_permit_t2, \
    t_livestock_export_certificate_t1, t_livestock_export_certificate_t2, \
    t_livestock_import_permit_animal_inspection_t1, t_livestock_import_permit_animal_inspection_t2, \
    t_livestock_import_permit_product_inspection_t1, t_livestock_import_permit_product_inspection_t2, \
    t_livestock_import_permit_animal_t1, t_livestock_import_permit_animal_t2, t_livestock_import_permit_product_t1, \
    t_livestock_import_permit_product_t2, t_livestock_clearance_meat_shop_t2, t_livestock_clearance_meat_shop_t5, \
    t_livestock_clearance_meat_shop_t4, t_livestock_clearance_meat_shop_t6, \
    t_livestock_import_permit_product_inspection_t3, t_livestock_import_permit_animal_inspection_t3, \
    t_livestock_movement_permit_t3
from plant.forms import ImportFormThree, ImportFormTwo
from plant.models import t_workflow_details, t_plant_movement_permit_t2, t_plant_movement_permit_t1, \
    t_plant_movement_permit_t3, t_file_attachment, t_plant_import_permit_t1, t_plant_import_permit_t2, \
    t_plant_export_certificate_plant_plant_products_t1, \
    t_plant_clearence_nursery_seed_grower_t1, t_plant_clearence_nursery_seed_grower_t2, t_plant_seed_certification_t1, \
    t_plant_seed_certification_t2, t_plant_seed_certification_t3, t_payment_details, \
    t_plant_import_permit_inspection_t3, t_plant_import_permit_inspection_t1, t_plant_import_permit_inspection_t2, \
    t_plant_clearence_nursery_seed_grower_t3, t_payment_details_master, \
    t_plant_export_certificate_plant_plant_products_t2
from certification.models import t_certification_gap_t1, t_certification_gap_t2, t_certification_food_t3, \
    t_certification_gap_t4, t_certification_gap_t5, t_certification_gap_t6, t_certification_gap_t7, \
    t_certification_gap_t8, t_certification_food_t1, t_certification_food_t2, t_certification_food_t3, \
    t_certification_food_t4, t_certification_food_t5, t_certification_organic_t1, t_certification_organic_t2, \
    t_certification_food_t3, t_certification_organic_t4, t_certification_organic_t5, t_certification_organic_t6, \
    t_certification_organic_t7, t_certification_organic_t8, t_certification_organic_t9, t_certification_organic_t10, \
    t_certification_organic_t11


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def focal_officer_application(request):
    try:
        Role_Id = request.session['Role_Id']
        section = request.session['section']
        Login_Id = request.session['Login_Id']
    except:
        Login_Id = None
    if Login_Id:
        section_details = t_section_master.objects.filter(Section_Id=section)
        for id_section in section_details:
            section_name = id_section.Section_Name

            application_details = t_workflow_details.objects.filter(assigned_role_id=Role_Id, application_status='ATA',
                                                                    action_date__isnull=False, section=section_name) \
                                  | t_workflow_details.objects.filter(assigned_role_id=Role_Id, application_status='P',
                                                                      action_date__isnull=False, section=section_name) \
                                  | t_workflow_details.objects.filter(assigned_role_id=Role_Id, application_status='AA',
                                                                      action_date__isnull=False, section=section_name) \
                                  | t_workflow_details.objects.filter(assigned_role_id=Role_Id,
                                                                      application_status='ACK',
                                                                      action_date__isnull=False, section=section_name) \
                                  | t_workflow_details.objects.filter(assigned_role_id=Role_Id, application_status='CA',
                                                                      action_date__isnull=False, section=section_name) \
                                  | t_workflow_details.objects.filter(assigned_role_id=Role_Id,
                                                                      application_status='FRA',
                                                                      action_date__isnull=False, section=section_name) | \
                                  t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APA',
                                                                    action_date__isnull=False) \
                                  | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                                      action_date__isnull=False) \
                                  | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='P',
                                                                      action_date__isnull=False) \
                                  | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='A',
                                                                      service_code='COM') \
                                  | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP')
            service_details = t_service_master.objects.all()
            message_count = (t_workflow_details.objects.filter(
                assigned_role_id=Role_Id, section=section_name,
                action_date__isnull=False, application_status='P') | t_workflow_details.objects.filter(
                assigned_role_id=Role_Id, section=section_name,
                action_date__isnull=False, application_status='ATA') | t_workflow_details.objects.filter(
                assigned_role_id=Role_Id, section=section_name,
                action_date__isnull=False, application_status='FRA') |
                             t_workflow_details.objects.filter(
                                 assigned_role_id=Role_Id, section=section_name,
                                 action_date__isnull=False, application_status='CA')
                             | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='P',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP')
                             ).count()
            return render(request, 'focal_officer_pending_list.html', {'application_details': application_details,
                                                                       'service_details': service_details,
                                                                       'count': message_count})
    else:
        return render(request, 'redirect_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def oic_application(request):
    try:
        Login_Id = request.session['Login_Id']
        Field_Office_Id = request.session['field_office_id']
    except:
        Login_Id = None
    if Login_Id:
        new_import_app = t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                           application_status='P', action_date__isnull=False) | \
                         t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                           application_status='I', action_date__isnull=False) | \
                         t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                           application_status='FR', action_date__isnull=False) | \
                         t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                           action_date__isnull=False) | \
                         t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP',
                                                           action_date__isnull=False) | \
                         t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APA',
                                                           action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                             action_date__isnull=False)

        service_details = t_service_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                           action_date__isnull=False) |
                         t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                           action_date__isnull=False) |
                         t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP',
                                                           action_date__isnull=False)).count()
        oic_count = (t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP',
                                                       action_date__isnull=False)
                     | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                         application_status='I',
                                                         action_date__isnull=False)
                     | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                         application_status='FI',
                                                         action_date__isnull=False)
                     | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                         application_status='FR',
                                                         action_date__isnull=False)
                     | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                         application_status='P',
                                                         action_date__isnull=False)
                     | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APA',
                                                         action_date__isnull=False)
                     | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                         action_date__isnull=False)).count()
        return render(request, 'oic_pending_list.html',
                      {'service_details': service_details, 'application_details': new_import_app,
                       'count': message_count, 'oic_count': oic_count})
    else:
        return render(request, 'redirect_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inspector_application(request):
    try:
        Login_Id = request.session['Login_Id']
        Field_Office_Id = request.session['field_office_id']
    except:
        Login_Id = None
    if Login_Id:
        new_import_app = t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP',
                                                           action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                             application_status='I', action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                             application_status='FI', action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                             application_status='FR', action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                             application_status='P', action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APA',
                                                             action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                             action_date__isnull=False)
        service_details = t_service_master.objects.all()

        message_count = (t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP',
                                                           action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                             application_status='I',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                             application_status='FI',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                             application_status='FR',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id,
                                                             application_status='P',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        fhc_count = (t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP',
                                                       action_date__isnull=False, service_code='FHC') |
                     t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='A',
                                                       action_date__isnull=False, service_code='FHC')).count()
        return render(request, 'inspector_pending_list.html',
                      {'service_details': service_details, 'application_details': new_import_app,
                       'ins_count': message_count, 'fhc_count': fhc_count})
    else:
        return render(request, 'redirect_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def complain_officer_application(request):
    try:
        Login_Id = request.session['Login_Id']
    except:
        Login_Id = None
    if Login_Id:
        new_import_app = t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP',
                                                           action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APA',
                                                             action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                             action_date__isnull=False)
        service_details = t_service_master.objects.all()
        return render(request, 'complain_officer_pending_list.html',
                      {'service_details': service_details, 'application_details': new_import_app})
    else:
        return render(request, 'redirect_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def chief_application(request):
    try:
        Login_Id = request.session['Login_Id']
    except:
        Login_Id = None
    if Login_Id:
        new_import_app = t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='AP',
                                                           action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APA',
                                                             action_date__isnull=False) \
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCF',
                                                             action_date__isnull=False)
        service_details = t_service_master.objects.all()
        return render(request, 'chief_pending_list.html',
                      {'service_details': service_details, 'application_details': new_import_app})
    else:
        return render(request, 'redirect_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apply_movement_permit(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None

    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        unit = t_unit_master.objects.filter(Unit_Type='S')
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'movement_permit/apply_movement_permit.html',
                      {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village, 'location': location,
                       'count': message_count, 'count_call': inspection_call_count,
                       'consignment_call_count': consignment_call_count, 'unit': unit})
    else:
        return render(request, 'redirect_page.html')


def save_details(request):
    appNo = request.POST.get('applicationNo')
    workflow_details = t_workflow_details.objects.filter(application_no=appNo)
    workflow_details.update(action_date=date.today())
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'movement_permit/apply_movement_permit.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def save_movement_permit(request):
    data = dict()
    service_code = "MPP"
    last_application_no = get_application_no(request, service_code)
    Applicant_Id = request.session['email']
    Permit_Type = request.POST.get('permitType')
    reg_No = request.POST.get('regNo')
    if reg_No is None:
        License_No = 'NA'
    else:
        License_No = reg_No
    companyName = request.POST.get('companyName')
    if companyName is None:
        Nursery_Name = 'NA'
    else:
        Nursery_Name = companyName
    CID = request.POST.get('cid')
    Applicant_Name = request.POST.get('Name')
    Contact_No = request.POST.get('contactNumber')
    Email = request.POST.get('email')
    Dzongkhag_Code = request.POST.get('dzongkhag')
    Gewog_Code = request.POST.get('gewog')
    Village_Code = request.POST.get('village')
    From_Dzongkhag_Code = request.POST.get('from_dzongkhag')
    From_Gewog_Code = request.POST.get('from_gewog')
    From_Location = request.POST.get('from_location')
    To_Dzongkhag_Code = request.POST.get('to_dzongkhag')
    To_Gewog_Code = request.POST.get('to_gewog')
    To_Location = request.POST.get('to_exact_location')
    Authorized_Route = request.POST.get('route')
    Movement_Purpose = request.POST.get('movementPurpose')
    Conveyance_Means = request.POST.get('conveyanceMeans')
    Vehicle_No = request.POST.get('vehicleNo')
    Movement_Date = request.POST.get('date')
    t_plant_movement_permit_t1.objects.create(
        Application_No=last_application_no,
        Permit_Type=Permit_Type,
        License_No=License_No,
        Nursery_Name=Nursery_Name,
        CID=CID,
        Applicant_Name=Applicant_Name,
        Contact_No=Contact_No,
        Email=Email,
        Dzongkhag=Dzongkhag_Code,
        Gewog=Gewog_Code,
        Village=Village_Code,
        From_Dzongkhag_Code=From_Dzongkhag_Code,
        From_Gewog_Code=From_Gewog_Code,
        From_Location=From_Location,
        To_Dzongkhag_Code=To_Dzongkhag_Code,
        To_Gewog_Code=To_Gewog_Code,
        To_Location=To_Location,
        Authorized_Route=Authorized_Route,
        Movement_Purpose=Movement_Purpose,
        Conveyance_Means=Conveyance_Means,
        Qty=None,
        Unit=None,
        Vehicle_No=Vehicle_No,
        Movement_Date=Movement_Date,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Application_Status=None,
        Movement_Permit_No=None,
        Remarks=None,
        Application_Date=date.today(),
        Applicant_Id=Applicant_Id,
        Approved_Date=None,
        Validity_Period=None,
        Validity=None
    )
    plant_details = t_plant_movement_permit_t1.objects.filter(Application_No=last_application_no)
    if Conveyance_Means == "Air":
        plant_details.update(Vehicle_No=Vehicle_No)
    field_id = t_location_field_office_mapping.objects.filter(pk=From_Gewog_Code)
    for field_office in field_id:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(application_no=last_application_no, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=field_office_id, section='Plant',
                                      assigned_role_id='4',
                                      action_date=None, application_status='P',
                                      service_code=service_code)
    data['applicationNo'] = last_application_no
    return JsonResponse(data)


def get_application_no(request, service_code):
    last_application_no = t_plant_movement_permit_t1.objects.aggregate(Max('Application_No'))
    lastAppNo = last_application_no['Application_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = service_code + "-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = service_code + "-" + str(year) + "-" + AppNo
    return newAppNo


def load_gewog(request):
    dzongkhag_id = request.GET.get('dzongkhag_id')
    gewog_list = t_gewog_master.objects.filter(Dzongkhag_Code_id=dzongkhag_id).order_by('Gewog_Name')
    return render(request, 'gewog_list.html', {'gewog_list': gewog_list})


def load_village(request):
    gewog_id = request.GET.get('gewog_id')
    village_list = t_village_master.objects.filter(Gewog_Code_id=gewog_id).order_by('Village_Name')
    return render(request, 'village_list.html', {'village_list': village_list})


def load_location(request):
    dzongkhag_id = request.GET.get('dzongkhag_id')
    location_list = t_location_field_office_mapping.objects.filter(Dzongkhag_Code_id=dzongkhag_id).order_by(
        'Location_Name')
    return render(request, 'movement_permit/location_list.html', {'location_list': location_list})


def load_to_location(request):
    dzongkhag_id = request.GET.get('dzongkhag_id')
    location_list = t_location_field_office_mapping.objects.filter(Dzongkhag_Code_id=dzongkhag_id).order_by(
        'Location_Name')
    return render(request, 'movement_permit/to_location_list.html', {'location_list': location_list})


def to_gewog_list(request):
    dzongkhag_id = request.GET.get('dzongkhag_id')
    location_list = t_location_field_office_mapping.objects.filter(Dzongkhag_Code_id=dzongkhag_id).order_by(
        'Location_Name')
    return render(request, 'movement_permit/to_gewog_list.html', {'location_list': location_list})


def load_location_nursery(request):
    dzongkhag_id = request.GET.get('dzongkhag_id')
    location_list = t_location_field_office_mapping.objects.filter(Dzongkhag_Code_id=dzongkhag_id).order_by(
        'Location_Name')
    return render(request, 'nursery_registration/location_list.html', {'location_list': location_list})


def movement_permit_app(request):
    appNo = request.GET.get('appId')
    imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=appNo)
    return render(request, 'movement_permit/apply_movement_permit_page.html', {'import': imports_plant, 'title': appNo})


def load_details_page(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    return render(request, 'movement_permit/movement_permit_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location': location})


def agro_details_page(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    return render(request, 'movement_permit/movement_permit_agro_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location': location})


def update_application_details(request):
    data = dict()
    application_id = request.POST.get('applicationNo')
    regNo = request.POST.get('regNo')
    companyName = request.POST.get('companyName')
    cid = request.POST.get('cid')
    Name = request.POST.get('Name')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location_code = request.POST.get('location_code')
    fromDzongkhag = request.POST.get('fromDzongkhag')
    toDzongkhag = request.POST.get('toDzongkhag')
    route = request.POST.get('route')
    productSource = request.POST.get('productSource')
    movementPurpose = request.POST.get('movementPurpose')
    conveyanceMeans = request.POST.get('conveyanceMeans')

    application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    application_details.update(License_No=regNo)
    application_details.update(Nursery_Name=companyName)
    application_details.update(CID=cid)
    application_details.update(Applicant_Name=Name)
    application_details.update(Contact_No=contact_number)
    application_details.update(Email=email)
    application_details.update(Dzongkhag_Code=dzongkhag)
    application_details.update(Gewog_Code=gewog)
    application_details.update(Village_Code=village)
    application_details.update(Location_Code=location_code)
    application_details.update(From_Dzongkhag_Code=fromDzongkhag)
    application_details.update(To_Dzongkhag_Code=toDzongkhag)
    application_details.update(Authorized_Route=route)
    application_details.update(Source_Of_Product=productSource)
    application_details.update(Movement_Purpose=movementPurpose)
    application_details.update(Conveyance_Means=conveyanceMeans)
    data['success'] = "Success"
    return JsonResponse(data)


def save_details_movement(request):
    commodity = request.POST.get('commodity')
    appNo = request.POST.get('appNo')
    qty = request.POST.get('qty')
    unit = request.POST.get('unit')
    remarks = request.POST.get('remarks')
    t_plant_movement_permit_t2.objects.create(Application_No=appNo, Commodity=commodity,
                                              Qty=qty, Unit=unit, Remarks=remarks)
    imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=appNo)
    movement_count = t_plant_movement_permit_t2.objects.filter(Application_No=appNo).count()
    return render(request, 'movement_permit/movement_page.html', {'import': imports_plant,
                                                                  'movement_count': movement_count})


def forward_application(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')

    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(assigned_to=forwardTo)
    application_details.update(action_date=date.today())
    application_details.update(assigned_role_id='5')
    Field_Office_Id = request.session['field_office_id']

    Role_Id = request.session['Role_Id']
    application_Lists = t_workflow_details.objects.filter(assigned_to=Role_Id, field_office_id=Field_Office_Id)
    return render(request, 'oic_pending_list.html', {'application_details': application_Lists})


def view_application_details(request):
    application_id = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    if service_code == 'MPP':
        application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_movement_permit_t2.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        movement_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        return render(request, 'movement_permit/app_details_inspector.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'inspector_list': user_role_list, 'movement_permit': movement_permit, 'file': file})
    elif service_code == 'IPP':
        application_details = t_plant_import_permit_inspection_t1.objects.filter(Application_No=application_id)
        location = t_field_office_master.objects.all()
        details_list = t_plant_import_permit_inspection_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        crop = t_plant_crop_master.objects.all()
        pesticide = t_plant_pesticide_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        decision_details = t_plant_import_permit_inspection_t3.objects.filter(Application_No=application_id)
        return render(request, 'import_permit/inspector_import_permit.html',
                      {'application_details': application_details,
                       'location': location, 'import': details_list, 'inspector_list': user_role_list,
                       'file': file, 'crop': crop, 'pesticide': pesticide,
                       'variety': variety, 'decision_details': decision_details})
    elif service_code == 'EPP':
        application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
            Application_No=application_id)
        export_details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(
            Application_No=application_id)
        unit = t_unit_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        dzongkhag = t_dzongkhag_master.objects.all()
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        country = t_country_master.objects.all()
        entry_point = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        return render(request, 'export_permit/inspector_export_permit.html',
                      {'application_details': application_details,
                       'location': location, 'inspector_list': user_role_list,
                       'file': file, 'dzongkhag': dzongkhag, 'unit': unit,
                       'Country': country, 'entry_point': entry_point, 'export_details': export_details})
    elif service_code == 'RNS':
        application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        crop_master = t_plant_crop_master.objects.all()
        crop_category = t_plant_crop_category_master.objects.all()
        decision = t_plant_clearence_nursery_seed_grower_t3.objects.filter(Application_No=application_id)
        return render(request, 'nursery_registration/inspector_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'inspector_list': user_role_list, 'file': file, 'crop_master': crop_master,
                       'crop_category': crop_category, 'decision_details': decision})
    elif service_code == 'RSC':
        application_details = t_plant_seed_certification_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_seed_certification_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        crop = t_plant_crop_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        unit = t_unit_master.objects.all()
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        decision = t_plant_seed_certification_t3.objects.filter(Application_No=application_id)
        return render(request, 'seed_certification/inspector_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'inspector_list': user_role_list, 'file': file, 'crop': crop, 'variety': variety, 'unit': unit,
                       'decision_details': decision})
    elif service_code == 'CMS':
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Application_Status = application.application_status
            if Application_Status == "I":
                application_details = t_livestock_clearance_meat_shop_t1.objects.filter(
                    application_no=application_id)
                details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=application_id)
                file = t_file_attachment.objects.filter(application_no=application_id)
                inspection_details = t_livestock_clearance_meat_shop_t5.objects.filter(
                    application_no=application_id, inspection_type="Feasibility Inspection")
                team_details = t_livestock_clearance_meat_shop_t4.objects.filter(application_no=application_id,
                                                                                 meeting_type="Feasibility Inspection")
                inspection_team_details = t_livestock_clearance_meat_shop_t6.objects.filter(
                    application_no=application_id, meeting_type="Feasibility Inspection")
                unit = t_unit_master.objects.all()
                inspector_list = t_user_master.objects.filter(Role_Id='5')
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                count = t_livestock_clearance_meat_shop_t5.objects.filter(application_no=application_id).count()
                yes_count = t_livestock_clearance_meat_shop_t5.objects.filter(application_no=application_id,
                                                                              concern='Yes').count()
                return render(request, 'meat_shop_registration/feasibility_inspection.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspector_list': inspector_list, 'unit': unit, 'inspection_details': inspection_details,
                               'team_details': team_details, 'inspection_team_details': inspection_team_details,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog, 'count': count,
                               'yes_count': yes_count})
            else:
                application_details = t_livestock_clearance_meat_shop_t1.objects.filter(
                    application_no=application_id)
                details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=application_id)
                file = t_file_attachment.objects.filter(application_no=application_id)
                unit = t_unit_master.objects.all()
                inspection_details = t_livestock_clearance_meat_shop_t5.objects.filter(
                    application_no=application_id, inspection_type="Factory Inspection")
                team_details = t_livestock_clearance_meat_shop_t4.objects.filter(application_no=application_id,
                                                                                 meeting_type="Factory Inspection")
                inspection_team_details = t_livestock_clearance_meat_shop_t6.objects.filter(
                    application_no=application_id, meeting_type="Factory Inspection")
                inspector_list = t_user_master.objects.filter(Role_Id='5')
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                count = t_livestock_clearance_meat_shop_t5.objects.filter(application_no=application_id,
                                                                          nc='Yes').count()
                yes_count = t_livestock_clearance_meat_shop_t5.objects.filter(application_no=application_id,
                                                                              nc='Yes').count()
                return render(request, 'meat_shop_registration/factory_inspection.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspector_list': inspector_list, 'unit': unit, 'inspection_details': inspection_details,
                               'team_details': team_details, 'inspection_team_details': inspection_team_details,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog, 'count': count,
                               'yes_count': yes_count})
    elif service_code == 'APM':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        application_details = t_livestock_ante_post_mortem_t1.objects.filter(Application_No=application_id)
        details = t_livestock_ante_post_mortem_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        return render(request, 'ante_post_mortem/inspector_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'mortem': details,
                       'inspector_list': user_role_list})
    elif service_code == 'LMP':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        application_details = t_livestock_movement_permit_t1.objects.filter(Application_No=application_id)
        details = t_livestock_movement_permit_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        observation = t_livestock_movement_permit_t3.objects.filter(Application_No=application_id)
        return render(request, 'Movement_Permit_Livestock/inspector_movement_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'details': details,
                       'inspector_list': user_role_list, 'observation': observation})
    elif service_code == 'LEC':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_field_office_master.objects.all()
        application_details = t_livestock_export_certificate_t1.objects.filter(Application_No=application_id)
        details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        species = t_livestock_species_master.objects.all()
        field_office = t_field_office_master.objects.all()
        return render(request, 'Export_Certificate/inspector_export_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'details': details,
                       'inspector_list': user_role_list, 'species': species, 'field_office': field_office})
    elif service_code == 'ILP':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        location_details = t_field_office_master.objects.all()
        application_details = t_livestock_import_permit_product_inspection_t1.objects.filter(
            Application_No=application_id)
        details = t_livestock_import_permit_product_inspection_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        observation_details = t_livestock_import_permit_product_inspection_t3.objects.filter(
            Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        return render(request, 'Livestock_Import/inspector_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'import': details,
                       'inspector_list': user_role_list, 'location_details': location_details,
                       'observation_details': observation_details})
    elif service_code == 'IAF':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        location_details = t_field_office_master.objects.all()
        application_details = t_livestock_import_permit_animal_inspection_t1.objects.filter(
            Application_No=application_id)
        details = t_livestock_import_permit_animal_inspection_t2.objects.filter(Application_No=application_id)
        observation_details = t_livestock_import_permit_animal_inspection_t3.objects.filter(
            Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        species = t_livestock_species_master.objects.all()
        breed = t_livestock_species_breed_master.objects.all()
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        return render(request, 'Animal_Fish_Import/inspector_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'import': details,
                       'inspector_list': user_role_list, 'species': species, 'breed': breed,
                       'location_details': location_details, 'observation_details': observation_details})
    elif service_code == 'FEC':
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        country = t_country_master.objects.all()
        field_office = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        location = t_location_field_office_mapping.objects.all()
        unit = t_unit_master.objects.all()
        application_details = t_food_export_certificate_t1.objects.filter(
            Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        return render(request, 'export_certificate_food/inspector_details.html',
                      {'application_details': application_details, 'file': file,
                       'gewog': gewog, 'dzongkhag': dzongkhag, 'country': country, 'field_office': field_office,
                       'unit': unit, 'village': village, 'location': location,
                       'inspector_list': user_role_list})
    elif service_code == "FIP":
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        country = t_country_master.objects.all()
        field_office = t_field_office_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        unit = t_unit_master.objects.all()
        application_details = t_food_import_permit_inspection_t1.objects.filter(
            Application_No=application_id)
        details = t_food_import_permit_inspection_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        observation = t_food_import_permit_inspection_t3.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
            print(Field_Office)
            user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        return render(request, 'import_certificate_food/inspector_details.html',
                      {'application_details': application_details, 'file': file,
                       'dzongkhag': dzongkhag, 'village': village,
                       'gewog': gewog, 'country': country,
                       'field_office': field_office, 'import': details,
                       'location': location, 'unit': unit, 'inspector_list': user_role_list,
                       'observation': observation})
    elif service_code == 'FBR':
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Application_Status = application.application_status
            if Application_Status == "I":
                application_details = t_food_business_registration_licensing_t1.objects.filter(
                    application_no=application_id)
                details = t_food_business_registration_licensing_t2.objects.filter(application_no=application_id)
                food_handler = t_food_business_registration_licensing_t3.objects.filter(application_no=application_id)
                raw_materials = t_food_business_registration_licensing_t7.objects.filter(application_no=application_id)
                packaging_material = t_food_business_registration_licensing_t8.objects.filter(
                    application_no=application_id)
                file = t_file_attachment.objects.filter(application_no=application_id)
                inspection_details = t_food_business_registration_licensing_t5.objects.filter(
                    application_no=application_id, inspection_type="Feasibility Inspection")
                team_details = t_food_business_registration_licensing_t4.objects.filter(
                    application_no=application_id, meeting_type="Feasibility Inspection")
                inspection_team_details = t_food_business_registration_licensing_t6.objects.filter(
                    application_no=application_id, meeting_type="Feasibility Inspection")
                unit = t_unit_master.objects.all()
                inspector_list = t_user_master.objects.filter(Role_Id='5')
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'registration_licensing/feasibility_inspection.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspector_list': inspector_list, 'unit': unit, 'inspection_details': inspection_details,
                               'team_details': team_details, 'inspection_team_details': inspection_team_details,
                               'food_handler': food_handler, 'dzongkhag': dzongkhag, 'gewog': gewog,
                               'village': village, 'packaging_material': packaging_material,
                               'raw_materials': raw_materials})
            else:
                application_details = t_food_business_registration_licensing_t1.objects.filter(
                    application_no=application_id)
                details = t_food_business_registration_licensing_t2.objects.filter(application_no=application_id)
                food_handler = t_food_business_registration_licensing_t3.objects.filter(application_no=application_id)
                raw_materials = t_food_business_registration_licensing_t7.objects.filter(application_no=application_id)
                packaging_material = t_food_business_registration_licensing_t8.objects.filter(
                    application_no=application_id)
                file = t_file_attachment.objects.filter(application_no=application_id)
                unit = t_unit_master.objects.all()
                inspection_details = t_food_business_registration_licensing_t5.objects.filter(
                    application_no=application_id, inspection_type="Factory Inspection")
                team_details = t_food_business_registration_licensing_t4.objects.filter(
                    application_no=application_id, meeting_type="Factory Inspection")
                inspection_team_details = t_food_business_registration_licensing_t6.objects.filter(
                    application_no=application_id, meeting_type="Factory Inspection")
                feasibility_inspection_team_details = t_food_business_registration_licensing_t6.objects.filter(
                    application_no=application_id, meeting_type='Feasibility Inspection')
                feasibility_team_details = t_food_business_registration_licensing_t4.objects.filter(
                    application_no=application_id,
                    meeting_type='Feasibility Inspection')
                feasibility_inspection_details = t_food_business_registration_licensing_t5.objects.filter(
                    application_no=application_id,
                    inspection_type='Feasibility Inspection')
                inspector_list = t_user_master.objects.filter(Role_Id='5')
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'registration_licensing/factory_inspection.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspector_list': inspector_list, 'unit': unit, 'inspection_details': inspection_details,
                               'team_details': team_details, 'inspection_team_details': inspection_team_details,
                               'food_handler': food_handler, 'dzongkhag': dzongkhag, 'gewog': gewog,
                               'village': village, 'feasibility_team_details': feasibility_team_details,
                               'feasibility_inspection_team_details': feasibility_inspection_team_details,
                               'feasibility_inspection_details': feasibility_inspection_details,
                               'packaging_material': packaging_material, 'raw_materials': raw_materials})
    elif service_code == 'OC':
        oc_work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if oc_work_details.exists():
            application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
            details = t_certification_organic_t2.objects.filter(Application_No=application_id)
            audit_team = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=application_id)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_id)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_id)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=application_id)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_id)
            api_details = t_certification_organic_t9.objects.filter(Application_No=application_id)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_id)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id)
            return render(request, 'organic_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation})
        else:
            application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
            details = t_certification_organic_t2.objects.filter(Application_No=application_id)
            audit_team = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=application_id)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_id)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_id)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=application_id)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_id)
            api_details = t_certification_organic_t9.objects.filter(Application_No=application_id)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_id)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            file_attach = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            leader = t_user_master.objects.all()
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'organic_certification/team_leader_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details, 'leader': leader, 'file_attach': file_attach,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'file_attach_count': file_attach_count})
    elif service_code == 'GAP':
        work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
            details = t_certification_gap_t2.objects.filter(Application_No=application_id)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=application_id)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id)
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_id)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_id)
            return render(request, 'GAP_Certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details})
        else:
            application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
            details = t_certification_gap_t2.objects.filter(Application_No=application_id)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=application_id)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_id)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_id)
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'GAP_Certification/team_leader_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details, 'audit_plan': audit_plan,
                           'file_attach_count': file_attach_count})
    elif service_code == 'FPC':
        work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
            details = t_certification_food_t2.objects.filter(Application_No=application_id)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_No=application_id, attachment_Type='AP')
            audit_findings = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_observation = t_certification_food_t5.objects.filter(Application_No=application_id)
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'food_product_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details, 'audit_plan': audit_plan,
                           'file_attach_count': file_attach_count
                           })
        else:
            application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
            details = t_certification_food_t2.objects.filter(Application_No=application_id)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            file_count = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP').count()
            audit_findings = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_observation = t_certification_food_t4.objects.filter(Application_No=application_id)
            return render(request, 'food_product_certification/team_leader_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details, 'file_count': file_count, 'audit_plan': audit_plan
                           })
    elif service_code == 'COM':
        application_no = request.GET.get('application_id')
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        details = t_common_complaint_t1.objects.filter(Application_No=application_no)
        complaint_file = t_file_attachment.objects.filter(application_no=application_no, role_id='8')
        investigation_file = t_file_attachment.objects.filter(application_no=application_no, role_id='5')

        return render(request, 'complaint_handling/investigation_complaint_update.html', {'complaint_details': details,
                                                                                          'dzongkhag': dzongkhag,
                                                                                          'gewog': gewog,
                                                                                          'village': village,
                                                                                          'complaint_file': complaint_file,
                                                                                          'investigation_file': investigation_file})


def approve_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    validity_period = request.GET.get('validity_period')
    permit_no = get_permit_no(request)
    details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=dateOfInspection)
    details.update(Movement_Permit_No=permit_no)
    details.update(Approved_Date=date.today())
    details.update(Application_Status='A')
    details.update(Validity_Period=validity_period)
    d = timedelta(days=int(validity_period))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='A')
    update_payment_details(application_id, permit_no, 'MPP', validity_date, 'Final', '131110007')
    for email_id in details:
        emailId = email_id.Email
        send_mpp_approve_email(permit_no, emailId, validity_date, application_id)
    return redirect(inspector_application)


def send_mpp_approve_email(permit_no, Email, validity_date, application_no):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Movement Permit for Plant And Plant Products Has Been Approved. Your " \
              " Application No is " + application_no + " And Movement Permit No is:" + permit_no + \
              " And is Valid Till " + " " + str(validity_date) + \
              " Please Make Payment Before Validity Expires. Visit The Nearest Bafra Office For Payment " \
              "or Pay Online at https://tinyurl.com/y3m7wa3c Thank you! "
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def reject_application(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    details.update(Remarks=remarks)
    details.update(Application_Status='R')
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='R')
    return render(request, 'movement_permit/application_details.html', {'application_details': application_details})


def reject_movement_application(request):
    application_id = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    details.update(Remarks=remarks)
    details.update(Application_Status='R')
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='R')
    for email_id in details:
        emailId = email_id.Email
        send_movement_reject_email(remarks, emailId)
    return render(request, 'movement_permit/application_details.html', {'application_details': application_details})


def add_details_ins(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_movement_permit_t3.objects.create(Application_No=application_id,
                                              Current_Observation=currentObservation,
                                              Decision_Conformity=decisionConform)
    movement_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)
    return render(request, 'movement_permit/add_application_details.html', {'movement_permit': movement_permit})


def get_permit_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_plant_movement_permit_t1.objects.aggregate(Max('Movement_Permit_No'))
    lastAppNo = last_application_no['Movement_Permit_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "-" + "MPP" + "-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "-" + "MPP" + "-" + str(year) + "-" + AppNo
    return newAppNo


def add_file(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def add_file_name(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
    return render(request, 'movement_permit/file_attachment_page.html', {'file_attach': file_attach})


def save_movement_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def movement_agro_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(application_no=Application_No, applicant_id=Applicant_Id,
                                         role_id=None,
                                         attachment=fileName)

        file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'movement_permit/file_attachment_page.html', {'file_attach': file_attach})


def delete_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'movement_permit/file_attachment_page.html', {'file_attach': file_attach})


def update_movement_permit(request):
    data = dict()
    service_code = "MPP"
    last_application_no = request.POST.get('applicationNo')
    Applicant_Id = request.session['email']
    Permit_Type = request.POST.get('permitType')
    License_No = request.POST.get('regNo')
    Nursery_Name = request.POST.get('companyName')
    CID = request.POST.get('cid')
    Applicant_Name = request.POST.get('Name')
    Contact_No = request.POST.get('contactNumber')
    Email = request.POST.get('email')
    Dzongkhag_Code = request.POST.get('dzongkhag')
    Gewog_Code = request.POST.get('gewog')
    Village_Code = request.POST.get('village')
    From_Dzongkhag_Code = request.POST.get('from_dzongkhag')
    From_Gewog_Code = request.POST.get('from_gewog')
    From_Location = request.POST.get('from_location')
    To_Dzongkhag_Code = request.POST.get('to_dzongkhag')
    To_Gewog_Code = request.POST.get('to_gewog')
    To_Location = request.POST.get('to_exact_location')
    Authorized_Route = request.POST.get('route')
    Movement_Purpose = request.POST.get('movementPurpose')
    Conveyance_Means = request.POST.get('conveyanceMeans')
    Vehicle_No = request.POST.get('vehicleNo')
    Movement_Date = request.POST.get('date')

    movement_permit_details = t_plant_movement_permit_t1.objects.filter(Application_No=last_application_no)

    movement_permit_details.update(
        Permit_Type=Permit_Type,
        License_No=License_No,
        Nursery_Name=Nursery_Name,
        CID=CID,
        Applicant_Name=Applicant_Name,
        Contact_No=Contact_No,
        Email=Email,
        Dzongkhag=Dzongkhag_Code,
        Gewog=Gewog_Code,
        Village=Village_Code,
        From_Dzongkhag_Code=From_Dzongkhag_Code,
        From_Gewog_Code=From_Gewog_Code,
        From_Location=From_Location,
        To_Dzongkhag_Code=To_Dzongkhag_Code,
        To_Gewog_Code=To_Gewog_Code,
        To_Location=To_Location,
        Authorized_Route=Authorized_Route,
        Movement_Purpose=Movement_Purpose,
        Conveyance_Means=Conveyance_Means,
        Qty=None,
        Unit=None,
        Movement_Date=Movement_Date,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Application_Status=None,
        Movement_Permit_No=None,
        Remarks=None,
        Application_Date=date.today(),
        Applicant_Id=Applicant_Id,
        Approved_Date=None,
        Validity_Period=None,
        Validity=None
    )
    plant_details = t_plant_movement_permit_t1.objects.filter(Application_No=last_application_no)
    if Conveyance_Means == "Air":
        plant_details.update(Vehicle_No=Vehicle_No)
    field_id = t_location_field_office_mapping.objects.filter(pk=From_Gewog_Code)
    for field_office in field_id:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(application_no=last_application_no, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=field_office_id, section='Plant',
                                      assigned_role_id='4',
                                      action_date=None, application_status='P',
                                      service_code=service_code)
    data['applicationNo'] = last_application_no
    return JsonResponse(data)


def load_plant_import_details(request):
    application_no = request.GET.get('appNo')
    import_type = request.GET.get('import_type')
    print(application_no)
    print(import_type)
    if import_type == 'P':
        count = t_plant_import_permit_t2.objects.filter(Application_No=application_no).count()
        import_details = t_plant_import_permit_t2.objects.filter(Application_No=application_no)
        unit = t_unit_master.objects.all()
        crop = t_plant_crop_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        return render(request, 'import_permit/import_page_plant.html',
                      {'import': import_details, 'count': count, 'unit': unit, 'crop': crop,
                       'variety': variety})
    else:
        count = t_plant_import_permit_t2.objects.filter(Application_No=application_no).count()
        import_details = t_plant_import_permit_t2.objects.filter(Application_No=application_no)
        unit = t_unit_master.objects.all()
        pesticide = t_plant_pesticide_master.objects.all()
        return render(request, 'import_permit/import_page_agro.html',
                      {'import': import_details, 'agro_count': count, 'unit': unit, 'pesticide': pesticide})


def load_plant_import_attachment(request):
    application_no = request.GET.get('appNo')

    file_attach = t_file_attachment.objects.filter(application_no=application_no)
    return render(request, 'import_permit/plant_attachment_page.html', {'file_attach': file_attach})


def mov_plant_details(request):
    Application_No = request.GET.get('application_id')
    movement_details = t_plant_movement_permit_t2.objects.filter(Application_No=Application_No)
    movement_count = t_plant_movement_permit_t2.objects.filter(Application_No=Application_No).count()
    return render(request, 'movement_permit/movement_page.html',
                  {'import': movement_details, 'movement_count': movement_count})


def mov_plant_attachment(request):
    Application_No = request.GET.get('application_id')
    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'movement_permit/file_attachment_page.html',
                  {'file_attach': file_attach})


def mov_agro_attachment(request):
    Application_No = request.GET.get('application_id')
    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'movement_permit/agro_file_attachment_page.html',
                  {'file_attach': file_attach})


def get_unit_master(request):
    unit = t_unit_master.objects.filter(Unit_Type='S')
    return render(request, 'unit_list_master.html',
                  {'unit': unit})


def get_variety(request):
    crop_id = request.GET.get('crop_id')
    print(crop_id)
    variety = t_plant_crop_variety_master.objects.filter(Crop_Id=crop_id)
    return render(request, 'variety_list.html',
                  {'variety': variety})


def get_crop(request):
    crop_category_id = request.GET.get('crop_category_id')
    crop_list = t_plant_crop_master.objects.filter(Crop_Category_Id=crop_category_id)
    return render(request, 'crop_list.html',
                  {'crop_list': crop_list})


# import permit
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apply_import_permit(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None

    if login_id:
        crop = t_plant_crop_master.objects.all()
        pesticide = t_plant_pesticide_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        location = t_field_office_master.objects.filter(Is_Entry_Point="Y")
        country = t_country_master.objects.all()
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        unit = t_unit_master.objects.filter(Unit_Type='S')
        unit_agro = t_unit_master.objects.filter(Unit_Type='L')
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'import_permit/apply_import_permit.html',
                      {'crop': crop, 'pesticide': pesticide, 'variety': variety,
                       'location': location, 'country': country, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'unit': unit, 'unit_agro': unit_agro, 'count': message_count,
                       'count_call': inspection_call_count, 'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def save_import_permit(request):
    data = dict()
    service_code = "IPP"
    last_application_no = get_import_application_no(request, service_code)

    Applicant_Id = request.session['email']
    importType = request.POST.get('Import_Type')
    Applicant_Type = request.POST.get('Application_Type')
    Nationality = request.POST.get('Nationality_Type')
    if Applicant_Type == "Commercial":
        regNo = request.POST.get('regNo')
        business_name = request.POST.get('p_businessName')
        commercial_presentAddress = request.POST.get('commercial_presentAddress')
        com_contactNumber = request.POST.get('com_contactNumber')
        com_email = request.POST.get('com_email')
        com_supplier = request.POST.get('com_supplier')
        Com_Country_Of_Origin = request.POST.get('Com_Country_Of_Origin')
        com_conveyanceMeans = request.POST.get('com_conveyanceMeans')
        com_entry_point = request.POST.get('com_entry_point')
        com_movementPurpose = request.POST.get('com_movementPurpose')
        com_final_Destination = request.POST.get('com_final_Destination')
        com_expected_arrival_date = request.POST.get('com_expected_arrival_date')
        t_plant_import_permit_t1.objects.create(
            Application_No=last_application_no,
            Import_Type=importType,
            License_No=regNo,
            Business_Name=business_name,
            CID=None,
            Applicant_Name=None,
            Present_Address=commercial_presentAddress,
            Contact_No=com_contactNumber,
            Email=com_email,
            Name_And_Address_Supplier=com_supplier,
            Means_of_Conveyance=com_conveyanceMeans,
            Place_Of_Entry=com_entry_point,
            Purpose=com_movementPurpose,
            Final_Destination=com_final_Destination,
            Import_Inspection_Submit_Date=None,
            Proposed_Inspection_Date=None,
            Actual_Point_Of_Entry=None,
            Inspection_Request_Remarks=None,
            Import_Permit_No=None,
            Inspection_Date=None,
            Inspection_Type=None,
            Inspection_Time=None,
            Inspection_Leader=None,
            Inspection_Team=None,
            Clearance_Ref_No=None,
            Expected_Arrival_Date=com_expected_arrival_date,
            FO_Remarks=None,
            Inspection_Remarks=None,
            Country_Of_Origin=Com_Country_Of_Origin,
            Application_Date=date.today(),
            Applicant_Id=Applicant_Id,
            Approved_Date=date.today(),
            Validity_Period=None,
            Validity=None,
            Application_Type=Applicant_Type,
            Nationality=None,
            Dzongkhag=None,
            Gewog=None,
            Nationality_Type=None,
            Village=None,
            Passport_Number=None
        )
    else:
        if Nationality == "Bhutanese":
            cid = request.POST.get('p_cid_number')
            Name = request.POST.get('name')
            dzongkhag = request.POST.get('dzongkhag')
            gewog = request.POST.get('gewog')
            village = request.POST.get('village')
            contactNumber = request.POST.get('contactNumber')
            email = request.POST.get('email')
            supplier = request.POST.get('supplier')
            Country_Of_Origin = request.POST.get('Country_Of_Origin')
            conveyanceMeans = request.POST.get('conveyanceMeans')
            entry_point = request.POST.get('entry_point')
            B_movementPurpose = request.POST.get('B_movementPurpose')
            B_finalDestination = request.POST.get('B_final_Destination')
            B_expectedDate = request.POST.get('B_expectedDate')

            t_plant_import_permit_t1.objects.create(
                Application_No=last_application_no,
                Import_Type=importType,
                License_No=None,
                Business_Name=None,
                CID=cid,
                Applicant_Name=Name,
                Present_Address=None,
                Contact_No=contactNumber,
                Email=email,
                Name_And_Address_Supplier=supplier,
                Means_of_Conveyance=conveyanceMeans,
                Place_Of_Entry=entry_point,
                Purpose=B_movementPurpose,
                Final_Destination=B_finalDestination,
                Import_Inspection_Submit_Date=None,
                Proposed_Inspection_Date=None,
                Actual_Point_Of_Entry=None,
                Inspection_Request_Remarks=None,
                Import_Permit_No=None,
                Inspection_Date=None,
                Inspection_Type=None,
                Inspection_Time=None,
                Inspection_Leader=None,
                Inspection_Team=None,
                Clearance_Ref_No=None,
                Expected_Arrival_Date=B_expectedDate,
                FO_Remarks=None,
                Inspection_Remarks=None,
                Country_Of_Origin=Country_Of_Origin,
                Application_Date=date.today(),
                Applicant_Id=Applicant_Id,
                Approved_Date=None,
                Validity_Period=None,
                Validity=None,
                Application_Type=Applicant_Type,
                Nationality=None,
                Dzongkhag=dzongkhag,
                Gewog=gewog,
                Nationality_Type=Nationality,
                Village=village,
                Passport_Number=None
            )
        else:
            passport_name = request.POST.get('passport_name')
            Address = request.POST.get('Address')
            p_email = request.POST.get('p_email')
            p_contactNumber = request.POST.get('p_contactNumber')
            name_supplier = request.POST.get('name_supplier')
            Origin = request.POST.get('Origin')
            p_conveyanceMeans = request.POST.get('p_conveyanceMeans')
            p_entry_point = request.POST.get('p_entry_point')
            p_movementPurpose = request.POST.get('p_movementPurpose')
            p_finalDestination = request.POST.get('p_finalDestination')
            p_expectedDate = request.POST.get('p_expectedDate')
            passport = request.POST.get('passport')
            nationality = request.POST.get('nationality')
            t_plant_import_permit_t1.objects.create(
                Application_No=last_application_no,
                Import_Type=importType,
                License_No=None,
                Business_Name=None,
                CID=None,
                Applicant_Name=passport_name,
                Present_Address=Address,
                Contact_No=p_contactNumber,
                Email=p_email,
                Name_And_Address_Supplier=name_supplier,
                Means_of_Conveyance=p_conveyanceMeans,
                Place_Of_Entry=p_entry_point,
                Purpose=p_movementPurpose,
                Final_Destination=p_finalDestination,
                Import_Inspection_Submit_Date=None,
                Proposed_Inspection_Date=None,
                Actual_Point_Of_Entry=None,
                Inspection_Request_Remarks=None,
                Import_Permit_No=None,
                Inspection_Date=None,
                Inspection_Type=None,
                Inspection_Time=None,
                Inspection_Leader=None,
                Inspection_Team=None,
                Clearance_Ref_No=None,
                Expected_Arrival_Date=p_expectedDate,
                FO_Remarks=None,
                Inspection_Remarks=None,
                Country_Of_Origin=Origin,
                Application_Date=date.today(),
                Applicant_Id=Applicant_Id,
                Approved_Date=None,
                Validity_Period=None,
                Validity=None,
                Application_Type=Applicant_Type,
                Nationality=nationality,
                Dzongkhag=None,
                Gewog=None,
                Nationality_Type=Nationality,
                Village=None,
                Passport_Number=passport
            )
    t_workflow_details.objects.create(application_no=last_application_no, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=None, section='Plant',
                                      assigned_role_id='2', action_date=None, application_status='P',
                                      service_code=service_code)
    data['applNo'] = last_application_no
    data['importType'] = importType
    return JsonResponse(data)


def get_import_application_no(request, service_code):
    last_application_no = t_plant_import_permit_t1.objects.aggregate(Max('Application_No'))
    lastAppNo = last_application_no['Application_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = service_code + "-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = service_code + "-" + str(year) + "-" + AppNo
    return newAppNo


def load_variety(request):
    crop_id = request.GET.get('crop_id')
    variety_list = t_plant_crop_variety_master.objects.filter(Crop_Id=crop_id).order_by('Crop_Variety_Name')
    return render(request, 'import_permit/crop_variety_list.html', {'variety': variety_list})


def load_seed_variety(request):
    crop = request.GET.get('crop_id')
    crop_list = t_plant_crop_master.objects.filter(Crop_Common_Name=crop)
    for crop in crop_list:
        crop_id = crop.Crop_Id
        print(crop_id)
        variety_list = t_plant_crop_variety_master.objects.filter(Crop_Id=crop_id) \
            .order_by('Crop_Variety_Name')
        return render(request, 'seed_certification/crop_variety_list.html', {'variety': variety_list})


def save_import_plant(request):
    if request.method == 'POST':
        appNo = request.POST['appNo']
        Import_Category = request.POST['plant_import_category']
        crop_variety_id = request.POST['crop_variety_id']
        crop_id = request.POST['crop_id']
        unit = request.POST['unit']
        qty = request.POST['qty']
        t_plant_import_permit_t2.objects.create(Application_No=appNo, Import_Category=Import_Category,
                                                Crop_Id=crop_id, Pesticide_Id=None, Description=None,
                                                Variety_Id=crop_variety_id, Unit=unit, Quantity=qty,
                                                Quantity_Released=None, Remarks=None, Quantity_Balance=qty)
        imports_plant = t_plant_import_permit_t2.objects.filter(Application_No=appNo)
        crop = t_plant_crop_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        count = t_plant_import_permit_t2.objects.filter(Application_No=appNo).count()
        return render(request, 'import_permit/import_page_plant.html', {'import': imports_plant, 'crop': crop,
                                                                        'variety': variety, 'count': count})


def save_import_agro(request):
    if request.method == 'POST':
        appNo = request.POST['agro_applicationNo']
        Import_Category = request.POST['agro_import_category']
        pesticide_id = request.POST['pesticide_id']
        description = request.POST['description']
        unit = request.POST['agro_unit']
        qty = request.POST['agro_qty']
        t_plant_import_permit_t2.objects.create(Application_No=appNo, Import_Category=Import_Category,
                                                Crop_Id=None, Pesticide_Id=pesticide_id,
                                                Description=description,
                                                Variety_Id=None, Unit=unit, Quantity=qty,
                                                Quantity_Released=None, Remarks=None, Quantity_Balance=qty)
        imports_plant = t_plant_import_permit_t2.objects.filter(Application_No=appNo)
        pesticide = t_plant_pesticide_master.objects.all()
        count = t_plant_import_permit_t2.objects.filter(Application_No=appNo).count()
        return render(request, 'import_permit/import_page_agro.html', {'import': imports_plant, 'pesticide': pesticide,
                                                                       'agro_count': count})


def fo_app_details(request):
    Application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    if service_code == 'IPP':
        new_import_app = t_plant_import_permit_t1.objects.filter(Application_No=Application_No)
        details = t_plant_import_permit_t2.objects.filter(Application_No=Application_No)
        file = t_file_attachment.objects.filter(application_no=Application_No)
        location_mapping = t_field_office_master.objects.all()
        country = t_country_master.objects.all()
        crop = t_plant_crop_master.objects.all()
        pesticide = t_plant_pesticide_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        return render(request, 'import_permit/fo_import_permit.html',
                      {'application_details': new_import_app, 'details': details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location_mapping, 'country': country,
                       'crop': crop, 'pesticide': pesticide, 'variety': variety})
    elif service_code == 'IAF':
        application_details = t_livestock_import_permit_animal_t1.objects.filter(Application_No=Application_No)
        details = t_livestock_import_permit_animal_t2.objects.filter(Application_No=Application_No)
        file = t_file_attachment.objects.filter(application_no=Application_No)
        location_mapping = t_field_office_master.objects.filter(Is_Entry_Point="Y")
        species = t_livestock_species_master.objects.all()
        return render(request, 'Animal_Fish_Import/fo_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'dzongkhag': dzongkhag, 'location_mapping': location_mapping,
                       'village': village, 'location': location, 'species': species})
    elif service_code == 'ILP':
        application_details = t_livestock_import_permit_product_t1.objects.filter(Application_No=Application_No)
        details = t_livestock_import_permit_product_t2.objects.filter(Application_No=Application_No)
        file = t_file_attachment.objects.filter(application_no=Application_No)
        field_list = t_field_office_master.objects.all()
        species = t_livestock_species_master.objects.all()
        return render(request, 'Livestock_Import/fo_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'dzongkhag': dzongkhag, 'location_mapping': field_list,
                       'village': village, 'location': location, 'species': species})
    elif service_code == 'FIP':
        application_details = t_food_import_permit_t1.objects.filter(Application_No=Application_No)
        details = t_food_import_permit_t2.objects.filter(Application_No=Application_No)
        file = t_file_attachment.objects.filter(application_no=Application_No)
        field_list = t_field_office_master.objects.all()
        country_list = t_country_master.objects.all()
        return render(request, 'import_certificate_food/fo_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': field_list, 'country_list': country_list})
    elif service_code == 'FBR':
        new_import_app = t_workflow_details.objects.filter(application_no=Application_No, application_status='FRA')
        if new_import_app.exists():
            application_details = t_food_business_registration_licensing_t1.objects.filter(
                application_no=Application_No)
            details = t_food_business_registration_licensing_t2.objects.filter(application_no=Application_No)
            food_handler = t_food_business_registration_licensing_t3.objects.filter(application_no=Application_No)
            file = t_file_attachment.objects.filter(application_no=Application_No)
            unit = t_unit_master.objects.all()
            oic_list = t_field_office_master.objects.all()
            inspector_list = t_user_master.objects.filter(Role_Id='5')
            inspection_team_details = t_food_business_registration_licensing_t6.objects.filter(
                application_no=Application_No, meeting_type='Feasibility Inspection')
            team_details = t_food_business_registration_licensing_t4.objects.filter(
                application_no=Application_No, meeting_type='Feasibility Inspection')
            inspection_details = t_food_business_registration_licensing_t5.objects.filter(
                application_no=Application_No, inspection_type='Feasibility Inspection')
            factory_inspection_team_details = t_food_business_registration_licensing_t6.objects.filter(
                application_no=Application_No, meeting_type='Factory Inspection')
            factory_team_details = t_food_business_registration_licensing_t4.objects.filter(
                application_no=Application_No,
                meeting_type='Factory Inspection')
            factory_inspection_details = t_food_business_registration_licensing_t5.objects.filter(
                application_no=Application_No,
                inspection_type='Factory Inspection')
            raw_materials = t_food_business_registration_licensing_t7.objects.filter(application_no=Application_No)
            packaging_material = t_food_business_registration_licensing_t8.objects.filter(application_no=Application_No)
            return render(request, 'registration_licensing/fo_approve_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'oic_list': oic_list, 'location': location, 'unit': unit, 'dzongkhag': dzongkhag,
                           'gewog': gewog, 'village': village, 'food_handler': food_handler,
                           'inspector_list': inspector_list, 'inspection_team_details': inspection_team_details,
                           'team_details': team_details, 'inspection_details': inspection_details,
                           'factory_inspection_team_details': factory_inspection_team_details,
                           'factory_team_details': factory_team_details,
                           'factory_inspection_details': factory_inspection_details, 'raw_materials': raw_materials,
                           'packaging_material': packaging_material})
        else:
            application_details = t_food_business_registration_licensing_t1.objects.filter(
                application_no=Application_No, application_source__isnull=False)
            if application_details.exists():
                details = t_food_business_registration_licensing_t2.objects.filter(application_no=Application_No)
                food_handler = t_food_business_registration_licensing_t3.objects.filter(application_no=Application_No)
                file = t_file_attachment.objects.filter(application_no=Application_No)
                unit = t_unit_master.objects.all()
                oic_list = t_field_office_master.objects.all()
                raw_materials = t_food_business_registration_licensing_t7.objects.filter(application_no=Application_No)
                packaging_material = t_food_business_registration_licensing_t8.objects.filter(
                    application_no=Application_No)
                return render(request, 'registration_licensing/fo_details.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'oic_list': oic_list, 'location': location, 'unit': unit, 'dzongkhag': dzongkhag,
                               'gewog': gewog, 'village': village, 'food_handler': food_handler,
                               'raw_materials': raw_materials, 'packaging_material': packaging_material})
            else:
                details = t_food_business_registration_licensing_t2.objects.filter(application_no=Application_No)
                food_handler = t_food_business_registration_licensing_t3.objects.filter(application_no=Application_No)
                file = t_file_attachment.objects.filter(application_no=Application_No)
                unit = t_unit_master.objects.all()
                oic_list = t_field_office_master.objects.all()
                raw_materials = t_food_business_registration_licensing_t7.objects.filter(application_no=Application_No)
                packaging_material = t_food_business_registration_licensing_t8.objects.filter(
                    application_no=Application_No)
                return render(request, 'registration_licensing/fo_details.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'oic_list': oic_list, 'location': location, 'unit': unit, 'dzongkhag': dzongkhag,
                               'gewog': gewog, 'village': village, 'food_handler': food_handler,
                               'raw_materials': raw_materials, 'packaging_material': packaging_material})
    # CERTIFICATION SECTION
    elif service_code == 'OC':
        oc_work_details = t_workflow_details.objects.filter(application_no=Application_No, application_status='NCF')
        if oc_work_details.exists():
            application_details = t_certification_organic_t1.objects.filter(Application_No=Application_No)
            details = t_certification_organic_t2.objects.filter(Application_No=Application_No)
            audit_team = t_certification_food_t3.objects.filter(Application_No=Application_No)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=Application_No)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=Application_No)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=Application_No)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=Application_No)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=Application_No)
            api_details = t_certification_organic_t9.objects.filter(Application_No=Application_No)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=Application_No)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=Application_No)
            file = t_file_attachment.objects.filter(application_no=Application_No, attachment_type__isnull=True)
            dzongkhag = t_dzongkhag_master.objects.all()
            gewog = t_gewog_master.objects.all()
            village = t_village_master.objects.all()
            audit_plan = t_file_attachment.objects.filter(application_no=Application_No, attachment_type='AP')
            return render(request, 'organic_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details, 'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'audit_plan': audit_plan})
        else:
            work_details = t_workflow_details.objects.filter(application_no=Application_No, application_status='AP')
            if work_details.exists():
                application_details = t_certification_organic_t1.objects.filter(Application_No=Application_No)
                details = t_certification_organic_t2.objects.filter(Application_No=Application_No)
                audit_team = t_certification_food_t3.objects.filter(Application_No=Application_No)
                crop_production = t_certification_organic_t4.objects.filter(Application_No=Application_No)
                processing_unit = t_certification_organic_t5.objects.filter(Application_No=Application_No)
                wild_collection = t_certification_organic_t6.objects.filter(Application_No=Application_No)
                ah_details = t_certification_organic_t7.objects.filter(Application_No=Application_No)
                aqua_details = t_certification_organic_t8.objects.filter(Application_No=Application_No)
                api_details = t_certification_organic_t9.objects.filter(Application_No=Application_No)
                audit_findings = t_certification_organic_t10.objects.filter(Application_No=Application_No)
                audit_observation = t_certification_organic_t11.objects.filter(Application_No=Application_No)
                file = t_file_attachment.objects.filter(application_no=Application_No, attachment_type__isnull=True)
                file_attach = t_file_attachment.objects.filter(application_no=Application_No, attachment_type='AP')
                leader = t_user_master.objects.all()
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                file_attach_count = t_file_attachment.objects.filter(application_no=Application_No,
                                                                     attachment_type='AP').count()

                return render(request, 'organic_certification/team_leader_details.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'crop_production': crop_production, 'audit_team': audit_team,
                               'processing_unit': processing_unit, 'wild_collection': wild_collection,
                               'ah_details': ah_details, 'aqua_details': aqua_details,
                               'api_details': api_details, 'leader': leader, 'file_attach': file_attach,
                               'audit_findings': audit_findings, 'audit_observation': audit_observation,
                               'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                               'file_attach_count': file_attach_count, 'audit_plan': file_attach})
            else:
                new_import_app = t_workflow_details.objects.filter(application_no=Application_No,
                                                                   application_status='ATA')
                if new_import_app.exists():
                    application_details = t_certification_organic_t1.objects.filter(Application_No=Application_No)
                    details = t_certification_organic_t2.objects.filter(Application_No=Application_No)
                    audit_team = t_certification_food_t3.objects.filter(Application_No=Application_No)
                    crop_production = t_certification_organic_t4.objects.filter(Application_No=Application_No)
                    processing_unit = t_certification_organic_t5.objects.filter(Application_No=Application_No)
                    wild_collection = t_certification_organic_t6.objects.filter(Application_No=Application_No)
                    ah_details = t_certification_organic_t7.objects.filter(Application_No=Application_No)
                    aqua_details = t_certification_organic_t8.objects.filter(Application_No=Application_No)
                    api_details = t_certification_organic_t9.objects.filter(Application_No=Application_No)
                    audit_findings = t_certification_organic_t10.objects.filter(Application_No=Application_No)
                    audit_observation = t_certification_organic_t11.objects.filter(Application_No=Application_No)
                    file = t_file_attachment.objects.filter(application_no=Application_No, attachment_type__isnull=True)
                    user_details = t_user_master.objects.all()
                    team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                    team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                    dzongkhag = t_dzongkhag_master.objects.all()
                    gewog = t_gewog_master.objects.all()
                    village = t_village_master.objects.all()
                    return render(request, 'organic_certification/fo_details.html',
                                  {'application_details': application_details, 'details': details, 'file': file,
                                   'crop_production': crop_production, 'audit_team': audit_team,
                                   'processing_unit': processing_unit, 'wild_collection': wild_collection,
                                   'ah_details': ah_details, 'aqua_details': aqua_details, 'api_details': api_details,
                                   'audit_findings': audit_findings, 'user_details': user_details,
                                   'audit_observation': audit_observation, 'team_leader': team_leader,
                                   'team_details': team_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                                   'village': village})
                else:
                    new_import_app = t_workflow_details.objects.filter(application_no=Application_No,
                                                                       application_status='CA')
                    if new_import_app.exists():
                        application_details = t_certification_organic_t1.objects.filter(Application_No=Application_No)
                        details = t_certification_organic_t2.objects.filter(Application_No=Application_No)
                        audit_team = t_certification_food_t3.objects.filter(Application_No=Application_No)
                        crop_production = t_certification_organic_t4.objects.filter(Application_No=Application_No)
                        processing_unit = t_certification_organic_t5.objects.filter(Application_No=Application_No)
                        wild_collection = t_certification_organic_t6.objects.filter(Application_No=Application_No)
                        ah_details = t_certification_organic_t7.objects.filter(Application_No=Application_No)
                        aqua_details = t_certification_organic_t8.objects.filter(Application_No=Application_No)
                        api_details = t_certification_organic_t9.objects.filter(Application_No=Application_No)
                        audit_findings = t_certification_organic_t10.objects.filter(Application_No=Application_No)
                        audit_observation = t_certification_organic_t11.objects.filter(Application_No=Application_No)
                        file = t_file_attachment.objects.filter(application_no=Application_No,
                                                                attachment_type__isnull=True)
                        user_details = t_user_master.objects.filter(Login_Type='I')
                        team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        audit_plan = t_file_attachment.objects.filter(application_no=Application_No,
                                                                      attachment_type='AP')
                        dzongkhag = t_dzongkhag_master.objects.all()
                        gewog = t_gewog_master.objects.all()
                        village = t_village_master.objects.all()
                        return render(request, 'organic_certification/approve_fo_details.html',
                                      {'application_details': application_details, 'details': details, 'file': file,
                                       'crop_production': crop_production, 'audit_team': audit_team,
                                       'processing_unit': processing_unit, 'wild_collection': wild_collection,
                                       'ah_details': ah_details, 'aqua_details': aqua_details,
                                       'api_details': api_details, 'audit_plan': audit_plan,
                                       'audit_findings': audit_findings, 'user_details': user_details,
                                       'audit_observation': audit_observation, 'team_leader': team_leader,
                                       'team_details': team_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                                       'village': village})
                    else:
                        application_details = t_certification_organic_t1.objects.filter(Application_No=Application_No)
                        details = t_certification_organic_t2.objects.filter(Application_No=Application_No)
                        audit_team = t_certification_food_t3.objects.filter(Application_No=Application_No)
                        crop_production = t_certification_organic_t4.objects.filter(Application_No=Application_No)
                        processing_unit = t_certification_organic_t5.objects.filter(Application_No=Application_No)
                        wild_collection = t_certification_organic_t6.objects.filter(Application_No=Application_No)
                        ah_details = t_certification_organic_t7.objects.filter(Application_No=Application_No)
                        aqua_details = t_certification_organic_t8.objects.filter(Application_No=Application_No)
                        api_details = t_certification_organic_t9.objects.filter(Application_No=Application_No)
                        file = t_file_attachment.objects.filter(application_no=Application_No,
                                                                attachment_type__isnull=True)
                        team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        dzongkhag = t_dzongkhag_master.objects.all()
                        gewog = t_gewog_master.objects.all()
                        village = t_village_master.objects.all()
                        return render(request, 'organic_certification/fo_details.html',
                                      {'application_details': application_details, 'farmer_group': details,
                                       'file': file,
                                       'crop_production': crop_production, 'audit_team': audit_team,
                                       'processing_unit': processing_unit, 'wild_collection': wild_collection,
                                       'ah_details': ah_details, 'aqua_details': aqua_details,
                                       'api_details': api_details, 'team_details': team_details,
                                       'team_leader': team_leader, 'dzongkhag': dzongkhag,
                                       'gewog': gewog, 'village': village})

    elif service_code == 'GAP':
        work_details = t_workflow_details.objects.filter(application_no=Application_No, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_gap_t1.objects.filter(Application_No=Application_No)
            details = t_certification_gap_t2.objects.filter(Application_No=Application_No)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=Application_No)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=Application_No)
            file = t_file_attachment.objects.filter(application_no=Application_No, attachment_type__isnull=True)
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=Application_No)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=Application_No)
            dzongkhag = t_dzongkhag_master.objects.all()
            gewog = t_gewog_master.objects.all()
            village = t_village_master.objects.all()
            audit_plan = t_file_attachment.objects.filter(application_no=Application_No, attachment_type='AP')
            return render(request, 'GAP_Certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details, 'dzongkhag': dzongkhag, 'village': village,
                           'gewog': gewog, 'audit_plan': audit_plan})
        else:
            audit_plan_details = t_workflow_details.objects.filter(application_no=Application_No,
                                                                   application_status='AP')
            if audit_plan_details.exists():
                application_details = t_certification_gap_t1.objects.filter(Application_No=Application_No)
                details = t_certification_gap_t2.objects.filter(Application_No=Application_No)
                audit_team_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                crop_production = t_certification_gap_t4.objects.filter(Application_No=Application_No)
                gap_house_details = t_certification_gap_t5.objects.filter(Application_No=Application_No)
                file = t_file_attachment.objects.filter(application_no=Application_No, attachment_type__isnull=True)
                audit_plan = t_file_attachment.objects.filter(application_no=Application_No, attachment_type='AP')
                farm_inputs = t_certification_gap_t7.objects.filter(Application_No=Application_No)
                audit_observation = t_certification_gap_t8.objects.filter(Application_No=Application_No)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                file_attach_count = t_file_attachment.objects.filter(application_no=Application_No,
                                                                     attachment_type='AP').count()
                return render(request, 'GAP_Certification/team_leader_details.html',
                              {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                               'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                               'crop_production': crop_production, 'pack_house_details': gap_house_details,
                               'audit_team_details': audit_team_details, 'audit_plan': audit_plan,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog,
                               'file_attach_count': file_attach_count})
            else:
                details_app = t_workflow_details.objects.filter(application_no=Application_No, application_status='ATA')
                if details_app.exists():
                    application_details = t_certification_gap_t1.objects.filter(Application_No=Application_No)
                    details = t_certification_gap_t2.objects.filter(Application_No=Application_No)
                    audit_team_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                    crop_production = t_certification_gap_t4.objects.filter(Application_No=Application_No)
                    gap_house_details = t_certification_gap_t5.objects.filter(Application_No=Application_No)
                    file = t_file_attachment.objects.filter(application_no=Application_No, attachment_type__isnull=True)
                    audit_findings = t_certification_gap_t7.objects.filter(Application_No=Application_No)
                    audit_observation = t_certification_gap_t8.objects.filter(Application_No=Application_No)
                    dzongkhag = t_dzongkhag_master.objects.all()
                    gewog = t_gewog_master.objects.all()
                    village = t_village_master.objects.all()
                    team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                    team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                    return render(request, 'GAP_Certification/fo_details.html',
                                  {'application_details': application_details, 'farmer_group': details, 'file': file,
                                   'audit_findings': audit_findings, 'audit_observation': audit_observation,
                                   'crop_production': crop_production, 'gap_house_details': gap_house_details,
                                   'audit_team': audit_team_details, 'team_leader': team_leader,
                                   'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                                   'team_details': team_details})
                else:
                    import_app = t_workflow_details.objects.filter(application_no=Application_No,
                                                                   application_status='CA')
                    if import_app.exists():
                        application_details = t_certification_gap_t1.objects.filter(Application_No=Application_No)
                        details = t_certification_gap_t2.objects.filter(Application_No=Application_No)
                        audit_team_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                        crop_production = t_certification_gap_t4.objects.filter(Application_No=Application_No)
                        gap_house_details = t_certification_gap_t5.objects.filter(Application_No=Application_No)
                        file = t_file_attachment.objects.filter(application_no=Application_No,
                                                                attachment_type__isnull=True)
                        audit_plan = t_file_attachment.objects.filter(application_no=Application_No,
                                                                      attachment_type='AP')
                        farm_inputs = t_certification_gap_t7.objects.filter(Application_No=Application_No)
                        audit_observation = t_certification_gap_t8.objects.filter(Application_No=Application_No)
                        dzongkhag = t_dzongkhag_master.objects.all()
                        gewog = t_gewog_master.objects.all()
                        village = t_village_master.objects.all()
                        user_details = t_user_master.objects.all()
                        team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        return render(request, 'GAP_Certification/approve_fo_details.html',
                                      {'application_details': application_details, 'farmer_group': details,
                                       'file': file,
                                       'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                                       'crop_production': crop_production, 'gap_house_details': gap_house_details,
                                       'audit_team': audit_team_details, 'team_leader': team_leader,
                                       'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                                       'user_details': user_details, 'audit_plan': audit_plan,
                                       'team_details': team_details})
                    else:
                        application_details = t_certification_gap_t1.objects.filter(Application_No=Application_No)
                        details = t_certification_gap_t2.objects.filter(Application_No=Application_No)
                        audit_team_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                        crop_production = t_certification_gap_t4.objects.filter(Application_No=Application_No)
                        gap_house_details = t_certification_gap_t5.objects.filter(Application_No=Application_No)
                        file = t_file_attachment.objects.filter(application_no=Application_No,
                                                                attachment_type__isnull=True)
                        audit_findings = t_certification_gap_t7.objects.filter(Application_No=Application_No)
                        audit_observation = t_certification_gap_t8.objects.filter(Application_No=Application_No)
                        dzongkhag = t_dzongkhag_master.objects.all()
                        gewog = t_gewog_master.objects.all()
                        village = t_village_master.objects.all()
                        team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        return render(request, 'GAP_Certification/fo_details.html',
                                      {'application_details': application_details, 'farmer_group': details,
                                       'file': file,
                                       'audit_findings': audit_findings, 'audit_observation': audit_observation,
                                       'crop_production': crop_production, 'gap_house_details': gap_house_details,
                                       'audit_team_details': audit_team_details, 'team_leader': team_leader,
                                       'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                                       'team_details': team_details})
    elif service_code == 'FPC':
        work_details = t_workflow_details.objects.filter(application_no=Application_No, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_food_t1.objects.filter(Application_No=Application_No)
            details = t_certification_food_t2.objects.filter(Application_No=Application_No)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
            file = t_file_attachment.objects.filter(application_no=Application_No, attachment_type__isnull=True)
            audit_findings = t_certification_food_t4.objects.filter(Application_No=Application_No)
            audit_observation = t_certification_food_t5.objects.filter(Application_No=Application_No)
            dzongkhag = t_dzongkhag_master.objects.all()
            gewog = t_gewog_master.objects.all()
            village = t_village_master.objects.all()
            audit_plan = t_file_attachment.objects.filter(application_no=Application_No, attachment_type='AP')
            return render(request, 'food_product_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details, 'dzongkhag': dzongkhag, 'village': village,
                           'gewog': gewog, 'audit_plan': audit_plan})
        else:
            audit_plan_details = t_workflow_details.objects.filter(application_no=Application_No,
                                                                   application_status='AP')
            if audit_plan_details.exists():
                application_details = t_certification_food_t1.objects.filter(Application_No=Application_No)
                details = t_certification_food_t2.objects.filter(Application_No=Application_No)
                inspection_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                file = t_file_attachment.objects.filter(application_no=Application_No,
                                                        attachment_type__isnull=True)
                audit_plan = t_file_attachment.objects.filter(application_no=Application_No, attachment_type='AP')
                file_attach_count = t_file_attachment.objects.filter(application_no=Application_No,
                                                                     attachment_type='AP').count()
                audit_findings = t_certification_food_t4.objects.filter(Application_No=Application_No)
                audit_observation = t_certification_food_t4.objects.filter(Application_No=Application_No)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'food_product_certification/team_leader_details.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'audit_findings': audit_findings, 'audit_observation': audit_observation,
                               'inspection_details': inspection_details, 'file_attach_count': file_attach_count,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog, 'audit_plan': audit_plan})
            else:
                new_import_app = t_workflow_details.objects.filter(application_no=Application_No,
                                                                   application_status='ATA')
                if new_import_app.exists():
                    application_details = t_certification_food_t1.objects.filter(Application_No=Application_No)
                    details = t_certification_food_t2.objects.filter(Application_No=Application_No)
                    inspection_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                    file = t_file_attachment.objects.filter(application_no=Application_No,
                                                            attachment_type__isnull=True)
                    audit_findings = t_certification_food_t4.objects.filter(Application_No=Application_No)
                    audit_observation = t_certification_food_t4.objects.filter(Application_No=Application_No)
                    dzongkhag = t_dzongkhag_master.objects.all()
                    gewog = t_gewog_master.objects.all()
                    village = t_village_master.objects.all()
                    audit_team_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                    user_details = t_user_master.objects.all()
                    team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                    team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                    return render(request, 'food_product_certification/fo_details.html',
                                  {'application_details': application_details, 'details': details, 'file': file,
                                   'audit_findings': audit_findings, 'audit_observation': audit_observation,
                                   'inspection_details': inspection_details, 'team_details': team_details,
                                   'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                                   'audit_team_details': audit_team_details, 'user_details': user_details,
                                   'team_leader': team_leader})
                else:
                    new_import_app = t_workflow_details.objects.filter(application_no=Application_No,
                                                                       application_status='CA')
                    if new_import_app.exists():
                        application_details = t_certification_food_t1.objects.filter(Application_No=Application_No)
                        details = t_certification_food_t2.objects.filter(Application_No=Application_No)
                        inspection_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                        file = t_file_attachment.objects.filter(application_no=Application_No,
                                                                attachment_type__isnull=True)
                        audit_findings = t_certification_food_t4.objects.filter(Application_No=Application_No)
                        audit_observation = t_certification_food_t5.objects.filter(Application_No=Application_No)
                        dzongkhag = t_dzongkhag_master.objects.all()
                        gewog = t_gewog_master.objects.all()
                        village = t_village_master.objects.all()
                        team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                        audit_plan = t_file_attachment.objects.filter(application_no=Application_No,
                                                                      attachment_type='AP')
                        return render(request, 'food_product_certification/approve_fo_details.html',
                                      {'application_details': application_details, 'details': details, 'file': file,
                                       'audit_findings': audit_findings, 'audit_observation': audit_observation,
                                       'inspection_details': inspection_details, 'team_details': team_details,
                                       'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                                       'team_leader': team_leader, 'audit_plan': audit_plan})
                    else:
                        fpc_app = t_workflow_details.objects.filter(application_no=Application_No,
                                                                    application_status='APA')
                        if fpc_app.exists():
                            application_details = t_certification_food_t1.objects.filter(Application_No=Application_No)
                            details = t_certification_food_t2.objects.filter(Application_No=Application_No)
                            inspection_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                            file = t_file_attachment.objects.filter(application_no=Application_No,
                                                                    attachment_type__isnull=True)
                            audit_plan = t_file_attachment.objects.filter(application_no=Application_No,
                                                                          attachment_type='AP')
                            file_count = t_file_attachment.objects.filter(application_no=Application_No,
                                                                          attachment_type='AP').count()
                            audit_findings = t_certification_food_t4.objects.filter(Application_No=Application_No)
                            audit_observation = t_certification_food_t4.objects.filter(Application_No=Application_No)
                            return render(request, 'food_product_certification/team_leader_details.html',
                                          {'application_details': application_details, 'details': details, 'file': file,
                                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                                           'inspection_details': inspection_details, 'file_count': file_count,
                                           'audit_plan': audit_plan
                                           })
                        else:
                            application_details = t_certification_food_t1.objects.filter(Application_No=Application_No)
                            file = t_file_attachment.objects.filter(application_no=Application_No,
                                                                    attachment_type__isnull=True)
                            dzongkhag = t_dzongkhag_master.objects.all()
                            inspection_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                            gewog = t_gewog_master.objects.all()
                            village = t_village_master.objects.all()
                            unit = t_unit_master.objects.all()
                            audit_team_details = t_certification_food_t3.objects.filter(Application_No=Application_No)
                            team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                            team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
                            return render(request, 'food_product_certification/fo_details.html',
                                          {'application_details': application_details, 'file': file,
                                           'team_details': team_details, 'dzongkhag': dzongkhag, 'village': village,
                                           'gewog': gewog, 'unit': unit, 'audit_team_details': audit_team_details,
                                           'inspection_details': inspection_details, 'team_leader': team_leader})
    elif service_code == 'CMS':
        new_import_app = t_workflow_details.objects.filter(application_no=Application_No, application_status='FRA')
        if new_import_app.exists():
            application_details = t_livestock_clearance_meat_shop_t1.objects.filter(
                application_no=Application_No)
            details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=Application_No)
            file = t_file_attachment.objects.filter(application_no=Application_No)
            unit = t_unit_master.objects.all()
            oic_list = t_field_office_master.objects.all()
            factory_inspection_details = t_livestock_clearance_meat_shop_t5.objects.filter(
                application_no=Application_No, inspection_type="Factory Inspection")
            factory_team_details = t_livestock_clearance_meat_shop_t4.objects.filter(application_no=Application_No,
                                                                                     meeting_type="Factory Inspection")
            factory_inspection_team_details = t_livestock_clearance_meat_shop_t6.objects.filter(
                application_no=Application_No, meeting_type="Factory Inspection")
            inspection_details = t_livestock_clearance_meat_shop_t5.objects.filter(
                application_no=Application_No, inspection_type="Feasibility Inspection")
            team_details = t_livestock_clearance_meat_shop_t4.objects.filter(application_no=Application_No,
                                                                             meeting_type="Feasibility Inspection")
            inspection_team_details = t_livestock_clearance_meat_shop_t6.objects.filter(
                application_no=Application_No, meeting_type="Feasibility Inspection")
            inspector_list = t_user_master.objects.all()
            return render(request, 'meat_shop_registration/fo_approve_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'oic_list': oic_list, 'location': location, 'unit': unit, 'dzongkhag': dzongkhag,
                           'village': village, 'gewog': gewog, 'factory_inspection_details': factory_inspection_details,
                           'factory_inspection_team_details': factory_inspection_team_details,
                           'factory_team_details': factory_team_details, 'inspection_details': inspection_details,
                           'team_details': team_details, 'inspection_team_details': inspection_team_details,
                           'inspector_list': inspector_list})
        else:
            application_details = t_livestock_clearance_meat_shop_t1.objects.filter(
                application_no=Application_No)
            details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=Application_No)
            file = t_file_attachment.objects.filter(application_no=Application_No)
            unit = t_unit_master.objects.all()
            oic_list = t_field_office_master.objects.all()
            return render(request, 'meat_shop_registration/fo_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'oic_list': oic_list, 'location': location, 'unit': unit, 'dzongkhag': dzongkhag,
                           'village': village, 'gewog': gewog})
    elif service_code == 'COM':
        application_no = request.GET.get('application_id')
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        details = t_common_complaint_t1.objects.filter(Application_No=application_no)
        complaint_file = t_file_attachment.objects.filter(application_no=application_no, Role_Id='8')
        investigation_file = t_file_attachment.objects.filter(application_no=application_no, Role_Id='5')

        return render(request, 'complaint_handling/investigation_complaint_update.html', {'complaint_details': details,
                                                                                          'dzongkhag': dzongkhag,
                                                                                          'gewog': gewog,
                                                                                          'village': village,
                                                                                          'complaint_file': complaint_file,
                                                                                          'investigation_file': investigation_file})


def approve_fo_app(request):
    appNo = request.POST['appNo']
    application_details = t_workflow_details.objects.filter(application_no=appNo)
    for application_details in application_details:
        App_id = application_details.applicant_id
    client_id = t_user_master.objects.filter(Application_No=App_id)
    for client in client_id:
        client_login = client.Login_Id
    application_details.update(assigned_to=client_login)
    return render(request, 'new_import_permit.html')


def print_import_details(request):
    application_no = request.GET.get('application_id')
    print_details = t_plant_import_permit_t1.objects.filter(Application_No=application_no)
    for print_import in print_details:
        finalDestination = print_import.Final_Destination
    return render(request, 'import_permit/plant_import_permit.html',
                  {'Final_Destination': finalDestination})


def view_oic_details(request):
    application_id = request.GET.get('application_id')
    service_code = request.GET.get('service_code')

    if service_code == 'MPP':
        application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
        details_list = t_plant_movement_permit_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()

        for application in workflow_details:
            Field_Office = application.field_office_id
        inspector_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)

        return render(request, 'movement_permit/oic_application_details.html',
                      {'application_details': application_details, 'details_list': details_list,
                       'file': file, 'inspector_list': inspector_list, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location})

    elif service_code == 'IPP':
        application_no = request.GET.get('application_id')
        new_import_app = t_plant_import_permit_inspection_t1.objects.filter(Application_No=application_no)
        details = t_plant_import_permit_inspection_t2.objects.filter(Application_No=application_no,
                                                                     Quantity_Balance__gt=0)
        file = t_file_attachment.objects.filter(application_no=application_no)
        location_mapping = t_field_office_master.objects.filter()
        country = t_country_master.objects.all()
        crop = t_plant_crop_master.objects.all()
        pesticide = t_plant_pesticide_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        return render(request, 'import_permit/oic_import_application.html',
                      {'application_details': new_import_app, 'details': details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location_mapping, 'country': country,
                       'crop': crop, 'pesticide': pesticide, 'variety': variety, 'gewog': gewog,
                       'inspector_list': user_role_list})

    elif service_code == 'EPP':
        application_id = request.GET.get('application_id')
        application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
            Application_No=application_id)
        export_details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(
            Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        file = t_file_attachment.objects.filter(application_no=application_id)
        entry_point = t_field_office_master.objects.all()
        Country_list = t_country_master.objects.all()
        return render(request, 'export_permit/oic_application_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'location': location, 'inspector_list': user_role_list, 'entry_point': entry_point,
                       'Country_list': Country_list, 'export_details': export_details})
    elif service_code == 'RNS':
        application_id = request.GET.get('application_id')
        application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        crop_master = t_plant_crop_master.objects.all()
        crop_category = t_plant_crop_category_master.objects.all()
        return render(request, 'nursery_registration/oic_application_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'file': file, 'inspector_list': user_role_list, 'crop_master': crop_master,
                       'crop_category': crop_category})
    elif service_code == 'RSC':
        application_id = request.GET.get('application_id')
        application_details = t_plant_seed_certification_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_seed_certification_t2.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)

        return render(request, 'seed_certification/oic_application_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'file': file, 'inspector_list': user_role_list})
    elif service_code == 'CMS':
        application_details = t_livestock_clearance_meat_shop_t1.objects.filter(application_no=application_id)
        details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        unit = t_unit_master.objects.all()
        for application in workflow_details:
            Field_Office = application.field_office_id
        inspector_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        return render(request, 'meat_shop_registration/oic_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'inspector_list': inspector_list, 'unit': unit, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village})
    elif service_code == 'APM':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        application_details = t_livestock_ante_post_mortem_t1.objects.filter(Application_No=application_id)
        details = t_livestock_ante_post_mortem_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        return render(request, 'ante_post_mortem/oic_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'mortem': details,
                       'inspector_list': user_role_list})
    elif service_code == 'LMP':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        location_mapping = t_location_field_office_mapping.objects.all()
        application_details = t_livestock_movement_permit_t1.objects.filter(Application_No=application_id)
        details = t_livestock_movement_permit_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        return render(request, 'Movement_Permit_Livestock/oic_movement_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'details': details,
                       'inspector_list': user_role_list, 'location_mapping': location_mapping})
    elif service_code == 'LEC':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_field_office_master.objects.all()
        application_details = t_livestock_export_certificate_t1.objects.filter(Application_No=application_id)
        details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        species = t_livestock_species_master.objects.all()
        field_office = t_field_office_master.objects.all()
        return render(request, 'Export_Certificate/oic_export_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'details': details,
                       'inspector_list': user_role_list, 'species': species, 'field_office': field_office})
    elif service_code == 'IAF':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        application_details = t_livestock_import_permit_animal_inspection_t1.objects.filter(
            Application_No=application_id)
        details = t_livestock_import_permit_animal_inspection_t2.objects.filter(Application_No=application_id,
                                                                                Quantity_Balance__gt=0)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        location_details = t_field_office_master.objects.all()
        location_mapping = t_field_office_master.objects.filter(Is_Entry_Point="Y")
        species = t_livestock_species_master.objects.all()
        breed = t_livestock_species_breed_master.objects.all()
        return render(request, 'Animal_Fish_Import/oic_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'import': details,
                       'inspector_list': user_role_list, 'location_details': location_details,
                       'location_mapping': location_mapping, 'species': species, 'breed': breed})
    elif service_code == 'ILP':
        dzongkhag = t_dzongkhag_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        application_details = t_livestock_import_permit_product_inspection_t1.objects.filter(
            Application_No=application_id)
        details = t_livestock_import_permit_product_inspection_t2.objects.filter(Application_No=application_id,
                                                                                 Quantity_Balance__gt=0)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        location_details = t_field_office_master.objects.all()
        return render(request, 'Livestock_Import/oic_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location, 'import': details,
                       'inspector_list': user_role_list, 'location_details': location_details})
    elif service_code == 'FEC':
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        country = t_country_master.objects.all()
        field_office = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        location = t_location_field_office_mapping.objects.all()
        unit = t_unit_master.objects.all()
        application_details = t_food_export_certificate_t1.objects.filter(
            Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        return render(request, 'export_certificate_food/oic_details.html',
                      {'application_details': application_details, 'file': file,
                       'gewog': gewog, 'dzongkhag': dzongkhag, 'country': country, 'field_office': field_office,
                       'unit': unit, 'village': village, 'location': location,
                       'inspector_list': user_role_list})
    elif service_code == 'FHL':
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        country = t_country_master.objects.all()
        field_office = t_field_office_master.objects.all()
        application_details = t_food_licensing_food_handler_t1.objects.filter(
            Application_No=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        return render(request, 'food_handler/oic_details.html',
                      {'application_details': application_details, 'file': file,
                       'gewog': gewog, 'dzongkhag': dzongkhag, 'country': country, 'field_office': field_office,
                       'village': village, 'inspector_list': user_role_list})
    elif service_code == "FIP":
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        field_office = t_field_office_master.objects.all()
        unit = t_unit_master.objects.all()
        application_details = t_food_import_permit_inspection_t1.objects.filter(
            Application_No=application_id)
        details = t_food_import_permit_inspection_t2.objects.filter(Application_No=application_id,
                                                                    Quantity_Balance__gt=0)
        for app_details in application_details:
            permit_no = app_details.Import_Permit_No
            detail_of_app = t_food_import_permit_t1.objects.filter(
                Import_Permit_No=permit_no)
            for detail_in in detail_of_app:
                file = t_file_attachment.objects.filter(application_no=detail_in.Application_No)
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        field_list = t_field_office_master.objects.all()
        country_list = t_country_master.objects.all()
        user_role_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        return render(request, 'import_certificate_food/oic_details.html',
                      {'application_details': application_details, 'file': file,
                       'dzongkhag': dzongkhag, 'village': village,
                       'gewog': gewog, 'field_office': field_office, 'import': details,
                       'unit': unit, 'inspector_list': user_role_list,
                       'location': field_list, 'country': country_list})
    elif service_code == 'FBR':
        application_details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)
        details = t_food_business_registration_licensing_t2.objects.filter(application_no=application_id)
        food_handler = t_food_business_registration_licensing_t3.objects.filter(application_no=application_id)
        file = t_file_attachment.objects.filter(application_no=application_id)
        unit = t_unit_master.objects.all()
        workflow_details = t_workflow_details.objects.filter(application_no=application_id)
        for application in workflow_details:
            Field_Office = application.field_office_id
        inspector_list = t_user_master.objects.filter(Field_Office_Id_id=Field_Office)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        raw_materials = t_food_business_registration_licensing_t7.objects.filter(application_no=application_id)
        packaging_material = t_food_business_registration_licensing_t8.objects.filter(application_no=application_id)
        return render(request, 'registration_licensing/oic_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'inspector_list': inspector_list, 'unit': unit, 'food_handler': food_handler,
                       'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village, 'raw_materials': raw_materials,
                       'packaging_material': packaging_material})
    elif service_code == 'OC':
        oc_work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if oc_work_details.exists():
            application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
            details = t_certification_organic_t2.objects.filter(Application_No=application_id)
            audit_team = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=application_id)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_id)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_id)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=application_id)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_id)
            api_details = t_certification_organic_t9.objects.filter(Application_No=application_id)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_id)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            return render(request, 'organic_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details, 'audit_plan': audit_plan,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation})
        else:
            application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
            details = t_certification_organic_t2.objects.filter(Application_No=application_id)
            audit_team = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=application_id)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_id)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_id)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=application_id)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_id)
            api_details = t_certification_organic_t9.objects.filter(Application_No=application_id)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_id)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'organic_certification/team_leader_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details, 'audit_plan': audit_plan,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'file_attach_count': file_attach_count})
    elif service_code == 'GAP':
        work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
            details = t_certification_gap_t2.objects.filter(Application_No=application_id)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=application_id)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_id)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_id)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            return render(request, 'GAP_Certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details, 'audit_plan': audit_plan})
        else:
            application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
            details = t_certification_gap_t2.objects.filter(Application_No=application_id)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=application_id)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_id)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_id)
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'GAP_Certification/team_leader_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details, 'audit_plan': audit_plan,
                           'file_attach_count': file_attach_count})
    elif service_code == 'FPC':
        work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
            details = t_certification_food_t2.objects.filter(Application_No=application_id)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_findings = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_observation = t_certification_food_t5.objects.filter(Application_No=application_id)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            return render(request, 'food_product_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details, 'audit_plan': audit_plan
                           })
        else:
            application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
            details = t_certification_food_t2.objects.filter(Application_No=application_id)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            audit_findings = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_observation = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            return render(request, 'food_product_certification/team_leader_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details, 'file_attach_count': file_attach_count,
                           'audit_plan': audit_plan
                           })
    elif service_code == 'COM':
        application_no = request.GET.get('application_id')
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        details = t_common_complaint_t1.objects.filter(Application_No=application_no)
        complaint_file = t_file_attachment.objects.filter(application_no=application_no, Role_Id='8')
        investigation_file = t_file_attachment.objects.filter(application_no=application_no, Role_Id='5')

        return render(request, 'complaint_handling/investigation_complaint_update.html', {'complaint_details': details,
                                                                                          'dzongkhag': dzongkhag,
                                                                                          'gewog': gewog,
                                                                                          'village': village,
                                                                                          'complaint_file': complaint_file,
                                                                                          'investigation_file': investigation_file})


def view_inspector_details(request):
    application_id = request.GET.get('application_id')
    application_details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    location = t_field_office_master.objects.all()
    details_list = t_plant_import_permit_t2.objects.filter(Application_No=application_id)
    file = t_file_attachment.objects.filter(application_no=application_id)
    workflow_details = t_workflow_details.objects.filter(application_no=application_id)
    for application in workflow_details:
        Field_Office = application.field_office_id
    user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
    import_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/inspector_import_permit.html',
                  {'application_details': application_details,
                   'location': location, 'import': details_list, 'inspector_list': user_role_list,
                   'file': file, 'import_permit': import_permit})


def add_import_details_ins(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_import_permit_inspection_t3.objects.create(Application_No=application_id,
                                                       Current_Observation=currentObservation,
                                                       Decision_Conformity=decisionConform)
    import_permit = t_plant_import_permit_inspection_t3.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/add_import_details.html', {'import_permit': import_permit})


def approve_import_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    validity_period = request.POST.get('validity')
    permit_no = get_permit_no(request)
    details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=dateOfInspection)
    details.update(Movement_Permit_No=permit_no)
    details.update(Validity_Period=validity_period)
    d = timedelta(days=int(validity_period))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='A')
    update_payment_details(application_id, permit_no, 'IPP', validity_date, 'Final', 'null')
    for email_id in application_details:
        emailId = email_id.Email
        send_ipp_approve_email(permit_no, emailId, validity_date, application_id)
    return render(request, 'import_permit/inspector_import_permit.html', {'application_details': application_details})


def send_ipp_approve_email(permit_no, Email, validity_date, application_id):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Plant And Plant Products Has Been Approved." \
              " Your Applicaton No is" + application_id + \
              " And Import Permit No is:" + permit_no + " And is Valid Till " + " " + str(validity_date) + \
              " Please Make Payment Before Validity Expires. Visit The Nearest Bafra Office For Payment " \
              "or Pay Online at https://tinyurl.com/y3m7wa3c Thank you! "
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_ipp_reject_email(Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Plant And Plant Products Has Been Rejected."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def reject_import_application(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='R')
    for email_id in application_details:
        emailId = email_id.Email
        send_ipp_reject_email(emailId)
    return render(request, 'import_permit/inspector_import_permit.html', {'application_details': application_details})


def update_inspection_call_details(request):
    data = dict()
    service_code = request.POST.get('service_code')
    appNo = request.POST.get('application_No')
    date_requested = request.POST.get('date')
    entry_point = request.POST.get('entry_point')
    remarks = request.POST.get('remarks')
    if service_code == 'IPP':
        details = t_plant_import_permit_t1.objects.filter(Application_No=appNo)
        import_app = t_plant_import_permit_t2.objects.filter(Application_No=appNo)
        new_import_application_no = new_plant_import_application_no(service_code)

        for details in details:
            t_plant_import_permit_inspection_t1.objects.create(
                Application_No=new_import_application_no,
                Import_Type=details.Import_Type,
                License_No=details.License_No,
                Business_Name=details.Business_Name,
                CID=details.CID,
                Applicant_Name=details.Applicant_Name,
                Present_Address=details.Present_Address,
                Contact_No=details.Contact_No,
                Email=details.Email,
                Name_And_Address_Supplier=details.Name_And_Address_Supplier,
                Means_of_Conveyance=details.Means_of_Conveyance,
                Place_Of_Entry=details.Place_Of_Entry,
                Purpose=details.Purpose,
                Final_Destination=details.Final_Destination,
                Import_Inspection_Submit_Date=date.today(),
                Proposed_Inspection_Date=date_requested,
                Actual_Point_Of_Entry=entry_point,
                Inspection_Request_Remarks=remarks,
                Import_Permit_No=details.Import_Permit_No,
                Inspection_Date=None,
                Inspection_Type=None,
                Inspection_Time=None,
                Inspection_Leader=None,
                Inspection_Team=None,
                Clearance_Ref_No=None,
                Expected_Arrival_Date=details.Expected_Arrival_Date,
                FO_Remarks=details.FO_Remarks,
                Inspection_Remarks=None,
                Country_Of_Origin=details.Country_Of_Origin,
                Application_Date=date.today(),
                Applicant_Id=details.Applicant_Id,
                Approved_Date=details.Approved_Date,
                Validity_Period=details.Validity_Period,
                Validity=details.Validity,
                Application_Type=details.Application_Type,
                Nationality=details.Nationality,
                Dzongkhag=details.Dzongkhag,
                Gewog=details.Gewog,
                Nationality_Type=details.Nationality_Type,
                Village=details.Village,
                Passport_Number=details.Passport_Number
            )
            for import_details in import_app:
                if import_details.Quantity_Balance > 0:
                    t_plant_import_permit_inspection_t2.objects.create(
                        Application_No=new_import_application_no,
                        Import_Category=import_details.Import_Category,
                        Crop_Id=import_details.Crop_Id,
                        Pesticide_Id=import_details.Pesticide_Id,
                        Description=import_details.Description,
                        Variety_Id=import_details.Variety_Id,
                        Unit=import_details.Unit,
                        Quantity=import_details.Quantity,
                        Quantity_Released=0,
                        Quantity_Rejected=0,
                        Remarks=import_details.Remarks,
                        Quantity_Balance=import_details.Quantity_Balance,
                        Quantity_Balance_1=import_details.Quantity_Balance,
                        Product_Record_Id=import_details.pk
                    )
        field = t_location_field_office_mapping.objects.filter(Location_Code=entry_point)
        for field_office in field:
            field_office_id = field_office.Field_Office_Id_id
        t_workflow_details.objects.create(application_no=new_import_application_no,
                                          applicant_id=request.session['email'],
                                          assigned_to=None, field_office_id=entry_point, section='Plant',
                                          assigned_role_id='4', action_date=date.today(), application_status='P',
                                          service_code=service_code, application_date=date.today())
        app_details = t_workflow_details.objects.filter(application_no=appNo)
        app_details.update(application_status='CN')
        return redirect(call_for_inspection)
    elif service_code == 'IAF':
        detail = t_livestock_import_permit_animal_t1.objects.filter(Application_No=appNo)
        import_app = t_livestock_import_permit_animal_t2.objects.filter(Application_No=appNo)

        new_import_application_no = new_animal_fish_import_application_no(service_code)
        for details in detail:
            t_livestock_import_permit_animal_inspection_t1.objects.create(
                Application_No=new_import_application_no,
                Application_Date=date.today(),
                Approve_Date=None,
                Import_Permit_No=details.Import_Permit_No,
                Validity_Period=None,
                Validity=None,
                Application_Type=details.Application_Type,
                Import_Type=details.Import_Type,
                License_No=details.License_No,
                Business_Name=details.Business_Name,
                Nationality=details.Nationality,
                Country=details.Country,
                CID=details.CID,
                Applicant_Name=details.Applicant_Name,
                Dzongkhag_Code=details.Dzongkhag_Code,
                Gewog_Code=details.Gewog_Code,
                Village_Code=details.Village_Code,
                Present_Address=details.Present_Address,
                Contact_No=details.Contact_No,
                Email=details.Email,
                Origin_Source_Products=details.Origin_Source_Products,
                Name_And_Address_Supplier=details.Name_And_Address_Supplier,
                Means_of_Conveyance=details.Means_of_Conveyance,
                Place_Of_Entry=details.Place_Of_Entry,
                Final_Destination=details.Final_Destination,
                Expected_Arrival_Date=details.Expected_Arrival_Date,
                Proposed_Inspection_Date=date_requested,
                Actual_Point_Of_Entry=entry_point,
                Inspection_Request_Remarks=remarks,
                Inspection_Date=None,
                Inspection_Type=None,
                Inspection_Time=None,
                Inspection_Leader=None,
                Inspection_Team=None,
                Clearance_Ref_No=None,
                FO_Remarks=details.FO_Remarks,
                Inspection_Remarks=None,
                Quarantine_Facilities=details.Quarantine_Facilities,
                Applicant_Id=details.Applicant_Id,
                Passport_Number=details.Passport_Number
            )
        for import_details in import_app:
            if import_details.Quantity_Balance > 0:
                t_livestock_import_permit_animal_inspection_t2.objects.create(
                    Application_No=new_import_application_no,
                    Species=import_details.Species,
                    Breed=import_details.Breed,
                    Age=import_details.Age,
                    Sex=import_details.Sex,
                    Description=import_details.Description,
                    Quantity=import_details.Quantity,
                    Quantity_Released=0,
                    Remarks=import_details.Remarks,
                    Quantity_Balance=import_details.Quantity_Balance,
                    Quantity_Balance_1=import_details.Quantity_Balance,
                    Product_Record_Id=import_details.pk
                )
        field = t_location_field_office_mapping.objects.filter(Location_Code=entry_point)
        for field_office in field:
            field_office_id = field_office.Field_Office_Id_id
        t_workflow_details.objects.create(application_no=new_import_application_no,
                                          applicant_id=request.session['email'],
                                          assigned_to=None, field_office_id=entry_point, section='Livestock',
                                          assigned_role_id='4', action_date=date.today(), application_status='P',
                                          service_code=service_code, application_date=date.today())
        login_id = request.session['Login_Id']
        workflow_details = t_workflow_details.objects.filter(application_no=appNo)
        workflow_details.update(application_status='CN')
        return redirect(call_for_inspection)
    elif service_code == 'ILP':
        detail = t_livestock_import_permit_product_t1.objects.filter(Application_No=appNo)
        import_details = t_livestock_import_permit_product_t2.objects.filter(Application_No=appNo)

        new_import_application_no = new_livestock_product_import_application_no(service_code)
        for details in detail:
            t_livestock_import_permit_product_inspection_t1.objects.create(
                Application_No=new_import_application_no,
                Application_Date=date.today(),
                Approve_Date=None,
                Validity_Period=None,
                Validity=None,
                Application_Type=details.Application_Type,
                Import_Type=details.Import_Type,
                License_No=details.License_No,
                Business_Name=details.Business_Name,
                Nationality=details.Nationality,
                Country=details.Country,
                CID=details.CID,
                Applicant_Name=details.Applicant_Name,
                Dzongkhag_Code=details.Dzongkhag_Code,
                Gewog_Code=details.Gewog_Code,
                Village_Code=details.Village_Code,
                Present_Address=details.Present_Address,
                Contact_No=details.Contact_No,
                Email=details.Email,
                Origin_Source_Products=details.Origin_Source_Products,
                Name_And_Address_Supplier=details.Name_And_Address_Supplier,
                Means_of_Conveyance=details.Means_of_Conveyance,
                Place_Of_Entry=details.Place_Of_Entry,
                Final_Destination=details.Final_Destination,
                Expected_Arrival_Date=details.Expected_Arrival_Date,
                Proposed_Inspection_Date=date_requested,
                Actual_Point_Of_Entry=entry_point,
                Inspection_Request_Remarks=remarks,
                Inspection_Date=None,
                Inspection_Type=None,
                Inspection_Time=None,
                Inspection_Leader=None,
                Inspection_Team=None,
                Clearance_Ref_No=None,
                FO_Remarks=details.FO_Remarks,
                Inspection_Remarks=None,
                Import_Permit_No=details.Import_Permit_No,
                Applicant_Id=details.Applicant_Id,
                Passport_Number=details.Passport_Number
            )
        for import_details_ILP in import_details:
            if import_details.Quantity_Balance > 0:
                t_livestock_import_permit_product_inspection_t2.objects.create(
                    Application_No=new_import_application_no,
                    Particulars=import_details_ILP.Particulars,
                    Company_Name=import_details_ILP.Company_Name,
                    Description=import_details_ILP.Description,
                    Quantity=import_details_ILP.Quantity,
                    Unit=import_details_ILP.Unit,
                    Quantity_Released=0,
                    Remarks=import_details_ILP.Remarks,
                    Quantity_Balance=import_details_ILP.Quantity_Balance,
                    Quantity_Balance_1=import_details_ILP.Quantity_Balance,
                    Product_Record_Id=import_details_ILP.pk
                )

        field = t_location_field_office_mapping.objects.filter(Location_Code=entry_point)
        for field_office in field:
            field_office_id = field_office.Field_Office_Id_id
        t_workflow_details.objects.create(application_no=new_import_application_no,
                                          applicant_id=request.session['email'],
                                          assigned_to=None, field_office_id=entry_point, section='Livestock',
                                          assigned_role_id='4', action_date=date.today(), application_status='P',
                                          service_code=service_code, application_date=date.today())
        login_id = request.session['Login_Id']
        workflow_details = t_workflow_details.objects.filter(application_no=appNo)
        workflow_details.update(application_status='CN')
        return redirect(call_for_inspection)
    elif service_code == 'FIP':
        detail = t_food_import_permit_t1.objects.filter(Application_No=appNo)
        import_details = t_food_import_permit_t2.objects.filter(Application_No=appNo)
        date_format_ins = request.POST.get('date')
        new_import_application_no = new_food_import_application_no(service_code)
        for details in detail:
            t_food_import_permit_inspection_t1.objects.create(
                Application_No=new_import_application_no,
                Import_Type=details.Import_Type,
                License_No=details.License_No,
                CID=details.CID,
                Applicant_Name=details.Applicant_Name,
                Dzongkhag_Code=details.Dzongkhag_Code,
                Gewog_Code=details.Gewog_Code,
                Village_Code=details.Village_Code,
                Present_Address=details.Present_Address,
                Contact_No=details.Contact_No,
                Email=details.Email,
                Operation_Type=details.Operation_Type,
                Origin_Country_Food=details.Origin_Country_Food,
                Transit_Country=details.Transit_Country,
                Country_Of_Transit=details.Country_Of_Transit,
                Means_of_Conveyance=details.Means_of_Conveyance,
                Place_Of_Entry=details.Place_Of_Entry,
                Final_Destination=details.Final_Destination,
                Expected_Arrival_Date=details.Expected_Arrival_Date,
                FO_Remarks=details.FO_Remarks,
                Application_Date=date.today(),
                Approve_Date=details.Approve_Date,
                Validity_Period=None,
                Validity=None,
                Import_Permit_No=details.Import_Permit_No,
                Proposed_Inspection_Date=date_format_ins,
                Actual_Point_Of_Entry=entry_point,
                Inspection_Request_Remarks=remarks,
                Inspection_Date=None,
                Inspection_Type=None,
                Inspection_Time=None,
                Inspection_Leader=None,
                Inspection_Team=None,
                Clearance_Ref_No=None,
                Inspection_Remarks=None,
                Applicant_Id=details.Applicant_Id,
                Terms=details.Terms
            )

        for import_details in import_details:
            if import_details.Quantity_Balance > 0:
                t_food_import_permit_inspection_t2.objects.create(
                    Application_No=new_import_application_no,
                    Common_Name=import_details.Common_Name,
                    Product_Category=import_details.Product_Category,
                    Product_Characteristics=import_details.Product_Characteristics,
                    Quantity=import_details.Quantity,
                    Unit=import_details.Unit,
                    Exporter_Type=import_details.Exporter_Type,
                    Quantity_Released=0,
                    Remarks=import_details.Remarks,
                    Quantity_Balance=import_details.Quantity_Balance,
                    Quantity_Balance_1=import_details.Quantity_Balance,
                    Product_Record_Id=import_details.pk
                )

        field = t_location_field_office_mapping.objects.filter(Location_Code=entry_point)
        for field_office in field:
            field_office_id = field_office.Field_Office_Id_id
        t_workflow_details.objects.create(application_no=new_import_application_no,
                                          applicant_id=request.session['email'],
                                          assigned_to=None, field_office_id=entry_point, section='Food',
                                          assigned_role_id='4', action_date=date.today(), application_status='P',
                                          service_code=service_code, application_date=date.today())
        login_id = request.session['Login_Id']
        workflow_details = t_workflow_details.objects.filter(application_no=appNo)
        workflow_details.update(application_status='CN')
        return redirect(call_for_inspection)


def new_animal_fish_import_application_no(service_code):
    last_application_no = t_livestock_import_permit_animal_inspection_t1.objects.aggregate(Max('Application_No'))
    lastAppNo = last_application_no['Application_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = service_code + "/I/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[12:15]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = service_code + "/I/" + str(year) + "/" + AppNo
    return newAppNo


def new_plant_import_application_no(service_code):
    last_application_no = t_plant_import_permit_inspection_t1.objects.aggregate(Max('Application_No'))
    lastAppNo = last_application_no['Application_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = service_code + "-I-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[12:15]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = service_code + "-I-" + str(year) + "-" + AppNo
    return newAppNo


def new_livestock_product_import_application_no(service_code):
    last_application_no = t_livestock_import_permit_product_inspection_t1.objects.aggregate(Max('Application_No'))
    lastAppNo = last_application_no['Application_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = service_code + "-I-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[12:15]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = service_code + "-I-" + str(year) + "-" + AppNo
    return newAppNo


def new_food_import_application_no(service_code):
    last_application_no = t_food_import_permit_inspection_t1.objects.aggregate(Max('Application_No'))
    lastAppNo = last_application_no['Application_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = service_code + "-I-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[12:15]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = service_code + "-I-" + str(year) + "-" + AppNo
    return newAppNo


def update_resubmit_details(request):
    service_code = request.POST.get('service_code')
    appNo = request.POST.get('appNo')
    inspection_date = request.POST.get('inspection_date')
    Resubmit_Remarks = request.POST.get('Resubmit_Remarks')

    application = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=appNo)
    application.update(Desired_Inspection_Date=inspection_date, Resubmit_Remarks=Resubmit_Remarks)
    login_id = request.session['Login_Id']
    application_details = t_workflow_details.objects.filter(assigned_to=login_id)
    return render(request, 'inspection_call.html', {'application_details': application_details})


def add_plant_import_file(request):
    data = dict()
    myFile = request.FILES['plant_document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/import_permit")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/import_permit" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def add_agro_import_file(request):
    data = dict()
    myFile = request.FILES['agro_document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/import_permit")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/import_permit" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def add_plant_attach(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
    return render(request, 'import_permit/plant_attachment_page.html', {'file_attach': file_attach})


def add_agro_attach(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        t_file_attachment.objects.create(application_no=Application_No, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=fileName)

        file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'import_permit/agro_attachment_page.html', {'file_attach': file_attach})


def delete_plant_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/import_permit")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'import_permit/plant_attachment_page.html', {'file_attach': file_attach})


def delete_agro_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/import_permit")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'import_permit/agro_attachment_page.html', {'file_attach': file_attach})


def save_details_import(request):
    Application_No = request.POST.get('applicationNo')
    print(Application_No)
    details = t_workflow_details.objects.filter(application_no=Application_No)
    details.update(application_date=date.today())
    details.update(action_date=date.today())

    crop = t_plant_crop_master.objects.all()
    pesticide = t_plant_pesticide_master.objects.all()
    variety = t_plant_crop_variety_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'import_permit/apply_import_permit.html',
                  {'crop': crop, 'pesticide': pesticide, 'variety': variety,
                   'location': location})


def fo_reject(request):
    Role_Id = request.session['Role_Id']
    appId = request.POST.get('application_id')
    remarks = request.POST.get('remarks')

    application_details = t_workflow_details.objects.filter(application_no=appId)
    details = t_plant_import_permit_t1.objects.filter(Application_No=appId)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    for app in details:
        email = app.Email
        send_import_reject_email(remarks, email)

    new_import_app = t_workflow_details.objects.filter(assigned_role_id=Role_Id, section='Plant',
                                                       application_status='P')
    return render(request, 'import_permit/new_import_permit_fo.html', {'new_import_app': new_import_app})


def send_import_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Application for Import Of Plant And Plant Products Has Been Rejected Because " + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_movement_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Application for Movement Permit For Plant And Plant Products Has Been Rejected Because " + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def fo_approve(request):
    new_import_permit = get_import_permit_no()
    appId = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    validity = request.POST.get('validity')
    Additional_Declaration = request.POST.get('additional_Info')
    details = t_plant_import_permit_t1.objects.filter(Application_No=appId)
    details.update(Import_Permit_No=new_import_permit)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    details.update(Approved_Date=date.today())
    details.update(Validity_Period=validity)
    details.update(Additional_Declaration=Additional_Declaration)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(application_no=appId)
    for app in application_details:
        client_login_id = app.applicant_id
        client_id = t_user_master.objects.filter(Email_Id=client_login_id)
        for client in client_id:
            login_id = client.Login_Id
            application_details.update(assigned_to=login_id)
            application_details.update(action_date=date.today())
            application_details.update(assigned_role_id=None)
    for email_id in details:
        email = email_id.Email
        send_import_approve_email(new_import_permit, email, validity_date, appId)
    for application_details in details:
        app_type = application_details.Import_Type
        if app_type == 'P':
            update_payment_details(appId, new_import_permit, 'IPP', validity_date, 'Final', '131110102')
        else:
            update_payment_details(appId, new_import_permit, 'IPP', validity_date, 'Final', '131110016')
    return redirect(dashboard)


def send_import_approve_email(new_import_permit, Email, validity_date, application_id):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Plant And Plant Products Has Been Approved." \
              " Your Application No is " + application_id + \
              " And Import Permit No is:" + new_import_permit + " And is Valid TIll " + str(validity_date) + \
              " Please Make Payment Before Validity Expires. Visit The Nearest Bafra Office For Payment" \
              " or Pay Online at https://tinyurl.com/y3m7wa3c Thank you! "
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def get_import_permit_no():
    last_import_permit_no = t_plant_import_permit_t1.objects.aggregate(Max('Import_Permit_No'))
    last_permit_no = last_import_permit_no['Import_Permit_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = "IPP" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_permit_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = "IPP" + "/" + str(year) + "/" + AppNo
    return newPermitNo


def assign_to_inspector(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')

    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(assigned_to=forwardTo)
    application_details.update(action_date=date.today())
    application_details.update(assigned_role_id='5')
    Field_Office_Id = request.session['field_office_id']
    Login_Id = request.session['Login_Id']
    application_details = t_workflow_details.objects.filter(assigned_to=Login_Id, field_office_id=Field_Office_Id)
    return render(request, 'import_permit/oic_application.html', {'application_details': application_details})


def edit_inspector_details(request, Record_Id):
    plant_import_permit = get_object_or_404(t_plant_import_permit_t2, pk=Record_Id)
    details = t_plant_import_permit_t2.objects.filter(pk=Record_Id)
    for plant in details:
        crop_id = plant.Crop_Id
    crop_master = t_plant_crop_master.objects.filter(pk=crop_id)
    for crop in crop_master:
        crop_name = crop.Crop_Common_Name
    variety = t_plant_crop_variety_master.objects.filter(Crop_Id=crop_id)
    for crop_variety in variety:
        variety_crop = crop_variety.Crop_Variety_Name
    if request.method == 'POST':
        form = ImportFormTwo(request.POST, instance=plant_import_permit)
    else:
        form = ImportFormTwo(instance=plant_import_permit)
    return save_details_form(request, form, crop_name, variety_crop, 'import_permit/edit_inspector_details.html')


def save_details_form(request, form, crop_name, variety_crop, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            import_details = t_plant_import_permit_t2.objects.all()
            data['html_form'] = render_to_string('import_permit/inspector_import_permit.html', {
                'import': import_details
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'Crop_Common_Name': crop_name, 'variety_crop': variety_crop}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def add_details_ins_import(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_import_permit_inspection_t3.objects.create(Application_No=application_id,
                                                       Current_Observation=currentObservation,
                                                       Decision_Conformity=decisionConform)
    import_permit = t_plant_import_permit_inspection_t3.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/add_import_details.html', {'import_permit': import_permit})


def edit_decision(request, Record_Id):
    decision = get_object_or_404(t_plant_import_permit_inspection_t3, pk=Record_Id)
    if request.method == 'POST':
        form = ImportFormThree(request.POST, instance=decision)
    else:
        form = ImportFormThree(instance=decision)
    return save_decision_form(request, form, 'import_permit/edit_decision.html')


def save_decision_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            decision = t_plant_import_permit_inspection_t3.objects.all()
            data['html_form'] = render_to_string('import_permit/add_import_details.html', {
                'import_permit': decision
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def approve_clearance_application(request):
    application_no = request.GET.get('application_no')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')

    clearnace_ref_no = clearance_ref_no(request)

    update_details = t_plant_import_permit_inspection_t1.objects.filter(Application_No=application_no)
    update_details.update(Clearance_Ref_No=clearnace_ref_no)
    update_details.update(Inspection_Leader=Inspection_Leader)
    update_details.update(Inspection_Team=Inspection_Team)
    update_details.update(Inspection_Date=dateOfInspection)
    update_details.update(Approved_Date=date.today())
    if remarks is not None:
        update_details.update(Inspection_Remarks=remarks)
    else:
        update_details.update(Inspection_Remarks=None)
    imp_update_details = t_plant_import_permit_inspection_t2.objects.filter(Application_No=application_no)
    for import_IPP in imp_update_details:
        import_details_sum = t_plant_import_permit_inspection_t2.objects.filter(
            Product_Record_Id=import_IPP.Product_Record_Id).aggregate(Sum('Quantity_Released'))

        sum_import = import_details_sum['Quantity_Released__sum']
        import_det = t_plant_import_permit_inspection_t2.objects.filter(pk=import_IPP.Record_Id)

        for import_details in import_det:
            if sum_import == int(import_details.Quantity):
                import_details = t_plant_import_permit_inspection_t1.objects.filter(
                    Application_No=application_no)
                for import_det in import_details:
                    la_details = t_plant_import_permit_t1.objects.filter(
                        Import_Permit_No=import_det.Import_Permit_No)
                    for la in la_details:
                        work_details = t_workflow_details.objects.filter(application_no=la.Application_No)
                        work_details.update(application_status='C')
            else:
                import_details = t_plant_import_permit_inspection_t1.objects.filter(
                    Application_No=application_no)
                for import_det in import_details:
                    la_details = t_plant_import_permit_t1.objects.filter(
                        Import_Permit_No=import_det.Import_Permit_No)
                    for la in la_details:
                        work_details = t_workflow_details.objects.filter(application_no=la.Application_No)
                        work_details.update(application_status='P')
    return redirect(inspector_application)


def clearance_ref_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_clearance_ref_no = t_plant_import_permit_inspection_t1.objects.aggregate(Max('Clearance_Ref_No'))
    last_permit_no = last_clearance_ref_no['Clearance_Ref_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = Field_Code + "-" + "IPP" + "-" + str(year) + "-" + "0001"
    else:
        substring = str(last_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = Field_Code + "-" + "IPP" + "-" + str(year) + "-" + AppNo
    return newPermitNo


def send_clearance_approve_email(clearance_ref_No, Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Release Form Has Been Approved. Your " \
              "Clearance Reference No is:" + clearance_ref_No + " . "
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def load_import_details(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/import_permit_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location': location})


def load_import_details_agro(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/import_agro_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location': location})


def permit_attachment_plant(request):
    permit_app_no = request.GET.get('applicationNo')
    file_attach = t_file_attachment.objects.filter(application_no=permit_app_no)
    return render(request, 'import_permit/plant_attachment_page.html',
                  {'file_attach': file_attach})


def permit_attachment_agro(request):
    permit_app_no = request.GET.get('applicationNo')
    file_attach = t_file_attachment.objects.filter(application_no=permit_app_no)
    return render(request, 'import_permit/agro_attachment_page.html',
                  {'file_attach': file_attach})


def details_plant(request):
    nursery_app_no = request.GET.get('applicationNo')
    import_details = t_plant_import_permit_t2.objects.filter(Application_No=nursery_app_no)
    return render(request, 'import_permit/import_page_plant.html',
                  {'import': import_details})


def details_agro(request):
    nursery_app_no = request.GET.get('applicationNo')
    import_details = t_plant_import_permit_t2.objects.filter(Application_No=nursery_app_no)
    return render(request, 'import_permit/import_page_agro.html',
                  {'import': import_details})


def plant_import_update(request):
    data = dict()
    Application_No = request.GET.get('application_id')
    regNo = request.POST.get('p_regNo')
    companyName = request.POST.get('p_businessName')
    presentAddress = request.POST.get('p_presentAddress')
    cid = request.POST.get('p_cid_number')
    Name = request.POST.get('p_Name')
    contact_number = request.POST.get('p_contactNo')
    email = request.POST.get('p_email')
    supplier = request.POST.get('p_supplier')
    conveyanceMeans = request.POST.get('p_conveyanceMeans')
    entry_place = request.POST.get('p_entry_point')
    movementPurpose = request.POST.get('p_movementPurpose')
    finalDestination = request.POST.get('p_final_Destination')
    expectedDate = request.POST.get('p_expected_arrival_date')

    details = t_plant_import_permit_t1.objects.filter(Application_No=Application_No)
    details.update(
        License_No=regNo,
        Business_Name=companyName,
        CID=cid,
        Applicant_Name=Name,
        Present_Address=presentAddress,
        Contact_No=contact_number,
        Email=email,
        Name_And_Address_Supplier=supplier,
        Means_of_Conveyance=conveyanceMeans,
        Place_Of_Entry=entry_place,
        Purpose=movementPurpose,
        Final_Destination=finalDestination,
        Import_Inspection_Submit_Date=None,
        Proposed_Inspection_Date=None,
        Actual_Point_Of_Entry=None,
        Inspection_Request_Remarks=None,
        Expected_Arrival_Date=expectedDate,
    )
    data['success'] = "Success"
    return JsonResponse(data)


def agro_import_update(request):
    data = dict()
    Application_No = request.GET.get('application_id')
    a_regNo = request.POST.get('a_regNo')
    a_businessName = request.POST.get('a_businessName')
    a_presentAddress = request.POST.get('a_presentAddress')
    a_cid_number = request.POST.get('a_cid_number')
    a_Name = request.POST.get('a_Name')
    a_contactNo = request.POST.get('a_contactNo')
    a_email = request.POST.get('a_email')
    a_supplier = request.POST.get('a_supplier')
    a_conveyanceMeans = request.POST.get('a_conveyanceMeans')
    a_entry_point = request.POST.get('a_entry_point')
    a_movementPurpose = request.POST.get('a_movementPurpose')
    a_final_Destination = request.POST.get('a_final_Destination')
    a_expected_arrival_date = request.POST.get('a_expected_arrival_date')

    details = t_plant_import_permit_t1.objects.filter(Application_No=Application_No)
    details.update(
        License_No=a_regNo,
        Business_Name=a_businessName,
        CID=a_cid_number,
        Applicant_Name=a_Name,
        Present_Address=a_presentAddress,
        Contact_No=a_contactNo,
        Email=a_email,
        Name_And_Address_Supplier=a_supplier,
        Means_of_Conveyance=a_conveyanceMeans,
        Place_Of_Entry=a_entry_point,
        Purpose=a_movementPurpose,
        Final_Destination=a_final_Destination,
        Expected_Arrival_Date=a_expected_arrival_date,

    )
    data['success'] = "Success"
    return JsonResponse(data)


def update_details_plant(request):
    application_no = request.POST.get('plant_applicationNo')
    record_id = request.POST.get('record_id')
    approved_quantity = request.POST.get('qty_approved')
    qty_balance = request.POST.get('qty_balance')
    remarks = request.POST.get('import_Remarks')
    edit_no = request.POST.get('qty')  # Total Quantity Approved
    import_det = t_plant_import_permit_inspection_t2.objects.filter(pk=record_id)
    if remarks is not None:
        import_det.update(Remarks=remarks)
    else:
        import_det.update(Remarks=None)
    import_det.update(Quantity_Released=approved_quantity)
    import_det.update(Quantity_Balance=qty_balance)
    for import_IPP in import_det:
        Product_Record_Id = import_IPP.Product_Record_Id
        balance = int(import_IPP.Quantity_Balance_1) - int(import_IPP.Quantity_Released)
        product_details = t_plant_import_permit_t2.objects.filter(pk=Product_Record_Id)
        product_details.update(Quantity_Balance=balance)
    application_details = t_plant_import_permit_inspection_t2.objects.filter(Application_No=application_no) \
        .order_by('Record_Id')
    crop = t_plant_crop_master.objects.all()
    variety = t_plant_crop_variety_master.objects.all()
    return render(request, 'import_permit/plant_details.html', {'import': application_details,
                                                                'crop': crop, 'variety': variety})


def update_details_agro(request):
    application_no = request.POST.get('agro_applicationNo')
    record_id = request.POST.get('agro_record_id')
    approved_quantity = request.POST.get('agro_qty_approved')
    agro_qty_balance = request.POST.get('agro_qty_balance')
    remarks = request.POST.get('agro_import_Remarks')
    edit_no = request.POST.get('agro_qty')  # Total Quantity Approved
    import_det = t_plant_import_permit_inspection_t2.objects.filter(pk=record_id)
    if remarks is not None:
        import_det.update(Remarks=remarks)
    else:
        import_det.update(Remarks=None)
    import_det.update(Quantity_Released=approved_quantity)
    import_det.update(Quantity_Balance=agro_qty_balance)
    for import_IPP in import_det:
        Product_Record_Id = import_IPP.Product_Record_Id
        balance = int(import_IPP.Quantity_Balance_1) - int(import_IPP.Quantity_Released)
        product_details = t_plant_import_permit_t2.objects.filter(pk=Product_Record_Id)
        product_details.update(Quantity_Balance=balance)
        import_details_sum = t_plant_import_permit_inspection_t2.objects.filter(
            Product_Record_Id=import_IPP.Product_Record_Id).aggregate(Sum('Quantity_Released'))

        sum_import = import_details_sum['Quantity_Released__sum']

        if sum_import == int(edit_no):
            import_details = t_plant_import_permit_inspection_t1.objects.filter(
                Application_No=application_no)
            for import_det in import_details:
                la_details = t_plant_import_permit_t1.objects.filter(
                    Import_Permit_No=import_det.Import_Permit_No)
                for la in la_details:
                    work_details = t_workflow_details.objects.filter(application_no=la.Application_No)
                    work_details.update(application_status='C')
        else:
            import_details = t_plant_import_permit_inspection_t1.objects.filter(
                Application_No=application_no)
            for import_det in import_details:
                la_details = t_plant_import_permit_t1.objects.filter(
                    Import_Permit_No=import_det.Import_Permit_No)
                for la in la_details:
                    work_details = t_workflow_details.objects.filter(application_no=la.Application_No)
                    work_details.update(application_status='P')
    application_details = t_plant_import_permit_inspection_t2.objects.filter(Application_No=application_no) \
        .order_by('Record_Id')
    pesticide = t_plant_pesticide_master.objects.all()
    return render(request, 'import_permit/agro_details.html', {'import': application_details, 'pesticide': pesticide})


def update_import_permit(request):
    data = dict()
    service_code = "IPP"
    application_no = request.POST.get('applicationNo')

    Applicant_Id = request.session['email']
    importType = request.POST.get('Import_Type')
    Applicant_Type = request.POST.get('Application_Type')
    Nationality = request.POST.get('Nationality_Type')
    if Applicant_Type == "Commercial":
        regNo = request.POST.get('regNo')
        business_name = request.POST.get('business_name')
        commercial_presentAddress = request.POST.get('commercial_presentAddress')
        com_contactNumber = request.POST.get('com_contactNumber')
        com_email = request.POST.get('com_email')
        com_supplier = request.POST.get('com_email')
        Com_Country_Of_Origin = request.POST.get('Com_Country_Of_Origin')
        com_conveyanceMeans = request.POST.get('Com_Country_Of_Origin')
        com_entry_point = request.POST.get('com_entry_point')
        com_movementPurpose = request.POST.get('com_movementPurpose')
        com_final_Destination = request.POST.get('com_final_Destination')
        com_expected_arrival_date = request.POST.get('com_expected_arrival_date')

        import_details = t_plant_import_permit_t1.objects.filter(Application_No=application_no)
        import_details.update(
            Import_Type=importType,
            License_No=regNo,
            Business_Name=business_name,
            CID=None,
            Applicant_Name=None,
            Present_Address=commercial_presentAddress,
            Contact_No=com_contactNumber,
            Email=com_email,
            Name_And_Address_Supplier=com_supplier,
            Means_of_Conveyance=com_conveyanceMeans,
            Place_Of_Entry=com_entry_point,
            Purpose=com_movementPurpose,
            Final_Destination=com_final_Destination,
            Import_Inspection_Submit_Date=None,
            Proposed_Inspection_Date=None,
            Actual_Point_Of_Entry=None,
            Inspection_Request_Remarks=None,
            Import_Permit_No=None,
            Inspection_Date=None,
            Inspection_Type=None,
            Inspection_Time=None,
            Inspection_Leader=None,
            Inspection_Team=None,
            Clearance_Ref_No=None,
            Expected_Arrival_Date=com_expected_arrival_date,
            FO_Remarks=None,
            Inspection_Remarks=None,
            Country_Of_Origin=Com_Country_Of_Origin,
            Application_Date=date.today(),
            Applicant_Id=Applicant_Id,
            Approved_Date=date.today(),
            Validity_Period=None,
            Validity=None,
            Application_Type=Applicant_Type,
            Nationality=None,
            Dzongkhag=None,
            Gewog=None,
            Nationality_Type=None,
            Village=None,
            Passport_Number=None
        )
    else:
        if Nationality == "Bhutanese":
            cid = request.POST.get('p_cid_number')
            Name = request.POST.get('name')
            dzongkhag = request.POST.get('dzongkhag')
            gewog = request.POST.get('gewog')
            village = request.POST.get('village')
            contactNumber = request.POST.get('contactNumber')
            email = request.POST.get('email')
            supplier = request.POST.get('supplier')
            Country_Of_Origin = request.POST.get('Country_Of_Origin')
            conveyanceMeans = request.POST.get('conveyanceMeans')
            entry_point = request.POST.get('entry_point')
            B_movementPurpose = request.POST.get('B_movementPurpose')
            B_finalDestination = request.POST.get('B_final_Destination')
            B_expectedDate = request.POST.get('date_expected')

            import_details = t_plant_import_permit_t1.objects.filter(Application_No=application_no)
            import_details.update(
                Import_Type=importType,
                License_No=None,
                Business_Name=None,
                CID=cid,
                Applicant_Name=Name,
                Present_Address=None,
                Contact_No=contactNumber,
                Email=email,
                Name_And_Address_Supplier=supplier,
                Means_of_Conveyance=conveyanceMeans,
                Place_Of_Entry=entry_point,
                Purpose=B_movementPurpose,
                Final_Destination=B_finalDestination,
                Import_Inspection_Submit_Date=None,
                Proposed_Inspection_Date=None,
                Actual_Point_Of_Entry=None,
                Inspection_Request_Remarks=None,
                Import_Permit_No=None,
                Inspection_Date=None,
                Inspection_Type=None,
                Inspection_Time=None,
                Inspection_Leader=None,
                Inspection_Team=None,
                Clearance_Ref_No=None,
                Expected_Arrival_Date=B_expectedDate,
                FO_Remarks=None,
                Inspection_Remarks=None,
                Country_Of_Origin=Country_Of_Origin,
                Application_Date=None,
                Applicant_Id=Applicant_Id,
                Approved_Date=date.today(),
                Validity_Period=None,
                Validity=None,
                Application_Type=Applicant_Type,
                Nationality=None,
                Dzongkhag=dzongkhag,
                Gewog=gewog,
                Nationality_Type=Nationality,
                Village=village,
                Passport_Number=None
            )
        else:
            passport_name = request.POST.get('passport_name')
            Address = request.POST.get('Address')
            p_email = request.POST.get('p_email')
            p_contactNumber = request.POST.get('p_contactNumber')
            name_supplier = request.POST.get('name_supplier')
            Origin = request.POST.get('Origin')
            p_conveyanceMeans = request.POST.get('p_conveyanceMeans')
            p_entry_point = request.POST.get('p_entry_point')
            p_movementPurpose = request.POST.get('p_movementPurpose')
            p_finalDestination = request.POST.get('p_finalDestination')
            p_expectedDate = request.POST.get('expected_date')
            passport = request.POST.get('passport')
            nationality = request.POST.get('nationality')

            import_details = t_plant_import_permit_t1.objects.filter(Application_No=application_no)
            import_details.update(
                Import_Type=importType,
                License_No=None,
                Business_Name=None,
                CID=None,
                Applicant_Name=passport_name,
                Present_Address=Address,
                Contact_No=p_contactNumber,
                Email=p_email,
                Name_And_Address_Supplier=name_supplier,
                Means_of_Conveyance=p_conveyanceMeans,
                Place_Of_Entry=p_entry_point,
                Purpose=p_movementPurpose,
                Final_Destination=p_finalDestination,
                Import_Inspection_Submit_Date=None,
                Proposed_Inspection_Date=None,
                Actual_Point_Of_Entry=None,
                Inspection_Request_Remarks=None,
                Import_Permit_No=None,
                Inspection_Date=None,
                Inspection_Type=None,
                Inspection_Time=None,
                Inspection_Leader=None,
                Inspection_Team=None,
                Clearance_Ref_No=None,
                Expected_Arrival_Date=p_expectedDate,
                FO_Remarks=None,
                Inspection_Remarks=None,
                Country_Of_Origin=Origin,
                Application_Date=date.today(),
                Applicant_Id=Applicant_Id,
                Approved_Date=None,
                Validity_Period=None,
                Validity=None,
                Application_Type=Applicant_Type,
                Nationality=nationality,
                Dzongkhag=None,
                Gewog=None,
                Nationality_Type=Nationality,
                Village=None,
                Passport_Number=passport
            )
    work_flow_details = t_workflow_details.objects.filter(application_no=application_no)
    work_flow_details.update(applicant_id=request.session['email'],
                             assigned_to=None, field_office_id=None, section='Plant',
                             assigned_role_id='2', action_date=None, application_status='P',
                             service_code=service_code)
    plant_details = t_plant_import_permit_t2.objects.filter(Application_No=application_no)
    if plant_details.exists():
        count = t_plant_import_permit_t2.objects.filter(Application_No=application_no).count()
        data['count'] = count
    else:
        data['count'] = 0
    data['applNo'] = application_no
    data['importType'] = importType
    return JsonResponse(data)


# Export Permit
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apply_export_permit(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        country = t_country_master.objects.all()
        entry_point = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        unit = t_unit_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'export_permit/apply_permit.html',
                      {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                       'location': location, 'entry_point': entry_point, 'country': country, 'count': message_count,
                       'count_call': inspection_call_count, 'consignment_call_count': consignment_call_count,
                       'unit': unit})
    else:
        return render(request, 'redirect_page.html')


def submit_export(request):
    data = dict()
    serviceCode = "EPP"
    lastExportApplication = get_export_application_no(serviceCode)
    Applicant_Type = request.POST.get('Applicant_Type')
    Certificate_Type = request.POST.get('Certificate_Type')
    License_No = request.POST.get('p_License_No')
    CID = request.POST.get('p_cid')
    Exporter_Name = request.POST.get('p_Exporter_Name')
    Exporter_Address = request.POST.get('p_Exporter_Address')
    Contact_No = request.POST.get('p_Contact_No')
    Email = request.POST.get('p_Email')
    Dzongkhag_Code = request.POST.get('p_Dzongkhag_Code')
    Locatipn_Code = request.POST.get('p_Location_Code')
    Consingee_Name_Address = request.POST.get('p_Name_Address')
    Importing_Country = request.POST.get('p_Country_Code')
    Entry_Point = request.POST.get('p_Entry_Point')
    Exit_Point = request.POST.get('p_Exit_Point')
    Packages_No = request.POST.get('p_Package_number')
    Packages_Description = request.POST.get('p_Package_description')
    Distinguishing_Marks = request.POST.get('p_Distinguish_Marks')
    Purpose_End_Use = request.POST.get('p_purpose')
    Mode_Of_Conveyance = request.POST.get('p_conveyanceMeans')
    Name_Of_Conveyance = request.POST.get('p_Conveyance_Name')
    Desired_Inspection_Date = request.POST.get('date_for_Inspection')
    Desired_Inspection_Place = request.POST.get('Desired_Inspection_Place')
    Additional_Declaring = request.POST.get('p_additional_declaration')
    Pre_Application_Treatment = request.POST.get('treatmentType')
    Chemical_Name_Pre = request.POST.get('p_chemcial_name')
    Treatment_Pre = request.POST.get('p_treatment')
    Concentration_Pre = request.POST.get('p_Concentration')
    Duration_Temperature_Pre = request.POST.get('p_Duration_Temperature')
    Treated_By_Pre = request.POST.get('p_treated_by')
    Treated_Supervised_By_Pre = request.POST.get('p_treatment_supervised')
    Additional_Information_Pre = request.POST.get('p_additional_Info')
    Other_Pre = request.POST.get('p_others_treatment')
    Other_Treatment = request.POST.get('p_others')

    C_CID = request.POST.get('c_cid')
    C_Exporter_Name = request.POST.get('c_Exporter_Name')
    C_Contact_No = request.POST.get('c_Contact_No')
    C_Email = request.POST.get('c_Email')
    C_Dzongkhag_Code = request.POST.get('c_Dzongkhag_Code')
    C_Locatipn_Code = request.POST.get('c_Location_Code')
    c_current_address = request.POST.get('c_current_address')
    c_permanent_address = request.POST.get('c_permanent_address')
    c_License_No = request.POST.get('c_License_No')
    gross_weight_gms = request.POST.get('gross_weight_gms')
    gross_weight_pieces = request.POST.get('gross_weight_pieces')
    net_weight_gms = request.POST.get('net_weight_gms')
    net_weight_pieces = request.POST.get('net_weight_pieces')
    c_package = request.POST.get('c_package')
    c_country = request.POST.get('c_country')
    c_Name_Address = request.POST.get('c_Name_Address')
    c_conveyanceMeans = request.POST.get('c_conveyanceMeans')
    Applicant_Id = request.session['email']
    retail_gross_weight_gms = request.POST.get('retail_gross_weight_gms')
    retail_gross_weight_pieces = request.POST.get('retail_gross_weight_pieces')
    retail_net_weight_gms = request.POST.get('retail_net_weight_gms')
    retail_net_weight_pieces = request.POST.get('retail_net_weight_pieces')
    c_retail_package = request.POST.get('c_retail_package')
    c_outlet_name = request.POST.get('c_outlet_name')
    c_phoneNumber = request.POST.get('c_phoneNumber')
    c_address = request.POST.get('c_address')
    if Certificate_Type == 'P':
        t_plant_export_certificate_plant_plant_products_t1.objects.create(
            Application_No=lastExportApplication,
            Applicant_Type=None,
            Certificate_Type=Certificate_Type,
            License_No=License_No,
            CID=CID,
            Exporter_Name=Exporter_Name,
            Exporter_Address=Exporter_Address,
            Permanent_Address=None,
            Contact_No=Contact_No,
            Email=Email,
            Dzongkhag_Code=Dzongkhag_Code,
            Locatipn_Code=Locatipn_Code,
            Consingee_Name_Address=Consingee_Name_Address,
            Pieces_Net=None,
            Importing_Country=Importing_Country,
            Entry_Point=Entry_Point,
            Exit_Point=Exit_Point,
            Packages_No=Packages_No,
            Packages_Description=Packages_Description,
            Distinguishing_Marks=Distinguishing_Marks,
            Purpose_End_Use=Purpose_End_Use,
            Mode_Of_Conveyance=Mode_Of_Conveyance,
            Name_Of_Conveyance=Name_Of_Conveyance,
            Departure_Date=None,
            Desired_Inspection_Date=None,
            Desired_Inspection_Place=None,
            Additional_Declaring=Additional_Declaring,
            Outlet_name=None,
            Outlet_Contact_No=None,
            Outlet_Address=None,
            Inspection_Date=None,
            Sample_Drawn_By=None,
            Sample_Inspected_By=None,
            Sample_Drawn=None,
            Sample_Size=None,
            Inspection_Method=None,
            Inspection_Method_Other=None,
            Pest_Detected=None,
            Pest_Insect=None,
            Pest_Mite=None,
            Pest_Fungi=None,
            Pest_Bacteria=None,
            Pest_Virus=None,
            Pest_Nematode=None,
            Pest_Weed=None,
            Pest_Scientific_Name=None,
            Infestation_Level=None,
            Pest_Status=None,
            Pest_Risk_Category=None,
            Pest_QR_Detected=None,
            Pest_QR_Comment=None,
            Treatment_Possible=None,
            Treatment_Comment=None,
            Phytosanitary_Measures=None,
            Phytosanitary_Measures_Comment=None,
            Treatment_Chemical_Name=None,
            Treatment_Chemical_Fumigation=None,
            Treatment_Chemical_Spray=None,
            Treatment_Chemical_Seed=None,
            Treatment_Chemical_Other=None,
            Treatment_Chemical_Other_Specific=None,
            Treatment_Chemical_Concentration=None,
            Treatment_Chemical_Duration=None,
            Treatment_Chemical_Treated_By=None,
            Treatment_Chemical_Additional_Info=None,
            Treatment_Irradiation=None,
            Treatment_Hot_Water=None,
            Treatment_Dry_Heat=None,
            Treatment_Vapour_Heat=None,
            Treatment_Cold_Treatment=None,
            Feasibility_Status=None,
            Export_Permit=None,
            Additional_Information_Pre=Additional_Information_Pre,
            Chemical_Name_Pre=Chemical_Name_Pre,
            Concentration_Pre=Concentration_Pre,
            Duration_Temperature_Pre=Duration_Temperature_Pre,
            Pre_Application_Treatment=Pre_Application_Treatment,
            Treated_By_Pre=Treated_By_Pre,
            Treated_Supervised_By_Pre=Treated_Supervised_By_Pre,
            Treatment_Pre=Treatment_Pre,
            Other_Pre=Other_Pre,
            Other_Treatment=Other_Treatment,
            Application_Date=date.today(),
            Applicant_Id=Applicant_Id,
        )
        field_id = t_location_field_office_mapping.objects.filter(pk=Locatipn_Code)
        for field_office in field_id:
            field_office_id = field_office.Field_Office_Id_id
        t_workflow_details.objects.create(application_no=lastExportApplication, applicant_id=request.session['email'],
                                          assigned_to=None, field_office_id=field_office_id, section='Plant',
                                          assigned_role_id='4', action_date=None, application_status='P',
                                          service_code=serviceCode)
    else:
        if Applicant_Type == "directRadio":
            t_plant_export_certificate_plant_plant_products_t1.objects.create(
                Application_No=lastExportApplication,
                Applicant_Type=Applicant_Type,
                Certificate_Type=Certificate_Type,
                License_No=c_License_No,
                CID=C_CID,
                Exporter_Name=C_Exporter_Name,
                Exporter_Address=c_current_address,
                Permanent_Address=c_permanent_address,
                Contact_No=C_Contact_No,
                Email=C_Email,
                Dzongkhag_Code=C_Dzongkhag_Code,
                Locatipn_Code=C_Locatipn_Code,
                Consingee_Name_Address=c_Name_Address,
                Qty_Gross=gross_weight_gms,
                Unit_Gross="Gm(s)",
                Pieces_Gross=gross_weight_pieces,
                Qty_Net=net_weight_gms,
                Unit_Net="Gm(s)",
                Pieces_Net=net_weight_pieces,
                Importing_Country=c_country,
                Entry_Point=None,
                Packages_No=c_package,
                Packages_Description=None,
                Distinguishing_Marks=None,
                Purpose_End_Use=None,
                Mode_Of_Conveyance=c_conveyanceMeans,
                Name_Of_Conveyance=None,
                Departure_Date=None,
                Desired_Inspection_Date=Desired_Inspection_Date,
                Desired_Inspection_Place=Desired_Inspection_Place,
                Additional_Declaring=None,
                Outlet_name=None,
                Outlet_Contact_No=None,
                Outlet_Address=None,
                Inspection_Date=None,
                Sample_Drawn_By=None,
                Sample_Inspected_By=None,
                Sample_Drawn=None,
                Sample_Size=None,
                Inspection_Method=None,
                Inspection_Method_Other=None,
                Pest_Detected=None,
                Pest_Insect=None,
                Pest_Mite=None,
                Pest_Fungi=None,
                Pest_Bacteria=None,
                Pest_Virus=None,
                Pest_Nematode=None,
                Pest_Weed=None,
                Pest_Scientific_Name=None,
                Infestation_Level=None,
                Pest_Status=None,
                Pest_Risk_Category=None,
                Pest_QR_Detected=None,
                Pest_QR_Comment=None,
                Treatment_Possible=None,
                Treatment_Comment=None,
                Phytosanitary_Measures=None,
                Phytosanitary_Measures_Comment=None,
                Treatment_Chemical_Name=None,
                Treatment_Chemical_Fumigation=None,
                Treatment_Chemical_Spray=None,
                Treatment_Chemical_Seed=None,
                Treatment_Chemical_Other=None,
                Treatment_Chemical_Other_Specific=None,
                Treatment_Chemical_Concentration=None,
                Treatment_Chemical_Duration=None,
                Treatment_Chemical_Treated_By=None,
                Treatment_Chemical_Additional_Info=None,
                Treatment_Irradiation=None,
                Treatment_Hot_Water=None,
                Treatment_Dry_Heat=None,
                Treatment_Vapour_Heat=None,
                Treatment_Cold_Treatment=None,
                Feasibility_Status=None,
                Export_Permit=None,
                Additional_Information_Pre=None,
                Chemical_Name_Pre=None,
                Concentration_Pre=None,
                Duration_Temperature_Pre=None,
                Pre_Application_Treatment=None,
                Treated_By_Pre=None,
                Treated_Supervised_By_Pre=None,
                Treatment_Pre=None,
                Other_Pre=None,
                Other_Treatment=None,
                Application_Date=date.today(),
                Applicant_Id=Applicant_Id,
            )
        else:
            t_plant_export_certificate_plant_plant_products_t1.objects.create(
                Application_No=lastExportApplication,
                Applicant_Type=Applicant_Type,
                Certificate_Type=Certificate_Type,
                License_No=c_License_No,
                CID=C_CID,
                Exporter_Name=C_Exporter_Name,
                Exporter_Address=c_current_address,
                Permanent_Address=c_permanent_address,
                Contact_No=C_Contact_No,
                Email=C_Email,
                Dzongkhag_Code=C_Dzongkhag_Code,
                Locatipn_Code=C_Locatipn_Code,
                Consingee_Name_Address=c_Name_Address,
                Qty_Gross=retail_gross_weight_gms,
                Unit_Gross="Gm(s)",
                Pieces_Gross=retail_gross_weight_pieces,
                Qty_Net=retail_net_weight_gms,
                Unit_Net="Gm(s)",
                Pieces_Net=retail_net_weight_pieces,
                Importing_Country=None,
                Entry_Point=None,
                Packages_No=c_retail_package,
                Packages_Description=None,
                Distinguishing_Marks=None,
                Purpose_End_Use=None,
                Mode_Of_Conveyance=None,
                Name_Of_Conveyance=None,
                Departure_Date=None,
                Desired_Inspection_Date=Desired_Inspection_Date,
                Desired_Inspection_Place=Desired_Inspection_Place,
                Additional_Declaring=None,
                Outlet_name=c_outlet_name,
                Outlet_Contact_No=c_phoneNumber,
                Outlet_Address=c_address,
                Inspection_Date=None,
                Sample_Drawn_By=None,
                Sample_Inspected_By=None,
                Sample_Drawn=None,
                Sample_Size=None,
                Inspection_Method=None,
                Inspection_Method_Other=None,
                Pest_Detected=None,
                Pest_Insect=None,
                Pest_Mite=None,
                Pest_Fungi=None,
                Pest_Bacteria=None,
                Pest_Virus=None,
                Pest_Nematode=None,
                Pest_Weed=None,
                Pest_Scientific_Name=None,
                Infestation_Level=None,
                Pest_Status=None,
                Pest_Risk_Category=None,
                Pest_QR_Detected=None,
                Pest_QR_Comment=None,
                Treatment_Possible=None,
                Treatment_Comment=None,
                Phytosanitary_Measures=None,
                Phytosanitary_Measures_Comment=None,
                Treatment_Chemical_Name=None,
                Treatment_Chemical_Fumigation=None,
                Treatment_Chemical_Spray=None,
                Treatment_Chemical_Seed=None,
                Treatment_Chemical_Other=None,
                Treatment_Chemical_Other_Specific=None,
                Treatment_Chemical_Concentration=None,
                Treatment_Chemical_Duration=None,
                Treatment_Chemical_Treated_By=None,
                Treatment_Chemical_Additional_Info=None,
                Treatment_Irradiation=None,
                Treatment_Hot_Water=None,
                Treatment_Dry_Heat=None,
                Treatment_Vapour_Heat=None,
                Treatment_Cold_Treatment=None,
                Feasibility_Status=None,
                Export_Permit=None,
                Additional_Information_Pre=None,
                Chemical_Name_Pre=None,
                Concentration_Pre=None,
                Duration_Temperature_Pre=None,
                Pre_Application_Treatment=None,
                Treated_By_Pre=None,
                Treated_Supervised_By_Pre=None,
                Treatment_Pre=None,
                Other_Pre=None,
                Other_Treatment=None,
                Application_Date=date.today(),
                Applicant_Id=Applicant_Id,
            )
        field_id = t_location_field_office_mapping.objects.filter(pk=C_Locatipn_Code)
        for field_office in field_id:
            field_office_id = field_office.Field_Office_Id_id
        t_workflow_details.objects.create(application_no=lastExportApplication, applicant_id=request.session['email'],
                                          assigned_to=None, field_office_id=field_office_id, section='Plant',
                                          assigned_role_id='4', action_date=None, application_status='P',
                                          service_code=serviceCode)
    data['applicationNo'] = lastExportApplication
    return JsonResponse(data)


def get_export_application_no(serviceCode):
    last_export_application_no = t_plant_export_certificate_plant_plant_products_t1.objects.aggregate(
        Max('Application_No'))
    last_application_no = last_export_application_no['Application_No__max']
    if not last_application_no:
        year = timezone.now().year
        newApplicationNo = serviceCode + "-" + str(year) + "-" + "0001"
    else:
        substring = str(last_application_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newApplicationNo = serviceCode + "-" + str(year) + "-" + AppNo
    return newApplicationNo


def add_file_phyto(request):
    data = dict()
    myFile = request.FILES['phyto_document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/export_permit")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/export_permit" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def add_file_name_phyto(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)
        file_attach = t_file_attachment.objects.filter(application_no=app_no)
    return render(request, 'export_permit/phyto_file_attachment_page.html', {'file_attach': file_attach})


def add_file_cordyceps(request):
    data = dict()
    myFile = request.FILES['cordyceps_document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/export_permit")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/export_permit" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def add_file_name_cordyceps(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
    return render(request, 'export_permit/cordyceps_file_attachment_page.html', {'file_attach': file_attach})


def delete_file_phyto(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    print(File_Id)
    print(Application_No)

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/export_permit")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'export_permit/phyto_file_attachment_page.html', {'file_attach': file_attach})


def delete_file_export(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/export_permit")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'export_permit/cordyceps_file_attachment_page.html', {'file_attach': file_attach})


def get_export_permit_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_export_permit = t_plant_export_certificate_plant_plant_products_t1.objects.aggregate(Max('Export_Permit'))
    last_export_permit_no = last_export_permit['Export_Permit__max']
    if not last_export_permit_no:
        year = timezone.now().year
        new_export_permit = Field_Code + "-" + "EPP" + "-" + str(year) + "-" + "0001"
    else:
        substring = str(last_export_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        new_export_permit = Field_Code + "-" + "EPP" + "-" + str(year) + "-" + AppNo
    return new_export_permit


def update_export(request):
    data = dict()
    serviceCode = "EPP"
    lastExportApplication = request.POST.get('applicationNo')
    Applicant_Type = request.POST.get('Applicant_Type')
    Certificate_Type = request.POST.get('Certificate_Type')
    License_No = request.POST.get('p_License_No')
    CID = request.POST.get('p_cid')
    Exporter_Name = request.POST.get('p_Exporter_Name')
    Exporter_Address = request.POST.get('p_Exporter_Address')
    Contact_No = request.POST.get('p_Contact_No')
    Email = request.POST.get('p_Email')
    Dzongkhag_Code = request.POST.get('p_Dzongkhag_Code')
    Locatipn_Code = request.POST.get('p_Location_Code')
    Consingee_Name_Address = request.POST.get('p_Name_Address')
    Importing_Country = request.POST.get('p_Country_Code')
    Entry_Point = request.POST.get('p_Entry_Point')
    Packages_No = request.POST.get('p_Package_number')
    Packages_Description = request.POST.get('p_Package_description')
    Distinguishing_Marks = request.POST.get('p_Distinguish_Marks')
    Purpose_End_Use = request.POST.get('p_purpose')
    Mode_Of_Conveyance = request.POST.get('p_conveyanceMeans')
    Name_Of_Conveyance = request.POST.get('p_Conveyance_Name')
    Desired_Inspection_Date = request.POST.get('date_for_Inspection')
    Desired_Inspection_Place = request.POST.get('requested_place')
    Additional_Declaring = request.POST.get('p_additional_declaration')
    Pre_Application_Treatment = request.POST.get('treatmentType')
    Chemical_Name_Pre = request.POST.get('p_chemcial_name')
    Treatment_Pre = request.POST.get('p_treatment')
    Concentration_Pre = request.POST.get('p_Concentration')
    Duration_Temperature_Pre = request.POST.get('p_Duration_Temperature')
    Treated_By_Pre = request.POST.get('p_treated_by')
    Treated_Supervised_By_Pre = request.POST.get('p_treatment_supervised')
    Additional_Information_Pre = request.POST.get('p_additional_Info')
    Other_Pre = request.POST.get('p_others_treatment')
    Other_Treatment = request.POST.get('p_others')

    C_CID = request.POST.get('c_cid')
    C_Exporter_Name = request.POST.get('c_Exporter_Name')
    C_Contact_No = request.POST.get('c_Contact_No')
    C_Email = request.POST.get('c_Email')
    C_Dzongkhag_Code = request.POST.get('c_Dzongkhag_Code')
    C_Locatipn_Code = request.POST.get('c_Location_Code')
    c_current_address = request.POST.get('c_current_address')
    c_permanent_address = request.POST.get('c_permanent_address')
    c_License_No = request.POST.get('c_License_No')
    gross_weight_gms = request.POST.get('gross_weight_gms')
    gross_weight_pieces = request.POST.get('gross_weight_pieces')
    net_weight_gms = request.POST.get('net_weight_gms')
    net_weight_pieces = request.POST.get('net_weight_pieces')
    c_package = request.POST.get('c_package')
    c_country = request.POST.get('c_country')
    c_Name_Address = request.POST.get('c_Name_Address')
    c_conveyanceMeans = request.POST.get('c_conveyanceMeans')
    Applicant_Id = request.session['email']
    retail_gross_weight_gms = request.POST.get('retail_gross_weight_gms')
    retail_gross_weight_pieces = request.POST.get('retail_gross_weight_pieces')
    retail_net_weight_gms = request.POST.get('retail_net_weight_gms')
    retail_net_weight_pieces = request.POST.get('retail_net_weight_pieces')
    c_retail_package = request.POST.get('c_retail_package')
    c_outlet_name = request.POST.get('c_outlet_name')
    c_phoneNumber = request.POST.get('c_phoneNumber')
    c_address = request.POST.get('c_address')
    if Certificate_Type == 'P':
        export_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
            Application_No=lastExportApplication)
        export_details.update(
            Applicant_Type=None,
            Certificate_Type=Certificate_Type,
            License_No=License_No,
            CID=CID,
            Exporter_Name=Exporter_Name,
            Exporter_Address=Exporter_Address,
            Permanent_Address=None,
            Contact_No=Contact_No,
            Email=Email,
            Dzongkhag_Code=Dzongkhag_Code,
            Locatipn_Code=Locatipn_Code,
            Consingee_Name_Address=Consingee_Name_Address,
            Pieces_Net=None,
            Importing_Country=Importing_Country,
            Entry_Point=Entry_Point,
            Packages_No=Packages_No,
            Packages_Description=Packages_Description,
            Distinguishing_Marks=Distinguishing_Marks,
            Purpose_End_Use=Purpose_End_Use,
            Mode_Of_Conveyance=Mode_Of_Conveyance,
            Name_Of_Conveyance=Name_Of_Conveyance,
            Departure_Date=None,
            Desired_Inspection_Date=None,
            Desired_Inspection_Place=None,
            Additional_Declaring=Additional_Declaring,
            Outlet_name=None,
            Outlet_Contact_No=None,
            Outlet_Address=None,
            Inspection_Date=None,
            Sample_Drawn_By=None,
            Sample_Inspected_By=None,
            Sample_Drawn=None,
            Sample_Size=None,
            Inspection_Method=None,
            Inspection_Method_Other=None,
            Pest_Detected=None,
            Pest_Insect=None,
            Pest_Mite=None,
            Pest_Fungi=None,
            Pest_Bacteria=None,
            Pest_Virus=None,
            Pest_Nematode=None,
            Pest_Weed=None,
            Pest_Scientific_Name=None,
            Infestation_Level=None,
            Pest_Status=None,
            Pest_Risk_Category=None,
            Pest_QR_Detected=None,
            Pest_QR_Comment=None,
            Treatment_Possible=None,
            Treatment_Comment=None,
            Phytosanitary_Measures=None,
            Phytosanitary_Measures_Comment=None,
            Treatment_Chemical_Name=None,
            Treatment_Chemical_Fumigation=None,
            Treatment_Chemical_Spray=None,
            Treatment_Chemical_Seed=None,
            Treatment_Chemical_Other=None,
            Treatment_Chemical_Other_Specific=None,
            Treatment_Chemical_Concentration=None,
            Treatment_Chemical_Duration=None,
            Treatment_Chemical_Treated_By=None,
            Treatment_Chemical_Additional_Info=None,
            Treatment_Irradiation=None,
            Treatment_Hot_Water=None,
            Treatment_Dry_Heat=None,
            Treatment_Vapour_Heat=None,
            Treatment_Cold_Treatment=None,
            Feasibility_Status=None,
            Export_Permit=None,
            Additional_Information_Pre=Additional_Information_Pre,
            Chemical_Name_Pre=Chemical_Name_Pre,
            Concentration_Pre=Concentration_Pre,
            Duration_Temperature_Pre=Duration_Temperature_Pre,
            Pre_Application_Treatment=Pre_Application_Treatment,
            Treated_By_Pre=Treated_By_Pre,
            Treated_Supervised_By_Pre=Treated_Supervised_By_Pre,
            Treatment_Pre=Treatment_Pre,
            Other_Pre=Other_Pre,
            Other_Treatment=Other_Treatment,
            Application_Date=date.today(),
            Applicant_Id=Applicant_Id,
        )
        field_id = t_location_field_office_mapping.objects.filter(pk=Locatipn_Code)
        for field_office in field_id:
            field_office_id = field_office.Field_Office_Id_id
    else:
        if Applicant_Type == "":
            export_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
                Application_No=lastExportApplication)
            export_details.update(
                Applicant_Type=Applicant_Type,
                Certificate_Type=Certificate_Type,
                License_No=c_License_No,
                CID=C_CID,
                Exporter_Name=C_Exporter_Name,
                Exporter_Address=c_current_address,
                Permanent_Address=c_permanent_address,
                Contact_No=C_Contact_No,
                Email=C_Email,
                Dzongkhag_Code=C_Dzongkhag_Code,
                Locatipn_Code=C_Locatipn_Code,
                Consingee_Name_Address=c_Name_Address,
                Botanical_Name=None,
                Description=None,
                Qty_Gross=gross_weight_gms,
                Unit_Gross="Gm(s)",
                Pieces_Gross=gross_weight_pieces,
                Qty_Net=net_weight_gms,
                Unit_Net="Gm(s)",
                Pieces_Net=net_weight_pieces,
                Importing_Country=c_country,
                Entry_Point=None,
                Packages_No=c_package,
                Packages_Description=None,
                Distinguishing_Marks=None,
                Purpose_End_Use=None,
                Mode_Of_Conveyance=c_conveyanceMeans,
                Name_Of_Conveyance=None,
                Departure_Date=None,
                Desired_Inspection_Date=None,
                Desired_Inspection_Place=None,
                Additional_Declaring=None,
                Outlet_name=None,
                Outlet_Contact_No=None,
                Outlet_Address=None,
                Inspection_Date=None,
                Sample_Drawn_By=None,
                Sample_Inspected_By=None,
                Sample_Drawn=None,
                Sample_Size=None,
                Inspection_Method=None,
                Inspection_Method_Other=None,
                Pest_Detected=None,
                Pest_Insect=None,
                Pest_Mite=None,
                Pest_Fungi=None,
                Pest_Bacteria=None,
                Pest_Virus=None,
                Pest_Nematode=None,
                Pest_Weed=None,
                Pest_Scientific_Name=None,
                Infestation_Level=None,
                Pest_Status=None,
                Pest_Risk_Category=None,
                Pest_QR_Detected=None,
                Pest_QR_Comment=None,
                Treatment_Possible=None,
                Treatment_Comment=None,
                Phytosanitary_Measures=None,
                Phytosanitary_Measures_Comment=None,
                Treatment_Chemical_Name=None,
                Treatment_Chemical_Fumigation=None,
                Treatment_Chemical_Spray=None,
                Treatment_Chemical_Seed=None,
                Treatment_Chemical_Other=None,
                Treatment_Chemical_Other_Specific=None,
                Treatment_Chemical_Concentration=None,
                Treatment_Chemical_Duration=None,
                Treatment_Chemical_Treated_By=None,
                Treatment_Chemical_Additional_Info=None,
                Treatment_Irradiation=None,
                Treatment_Hot_Water=None,
                Treatment_Dry_Heat=None,
                Treatment_Vapour_Heat=None,
                Treatment_Cold_Treatment=None,
                Feasibility_Status=None,
                Export_Permit=None,
                Additional_Information_Pre=None,
                Chemical_Name_Pre=None,
                Concentration_Pre=None,
                Duration_Temperature_Pre=None,
                Pre_Application_Treatment=None,
                Treated_By_Pre=None,
                Treated_Supervised_By_Pre=None,
                Treatment_Pre=None,
                Other_Pre=None,
                Other_Treatment=None,
                Application_Date=date.today(),
                Applicant_Id=Applicant_Id,
                Common_Name=None
            )
        else:
            export_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
                Application_No=lastExportApplication)
            export_details.update(
                Applicant_Type=Applicant_Type,
                Certificate_Type=Certificate_Type,
                License_No=c_License_No,
                CID=C_CID,
                Exporter_Name=C_Exporter_Name,
                Exporter_Address=c_current_address,
                Permanent_Address=c_permanent_address,
                Contact_No=C_Contact_No,
                Email=C_Email,
                Dzongkhag_Code=C_Dzongkhag_Code,
                Locatipn_Code=C_Locatipn_Code,
                Consingee_Name_Address=c_Name_Address,
                Botanical_Name=None,
                Description=None,
                Qty_Gross=retail_gross_weight_gms,
                Unit_Gross="Gm(s)",
                Pieces_Gross=retail_gross_weight_pieces,
                Qty_Net=retail_net_weight_gms,
                Unit_Net="Gm(s)",
                Pieces_Net=retail_net_weight_pieces,
                Importing_Country=None,
                Entry_Point=None,
                Packages_No=c_retail_package,
                Packages_Description=None,
                Distinguishing_Marks=None,
                Purpose_End_Use=None,
                Mode_Of_Conveyance=None,
                Name_Of_Conveyance=None,
                Departure_Date=None,
                Desired_Inspection_Date=None,
                Desired_Inspection_Place=None,
                Additional_Declaring=None,
                Outlet_name=c_outlet_name,
                Outlet_Contact_No=c_phoneNumber,
                Outlet_Address=c_address,
                Inspection_Date=None,
                Sample_Drawn_By=None,
                Sample_Inspected_By=None,
                Sample_Drawn=None,
                Sample_Size=None,
                Inspection_Method=None,
                Inspection_Method_Other=None,
                Pest_Detected=None,
                Pest_Insect=None,
                Pest_Mite=None,
                Pest_Fungi=None,
                Pest_Bacteria=None,
                Pest_Virus=None,
                Pest_Nematode=None,
                Pest_Weed=None,
                Pest_Scientific_Name=None,
                Infestation_Level=None,
                Pest_Status=None,
                Pest_Risk_Category=None,
                Pest_QR_Detected=None,
                Pest_QR_Comment=None,
                Treatment_Possible=None,
                Treatment_Comment=None,
                Phytosanitary_Measures=None,
                Phytosanitary_Measures_Comment=None,
                Treatment_Chemical_Name=None,
                Treatment_Chemical_Fumigation=None,
                Treatment_Chemical_Spray=None,
                Treatment_Chemical_Seed=None,
                Treatment_Chemical_Other=None,
                Treatment_Chemical_Other_Specific=None,
                Treatment_Chemical_Concentration=None,
                Treatment_Chemical_Duration=None,
                Treatment_Chemical_Treated_By=None,
                Treatment_Chemical_Additional_Info=None,
                Treatment_Irradiation=None,
                Treatment_Hot_Water=None,
                Treatment_Dry_Heat=None,
                Treatment_Vapour_Heat=None,
                Treatment_Cold_Treatment=None,
                Feasibility_Status=None,
                Export_Permit=None,
                Additional_Information_Pre=None,
                Chemical_Name_Pre=None,
                Concentration_Pre=None,
                Duration_Temperature_Pre=None,
                Pre_Application_Treatment=None,
                Treated_By_Pre=None,
                Treated_Supervised_By_Pre=None,
                Treatment_Pre=None,
                Other_Pre=None,
                Other_Treatment=None,
                Application_Date=date.today(),
                Applicant_Id=Applicant_Id,
                Common_Name=None
            )
        field_id = t_location_field_office_mapping.objects.filter(pk=C_Locatipn_Code)
        for field_office in field_id:
            field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(application_no=lastExportApplication, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=field_office_id, section='Plant',
                                      assigned_role_id='4', action_date=None, application_status='P',
                                      service_code=serviceCode)
    data['applicationNo'] = lastExportApplication
    return JsonResponse(data)


def save_phyto_export_details(request):
    application_no = request.GET.get('application_no')
    botanical_name = request.GET.get('p_Botanical_Name')
    common_name = request.GET.get('p_Common_Name')
    description = request.GET.get('p_Description')
    quantity = request.GET.get('quantity')
    unit = request.GET.get('unit')
    gross_weight = request.GET.get('gross_weight')
    net_weight = request.GET.get('net_weight')

    t_plant_export_certificate_plant_plant_products_t2.objects.create(Application_No=application_no,
                                                                      Botanical_Name=botanical_name,
                                                                      Common_Name=common_name, Description=description,
                                                                      Quantity=quantity, Unit=unit,
                                                                      Gross_Weight=gross_weight,
                                                                      Net_Weight=net_weight)
    export_details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(
        Application_No=application_no).order_by('Record_Id')
    count = t_plant_export_certificate_plant_plant_products_t2.objects.filter(Application_No=application_no).count()
    return render(request, 'export_permit/phyto_details_page.html', {'export_details': export_details,
                                                                     'export_count': count})


def update_pec_details(request):
    record_id = request.POST.get('record_id')
    application_no = request.POST.get('edit_application_no')
    gross_weight = request.POST.get('edit_gross_weight')
    net_weight = request.POST.get('edit_net_weight')

    plant_export_details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(Record_Id=record_id)
    plant_export_details.update(Gross_Weight=gross_weight,
                                Net_Weight=net_weight)
    export_details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(
        Application_No=application_no).order_by('Record_Id')
    return render(request, 'export_permit/phyto_ins_details.html', {'export_details': export_details})


def export_complete(request):
    export_permit = get_export_permit_no(request)
    Application_No = request.POST.get('appNo')
    Inspection_Date = request.POST.get('date')
    no_of_sample_drawn = request.POST.get('no_of_sample_drawn')
    total_sample_size = request.POST.get('total_sample_size')
    sample_drawn_by = request.POST.get('sample_drawn_by')
    inspection_method = request.POST.getlist('inspection_method')
    pest_detected = request.POST.get('pest_detected')
    pest_category = request.POST.get('pest_category')
    certificate_type = request.POST.get('certificate_type')
    infestation_level = request.POST.get('infestation_level')
    live_dead = request.POST.get('live_dead')
    risk_category = request.POST.get('risk_category')
    remarks = request.POST.get('remarks')
    inspection_method_other = request.POST.get('inspection_method_other')
    Pest_QR_Detected = request.POST.get('Pest_QR_Detected')
    Pest_QR_Detected_Comments = request.POST.get('Pest_QR_Detected_Comments')
    treatment_possible = request.POST.get('treatment_possible')
    Treatment_Comment = request.POST.get('Treatment_Comment')
    Pest_Scientific_Name = request.POST.get('Scientific_Name')
    Laboratory_Analysis_Required = request.POST.get('Laboratory_Analysis_Required')
    Laboratory_Analysis_Comment = request.POST.get('analysis_Comment')
    Phytosanitary_Measures = request.POST.get('Phytosanitary_Measures')
    Phytosanitary_Measures_Comment = request.POST.get('phytosanitary_Comment')
    additional_Info = request.POST.get('additional_Info')
    treated_by = request.POST.get('treated_by')
    Duration_Temperature = request.POST.get('Duration_Temperature')
    Concentration = request.POST.get('Concentration')
    treatment = request.POST.get('treatment')
    chemcial_name = request.POST.get('chemical_name')
    others_treatment = request.POST.get('others_treatment')
    treatmentType = request.POST.get('treatmentType')
    C_Inspection_Date = request.POST.get('c_dateOfInspection')
    c_remarks = request.POST.get('c_remarks')
    print(pest_detected)
    if certificate_type == 'P':
        if pest_detected == 'Yes':
            application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
                Application_No=Application_No)
            application_details.update(Inspection_Date=Inspection_Date,
                                       Sample_Drawn_By=sample_drawn_by,
                                       Sample_Inspected_By=None,
                                       Sample_Drawn=no_of_sample_drawn,
                                       Sample_Size=total_sample_size,
                                       Inspection_Method=inspection_method,
                                       Inspection_Method_Other=inspection_method_other,
                                       Pest_Detected=pest_detected,
                                       Pest_Scientific_Name=Pest_Scientific_Name,
                                       Infestation_Level=infestation_level,
                                       Pest_Status=live_dead,
                                       Pest_Risk_Category=risk_category,
                                       Pest_QR_Detected=Pest_QR_Detected,
                                       Pest_QR_Comment=Pest_QR_Detected_Comments,
                                       Treatment_Possible=treatment_possible,
                                       Treatment_Comment=Treatment_Comment,
                                       Laboratory_Analysis_Required=Laboratory_Analysis_Required,
                                       Laboratory_Analysis_Comment=Laboratory_Analysis_Comment,
                                       Phytosanitary_Measures=Phytosanitary_Measures,
                                       Phytosanitary_Measures_Comment=Phytosanitary_Measures_Comment,
                                       Inspection_Remarks=remarks,
                                       Export_Permit=export_permit,
                                       Approved_Date=date.today()
                                       )
            if pest_category == "Insect":
                application_details.update(Pest_Insect=pest_category)
            elif pest_category == "Mite":
                application_details.update(Pest_Mite=pest_category)
            elif pest_category == "Fungi":
                application_details.update(Pest_Fungi=pest_category)
            elif pest_category == "Bacteria":
                application_details.update(Pest_Bacteria=pest_category)
            elif pest_category == "Virus":
                application_details.update(Pest_Virus=pest_category)
            elif pest_category == "Nematode":
                application_details.update(Pest_Nematode=pest_category)
            elif pest_category == "Weed":
                application_details.update(Pest_Weed=pest_category)

            if treatment_possible == "Yes":
                if treatmentType == "Chemical":
                    application_details.update(Treatment_Chemical=treatmentType)
                    application_details.update(Treatment_Chemical_Name=chemcial_name)
                    if treatment == "Fumigation":
                        application_details.update(Treatment_Chemical_Fumigation=treatment)
                    elif treatment == "Spray":
                        application_details.update(Treatment_Chemical_Spray=treatment)
                    elif treatment == "Seed treatment":
                        application_details.update(Treatment_Chemical_Seed=treatment)
                    elif treatment == "others":
                        application_details.update(Treatment_Chemical_Other=treatment)
                        application_details.update(Treatment_Chemical_Other_Specific=others_treatment)
                    application_details.update(Treatment_Chemical_Concentration=Concentration)
                    application_details.update(Treatment_Chemical_Duration=Duration_Temperature)
                    application_details.update(Treatment_Chemical_Treated_By=treated_by)
                    application_details.update(Treatment_Chemical_Additional_Info=additional_Info)
                elif treatmentType == "Irradiation":
                    application_details.update(Treatment_Irradiation=treatmentType)
                elif treatmentType == "Hot Water":
                    application_details.update(Treatment_Hot_Water=treatmentType)
                elif treatmentType == "Dry Heat":
                    application_details.update(Treatment_Dry_Heat=treatmentType)
                elif treatmentType == "Vapour Heat":
                    application_details.update(Treatment_Vapour_Heat=treatmentType)
                elif treatmentType == "Cold Treatment":
                    application_details.update(Treatment_Cold_Treatment=treatmentType)
        else:
            application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
                Application_No=Application_No)
            application_details.update(Inspection_Date=Inspection_Date,
                                       Sample_Drawn_By=sample_drawn_by,
                                       Sample_Inspected_By=None,
                                       Sample_Drawn=no_of_sample_drawn,
                                       Sample_Size=total_sample_size,
                                       Inspection_Method=inspection_method,
                                       Inspection_Method_Other=inspection_method_other,
                                       Pest_Detected=pest_detected,
                                       Pest_Scientific_Name=None,
                                       Infestation_Level=None,
                                       Pest_Status=None,
                                       Pest_Risk_Category=None,
                                       Pest_QR_Detected=None,
                                       Pest_QR_Comment=None,
                                       Treatment_Possible=None,
                                       Treatment_Comment=None,
                                       Laboratory_Analysis_Required=None,
                                       Laboratory_Analysis_Comment=None,
                                       Phytosanitary_Measures=None,
                                       Phytosanitary_Measures_Comment=None,
                                       Inspection_Remarks=remarks,
                                       Export_Permit=export_permit,
                                       Approved_Date=date.today()
                                       )

    else:
        application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
            Application_No=Application_No)
        application_details.update(Inspection_Date=C_Inspection_Date,
                                   Inspection_Remarks=c_remarks,
                                   Export_Permit=export_permit,
                                   Approved_Date=date.today()
                                   )
    work_details = t_workflow_details.objects.filter(application_no=Application_No)
    work_details.update(action_date=date.today())
    work_details.update(application_status='A')
    update_payment_details(Application_No, export_permit, 'EPP', None, 'Final', '131110018')
    for email_id in application_details:
        emailId = email_id.Email
        send_export_approve_email(export_permit, emailId, Application_No)
    return redirect(inspector_application)


def send_export_approve_email(export_permit, Email, Application_No):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Export Permit for Plant And Plant Products Has Been Approved." \
              " Your Application No is" + Application_No + \
              " And Export Permit No is:" + export_permit + ". Please Make Payment To Download The Permit." \
                                                            " Visit The Nearest Bafra Office For Payment or Pay Online " \
                                                            "at https://tinyurl.com/y3m7wa3c Thank you! "
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def permit_plant_details(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    country = t_country_master.objects.all()
    entry_point = t_field_office_master.objects.filter(Is_Entry_Point='Y')
    application_id = request.GET.get('application_id')
    application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
        Application_No=application_id)
    return render(request, 'export_permit/phyto_permit_details.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'entry_point': entry_point, 'country': country,
                   'application_details': application_details})


def permit_agro_details(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    country = t_country_master.objects.all()
    entry_point = t_field_office_master.objects.filter(Is_Entry_Point='Y')
    application_id = request.GET.get('application_id')
    application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
        Application_No=application_id)
    return render(request, 'export_permit/cordyceps_permit_details.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'entry_point': entry_point, 'country': country,
                   'application_details': application_details})


def plant_file_details(request):
    permit_app_no = request.GET.get('applicationNo')
    file_attach = t_file_attachment.objects.filter(application_no=permit_app_no)
    return render(request, 'export_permit/phyto_file_attachment_page.html',
                  {'file_attach': file_attach})


def cordyceps_file_details(request):
    permit_app_no = request.GET.get('applicationNo')
    file_attach = t_file_attachment.objects.filter(application_no=permit_app_no)
    return render(request, 'export_permit/cordyceps_file_attachment_page.html',
                  {'file_attach': file_attach})


def save_export_permit(request):
    appNo = request.POST.get('applicationNo')
    workflow_details = t_workflow_details.objects.filter(application_no=appNo)
    workflow_details.update(application_date=date.today())
    workflow_details.update(action_date=date.today())
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'export_permit/apply_permit.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


# Registration Of Nursery/Seed Growers
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registration_application(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        crop = t_plant_crop_master.objects.all()
        crop_category = t_plant_crop_category_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        unit = t_unit_master.objects.filter(Unit_Type='S')
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'nursery_registration/apply_nursery_registration.html',
                      {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                       'location': location, 'crop': crop, 'crop_category': crop_category, 'variety': variety,
                       'unit': unit, 'count': message_count, 'count_call': inspection_call_count,
                       'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def save_nursery_reg(request):
    data = dict()
    service_code = "RNS"
    nursery_app_no = nursery_reg_app_no(service_code)
    Nursery_Category = request.POST.get('Nursery_Category')
    License_No = request.POST.get('License_No')
    Company_Name = request.POST.get('Company_Name')
    Company_Address = request.POST.get('Company_Address')
    CID = request.POST.get('CID')
    Owner_Name = request.POST.get('Owner_Name')
    contactNo = request.POST.get('contactNo')
    email = request.POST.get('email')
    Unit_Area = request.POST.get('Unit_Area')
    Area = request.POST.get('Area')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location_code = request.POST.get('location')
    Nursery_Type = request.POST.get('Nursery_Type')
    Applicant_Id = request.session['email']

    t_plant_clearence_nursery_seed_grower_t1.objects.create(
        Application_No=nursery_app_no,
        Nursery_Category=Nursery_Category,
        License_No=License_No,
        Company_Name=Company_Name,
        Company_Address=Company_Address,
        CID=CID,
        Owner_Name=Owner_Name,
        Contact_No=contactNo,
        Email=email,
        Unit_Area=Unit_Area,
        Area=Area,
        Dzongkhag=dzongkhag,
        Gewog=gewog,
        Village=village,
        Location_Code=location_code,
        Nursery_Type=Nursery_Type,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Facilities_Land=None,
        Facilities_Nursery_House=None,
        Facilities_Irrigation=None,
        Facilities_Tools=None,
        Facilities_Store=None,
        Manpower=None,
        Seed_Type=None,
        Technical_Clearance=None,
        Recommendation=None,
        Resubmit_Remarks=None,
        Resubmit_Date=None,
        Desired_Inspection_Date=None,
        Clearance_Number=None,
        Application_Date=date.today(),
        Applicant_Id=Applicant_Id
    )
    field_id = t_location_field_office_mapping.objects.filter(pk=location_code)
    for field_office in field_id:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(application_no=nursery_app_no, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=field_office_id, section='Plant',
                                      assigned_role_id='4',
                                      action_date=None, application_status='P',
                                      service_code=service_code)
    data['applicationNo'] = nursery_app_no
    return JsonResponse(data)


def nursery_reg_app_no(serviceCode):
    last_export_application_no = t_plant_clearence_nursery_seed_grower_t1.objects.aggregate(Max('Application_No'))
    last_application_no = last_export_application_no['Application_No__max']
    if not last_application_no:
        year = timezone.now().year
        newApplicationNo = serviceCode + "-" + str(year) + "-" + "0001"
    else:
        substring = str(last_application_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newApplicationNo = serviceCode + "-" + str(year) + "-" + AppNo
    return newApplicationNo


def add_file_reg(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/nursery_registration")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/nursery_registration" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def add_file_name_reg(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
    return render(request, 'nursery_registration/file_attachment_page.html', {'file_attach': file_attach})


def delete_file_nursery(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/nursery_registration")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'nursery_registration/file_attachment_page.html', {'file_attach': file_attach})


def update_nursery_reg(request):
    data = dict()
    service_code = "RNS"
    nursery_app_no = request.POST.get('applicationNo')
    Nursery_Category = request.POST.get('Nursery_Category')
    License_No = request.POST.get('Nursery_Category')
    Company_Name = request.POST.get('License_No')
    Company_Address = request.POST.get('Company_Address')
    CID = request.POST.get('CID')
    Owner_Name = request.POST.get('Owner_Name')
    contactNo = request.POST.get('contactNo')
    email = request.POST.get('email')
    Unit_Area = request.POST.get('Unit_Area')
    Area = request.POST.get('Area')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location_code = request.POST.get('location')
    Nursery_Type = request.POST.get('Nursery_Type')
    Applicant_Id = request.session['email']

    nursery_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=nursery_app_no)

    nursery_details.update(
        Nursery_Category=Nursery_Category,
        License_No=License_No,
        Company_Name=Company_Name,
        Company_Address=Company_Address,
        CID=CID,
        Owner_Name=Owner_Name,
        Contact_No=contactNo,
        Email=email,
        Unit_Area=Unit_Area,
        Area=Area,
        Dzongkhag=dzongkhag,
        Gewog=gewog,
        Village=village,
        Location_Code=location_code,
        Nursery_Type=Nursery_Type,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Facilities_Land=None,
        Facilities_Nursery_House=None,
        Facilities_Irrigation=None,
        Facilities_Tools=None,
        Facilities_Store=None,
        Manpower=None,
        Seed_Type=None,
        Technical_Clearance=None,
        Recommendation=None,
        Resubmit_Remarks=None,
        Resubmit_Date=None,
        Desired_Inspection_Date=None,
        Clearance_Number=None,
        Application_Date=date.today(),
        Applicant_Id=Applicant_Id
    )
    field_id = t_location_field_office_mapping.objects.filter(pk=location_code)
    for field_office in field_id:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(application_no=nursery_app_no, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=field_office_id, section='Plant',
                                      assigned_role_id='4',
                                      action_date=None, application_status='P',
                                      service_code=service_code)
    data['applicationNo'] = nursery_app_no
    return JsonResponse(data)


def add_reg_details(request):
    Application_No = request.POST.get('nursery_appNo')
    scientific_name = request.POST.get('scientific_name')
    crop_category_id = request.POST.get('crop_category_id')
    crop_variety_id = request.POST.get('crop_variety_id')
    Source = request.POST.get('Source')
    qty = request.POST.get('qty')
    unit = request.POST.get('unit')
    remarks = request.POST.get('remarks')
    t_plant_clearence_nursery_seed_grower_t2.objects.create(
        Application_No=Application_No,
        Crop_Category=crop_category_id,
        Crop=None,
        Crop_Scientific_Name=scientific_name,
        Variety=crop_variety_id,
        Source=Source,
        Qty=qty,
        Unit=unit,
        Remarks=remarks)

    seed_details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=Application_No)
    seed_details_count = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=Application_No).count()
    crop_master = t_plant_crop_master.objects.all()
    crop_category = t_plant_crop_category_master.objects.all()
    return render(request, 'nursery_registration/seed_details_page.html', {'seed_details': seed_details,
                                                                           'seed_details_count': seed_details_count,
                                                                           'crop_master': crop_master,
                                                                           'crop_category': crop_category})


def submit_nursery_details(request):
    appNo = request.POST.get('applicationNo')
    workflow_details = t_workflow_details.objects.filter(application_no=appNo)
    workflow_details.update(application_date=date.today())
    workflow_details.update(action_date=date.today())
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    crop = t_plant_crop_master.objects.all()
    crop_category = t_plant_crop_category_master.objects.all()
    variety = t_plant_crop_variety_master.objects.all()

    return render(request, 'nursery_registration/apply_nursery_registration.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'crop': crop, 'crop_category': crop_category, 'variety': variety})


def approve_nursery_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    Inspection_Date = request.GET.get('dateOfInspection')
    clearance_ref_no = get_nursery_clearnace_no(request)
    Facilities_Land = request.GET.get('Facilities_Land')
    Facilities_Nursery_House = request.GET.get('Facilities_Nursery_House')
    Facilities_Irrigation = request.GET.get('Facilities_Irrigation')
    Facilities_Tools = request.GET.get('Facilities_Tools')
    Facilities_Store = request.GET.get('Facilities_Store')
    Manpower = request.GET.get('Manpower')
    Seed_Type = request.GET.get('Seed_Type')
    Technical_Clearance = request.GET.get('Technical_Clearance')
    Recommendation = request.GET.get('Recommendation')
    Remarks = request.GET.get('remarks')

    details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
    if Remarks is not None:
        details.update(Remarks=Remarks)
    else:
        details.update(Remarks=None)

    details.update(Inspection_Date=Inspection_Date)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Facilities_Land=Facilities_Land)
    details.update(Facilities_Nursery_House=Facilities_Nursery_House)
    details.update(Facilities_Irrigation=Facilities_Irrigation)
    details.update(Facilities_Tools=Facilities_Tools)
    details.update(Facilities_Store=Facilities_Store)
    details.update(Manpower=Manpower)
    details.update(Seed_Type=Seed_Type)
    details.update(Technical_Clearance=Technical_Clearance)
    details.update(Recommendation=Recommendation)
    details.update(Clearance_Number=clearance_ref_no)
    details.update(Approved_Date=date.today())
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='A')
    # update_payment_details(application_id, clearance_ref_no, 'RNS', None)
    for email_id in details:
        emailId = email_id.Email
        send_nursery_approve_email(clearance_ref_no, emailId)
    return redirect(inspector_application)


def send_nursery_approve_email(clearance_ref_no, Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Nursery/Seed Growers Registration Has Been Approved. Your " \
              "Registration No is:" + clearance_ref_no + "."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_nursery_reject_email(remarks, email):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Nursery/Seed Growers Registration Has Been Rejected." \
              "Because :" + remarks + "."
    recipient_list = [email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def reject_nursery_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    Inspection_Date = request.GET.get('dateOfInspection')
    Facilities_Land = request.GET.get('Facilities_Land')
    Facilities_Nursery_House = request.GET.get('Facilities_Nursery_House')
    Facilities_Irrigation = request.GET.get('Facilities_Irrigation')
    Facilities_Tools = request.GET.get('Facilities_Tools')
    Facilities_Store = request.GET.get('Facilities_Store')
    Manpower = request.GET.get('Manpower')
    Seed_Type = request.GET.get('Seed_Type')
    Technical_Clearance = request.GET.get('Technical_Clearance')
    Recommendation = request.GET.get('Recommendation')
    Remarks = request.GET.get('remarks')

    details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
    if Remarks is not None:
        details.update(Remarks=Remarks)
    else:
        details.update(Remarks=None)

    details.update(Inspection_Date=Inspection_Date)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Facilities_Land=Facilities_Land)
    details.update(Facilities_Nursery_House=Facilities_Nursery_House)
    details.update(Facilities_Irrigation=Facilities_Irrigation)
    details.update(Facilities_Tools=Facilities_Tools)
    details.update(Facilities_Store=Facilities_Store)
    details.update(Manpower=Manpower)
    details.update(Seed_Type=Seed_Type)
    details.update(Technical_Clearance=Technical_Clearance)
    details.update(Recommendation=Recommendation)

    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='R')
    application_details.update(assigned_role_id=None)
    for email_id in details:
        emailId = email_id.Email
        send_nursery_reject_email(Remarks, emailId)
    return redirect(inspector_application)


def resubmit_nursery_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    Inspection_Date = request.GET.get('dateOfInspection')
    Facilities_Land = request.GET.get('Facilities_Land')
    Facilities_Nursery_House = request.GET.get('Facilities_Nursery_House')
    Facilities_Irrigation = request.GET.get('Facilities_Irrigation')
    Facilities_Tools = request.GET.get('Facilities_Tools')
    Facilities_Store = request.GET.get('Facilities_Store')
    Manpower = request.GET.get('Manpower')
    Seed_Type = request.GET.get('Seed_Type')
    Technical_Clearance = request.GET.get('Technical_Clearance')
    Recommendation = request.GET.get('Recommendation')
    Remarks = request.GET.get('remarks')

    details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
    if Remarks is not None:
        details.update(Remarks=Remarks)
    else:
        details.update(Remarks=None)

    details.update(Inspection_Date=Inspection_Date)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Facilities_Land=Facilities_Land)
    details.update(Facilities_Nursery_House=Facilities_Nursery_House)
    details.update(Facilities_Irrigation=Facilities_Irrigation)
    details.update(Facilities_Tools=Facilities_Tools)
    details.update(Facilities_Store=Facilities_Store)
    details.update(Manpower=Manpower)
    details.update(Seed_Type=Seed_Type)
    details.update(Technical_Clearance=Technical_Clearance)
    details.update(Recommendation=Recommendation)

    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='RS')
    application_details.update(assigned_role_id=None)
    for app_details in application_details:
        email_id = app_details.Applicant_Id
        login_details = t_user_master.objects.filter(Email_Id=email_id)
        for user_details in login_details:
            login_id = user_details.Login_Id
            application_details.update(Assigned_To=login_id)
    return redirect(inspector_application)


def nursery_client_resubmit(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('Resubmit_Remarks')
    inspection_date = request.GET.get('inspection_date')
    details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
    details.update(Resubmit_Remarks=remarks)
    details.update(Resubmit_Date=inspection_date)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='P')
    application_details.update(assigned_role_id='4')
    return redirect(resubmit_application)


def add_details_nursery(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_clearence_nursery_seed_grower_t3.objects.create(Application_No=application_id,
                                                            Observation=currentObservation,
                                                            Action=decisionConform)
    decision_details = t_plant_clearence_nursery_seed_grower_t3.objects.filter(Application_No=application_id)
    return render(request, 'nursery_registration/add_decision_details.html', {'decision_details': decision_details})


def get_nursery_clearnace_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_export_permit = t_plant_clearence_nursery_seed_grower_t1.objects.aggregate(Max('Clearance_Number'))
    last_export_permit_no = last_export_permit['Clearance_Number__max']
    if not last_export_permit_no:
        year = timezone.now().year
        new_clearnace_no = Field_Code + "-" + "RNS" + "-" + str(year) + "-" + "0001"
    else:
        substring = str(last_export_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        new_clearnace_no = Field_Code + "-" + "RNS" + "-" + str(year) + "-" + AppNo
    return new_clearnace_no


def load_nursery_details(request):
    Application_No = request.GET.get('appNo')
    seed_details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=Application_No)
    seed_details_count = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=Application_No).count()
    return render(request, 'nursery_registration/seed_details_page.html', {'seed_details': seed_details,
                                                                           'seed_details_count': seed_details_count})


def load_nursery_attachment(request):
    Application_No = request.GET.get('appNo')
    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'nursery_registration/file_attachment_page.html', {'file_attach': file_attach})


def update_nursery_details(request):
    data = dict()
    nursery_app_no = request.POST.get('applicationNo')
    Nursery_Category = request.POST.get('Nursery_Category')
    License_No = request.POST.get('Nursery_Category')
    Company_Name = request.POST.get('License_No')
    Company_Address = request.POST.get('Company_Address')
    CID = request.POST.get('CID')
    Owner_Name = request.POST.get('Owner_Name')
    contactNo = request.POST.get('contactNo')
    email = request.POST.get('email')
    Unit_Area = request.POST.get('Unit_Area')
    Area = request.POST.get('Area')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location_code = request.POST.get('location_code')
    Nursery_Type = request.POST.get('Nursery_Type')

    app_details = t_plant_clearence_nursery_seed_grower_t1.objects.create(Application_No=nursery_app_no)
    app_details.update(
        Nursery_Category=Nursery_Category,
        License_No=License_No,
        Company_Name=Company_Name,
        Company_Address=Company_Address,
        CID=CID,
        Owner_Name=Owner_Name,
        Contact_No=contactNo,
        email=email,
        Unit_Area=Unit_Area,
        Area=Area,
        Dzongkhag=dzongkhag,
        Gewog=gewog,
        Village=village,
        Location_Code=location_code,
        Nursery_Type=Nursery_Type,
    )
    data['success'] = "Success"
    return JsonResponse(data)


def load_details(request):
    nursery_app_no = request.GET.get('applicationNo')
    seed_details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=nursery_app_no)
    seed_details_count = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=nursery_app_no).count()
    return render(request, 'nursery_registration/seed_details_page.html',
                  {'seed_details': seed_details, 'seed_details_count': seed_details_count})


def load_file_details(request):
    nursery_app_no = request.GET.get('applicationNo')
    file_attach = t_file_attachment.objects.filter(application_no=nursery_app_no)
    return render(request, 'nursery_registration/file_attachment_page.html',
                  {'file_attach': file_attach})


# Seed Certification
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def seed_certificate_application(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        crop = t_plant_crop_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        unit = t_unit_master.objects.filter(Unit_Type='S')
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'seed_certification/apply_seed_certification.html',
                      {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                       'location': location, 'crop': crop, 'variety': variety, 'unit': unit, 'count': message_count,
                       'count_call': inspection_call_count, 'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def save_seed_cert(request):
    data = dict()
    serviceCode = "RSC"
    application_No = certifcate_app_no(serviceCode)
    Nursery_Category = request.POST.get('Nursery_Category')
    License_No = request.POST.get('License_No')
    Company_Name = request.POST.get('Company_Name')
    Company_Address = request.POST.get('Company_Address')
    CID = request.POST.get('CID')
    Owner_Name = request.POST.get('Owner_Name')
    contactNo = request.POST.get('contactNo')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    Applicant_Id = request.session['email']
    location = request.POST.get('location')
    t_plant_seed_certification_t1.objects.create(
        Application_No=application_No,
        Nursery_Category=Nursery_Category,
        License_No=License_No,
        Company_Name=Company_Name,
        Company_Address=Company_Address,
        CID=CID,
        Owner_Name=Owner_Name,
        Contact_No=contactNo,
        Email=email,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=None,
        Village_Code=None,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Seed_Certificate=None,
        Application_Date=date.today(),
        Applicant_Id=Applicant_Id,
        Location_Code=location
    )
    field_id = t_location_field_office_mapping.objects.filter(pk=location)
    for field_office in field_id:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(application_no=application_No, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=field_office_id, section='Plant',
                                      assigned_role_id='4',
                                      action_date=None, application_status='P',
                                      service_code=serviceCode)
    data['applicationNo'] = application_No
    return JsonResponse(data)


def certifcate_app_no(serviceCode):
    last_certificate_application_no = t_plant_seed_certification_t1.objects.aggregate(Max('Application_No'))
    last_application_no = last_certificate_application_no['Application_No__max']
    if not last_application_no:
        year = timezone.now().year
        newApplicationNo = serviceCode + "-" + str(year) + "-" + "0001"
    else:
        substring = str(last_application_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newApplicationNo = serviceCode + "-" + str(year) + "-" + AppNo
    return newApplicationNo


def add_file_certificate(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/seed_certification")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/seed_certification" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def add_file_name_certificate(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
        return render(request, 'seed_certification/file_attachment_page.html', {'file_attach': file_attach})


def delete_file_seed(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/seed_certification")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'seed_certification/file_attachment_page.html', {'file_attach': file_attach})


def update_seed_certificate(request):
    data = dict()
    serviceCode = "RSC"
    application_No = request.POST.get('applicationNo')
    Nursery_Category = request.POST.get('Nursery_Category')
    License_No = request.POST.get('Nursery_Category')
    Company_Name = request.POST.get('License_No')
    Company_Address = request.POST.get('Company_Address')
    CID = request.POST.get('CID')
    Owner_Name = request.POST.get('Owner_Name')
    contactNo = request.POST.get('contactNo')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    Applicant_Id = request.session['email']
    location = request.POST.get('location')

    seed_details = t_plant_seed_certification_t1.objects.filter(Application_No=application_No)

    seed_details.update(
        Nursery_Category=Nursery_Category,
        License_No=License_No,
        Company_Name=Company_Name,
        Company_Address=Company_Address,
        CID=CID,
        Owner_Name=Owner_Name,
        Contact_No=contactNo,
        Email=email,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=None,
        Village_Code=None,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Seed_Certificate=None,
        Application_Date=date.today(),
        Applicant_Id=Applicant_Id,
        Location_Code=location
    )
    field_id = t_location_field_office_mapping.objects.filter(Dzongkhag_Code=dzongkhag)
    for field_office in field_id:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(application_no=application_No, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=field_office_id, section='Plant',
                                      assigned_role_id='4',
                                      action_date=None, application_status='P',
                                      service_code=serviceCode)
    data['applicationNo'] = application_No
    return JsonResponse(data)


def get_seed_cerficate_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_export_permit = t_plant_seed_certification_t1.objects.aggregate(Max('Seed_Certificate'))
    last_export_permit_no = last_export_permit['Seed_Certificate__max']
    if not last_export_permit_no:
        year = timezone.now().year
        new_cerficate_no = Field_Code + "-" + "RSC" + "-" + str(year) + "-" + "0001"
    else:
        substring = str(last_export_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        new_cerficate_no = Field_Code + "-" + "RSC" + "-" + str(year) + "-" + AppNo
    return new_cerficate_no


def add_certificate_details(request):
    Application_No = request.POST.get('appNo')
    crop_id = request.POST.get('crop_id')
    crop_variety_id = request.POST.get('crop_variety_id')
    Source = request.POST.get('Source')
    qty = request.POST.get('qty')
    unit = request.POST.get('Unit')
    purpose = request.POST.get('purpose')
    t_plant_seed_certification_t2.objects.create(
        Application_No=Application_No,
        Crop=crop_id,
        Variety=crop_variety_id,
        Seed_Source=Source,
        Quantity=qty,
        Unit=unit,
        Purpose=purpose,
        Qty_Certified=None,
        Value_Certified=None,
        Qty_Rejected=None,
        Unit_Rejected=None,
        Value_Rejected=None,
        Remarks=None
    )
    certification_details = t_plant_seed_certification_t2.objects.filter(Application_No=Application_No)
    seed_details_count = t_plant_seed_certification_t2.objects.filter(Application_No=Application_No).count()
    return render(request, 'seed_certification/seed_certification_details_page.html',
                  {'certification_details': certification_details, 'seed_details_count': seed_details_count})


def submit_certificate_details(request):
    applicationNo = request.POST.get('applicationNo')
    workflow_details = t_workflow_details.objects.filter(application_no=applicationNo)
    workflow_details.update(application_date=date.today())
    workflow_details.update(action_date=date.today())
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    crop = t_plant_crop_master.objects.all()
    variety = t_plant_crop_variety_master.objects.all()

    return render(request, 'seed_certification/apply_seed_certification.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'crop': crop, 'variety': variety})


def approve_certificate_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('inspector_remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    validity_period = request.GET.get('validity')
    certificate_no = get_seed_cerficate_no(request)
    details = t_plant_seed_certification_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Inspector_Remarks=remarks)
    else:
        details.update(Inspector_Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=dateOfInspection)
    details.update(Seed_Certificate=certificate_no)
    details.update(Approved_Date=date.today())
    details.update(Validity_Period=validity_period)
    d = timedelta(days=int(validity_period))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='A')
    update_payment_details(application_id, certificate_no, 'RSC', validity_date, 'Final', '131110002')
    for email_id in details:
        emailId = email_id.Email
        send_seed_approve_email(certificate_no, emailId, validity_date, application_id)
    return redirect(inspector_application)


def send_seed_approve_email(clearance_ref_no, Email, validity_date, application_id):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Seed Certification Has Been Approved." \
              " Your Application No is " + application_id + \
              " And Seed Certificate No is:" + clearance_ref_no + " And is Valid Till " + " " + str(validity_date) + \
              " Please Make Payment Before Validity Expires.Visit The Nearest Bafra Office For" \
              " Payment or Pay Online at https://tinyurl.com/y3m7wa3c Thank you! "
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def reject_certificate_application(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('inspector_remarks')

    details = t_plant_seed_certification_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Inspector_Remarks=remarks)
    else:
        details.update(Inspector_Remarks=None)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='R')
    for email_id in application_details:
        emailId = email_id.Email
        send_seed_reject_email(emailId)

    return redirect(inspector_application)


def send_seed_reject_email(Email):
    subject = 'APPLICATION REJECT'
    message = "Dear Sir," \
              "" \
              "Your Application for Seed Certification Has Been Rejected. "
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def resubmit_seed_application(request):
    application_id = request.GET.get('application_id')
    Remarks = request.GET.get('inspector_remarks')

    details = t_plant_seed_certification_t1.objects.filter(Application_No=application_id)
    if Remarks is not None:
        details.update(Inspector_Remarks=Remarks)
    else:
        details.update(Inspector_Remarks=None)

    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='RS')
    application_details.update(assigned_role_id=None)
    for app_details in application_details:
        email_id = app_details.Applicant_Id
        login_details = t_user_master.objects.filter(Email_Id=email_id)
        for user_details in login_details:
            login_id = user_details.Login_Id
            application_details.update(Assigned_To=login_id)
    return redirect(inspector_application)


def seed_certification_client_resubmit(request):
    application_id = request.GET.get('application_id')
    Remarks = request.GET.get('Resubmit_Remarks')
    inspection_date = request.GET.get('inspection_date')
    details = t_plant_seed_certification_t1.objects.filter(Application_No=application_id)
    if Remarks is not None:
        details.update(Client_Remarks=Remarks)
    else:
        details.update(Client_Remarks=None)
    details.update(Resubmit_Date=inspection_date)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='P')
    application_details.update(assigned_role_id='4')
    return redirect(resubmit_application)


def add_details_ins_certificate(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_seed_certification_t3.objects.create(Application_No=application_id,
                                                 Observation=currentObservation,
                                                 Action=decisionConform)
    details_statement = t_plant_seed_certification_t3.objects.filter(Application_No=application_id)
    return render(request, 'seed_certification/add_decision_details.html', {'decision': details_statement})


def add_recommendation_details(request):
    record_id = request.GET.get('record_id')
    quantity = request.GET.get('quantity')
    unit = request.GET.get('unit')
    quantity_certified = request.GET.get('quantity_certified')
    unit_certified = request.GET.get('unit_certified')
    value_certified = request.GET.get('value_certified')
    quantity_rejected = request.GET.get('quantity_rejected')
    unit_rejected = request.GET.get('unit_rejected')
    value_rejected = request.GET.get('value_rejected')
    recommend_remarks = request.GET.get('remarks')
    application_no = request.GET.get('application_no')
    details_statement = t_plant_seed_certification_t2.objects.filter(Record_Id=record_id)
    if recommend_remarks is not None:
        details_statement.update(Remarks=recommend_remarks)
    else:
        details_statement.update(Remarks=None)
    details_statement.update(
        Quantity=quantity,
        Unit=unit,
        Qty_Certified=quantity_certified,
        Unit_Certified=unit_certified,
        Value_Certified=value_certified,
        Qty_Rejected=quantity_rejected,
        Unit_Rejected=unit_rejected,
        Value_Rejected=value_rejected,
    )
    recommendation = t_plant_seed_certification_t2.objects.filter(Application_No=application_no)
    return render(request, 'seed_certification/add_recommendation_details.html', {'recommendation': recommendation})


def load_certificate_details(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
    return render(request, 'seed_certificate/certificate_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village})


def update_certificate_details(request):
    data = dict()
    nursery_app_no = request.POST.get('applicationNo')
    Nursery_Category = request.POST.get('Nursery_Category')
    License_No = request.POST.get('Nursery_Category')
    Company_Name = request.POST.get('License_No')
    Company_Address = request.POST.get('Company_Address')
    CID = request.POST.get('CID')
    Owner_Name = request.POST.get('Owner_Name')
    contactNo = request.POST.get('contactNo')
    email = request.POST.get('email')
    Unit_Area = request.POST.get('Unit_Area')
    Area = request.POST.get('Area')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location_code = request.POST.get('location_code')
    Nursery_Type = request.POST.get('Nursery_Type')

    app_details = t_plant_clearence_nursery_seed_grower_t1.objects.create(Application_No=nursery_app_no)
    app_details.update(
        Nursery_Category=Nursery_Category,
        License_No=License_No,
        Company_Name=Company_Name,
        Company_Address=Company_Address,
        CID=CID,
        Owner_Name=Owner_Name,
        Contact_No=contactNo,
        Email=email,
        Unit_Area=Unit_Area,
        Area=Area,
        Dzongkhag=dzongkhag,
        Gewog=gewog,
        Village=village,
        Location_Code=location_code,
        Nursery_Type=Nursery_Type,
    )
    data['success'] = "Success"
    return JsonResponse(data)


def certificate_details(request):
    nursery_app_no = request.GET.get('applicationNo')
    seed_details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=nursery_app_no)
    seed_details_count = t_plant_seed_certification_t2.objects.filter(Application_No=nursery_app_no).count()
    return render(request, 'seed_certificate/seed_certification_details_page.html',
                  {'seed_details': seed_details, 'seed_details_count': seed_details_count})


def certificate_file_details(request):
    nursery_app_no = request.GET.get('applicationNo')
    file_attach = t_file_attachment.objects.filter(application_no=nursery_app_no)
    return render(request, 'seed_certificate/file_attachment_page.html',
                  {'file_attach': file_attach})


# certification_certificates
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def certificate_print(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        login_type = request.session['Login_Type']
        if login_type == 'I':
            Role = request.session['role']
            Role_Id = request.session['Role_Id']
            if Role == 'Focal Officer':
                section = request.session['section']
                section_details = t_section_master.objects.filter(Section_Id=section)
                for id_section in section_details:
                    section_name = id_section.Section_Name
                    message_count = (t_workflow_details.objects.filter(
                        assigned_role_id=Role_Id, section=section_name,
                        action_date__isnull=False, application_status='P') | t_workflow_details.objects.filter(
                        assigned_role_id=Role_Id, section=section_name,
                        action_date__isnull=False, application_status='ATA') | t_workflow_details.objects.filter(
                        assigned_role_id=Role_Id, section=section_name,
                        action_date__isnull=False, application_status='FRA') |
                                     t_workflow_details.objects.filter(
                                         assigned_role_id=Role_Id, section=section_name,
                                         action_date__isnull=False, application_status='CA')
                                     ).count()
                    return render(request, 'certificate_printing.html', {'count': message_count})
            elif Role == 'OIC':
                login_id = request.session['Login_Id']
                Field_Office_Id = request.session['field_office_id']
                message_count = (
                        t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                          action_date__isnull=False) |
                        t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                          action_date__isnull=False)).count()

                return render(request, 'certificate_printing.html', {'count': message_count})
            elif Role == 'Inspector':
                login_id = request.session['Login_Id']
                Field_Office_Id = request.session['field_office_id']
                message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                                   action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id,
                                                                     field_office_id=Field_Office_Id,
                                                                     application_status='I',
                                                                     action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id,
                                                                     field_office_id=Field_Office_Id,
                                                                     application_status='FI',
                                                                     action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id,
                                                                     field_office_id=Field_Office_Id,
                                                                     application_status='FR',
                                                                     action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id,
                                                                     field_office_id=Field_Office_Id,
                                                                     application_status='P',
                                                                     action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                     action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                     action_date__isnull=False)).count()
                fhc_count = t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                              action_date__isnull=False, service_code='FHC').count()
                return render(request, 'certificate_printing.html',
                              {'ins_count': message_count, 'fhc_count': fhc_count})
        else:
            login_id = request.session['Login_Id']
            message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                             | t_workflow_details.objects.filter(assigned_to=login_id,
                                                                 application_status='NCR')).count()

            inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                      action_date__isnull=False).count()
            consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                       action_date__isnull=False,
                                                                       application_status='P') \
                .count()
            return render(request, 'certificate_printing.html',
                          {'count': message_count, 'count_call': inspection_call_count,
                           'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def view_certificate_details(request):
    service_code = request.GET.get('service_code')
    login_id = request.session['email']
    login_type = request.session['Login_Type']

    if login_type == 'I':
        if service_code == 'MPP':
            application_details = t_plant_movement_permit_t1.objects.filter(Movement_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/movement_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'IPP':
            application_details = t_plant_import_permit_t1.objects.filter(Import_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/import_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'EPP':
            application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
                Export_Permit__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/export_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'RNS':
            application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(
                Clearance_Number__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/nursery_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'RSC':
            application_details = t_plant_seed_certification_t1.objects.filter(Seed_Certificate__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/seed_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'FFC':
            application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
                Export_Permit__isnull=False)
            return render(request, 'certificates/fit_for_consumption_details.html',
                          {'application_details': application_details})
        elif service_code == 'NC':
            application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(
                Clearance_Number__isnull=False)
            return render(request, 'certificates/nursery_clearance_details.html',
                          {'application_details': application_details})
        elif service_code == 'RF':
            application_details = t_plant_import_permit_inspection_t1.objects.filter(Clearance_Ref_No__isnull=False)
            return render(request, 'certificates/release_form_details.html',
                          {'application_details': application_details})
        # LIVESTOCK_CERTIFICATE_DETAILS
        elif service_code == 'APM':
            application_details = t_livestock_ante_post_mortem_t1.objects.filter(Clearance_No__isnull=False)
            for application in application_details:
                app_no = application.Clearance_No
                payment_details = t_payment_details.objects.filter(permit_no=app_no)
            return render(request, 'livestock_certificates/ante_post_mortem/certificate_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'CMS':
            application_details = t_livestock_clearance_meat_shop_t1.objects.filter(
                meat_shop_clearance_no__isnull=False)
            payment_details = t_payment_details.objects.filter(permit_type='Final')
            return render(request, 'livestock_certificates/meat_shop_clearance/clearance_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'CCMS':
            application_details = t_livestock_clearance_meat_shop_t1.objects.filter(
                conditional_clearance_no__isnull=False)
            payment_details = t_payment_details.objects.filter(permit_type='Feasibility')
            return render(request, 'livestock_certificates/meat_shop_clearance/conditional_clearance_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'LMP':
            application_details = t_livestock_movement_permit_t1.objects.filter(Movement_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/movement_permit/movement_permit_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'RFAF':
            application_details = t_livestock_import_permit_animal_inspection_t1.objects.filter(
                Clearance_Ref_No__isnull=False)

            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/import/release_form_list_animal.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'RFLP':
            application_details = t_livestock_import_permit_product_inspection_t1.objects.filter(
                Clearance_Ref_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/import/release_form_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'IAF':
            application_details = t_livestock_import_permit_animal_t1.objects.filter(Import_Permit_No__isnull=False)

            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/import/import_cert_animal_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'ILP':
            application_details = t_livestock_import_permit_product_t1.objects.filter(Import_Permit_No__isnull=False)

            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/import/import_cert_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'LEC':
            application_details = t_livestock_export_certificate_t1.objects.filter(Export_Permit_No__isnull=False)
            for application in application_details:
                app_no = application.Export_Permit_No
                payment_details = t_payment_details.objects.filter(permit_no=app_no)
                return render(request, 'livestock_certificates/export_certificate/export_cert_list.html',
                              {'application_details': application_details, 'payment_details': payment_details})

        # FOOD SECTION
        elif service_code == 'FIP':  # Import Permit Food
            import_permit_details = t_food_import_permit_t1.objects.filter(Import_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'food_certificates/import_permit_food_list.html',
                          {'import_permit_details': import_permit_details, 'payment_details': payment_details})

        elif service_code == 'RFF':  # Release Form Food
            application_details = t_food_import_permit_inspection_t1.objects.filter(Clearance_Ref_No__isnull=False)
            return render(request, 'food_certificates/release_form_food_list.html',
                          {'application_details': application_details})

        elif service_code == 'ECF':  # Export Certificate Food
            application_details = t_food_export_certificate_t1.objects.filter(Export_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'food_certificates/export_certificate_food_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'CFC':  # Conditional Food Safety Clearance
            application_details = t_food_business_registration_licensing_t1.objects.filter(
                conditional_clearance_no__isnull=False)
            payment_details = t_payment_details.objects.filter(permit_type='Feasibility')
            return render(request, 'food_certificates/safety_clearance_food_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'FSL':  # Food Safety License
            application_details = t_food_business_registration_licensing_t1.objects.filter(fb_license_no__isnull=False)
            payment_details = t_payment_details.objects.filter(permit_type='Final')
            return render(request, 'food_certificates/safety_license_food_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'FHL':  # Food Handler License
            role = request.session['Role_Id']
            if role == 2:
                application_details = t_food_licensing_food_handler_t1.objects.filter(FH_License_No__isnull=False)
                payment_details = t_payment_details.objects.all()
                return render(request, 'food_certificates/handler_license_food_list.html',
                              {'application_details': application_details, 'payment_details': payment_details})
            else:
                application_details = t_food_licensing_food_handler_t1.objects.filter(FH_License_No__isnull=False,
                                                                                      Preferred_Inspection_Place=
                                                                                      request.session[
                                                                                          'field_office_id'])
                payment_details = t_payment_details.objects.all()
                return render(request, 'food_certificates/handler_license_food_list.html',
                              {'application_details': application_details, 'payment_details': payment_details})

        # CERTIFICATION SECTION
        elif service_code == 'GAP':  # GAP Certificate
            application_details = t_certification_gap_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/gap_certificate_list.html',
                          {'application_details': application_details})

        elif service_code == 'ORC':  # Organic Certificate
            application_details = t_certification_organic_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/organic_certificate_list.html',
                          {'application_details': application_details})

        elif service_code == 'FPC':  # Food Product Certificate
            application_details = t_certification_food_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/food_certificate_list.html',
                          {'application_details': application_details})
        elif service_code == 'GAP':  # GAP Certificate Details
            application_details = t_certification_gap_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/gap_certificate_detail_list.html',
                          {'application_details': application_details})

        elif service_code == 'ORC':  # Organic Certificate Details
            application_details = t_certification_organic_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/organic_certificate_detail_list.html',
                          {'application_details': application_details})

        elif service_code == 'FPC':  # Food Product Certificate Details
            application_details = t_certification_food_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/food_certificate_detail_list.html',
                          {'application_details': application_details})
    else:
        if service_code == 'MPP':
            application_details = t_plant_movement_permit_t1.objects.filter(Applicant_Id=login_id,
                                                                            Movement_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/movement_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'IPP':
            application_details = t_plant_import_permit_t1.objects.filter(Applicant_Id=login_id,
                                                                          Import_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/import_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'EPP':
            application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
                Applicant_Id=login_id,
                Export_Permit__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/export_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'RNS':
            application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Applicant_Id=login_id,
                                                                                          Clearance_Number__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/nursery_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'RSC':
            application_details = t_plant_seed_certification_t1.objects.filter(Applicant_Id=login_id,
                                                                               Seed_Certificate__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'certificates/seed_certificate_printing_details.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'FFC':
            application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
                Applicant_Id=login_id,
                Export_Permit__isnull=False)
            return render(request, 'certificates/fit_for_consumption_details.html',
                          {'application_details': application_details})
        elif service_code == 'NC':
            application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Applicant_Id=login_id,
                                                                                          Clearance_Number__isnull=False)
            return render(request, 'certificates/nursery_clearance_details.html',
                          {'application_details': application_details})
        elif service_code == 'RF':
            application_details = t_plant_import_permit_inspection_t1.objects.filter(Applicant_Id=login_id,
                                                                                     Clearance_Ref_No__isnull=False)
            return render(request, 'certificates/release_form_details.html',
                          {'application_details': application_details})
        # LIVESTOCK_CERTIFICATE_DETAILS
        elif service_code == 'APM':
            application_details = t_livestock_ante_post_mortem_t1.objects.filter(Applicant_Id=login_id,
                                                                                 Clearance_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/ante_post_mortem/certificate_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'CMS':
            application_details = t_livestock_clearance_meat_shop_t1.objects.filter(applicant_id=login_id,
                                                                                    meat_shop_clearance_no__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/meat_shop_clearance/clearance_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'CCMS':
            application_details = t_livestock_clearance_meat_shop_t1.objects.filter(
                conditional_clearance_no__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/meat_shop_clearance/conditional_clearance_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'LMP':
            application_details = t_livestock_movement_permit_t1.objects.filter(Applicant_Id=login_id,
                                                                                Movement_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/movement_permit/movement_permit_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})
        elif service_code == 'RFAF':
            application_details = t_livestock_import_permit_animal_inspection_t1.objects.filter(Applicant_Id=login_id,
                                                                                                Clearance_Ref_No__isnull=False)
            return render(request, 'livestock_certificates/import/release_form_list_animal.html',
                          {'application_details': application_details})
        elif service_code == 'RFLP':
            application_details = t_livestock_import_permit_product_inspection_t1.objects.filter(
                Applicant_Id=login_id, Clearance_Ref_No__isnull=False)
            return render(request, 'livestock_certificates/import/release_form_list.html',
                          {'application_details': application_details})
        elif service_code == 'IAF':
            application_details = t_livestock_import_permit_animal_t1.objects.filter(Applicant_Id=login_id,
                                                                                     Import_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/import/import_cert_animal_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'ILP':
            application_details = t_livestock_import_permit_product_t1.objects.filter(Applicant_Id=login_id,
                                                                                      Import_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/import/import_cert_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'LEC':
            application_details = t_livestock_export_certificate_t1.objects.filter(Applicant_Id=login_id,
                                                                                   Export_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'livestock_certificates/export_certificate/export_cert_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        # FOOD SECTION
        elif service_code == 'FIP':  # Import Permit Food
            import_permit_details = t_food_import_permit_t1.objects.filter(Applicant_Id=login_id,
                                                                           Import_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'food_certificates/import_permit_food_list.html',
                          {'import_permit_details': import_permit_details, 'payment_details': payment_details})

        elif service_code == 'RFF':  # Release Form Food
            application_details = t_food_import_permit_inspection_t1.objects.filter(Applicant_Id=login_id,
                                                                                    Clearance_Ref_No__isnull=False)
            return render(request, 'food_certificates/release_form_food_list.html',
                          {'application_details': application_details})

        elif service_code == 'ECF':  # Export Certificate Food
            application_details = t_food_export_certificate_t1.objects.filter(Applicant_Id=login_id,
                                                                              Export_Permit_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'food_certificates/export_certificate_food_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'CFC':  # Conditional Food Safety Clearance
            application_details = t_food_business_registration_licensing_t1.objects.filter(applicant_id=login_id,
                                                                                           conditional_clearance_no__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'food_certificates/safety_clearance_food_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'FSL':  # Food Safety License
            application_details = t_food_business_registration_licensing_t1.objects.filter(applicant_id=login_id,
                                                                                           fb_license_no__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'food_certificates/safety_license_food_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        elif service_code == 'FHL':  # Food Handler License
            application_details = t_food_licensing_food_handler_t1.objects.filter(Applicant_Id=login_id,
                                                                                  FH_License_No__isnull=False)
            payment_details = t_payment_details.objects.all()
            return render(request, 'food_certificates/handler_license_food_list.html',
                          {'application_details': application_details, 'payment_details': payment_details})

        # CERTIFICATION SECTION
        elif service_code == 'GAP':  # GAP Certificate
            application_details = t_certification_gap_t1.objects.filter(Applicant_Id=login_id,
                                                                        Certificate_No__isnull=False)
            return render(request, 'certification_certificates/gap_certificate_list.html',
                          {'application_details': application_details})

        elif service_code == 'ORC':  # Organic Certificate
            application_details = t_certification_organic_t1.objects.filter(Applicant_Id=login_id,
                                                                            Certificate_No__isnull=False)
            return render(request, 'certification_certificates/organic_certificate_list.html',
                          {'application_details': application_details})

        elif service_code == 'FPC':  # Food Product Certificate
            application_details = t_certification_food_t1.objects.filter(Applicant_Id=login_id,
                                                                         Certificate_No__isnull=False)
            return render(request, 'certification_certificates/food_certificate_list.html',
                          {'application_details': application_details})
        elif service_code == 'GAP':  # GAP Certificate Details
            application_details = t_certification_gap_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/gap_certificate_detail_list.html',
                          {'application_details': application_details})

        elif service_code == 'ORC':  # Organic Certificate Details
            application_details = t_certification_organic_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/organic_certificate_detail_list.html',
                          {'application_details': application_details})

        elif service_code == 'FPC':  # Food Product Certificate Details
            application_details = t_certification_food_t1.objects.filter(Certificate_No__isnull=False)
            return render(request, 'certification_certificates/food_certificate_detail_list.html',
                          {'application_details': application_details})


def oic_inspector_certificate_details(request):
    service_code = request.GET.get('service_code')
    field_office_id = request.session['fiel_office_id']
    if service_code == 'MPP':
        application_details = t_workflow_details.objects.filter(field_office_id=field_office_id, application_status='A')
        return render(request, 'certification_certificates/movement_certificate_printing_details.html',
                      {'application_details': application_details})
    elif service_code == 'IPP':
        application_details = t_workflow_details.objects.filter(field_office_id=field_office_id, application_status='A')
        return render(request, 'certification_certificates/import_certificate_printing_details.html',
                      {'application_details': application_details})
    elif service_code == 'EPP':
        application_details = t_workflow_details.objects.filter(field_office_id=field_office_id, application_status='A')
        return render(request, 'certification_certificates/export_certificate_printing_details.html',
                      {'application_details': application_details})
    elif service_code == 'RNS':
        application_details = t_workflow_details.objects.filter(field_office_id=field_office_id, application_status='A')
        return render(request, 'certification_certificates/nursery_certificate_printing_details.html',
                      {'application_details': application_details})
    elif service_code == 'RSC':
        application_details = t_workflow_details.objects.filter(field_office_id=field_office_id, application_status='A')
        return render(request, 'certification_certificates/seed_certificate_printing_details.html',
                      {'application_details': application_details})


def get_certificate_details(request):
    application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    current_date = date.today()
    if service_code == 'MPP':
        certificate_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_No, Permit_Type='A')
        if certificate_details.exists():
            details_permit = t_plant_movement_permit_t2.objects.filter(Application_No=application_No)
            dzongkhag = t_dzongkhag_master.objects.all()
            return render(request, 'certificates/movement_permit_agro.html',
                          {'certificate_details': certificate_details, 'date': current_date,
                           'details_permit': details_permit, 'dzongkhag': dzongkhag})
        else:
            details = t_plant_movement_permit_t1.objects.filter(Application_No=application_No)
            details_permit = t_plant_movement_permit_t2.objects.filter(Application_No=application_No)
            dzongkhag = t_dzongkhag_master.objects.all()
            return render(request, 'certificates/movement_permit_plant.html',
                          {'details': details, 'date': current_date,
                           'details_permit': details_permit, 'dzongkhag': dzongkhag})
    elif service_code == 'EPP':
        details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(Application_No=application_No,
                                                                                    Certificate_Type='P')
        dzongkhag = t_dzongkhag_master.objects.all()
        if details.exists():
            return render(request, 'certificates/phytosanitary_certificate.html',
                          {'certificate_details': details, 'dzongkhag': dzongkhag})
        else:
            details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(Application_No=application_No,
                                                                                        Certificate_Type='C')
            return render(request, 'certificates/cordyceps_certificate.html',
                          {'certificate_details': details, 'dzongkhag': dzongkhag})
    elif service_code == 'IPP':
        details = t_plant_import_permit_t1.objects.filter(Application_No=application_No, Import_Type='P')
        application_details = t_workflow_details.objects.filter(application_no=application_No)
        details_permit = t_plant_import_permit_t2.objects.filter(Application_No=application_No)
        location_mapping = t_field_office_master.objects.all()
        country = t_country_master.objects.all()
        crop = t_plant_crop_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        if details.exists():
            for date_approved in application_details:
                approved_date = date_approved.action_date
            return render(request, 'certificates/plant_import_permit.html',
                          {'certificate_details': details, 'import': details_permit,
                           'approved_date': approved_date, 'location': location_mapping, 'country': country,
                           'variety': variety, 'crop': crop})
        else:
            details = t_plant_import_permit_t1.objects.filter(Application_No=application_No, Import_Type='A')
            for date_approved in application_details:
                approved_date = date_approved.action_date
            location_mapping = t_field_office_master.objects.all()
            country = t_country_master.objects.all()
            pesticide = t_plant_pesticide_master.objects.all()
            return render(request, 'certificates/agro_import_permit.html',
                          {'certificate_details': details, 'import': details_permit,
                           'approved_date': approved_date, 'location': location_mapping, 'country': country,
                           'pesticide': pesticide})
    elif service_code == 'RNS':
        details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_No)
        application_details = t_workflow_details.objects.filter(application_no=application_No)

        for date_approved in application_details:
            approved_date = date_approved.action_date
        return render(request, 'certificates/nursery_clearance.html',
                      {'certificate_details': details,
                       'approved_date': approved_date})
    elif service_code == 'RSC':
        details = t_plant_seed_certification_t1.objects.filter(Application_No=application_No)
        application_details = t_workflow_details.objects.filter(application_no=application_No)
        details_permit = t_plant_seed_certification_t2.objects.filter(Application_No=application_No)
        for date_approved in application_details:
            approved_date = date_approved.action_date
        crop = t_plant_crop_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        return render(request, 'certificates/seed_certificate.html',
                      {'certificate_details': details, 'details_permit': details_permit,
                       'approved_date': approved_date, 'crop': crop, 'variety': variety})
    elif service_code == 'FFC':
        details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(Application_No=application_No,
                                                                                    Certificate_Type='P')
        application_details = t_workflow_details.objects.filter(application_no=application_No)
        if details.exists():
            return render(request, 'certificates/fit_for_human_consumtion_p.html',
                          {'certificate_details': details})
        else:
            details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(Application_No=application_No,
                                                                                        Certificate_Type='C')
            return render(request, 'certificates/fit_for_human_consumtion_c.html',
                          {'certificate_details': details})
    elif service_code == 'RF':
        details = t_plant_import_permit_inspection_t1.objects.filter(Application_No=application_No)
        details_permit = t_plant_import_permit_inspection_t2.objects.filter(Application_No=application_No)
        country = t_country_master.objects.all()
        crop = t_plant_crop_master.objects.all()
        pesticide = t_plant_pesticide_master.objects.all()
        return render(request, 'certificates/release_form.html',
                      {'certificate_details': details, 'release_form': details_permit,
                       'country': country, 'crop': crop, 'pesticide': pesticide})
    elif service_code == 'APM':
        details = t_livestock_ante_post_mortem_t1.objects.filter(Application_No=application_No)
        details_permit = t_livestock_ante_post_mortem_t2.objects.filter(Application_No=application_No)
        dzongkhag = t_dzongkhag_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        return render(request, 'livestock_certificates/ante_post_mortem/certificate.html',
                      {'certificate_details': details, 'mortem': details_permit,
                       'dzongkhag': dzongkhag, 'location': location})
    elif service_code == 'LMP':
        details = t_livestock_movement_permit_t1.objects.filter(Application_No=application_No)
        details_permit = t_livestock_movement_permit_t2.objects.filter(Application_No=application_No)
        dzongkhag = t_dzongkhag_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        return render(request, 'livestock_certificates/movement_permit/movement_permit.html',
                      {'certificate_details': details, 'details_permit': details_permit,
                       'dzongkhag': dzongkhag, 'location': location})
    elif service_code == 'CMS':
        details = t_livestock_clearance_meat_shop_t1.objects.filter(application_no=application_No)
        for det in details:
            dzongkhag_code = t_dzongkhag_master.objects.filter(Dzongkhag_Code=det.dzongkhag_code)
            for det_dz in dzongkhag_code:
                dzongkhag_code_name = det_dz.Dzongkhag_Name
            village_code = t_village_master.objects.filter(Village_Code=det.village_code)
            for name_vill in village_code:
                village_code_name = name_vill.Village_Name
            gewog_code = t_gewog_master.objects.filter(Gewog_Code=det.gewog_code)
            for gew in gewog_code:
                gewog_code_name = gew.Gewog_Name
        return render(request, 'livestock_certificates/meat_shop_clearance/meat_safety_clearance.html',
                      {'certificate_details': details, 'Dzongkhag': dzongkhag_code_name,
                       'Village': village_code_name, 'Gewog': gewog_code_name})
    elif service_code == 'CCMS':
        details = t_livestock_clearance_meat_shop_t1.objects.filter(application_no=application_No)
        for det in details:
            dzongkhag_code = t_dzongkhag_master.objects.filter(Dzongkhag_Code=det.dzongkhag_code)
            for det_dz in dzongkhag_code:
                dzongkhag_code_name = det_dz.Dzongkhag_Name
            village_code = t_village_master.objects.filter(Village_Code=det.village_code)
            for name_vill in village_code:
                village_code_name = name_vill.Village_Name
            gewog_code = t_gewog_master.objects.filter(Gewog_Code=det.gewog_code)
            for gew in gewog_code:
                gewog_code_name = gew.Gewog_Name
        return render(request, 'livestock_certificates/meat_shop_clearance/conditional_clearance.html',
                      {'certificate_details': details, 'Dzongkhag': dzongkhag_code_name,
                       'Village': village_code_name, 'Gewog': gewog_code_name})
    elif service_code == 'LEC':
        details = t_livestock_export_certificate_t1.objects.filter(Application_No=application_No)
        export_details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_No)
        location = t_location_field_office_mapping.objects.all()
        species = t_livestock_species_master.objects.all()
        field_office = t_field_office_master.objects.all()
        return render(request, 'livestock_certificates/export_certificate/export_certificate.html',
                      {'certificate_details': details, 'location': location, 'export_details': export_details,
                       'species': species, 'field_office': field_office})
    elif service_code == 'ILP':
        details = t_livestock_import_permit_product_t1.objects.filter(Application_No=application_No)
        import_details = t_livestock_import_permit_product_t2.objects.filter(Application_No=application_No)
        location = t_field_office_master.objects.all()
        return render(request, 'livestock_certificates/import/import_permit.html',
                      {'certificate_details': details, 'import': import_details, 'location': location})
    elif service_code == 'IAF':
        details = t_livestock_import_permit_animal_t1.objects.filter(Application_No=application_No)
        import_details = t_livestock_import_permit_animal_t2.objects.filter(Application_No=application_No)
        location = t_field_office_master.objects.all()
        species = t_livestock_species_master.objects.all()
        return render(request, 'livestock_certificates/import/import_permit_animal.html',
                      {'certificate_details': details, 'import': import_details, 'species': species,
                       'location': location})
    elif service_code == 'RFAF':
        details = t_livestock_import_permit_animal_inspection_t1.objects.filter(Application_No=application_No)
        import_details = t_livestock_import_permit_animal_inspection_t2.objects.filter(Application_No=application_No)
        species = t_livestock_species_master.objects.all()
        place_of_issue = t_field_office_master.objects.all()
        return render(request, 'livestock_certificates/import/release_form_animal_fish.html',
                      {'certificate_details': details, 'species': species, 'import': import_details,
                       'place_of_issue': place_of_issue})
    elif service_code == 'RFLP':
        details = t_livestock_import_permit_product_inspection_t1.objects.filter(Application_No=application_No)
        import_details = t_livestock_import_permit_product_inspection_t2.objects.filter(Application_No=application_No)
        place_of_issue = t_field_office_master.objects.all()
        return render(request, 'livestock_certificates/import/release_form.html',
                      {'certificate_details': details, 'import': import_details, 'place_of_issue': place_of_issue})
    # FOOD SECTION
    elif service_code == 'FIP':
        details = t_food_import_permit_t1.objects.filter(Application_No=application_No)
        details_permit = t_food_import_permit_t2.objects.filter(Application_No=application_No)
        for import_details in details:
            field_id = import_details.Place_Of_Entry
            entry_point = t_field_office_master.objects.filter(Field_Office_Id=field_id)
            return render(request, 'food_certificates/Import_permit_food.html',
                          {'certificate_details': details, 'import': details_permit,
                           'entry_point': entry_point})

    elif service_code == 'RFF':
        details = t_food_import_permit_inspection_t1.objects.filter(Clearance_Ref_No=application_No)
        for app in details:
            application_id = app.Application_No
        details_clearance = t_food_import_permit_inspection_t2.objects.filter(Application_No=application_id)

        return render(request, 'food_certificates/release_form_food.html',
                      {'certificate_details': details, 'clearance': details_clearance})

    elif service_code == 'ECF':
        ex_certificate_details = t_food_export_certificate_t1.objects.filter(Application_No=application_No)
        for import_details in ex_certificate_details:
            field_id = import_details.Declared_Point_of_Exit
            entry_point = t_field_office_master.objects.filter(Field_Office_Id=field_id)
            return render(request, 'food_certificates/export_certificate_food.html',
                          {'certificate_details': ex_certificate_details, 'entry_point': entry_point})

    elif service_code == 'CFC':
        cfc_clearance_details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_No)
        details_safety_clearance = t_food_business_registration_licensing_t2.objects.filter(
            application_no=application_No)
        return render(request, 'food_certificates/safety_clearance_food.html',
                      {'cfc_clearance_details': cfc_clearance_details,
                       'details_safety_clearance': details_safety_clearance})

    elif service_code == 'FSL':
        fsl_safety_details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_No)
        details_safety_license = t_food_business_registration_licensing_t2.objects.filter(application_no=application_No)
        return render(request, 'food_certificates/safety_license_food.html',
                      {'fsl_safety_details': fsl_safety_details, 'details_safety_license': details_safety_license})

    elif service_code == 'FHL':
        food_handler_details = t_food_licensing_food_handler_t1.objects.filter(Application_No=application_No)
        file_attach = t_file_attachment.objects.filter(application_no=application_No, attachment_type='FH')
        return render(request, 'food_certificates/handler_license_food.html',
                      {'food_handler_details': food_handler_details, 'file_attach': file_attach})

    # CERTIFICATION SECTION
    elif service_code == 'GAP':
        gap_details = t_certification_gap_t1.objects.filter(Application_No=application_No)
        gap_certificate_details = t_certification_gap_t4.objects.filter(Application_No=application_No)

        return render(request, 'certification_certificates/gap_certificate.html',
                      {'certificate_details': gap_details, 'gap_certificate_details': gap_certificate_details})

    elif service_code == 'ORC':
        orc_details = t_certification_organic_t1.objects.filter(Application_No=application_No)
        orc_certificate_details = t_certification_organic_t4.objects.filter(Application_No=application_No)

        return render(request, 'certification_certificates/organic_certificate.html',
                      {'certificate_details': orc_details, 'orc_certificate_details': orc_certificate_details})

    elif service_code == 'FPC':
        fpc_details = t_certification_food_t1.objects.filter(Application_No=application_No)
        # fpc_certificate_details = t_certification_food_t2.objects.filter(Application_No=application_No)

        return render(request, 'certification_certificates/food_certificate.html',
                      {'certificate_details': fpc_details})
    elif service_code == 'GAP-DET':
        application_details = t_certification_gap_t1.objects.filter(Application_No=application_No)
        details = t_certification_gap_t2.objects.filter(Application_No=application_No)
        audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_No)
        crop_production = t_certification_gap_t4.objects.filter(Application_No=application_No)
        gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_No)
        file = t_file_attachment.objects.filter(application_no=application_No,
                                                attachment_type__isnull=True)
        audit_plan = t_file_attachment.objects.filter(application_no=application_No,
                                                      attachment_type='AP')
        farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_No)
        audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_No)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        user_details = t_user_master.objects.all()
        team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
        team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
        return render(request, 'certification_certificates/gap_details.html',
                      {'application_details': application_details, 'farmer_group': details,
                       'file': file,
                       'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                       'crop_production': crop_production, 'gap_house_details': gap_house_details,
                       'audit_team': audit_team_details, 'team_leader': team_leader,
                       'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                       'user_details': user_details, 'audit_plan': audit_plan,
                       'team_details': team_details})
    elif service_code == 'ORC-DET':
        application_details = t_certification_organic_t1.objects.filter(Application_No=application_No)
        details = t_certification_organic_t2.objects.filter(Application_No=application_No)
        audit_team = t_certification_food_t3.objects.filter(Application_No=application_No)
        crop_production = t_certification_organic_t4.objects.filter(Application_No=application_No)
        processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_No)
        wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_No)
        ah_details = t_certification_organic_t7.objects.filter(Application_No=application_No)
        aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_No)
        api_details = t_certification_organic_t9.objects.filter(Application_No=application_No)
        audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_No)
        audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_No)
        file = t_file_attachment.objects.filter(application_no=application_No,
                                                attachment_type__isnull=True)
        user_details = t_user_master.objects.filter(Login_Type='I')
        team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
        team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
        audit_plan = t_file_attachment.objects.filter(application_no=application_No,
                                                      attachment_type='AP')
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        return render(request, 'certification_certificates/oc_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'crop_production': crop_production, 'audit_team': audit_team,
                       'processing_unit': processing_unit, 'wild_collection': wild_collection,
                       'ah_details': ah_details, 'aqua_details': aqua_details,
                       'api_details': api_details, 'audit_plan': audit_plan,
                       'audit_findings': audit_findings, 'user_details': user_details,
                       'audit_observation': audit_observation, 'team_leader': team_leader,
                       'team_details': team_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village})

    elif service_code == 'FPC-DET':
        application_details = t_certification_food_t1.objects.filter(Application_No=application_No)
        details = t_certification_food_t2.objects.filter(Application_No=application_No)
        inspection_details = t_certification_food_t3.objects.filter(Application_No=application_No)
        file = t_file_attachment.objects.filter(application_no=application_No,
                                                attachment_type__isnull=True)
        audit_findings = t_certification_food_t4.objects.filter(Application_No=application_No)
        audit_observation = t_certification_food_t5.objects.filter(Application_No=application_No)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        team_leader = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
        team_details = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])
        audit_plan = t_file_attachment.objects.filter(application_no=application_No,
                                                      attachment_type='AP')
        return render(request, 'certification_certificates/fpc_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'audit_findings': audit_findings, 'audit_observation': audit_observation,
                       'inspection_details': inspection_details, 'team_details': team_details,
                       'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                       'team_leader': team_leader, 'audit_plan': audit_plan})


# Common Details
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def call_for_inspection(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        application_details = t_workflow_details.objects.filter(assigned_to=login_id, action_date__isnull=False,
                                                                application_status='P')
        service_details = t_service_master.objects.all()
        payment_details = t_payment_details.objects.all()

        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'inspection_call.html',
                      {'application_details': application_details, 'service_details': service_details,
                       'payment_details': payment_details, 'count': message_count, 'count_call': inspection_call_count,
                       'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def application_status(request):
    try:
        login_id = request.session['email']
        login_user = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        application_details = t_workflow_details.objects.filter(applicant_id=login_id,
                                                                action_date__isnull=False)
        service_details = t_service_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_to=login_user, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_user, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_user, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_user, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_user, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_user,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_user,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'application_status.html', {'application_details': application_details,
                                                           'service_details': service_details, 'count': message_count,
                                                           'count_call': inspection_call_count,
                                                           'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def resubmit_application(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        application_details = t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS') \
                              | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS') \
                              | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR') \
                              | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR') \
                              | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')

        service_details = t_service_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'resubmit_application.html', {'application_details': application_details,
                                                             'service_details': service_details, 'count': message_count,
                                                             'count_call': inspection_call_count,
                                                             'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def call_for_inspection_details(request):
    application_no = request.GET.get('application_id')
    service_id = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    if service_id == 'IPP':
        new_import_app = t_plant_import_permit_t1.objects.filter(Application_No=application_no)
        details = t_plant_import_permit_t2.objects.filter(Application_No=application_no, Quantity_Balance__gt=0)
        file = t_file_attachment.objects.filter(application_no=application_no)
        location_mapping = t_field_office_master.objects.filter(Is_Entry_Point="Y")
        country = t_country_master.objects.all()
        crop = t_plant_crop_master.objects.all()
        pesticide = t_plant_pesticide_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        return render(request, 'import_permit/inspection_call_details.html',
                      {'application_details': new_import_app, 'details': details, 'file': file, 'dzongkhag': dzongkhag,
                       'village': village, 'location': location_mapping, 'country': country,
                       'crop': crop, 'pesticide': pesticide, 'variety': variety})
    elif service_id == 'RNS':
        application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_no)
        details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_no)
        file = t_file_attachment.objects.filter(application_no=application_no)
        location_details = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        return render(request, 'nursery_registration/inspection_call_details.html',
                      {'application_details': application_details, 'seed_details': details, 'file': file,
                       'application_no': application_no, 'location': location_details})
    elif service_id == 'ILP':
        application_details = t_livestock_import_permit_product_t1.objects.filter(Application_No=application_no)
        details = t_livestock_import_permit_product_t2.objects.filter(Application_No=application_no,
                                                                      Quantity_Balance__gt=0)
        file = t_file_attachment.objects.filter(application_no=application_no)
        location_details = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        return render(request, 'Livestock_Import/call_for_inspection_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'dzongkhag': dzongkhag, 'village': village, 'location': location,
                       'location_details': location_details})
    elif service_id == 'IAF':
        application_details = t_livestock_import_permit_animal_t1.objects.filter(Application_No=application_no)
        details = t_livestock_import_permit_animal_t2.objects.filter(Application_No=application_no,
                                                                     Quantity_Balance__gt=0)
        file = t_file_attachment.objects.filter(application_no=application_no)
        location_details = t_field_office_master.objects.all()
        location_mapping = t_field_office_master.objects.filter(Is_Entry_Point="Y")
        species = t_livestock_species_master.objects.all()
        return render(request, 'Animal_Fish_Import/call_for_inspection_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'dzongkhag': dzongkhag, 'village': village, 'location': location,
                       'location_details': location_details, 'location_mapping': location_mapping, 'species': species})
    elif service_id == 'FIP':
        application_details = t_food_import_permit_t1.objects.filter(Application_No=application_no)
        details = t_food_import_permit_t2.objects.filter(Application_No=application_no, Quantity_Balance__gt=0)
        file = t_file_attachment.objects.filter(application_no=application_no)
        location_details = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        field_list = t_field_office_master.objects.all()
        country_list = t_country_master.objects.all()
        return render(request, 'import_certificate_food/call_for_inspection_details.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'field_list': field_list, 'country': country_list,
                       'location_details': location_details})


def resubmit_app_details(request, t_certification_gap_t10=None):
    service_code = request.GET.get('service_code')
    appNo = request.GET.get('application_id')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    if service_code == 'RNS':
        application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=appNo)
        seed_details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=appNo)
        file = t_file_attachment.objects.filter(application_no=appNo)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        crop_master = t_plant_crop_master.objects.all()
        crop_category = t_plant_crop_category_master.objects.all()
        return render(request, 'nursery_registration/resubmit_application.html',
                      {'application_details': application_details, 'seed_details': seed_details, 'file': file,
                       'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog, 'location': location,
                       'crop_master': crop_master, 'crop_category': crop_category})
    elif service_code == 'RSC':
        application_details = t_plant_seed_certification_t1.objects.filter(Application_No=appNo)
        seed_details = t_plant_seed_certification_t2.objects.filter(Application_No=appNo)
        file = t_file_attachment.objects.filter(application_no=appNo)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        return render(request, 'seed_certification/resubmit_application.html',
                      {'application_details': application_details, 'details_list': seed_details, 'file': file,
                       'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog, 'location': location})
    elif service_code == 'FBR':
        work_details = t_workflow_details.objects.filter(application_no=appNo)
        for app_status in work_details:
            status = app_status.application_status
            if status == 'IRS':
                application_details = t_food_business_registration_licensing_t1.objects.filter(application_no=appNo)
                details = t_food_business_registration_licensing_t2.objects.filter(application_no=appNo)
                inspection_details = t_food_business_registration_licensing_t5.objects.filter(
                    application_no=appNo, inspection_type='Feasibility Inspection')
                team_details = t_food_business_registration_licensing_t4.objects.filter(
                    application_no=appNo, meeting_type='Feasibility Inspection')
                inspection_team_details = t_food_business_registration_licensing_t6.objects.filter(
                    application_no=appNo, meeting_type='Feasibility Inspection')
                file = t_file_attachment.objects.filter(application_no=appNo)
                unit = t_unit_master.objects.all()
                inspector_list = t_user_master.objects.filter(Role_Id='5')
                return render(request, 'registration_licensing/resubmit_feasibility_inspection.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspector_list': inspector_list, 'unit': unit, 'inspection_details': inspection_details,
                               'team_details': team_details, 'inspection_team_details': inspection_team_details,
                               'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})
            else:
                application_details = t_food_business_registration_licensing_t1.objects.filter(application_no=appNo)
                details = t_food_business_registration_licensing_t2.objects.filter(application_no=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                unit = t_unit_master.objects.all()
                inspection_details = t_food_business_registration_licensing_t5.objects.filter(
                    application_no=appNo, inspection_type='Factory Inspection')
                team_details = t_food_business_registration_licensing_t4.objects.filter(
                    application_no=appNo, meeting_type='Factory Inspection')
                inspection_team_details = t_food_business_registration_licensing_t6.objects.filter(
                    application_no=appNo, meeting_type='Factory Inspection')
                inspector_list = t_user_master.objects.filter(Role_Id='5')
                return render(request, 'registration_licensing/resubmit_factory_inspection.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspector_list': inspector_list, 'unit': unit, 'inspection_details': inspection_details,
                               'team_details': team_details, 'inspection_team_details': inspection_team_details,
                               'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})
    elif service_code == 'OC':
        work_details = t_workflow_details.objects.filter(application_no=appNo)
        for app_status in work_details:
            status = app_status.application_status
            if status == 'ATR':
                application_details = t_certification_organic_t1.objects.filter(Application_No=appNo)
                details = t_certification_organic_t2.objects.filter(Application_No=appNo)
                audit_team = t_certification_food_t3.objects.filter(Application_No=appNo)
                crop_production = t_certification_organic_t4.objects.filter(Application_No=appNo)
                processing_unit = t_certification_organic_t5.objects.filter(Application_No=appNo)
                wild_collection = t_certification_organic_t6.objects.filter(Application_No=appNo)
                ah_details = t_certification_organic_t7.objects.filter(Application_No=appNo)
                aqua_details = t_certification_organic_t8.objects.filter(Application_No=appNo)
                api_details = t_certification_organic_t9.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                user_details = t_user_master.objects.all()
                return render(request, 'organic_certification/audit_team_accept.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'crop_production': crop_production, 'audit_team': audit_team,
                               'processing_unit': processing_unit, 'wild_collection': wild_collection,
                               'ah_details': ah_details, 'aqua_details': aqua_details, 'api_details': api_details,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog,
                               'user_details': user_details})
            elif status == 'APR':
                application_details = t_certification_organic_t1.objects.filter(Application_No=appNo)
                details = t_certification_organic_t2.objects.filter(Application_No=appNo)
                audit_team = t_certification_food_t3.objects.filter(Application_No=appNo)
                crop_production = t_certification_organic_t4.objects.filter(Application_No=appNo)
                processing_unit = t_certification_organic_t5.objects.filter(Application_No=appNo)
                wild_collection = t_certification_organic_t6.objects.filter(Application_No=appNo)
                ah_details = t_certification_organic_t7.objects.filter(Application_No=appNo)
                aqua_details = t_certification_organic_t8.objects.filter(Application_No=appNo)
                api_details = t_certification_organic_t9.objects.filter(Application_No=appNo)
                audit_findings = t_certification_organic_t10.objects.filter(Application_No=appNo)
                audit_observation = t_certification_organic_t11.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()

                return render(request, 'organic_certification/audit_plan_accept.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'crop_production': crop_production, 'audit_team': audit_team,
                               'processing_unit': processing_unit, 'wild_collection': wild_collection,
                               'ah_details': ah_details, 'aqua_details': aqua_details, 'api_details': api_details,
                               'audit_findings': audit_findings, 'audit_observation': audit_observation,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog})
            else:
                application_details = t_certification_organic_t1.objects.filter(Application_No=appNo)
                details = t_certification_organic_t2.objects.filter(Application_No=appNo)
                audit_team = t_certification_food_t3.objects.filter(Application_No=appNo)
                crop_production = t_certification_organic_t4.objects.filter(Application_No=appNo)
                processing_unit = t_certification_organic_t5.objects.filter(Application_No=appNo)
                wild_collection = t_certification_organic_t6.objects.filter(Application_No=appNo)
                ah_details = t_certification_organic_t7.objects.filter(Application_No=appNo)
                aqua_details = t_certification_organic_t8.objects.filter(Application_No=appNo)
                api_details = t_certification_organic_t9.objects.filter(Application_No=appNo)
                audit_findings = t_certification_organic_t10.objects.filter(Application_No=appNo)
                audit_observation = t_certification_organic_t11.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()

                return render(request, 'organic_certification/nc_details.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'crop_production': crop_production, 'audit_team': audit_team,
                               'processing_unit': processing_unit, 'wild_collection': wild_collection,
                               'ah_details': ah_details, 'aqua_details': aqua_details, 'api_details': api_details,
                               'audit_findings': audit_findings, 'audit_observation': audit_observation,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog})
    elif service_code == 'GAP':
        work_details = t_workflow_details.objects.filter(application_no=appNo)
        for app_status in work_details:
            status = app_status.application_status
            if status == 'ATR':
                application_details = t_certification_gap_t1.objects.filter(Application_No=appNo)
                details = t_certification_gap_t2.objects.filter(Application_No=appNo)
                audit_team_details = t_certification_food_t3.objects.filter(Application_No=appNo)
                crop_production = t_certification_gap_t4.objects.filter(Application_No=appNo)
                gap_house_details = t_certification_gap_t5.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                user_details = t_user_master.objects.all()
                return render(request, 'GAP_Certification/audit_team_accept.html',
                              {'application_details': application_details, 'farmer_group': details, 'file': file,
                               'audit_team_details': audit_team_details, 'crop_production': crop_production,
                               'gap_house_details': gap_house_details, 'dzongkhag': dzongkhag, 'village': village,
                               'gewog': gewog, 'user_details': user_details})
            elif status == 'APR':
                application_details = t_certification_gap_t1.objects.filter(Application_No=appNo)
                details = t_certification_gap_t2.objects.filter(Application_No=appNo)
                audit_team_details = t_certification_food_t3.objects.filter(Application_No=appNo)
                crop_production = t_certification_gap_t4.objects.filter(Application_No=appNo)
                gap_house_details = t_certification_gap_t5.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                audit_findings = t_certification_gap_t7.objects.filter(Application_No=appNo)
                audit_observation = t_certification_gap_t8.objects.filter(Application_No=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'GAP_Certification/audit_plan_accept.html',
                              {'application_details': application_details, 'farmer_group': details, 'file': file,
                               'audit_findings': audit_findings, 'audit_observation': audit_observation,
                               'crop_production': crop_production, 'gap_house_details': gap_house_details,
                               'audit_team_details': audit_team_details, 'dzongkhag': dzongkhag, 'village': village,
                               'gewog': gewog})
            else:
                application_details = t_certification_gap_t1.objects.filter(Application_No=appNo)
                details = t_certification_gap_t2.objects.filter(Application_No=appNo)
                audit_team_details = t_certification_food_t3.objects.filter(Application_No=appNo)
                crop_production = t_certification_gap_t4.objects.filter(Application_No=appNo)
                gap_house_details = t_certification_gap_t5.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                audit_observation = t_certification_gap_t8.objects.filter(Application_No=appNo)
                farm_inputs = t_certification_gap_t7.objects.filter(Application_No=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'GAP_Certification/nc_details.html',
                              {'application_details': application_details, 'farmer_group': details, 'file': file,
                               'audit_observation': audit_observation,
                               'crop_production': crop_production, 'gap_house_details': gap_house_details,
                               'audit_team_details': audit_team_details, 'dzongkhag': dzongkhag, 'village': village,
                               'gewog': gewog, 'farm_inputs': farm_inputs})
    elif service_code == 'FPC':
        work_details = t_workflow_details.objects.filter(application_no=appNo)
        for app_status in work_details:
            status = app_status.application_status
            if status == 'ATR':
                application_details = t_certification_food_t1.objects.filter(Application_No=appNo)
                details = t_certification_food_t2.objects.filter(Application_No=appNo)
                inspection_details = t_certification_food_t3.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                audit_team_details = t_certification_food_t3.objects.filter(Application_No=appNo)
                user_details = t_user_master.objects.all()
                return render(request, 'food_product_certification/audit_team_accept.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspection_details': inspection_details, 'dzongkhag': dzongkhag, 'village': village,
                               'gewog': gewog, 'audit_team_details': audit_team_details, 'user_details': user_details})
            elif status == 'APR':
                application_details = t_certification_food_t1.objects.filter(Application_No=appNo)
                details = t_certification_food_t2.objects.filter(Application_No=appNo)
                inspection_details = t_certification_food_t3.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                audit_findings = t_certification_food_t4.objects.filter(Application_No=appNo)
                audit_observation = t_certification_food_t4.objects.filter(Application_No=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'food_product_certification/audit_plan_accept.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'audit_findings': audit_findings, 'audit_observation': audit_observation,
                               'inspection_details': inspection_details, 'dzongkhag': dzongkhag, 'village': village,
                               'gewog': gewog})
            else:
                application_details = t_certification_food_t1.objects.filter(Application_No=appNo)
                details = t_certification_food_t2.objects.filter(Application_No=appNo)
                inspection_details = t_certification_food_t3.objects.filter(Application_No=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                audit_findings = t_certification_food_t4.objects.filter(Application_No=appNo)
                audit_observation = t_certification_food_t5.objects.filter(Application_No=appNo)
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'food_product_certification/nc_details.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'audit_findings': audit_findings, 'audit_observation': audit_observation,
                               'inspection_details': inspection_details, 'dzongkhag': dzongkhag, 'village': village,
                               'gewog': gewog})
    elif service_code == 'CMS':
        work_details = t_workflow_details.objects.filter(application_no=appNo)
        for app_status in work_details:
            status = app_status.application_status
            if status == 'IRS':
                application_details = t_livestock_clearance_meat_shop_t1.objects.filter(application_no=appNo)
                details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=appNo)
                inspection_details = t_livestock_clearance_meat_shop_t5.objects.filter(
                    application_no=appNo, inspection_type='Feasibility Inspection')
                team_details = t_livestock_clearance_meat_shop_t4.objects.filter(
                    application_no=appNo, meeting_type='Feasibility Inspection')
                inspection_team_details = t_livestock_clearance_meat_shop_t6.objects.filter(
                    application_no=appNo, meeting_type='Feasibility Inspection')
                file = t_file_attachment.objects.filter(application_no=appNo)
                unit = t_unit_master.objects.all()
                inspector_list = t_user_master.objects.filter(Role_Id='5')
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'meat_shop_registration/resubmit_feasibility_inspection.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspector_list': inspector_list, 'unit': unit, 'inspection_details': inspection_details,
                               'team_details': team_details, 'inspection_team_details': inspection_team_details,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog})
            else:
                application_details = t_livestock_clearance_meat_shop_t1.objects.filter(application_no=appNo)
                details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=appNo)
                file = t_file_attachment.objects.filter(application_no=appNo)
                unit = t_unit_master.objects.all()
                inspection_details = t_livestock_clearance_meat_shop_t5.objects.filter(
                    application_no=appNo, inspection_type='Factory Inspection')
                team_details = t_livestock_clearance_meat_shop_t4.objects.filter(
                    application_no=appNo, meeting_type='Factory Inspection')
                inspection_team_details = t_livestock_clearance_meat_shop_t6.objects.filter(
                    application_no=appNo, meeting_type='Factory Inspection')
                inspector_list = t_user_master.objects.filter(Role_Id='5')
                dzongkhag = t_dzongkhag_master.objects.all()
                gewog = t_gewog_master.objects.all()
                village = t_village_master.objects.all()
                return render(request, 'meat_shop_registration/resubmit_factory_inspection.html',
                              {'application_details': application_details, 'details': details, 'file': file,
                               'inspector_list': inspector_list, 'unit': unit, 'inspection_details': inspection_details,
                               'team_details': team_details, 'inspection_team_details': inspection_team_details,
                               'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog})


def validate_receipt_no(request):
    data = dict()
    receipt_no = request.GET.get('receipt_no')
    application_list = t_payment_details.objects.filter(receipt_no=receipt_no)
    if application_list.exists():
        status = "Exists"
        data['status'] = status
        return JsonResponse(data)


def get_citizen_details(request):
    data = dict()
    cid = request.GET.get('cidNo')
    BASE_URL = 'https://datahub-apim.dit.gov.bt/dcrc_citizen_details_api/1.0.0/citizendetails/' + cid
    token = get_auth_token()

    headers = {'Authorization': "Bearer {}".format(token)}
    response = requests.get(BASE_URL, headers=headers, verify=False)

    data['response'] = response.json()
    return JsonResponse(data)


def get_auth_token():
    """
    get an auth token
    """
    credentials = {'client_id': 'GJ3SJ3TIgnPGRc3YhsFG8KDlWw4a',
                   'client_secret': 'P2Rvmzw23o37CTOfkwXQufAcCu0a',
                   'grant_type': 'client_credentials'}

    headers = {'Accept': 'application/json'}

    res = requests.post('https://datahub-apim.dit.gov.bt/token', params=credentials,
                        headers=headers, verify=False)

    json = res.json()
    return json["access_token"]


def update_payment_details(application_no, permit_no, service_code, validity_date, Permit_Type, account_head_code):
    account_details = t_payment_details_master.objects.filter(account_head_code=account_head_code)
    for pay_details in account_details:
        fees = pay_details.service_fee
        service_name = pay_details.service_name
        t_payment_details.objects.create(application_no=application_no,
                                         application_date=date.today(),
                                         permit_no=permit_no,
                                         service_id=service_code,
                                         validity=validity_date,
                                         payment_type=None,
                                         instrument_no=None,
                                         amount=fees,
                                         receipt_no=None,
                                         receipt_date=None,
                                         updated_by=None,
                                         updated_on=None,
                                         permit_type=Permit_Type,
                                         account_head_code=account_head_code)
        cl = Client('https://www.citizenservices.gov.bt/G2CPaymentAggregator/services/G2CPaymentInitiatorBusiness?wsdl')
        order_type = cl.get_type('ns1:PaymentDTO')
        paymentList = order_type(accountHeadId=account_head_code, serviceFee=fees)
        post_data = {'agencyCode': "BAFRA", 'applicationNo': application_no,
                     'serviceName': service_name,
                     'paymentList': paymentList}
        cl.service.insertPaymentDetailsOnApproval(post_data)


@csrf_exempt
def delete_details(request):
    identification_type = request.GET.get('identification_type')
    # Plant Section Delete
    if identification_type == 'PIP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_plant_import_permit_t2.objects.filter(Record_Id=record_id)
        details.delete()
        import_details = t_plant_import_permit_t2.objects.filter(Application_No=application_no).order_by('Record_Id')
        crop = t_plant_crop_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        count = t_plant_import_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'import_permit/import_page_plant.html', {'import': import_details, 'crop': crop,
                                                                        'variety': variety, 'count': count})
    elif identification_type == 'AIP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_plant_import_permit_t2.objects.filter(Record_Id=record_id)
        details.delete()
        import_details = t_plant_import_permit_t2.objects.filter(Application_No=application_no).order_by('Record_Id')
        pesticide = t_plant_pesticide_master.objects.all()
        count = t_plant_import_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'import_permit/import_page_agro.html', {'import': import_details, 'pesticide': pesticide,
                                                                       'count': count})
    elif identification_type == 'RNS':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Record_Id=record_id)
        details.delete()
        seed_details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_no).count()
        crop_master = t_plant_crop_master.objects.all()
        crop_category = t_plant_crop_category_master.objects.all()
        return render(request, 'nursery_registration/seed_details_page.html', {'seed_details': seed_details,
                                                                               'seed_details_count': count,
                                                                               'crop_master': crop_master,
                                                                               'crop_category': crop_category})
    elif identification_type == 'RSC':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_plant_seed_certification_t2.objects.filter(Record_Id=record_id)
        details.delete()
        certification_details = t_plant_seed_certification_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_plant_seed_certification_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'seed_certification/seed_certification_details_page.html',
                      {'certification_details': certification_details, 'seed_details_count': count})
    elif identification_type == 'MPP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_plant_movement_permit_t2.objects.filter(Record_Id=record_id)
        details.delete()
        imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=application_no).order_by('Record_Id')
        count = t_plant_movement_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'movement_permit/movement_page.html', {'import': imports_plant, 'movement_count': count})
    elif identification_type == 'PEC':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(Record_Id=record_id)
        details.delete()
        export_details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(
            Application_No=application_no).order_by('Record_Id')
        count = t_plant_export_certificate_plant_plant_products_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'export_permit/phyto_details_page.html', {'export_details': export_details,
                                                                         'export_count': count})
    # Livestock Section Delete

    elif identification_type == 'CMS':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_livestock_clearance_meat_shop_t2.objects.filter(record_id=record_id)
        details.delete()
        meat_details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=application_no) \
            .order_by('record_id')
        count = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=application_no).count()
        return render(request, 'meat_shop_registration/details.html', {'meat_details': meat_details,
                                                                       'count': count})
    elif identification_type == 'ALEC':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_livestock_export_certificate_t2.objects.filter(Record_Id=record_id)
        details.delete()
        export_details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no).count()
        species = t_livestock_species_master.objects.all()
        return render(request, 'Export_Certificate/animal_details.html', {'export_details': export_details,
                                                                          'count': count, 'species': species})
    elif identification_type == 'APLEC':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_livestock_export_certificate_t2.objects.filter(Record_Id=record_id)
        details.delete()
        export_details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'Export_Certificate/animal_product_details.html', {'export_details': export_details,
                                                                                  'count': count})
    elif identification_type == 'LPIP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_livestock_import_permit_product_t2.objects.filter(Record_Id=record_id)
        details.delete()
        import_details = t_livestock_import_permit_product_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_livestock_import_permit_product_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'Livestock_Import/permit_details.html', {'import': import_details, 'count': count})
    elif identification_type == 'AFIP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_livestock_import_permit_animal_t2.objects.filter(Record_Id=record_id)
        details.delete()
        import_details = t_livestock_import_permit_animal_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_livestock_import_permit_animal_t2.objects.filter(Application_No=application_no).count()
        species = t_livestock_species_master.objects.all()
        return render(request, 'Animal_Fish_Import/animal_details.html', {'import': import_details, 'count': count,
                                                                          'species': species})
    elif identification_type == 'APM':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_livestock_ante_post_mortem_t2.objects.filter(Record_Id=record_id)
        details.delete()
        mortem_details = t_livestock_ante_post_mortem_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_livestock_ante_post_mortem_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'ante_post_mortem/details.html', {'mortem': mortem_details, 'count': count})
    elif identification_type == 'ALMP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_livestock_movement_permit_t2.objects.filter(Record_Id=record_id)
        details.delete()
        movement_details = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'Movement_Permit_Livestock/animal_details.html', {'import': movement_details,
                                                                                 'count': count})
    elif identification_type == 'APLMP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_livestock_movement_permit_t2.objects.filter(Record_Id=record_id)
        details.delete()
        movement_details = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        count = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'Movement_Permit_Livestock/animal_details.html', {'import': movement_details,
                                                                                 'count': count})

    # Food Section Delete

    elif identification_type == 'FBR-OP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_food_business_registration_licensing_t2.objects.filter(record_id=record_id)
        details.delete()
        fh_details = t_food_business_registration_licensing_t2.objects.filter(application_no=application_no) \
            .order_by('record_id')
        count = t_food_business_registration_licensing_t2.objects.filter(application_no=application_no).count()
        return render(request, 'registration_licensing/details.html', {'fh_details': fh_details,
                                                                       'count': count})
    elif identification_type == 'FBR-FH':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_food_business_registration_licensing_t3.objects.filter(record_id=record_id)
        details.delete()
        fh_details = t_food_business_registration_licensing_t3.objects.filter(application_no=application_no) \
            .order_by('record_id')
        count = t_food_business_registration_licensing_t3.objects.filter(application_no=application_no).count()
        return render(request, 'registration_licensing/food_handler_details.html', {'fh_details': fh_details,
                                                                                    'count': count})
    elif identification_type == 'FBR-RM':
        application_no = request.GET.get('edit_raw_application_no')
        record_id = request.GET.get('raw_record_id')
        raw_materials_details = t_food_business_registration_licensing_t7.objects.filter(record_id=record_id)
        raw_materials_details.delete()
        raw_materials = t_food_business_registration_licensing_t7.objects.filter(
            application_no=application_no).order_by('record_id')
        raw_count = t_food_business_registration_licensing_t7.objects.filter(application_no=application_no).count()
        return render(request, 'registration_licensing/raw_material_details.html', {'raw_materials': raw_materials,
                                                                                    'raw_count': raw_count})
    elif identification_type == 'FBR-PM':
        application_no = request.GET.get('edit_packaging_application_no')
        record_id = request.GET.get('packaging_record_id')
        packaging_material_details = t_food_business_registration_licensing_t8.objects.filter(record_id=record_id)
        packaging_material_details.delete()
        packaging_material = t_food_business_registration_licensing_t8.objects.filter(
            application_no=application_no).order_by('record_id')
        packaging_count = t_food_business_registration_licensing_t8.objects.filter(
            application_no=application_no).count()
        return render(request, 'registration_licensing/packaging_material_details.html',
                      {'packaging_material': packaging_material, 'packaging_count': packaging_count})
    elif identification_type == 'FIP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_food_import_permit_t2.objects.filter(Record_Id=record_id)
        details.delete()
        import_details = t_food_import_permit_t2.objects.filter(Application_No=application_no).order_by('Record_Id')
        count = t_food_import_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'import_certificate_food/food_permit_details.html',
                      {'import': import_details, 'count': count})

    # Certification
    elif identification_type == 'GAP-CP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_certification_gap_t4.objects.filter(Record_Id=record_id)
        details.delete()
        crop_production_details = t_certification_gap_t4.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        return render(request, 'GAP_Certification/crop_production_details.html',
                      {'crop_production_details': crop_production_details})
    elif identification_type == 'GAP-PH':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_certification_gap_t5.objects.filter(Record_Id=record_id)
        details.delete()
        pack_house_details = t_certification_gap_t5.objects.filter(Application_No=application_no).order_by('Record_Id')
        return render(request, 'GAP_Certification/pack_house_details.html',
                      {'pack_house_details': pack_house_details})
    elif identification_type == 'OC-CP':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_certification_organic_t4.objects.filter(Record_Id=record_id)
        details.delete()
        pack_house_details = t_certification_organic_t4.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        return render(request, 'organic_Certification/crop_production_details.html',
                      {'pack_house_details': pack_house_details})
    elif identification_type == 'OC-WC':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_certification_organic_t6.objects.filter(Record_Id=record_id)
        details.delete()
        wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_no).order_by('Record_Id')
        return render(request, 'organic_certification/wild_collection_details.html',
                      {'wild_collection': wild_collection})
    elif identification_type == 'OC-AH':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_certification_organic_t7.objects.filter(Record_Id=record_id)
        details.delete()
        animal_husbandry = t_certification_organic_t7.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        return render(request, 'organic_certification/animal_husbandry_details.html',
                      {'animal_husbandry': animal_husbandry})
    elif identification_type == 'OC-AQUA':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_certification_organic_t8.objects.filter(Record_Id=record_id)
        details.delete()
        aquaculture_details = t_certification_organic_t8.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        return render(request, 'organic_certification/aquaculture_details.html',
                      {'aquaculture_details': aquaculture_details})
    elif identification_type == 'OC-API':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_certification_organic_t9.objects.filter(Record_Id=record_id)
        details.delete()
        apiculture_details = t_certification_organic_t9.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')
        return render(request, 'organic_certification/api_culture_details.html',
                      {'apiculture_details': apiculture_details})
    elif identification_type == 'OC-PU':
        application_no = request.GET.get('Application_No')
        record_id = request.GET.get('Record_Id')
        details = t_certification_organic_t5.objects.filter(Record_Id=record_id)
        details.delete()
        processing_details = t_certification_organic_t5.objects.filter(Application_No=application_no) \
            .order_by('Record_Id')

        return render(request, 'organic_certification/processing_unit_details.html',
                      {'processing_details': processing_details})


@csrf_exempt
def update_edit_details(request):
    identification_type = request.POST.get('identifier')

    if identification_type == 'PIP':
        application_no = request.POST['edit_plant_applicationNo']
        record_id = request.POST['record_id']
        Import_Category = request.POST['edit_plant_import_category']
        crop_variety_id = request.POST['edit_crop_variety']
        crop_id = request.POST['edit_crop_id']
        unit = request.POST['edit_unit']
        qty = request.POST['edit_qty']

        details = t_plant_import_permit_t2.objects.filter(Record_Id=record_id)

        details.update(Import_Category=Import_Category, Crop_Id=crop_id,
                       Variety_Id=crop_variety_id, Unit=unit, Quantity=qty,
                       Quantity_Balance=qty)
        crop = t_plant_crop_master.objects.all()
        variety = t_plant_crop_variety_master.objects.all()
        import_details = t_plant_import_permit_t2.objects.filter(Application_No=application_no).order_by('Record_Id')
        count = t_plant_import_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'import_permit/import_page_plant.html', {'import': import_details, 'crop': crop,
                                                                        'variety': variety, 'count': count})
    elif identification_type == 'AIP':
        application_no = request.POST['edit_agro_applicationNo']
        record_id = request.POST['edit_agro_record_id']
        Import_Category = request.POST['edit_agro_category']
        pesticide_id = request.POST['edit_pesticide_id']
        description = request.POST['edit_description']
        unit = request.POST['edit_agro_unit']
        qty = request.POST['edit_agro_qty']

        details = t_plant_import_permit_t2.objects.filter(Record_Id=record_id)

        details.update(Import_Category=Import_Category, Pesticide_Id=pesticide_id, Description=description,
                       Unit=unit, Quantity=qty, Quantity_Balance=qty)
        pesticide = t_plant_pesticide_master.objects.all()
        import_details = t_plant_import_permit_t2.objects.filter(Application_No=application_no).order_by('Record_Id')
        count = t_plant_import_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'import_permit/import_page_agro.html',
                      {'import': import_details, 'pesticide': pesticide, 'agro_count': count})
    elif identification_type == 'RNS':
        application_no = request.POST.get('edit_nursery_appNo')
        record_id = request.POST.get('nursery_record_id')
        crop_id = request.POST.get('edit_crop_id')
        crop_category_id = request.POST.get('edit_crop_category_id')
        crop_variety_id = request.POST.get('edit_crop_variety')
        Source = request.POST.get('edit_Source')
        qty = request.POST.get('edit_qty')
        unit = request.POST.get('edit_unit')
        remarks = request.POST.get('edit_remarks')
        details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Record_Id=record_id)
        details.update(
            Crop_Category=crop_category_id,
            Crop=None,
            Crop_Scientific_Name=crop_id,
            Variety=crop_variety_id,
            Source=Source,
            Qty=qty,
            Unit=unit,
            Remarks=remarks)

        seed_details = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_no).count()
        crop_master = t_plant_crop_master.objects.all()
        crop_category = t_plant_crop_category_master.objects.all()
        return render(request, 'nursery_registration/seed_details_page.html', {'seed_details': seed_details,
                                                                               'seed_details_count': count,
                                                                               'crop_master': crop_master,
                                                                               'crop_category': crop_category})
    elif identification_type == 'RSC':
        application_no = request.POST.get('edit_app_No')
        record_id = request.POST.get('seed_record_id')
        crop_id = request.POST.get('edit_crop_id')
        crop_variety_id = request.POST.get('edit_crop_variety')
        Source = request.POST.get('edit_Source')
        qty = request.POST.get('edit_qty')
        unit = request.POST.get('edit_Unit')
        purpose = request.POST.get('edit_purpose')

        details = t_plant_seed_certification_t2.objects.filter(Record_Id=record_id)

        details.update(
            Crop=crop_id,
            Variety=crop_variety_id,
            Seed_Source=Source,
            Quantity=qty,
            Unit=unit,
            Purpose=purpose,
        )

        certification_details = t_plant_seed_certification_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_plant_seed_certification_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'seed_certification/seed_certification_details_page.html',
                      {'certification_details': certification_details, 'seed_details_count': count})
    elif identification_type == 'MPP':
        application_no = request.POST.get('edit_app_No')
        record_id = request.POST.get('movement_record_id')
        commodity = request.POST.get('edit_commodity')
        qty = request.POST.get('edit_qty')
        unit = request.POST.get('edit_unit')
        remarks = request.POST.get('edit_remarks')
        details = t_plant_movement_permit_t2.objects.filter(Record_Id=record_id)

        details.update(Commodity=commodity, Qty=qty, Unit=unit, Remarks=remarks)

        imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=application_no).order_by('Record_Id')
        count = t_plant_movement_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'movement_permit/movement_page.html', {'import': imports_plant,
                                                                      'movement_count': count})

    elif identification_type == 'PEC':
        record_id = request.POST.get('record_id')
        application_no = request.POST.get('edit_application_no')
        botanical_name = request.POST.get('edit_p_Botanical_Name')
        common_name = request.POST.get('edit_p_Common_Name')
        description = request.POST.get('edit_p_Description')
        quantity = request.POST.get('edit_quantity')
        unit = request.POST.get('edit_unit')
        gross_weight = request.POST.get('edit_gross_weight')
        net_weight = request.POST.get('edit_net_weight')

        plant_export_details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(Record_Id=record_id)
        plant_export_details.update(Botanical_Name=botanical_name,
                                    Common_Name=common_name,
                                    Description=description,
                                    Quantity=quantity, Unit=unit,
                                    Gross_Weight=gross_weight,
                                    Net_Weight=net_weight)
        export_details = t_plant_export_certificate_plant_plant_products_t2.objects.filter(
            Application_No=application_no).order_by('Record_Id')
        return render(request, 'export_permit/phyto_details_page.html', {'export_details': export_details})

    # Livestock Section Update

    elif identification_type == 'CMS':
        application_no = request.POST.get('meat_item_application_no')
        record_id = request.POST.get('edit_meat_record_id')
        meat_name = request.POST.get('edit_meat_name')

        details = t_livestock_clearance_meat_shop_t2.objects.filter(record_id=record_id)
        details.update(meat_item=meat_name)

        meat_details = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=application_no).order_by(
            'record_id')
        count = t_livestock_clearance_meat_shop_t2.objects.filter(application_no=application_no).count()
        return render(request, 'meat_shop_registration/details.html', {'meat_details': meat_details,
                                                                       'count': count})
    elif identification_type == 'ALEC':
        application_no = request.POST.get('animal_application_no')
        record_id = request.POST.get('edit_record_id')
        Species = request.POST.get('edit_Species')
        Breed = request.POST.get('edit_Breed')
        Age = request.POST.get('edit_Age')
        Sex = request.POST.get('edit_Sex')
        No_Of_Animal = request.POST.get('edit_no')
        Remarks = request.POST.get('edit_AP_Remarks')
        Description = request.POST.get('edit_animal_Description')

        details = t_livestock_export_certificate_t2.objects.filter(Record_Id=record_id)
        details.update(
            Species=Species,
            Breed=Breed,
            Age=Age,
            Sex=Sex,
            Description=Description,
            Remarks=Remarks,
            No_Of_Animal=No_Of_Animal,
        )

        export_details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no).count()
        species = t_livestock_species_master.objects.all()
        return render(request, 'Export_Certificate/animal_details.html', {'export_details': export_details,
                                                                          'count': count, 'species': species})
    elif identification_type == 'APLEC':
        application_no = request.POST.get('edit_application_no')
        record_id = request.POST.get('edit_product_record_id')

        Particulars = request.POST.get('edit_Particulars')
        Company_Name = request.POST.get('edit_Company_Name')
        Quantity = request.POST.get('edit_qty')
        Unit = request.POST.get('edit_unit')
        Remarks = request.POST.get('edit_remarks')
        details = t_livestock_export_certificate_t2.objects.filter(Record_Id=record_id)
        details.update(
            Particulars=Particulars,
            Company_Name=Company_Name,
            Quantity=Quantity,
            Remarks=Remarks,
            Unit=Unit
        )

        export_details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'Export_Certificate/animal_product_details.html', {'export_details': export_details,
                                                                                  'count': count})
    elif identification_type == 'LPIP':
        application_no = request.POST.get('edit_applNo')
        record_id = request.POST.get('edit_product_record_id')
        Particulars = request.POST.get('edit_Particulars')
        Company_Name = request.POST.get('edit_Company_Name')
        Description = request.POST.get('edit_Description')
        Quantity = request.POST.get('edit_qty')
        Unit = request.POST.get('edit_unit')

        details = t_livestock_import_permit_product_t2.objects.filter(Record_Id=record_id)

        details.update(Particulars=Particulars,
                       Company_Name=Company_Name, Description=Description,
                       Quantity=Quantity, Quantity_Balance=Quantity, Unit=Unit)

        import_details = t_livestock_import_permit_product_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_livestock_import_permit_product_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'Livestock_Import/permit_details.html', {'import': import_details, 'count': count})
    elif identification_type == 'AFIP':
        application_no = request.POST.get('edit_app_no')
        record_id = request.POST.get('edit_la_record_id')

        Species = request.POST.get('edit_Species')
        Breed = request.POST.get('edit_Breed')
        Age = request.POST.get('edit_Age')
        Sex = request.POST.get('edit_Sex')
        No_Of_Animal = request.POST.get('edit_no')
        Description = request.POST.get('edit_animal_Description')

        details = t_livestock_import_permit_animal_t2.objects.filter(Record_Id=record_id)

        details.update(Species=Species,
                       Breed=Breed,
                       Age=Age,
                       Sex=Sex,
                       Description=Description,
                       Quantity=No_Of_Animal,
                       Quantity_Balance=No_Of_Animal,
                       )
        import_details = t_livestock_import_permit_animal_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_livestock_import_permit_animal_t2.objects.filter(Application_No=application_no).count()
        species = t_livestock_species_master.objects.all()
        return render(request, 'Animal_Fish_Import/animal_details.html', {'import': import_details, 'count': count,
                                                                          'species': species})
    elif identification_type == 'APM':
        application_no = request.POST.get('edit_application_no')
        record_id = request.POST.get('edit_mortem_record_id')
        species = request.POST.get('edit_Species')
        Nos = request.POST.get('edit_Nos')
        qty = request.POST.get('edit_qty')
        remarks = request.POST.get('edit_remarks')

        details = t_livestock_ante_post_mortem_t2.objects.filter(Record_Id=record_id)
        details.update(Species=species, Nos=Nos, Quantity=qty, Remarks=remarks)

        mortem_details = t_livestock_ante_post_mortem_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_livestock_ante_post_mortem_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'ante_post_mortem/details.html', {'mortem': mortem_details,
                                                                 'count': count})
    elif identification_type == 'ALMP':
        application_no = request.POST.get('edit_animal_application_no')
        record_id = request.POST.get('edit_animal_record_id')
        Common_Name = request.POST.get('edit_Common_Name')
        Scientific_Name = request.POST.get('edit_Scientific_Name')
        Age = request.POST.get('edit_Age')
        No_Of_Animal = request.POST.get('edit_No_Of_Animal')
        Remarks = request.POST.get('edit_Animal_Remarks')

        details = t_livestock_movement_permit_t2.objects.filter(Record_Id=record_id)

        details.update(
            Common_Name=Common_Name,
            Scientific_Name=Scientific_Name,
            Age=Age,
            Remarks=Remarks,
            No_Of_Animal=No_Of_Animal)

        movement_details = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'Movement_Permit_Livestock/animal_details.html', {'import': movement_details,
                                                                                 'count': count})
    elif identification_type == 'APLMP':
        application_no = request.POST.get('edit_app_No')
        record_id = request.POST.get('edit_product_record_id')
        Particulars = request.POST.get('edit_Particulars')
        Company_Name = request.POST.get('edit_Company_Name')
        Quantity = request.POST.get('edit_qty')
        Unit = request.POST.get('edit_unit')
        Remarks = request.POST.get('edit_remarks')

        details = t_livestock_movement_permit_t2.objects.filter(Record_Id=record_id)

        details.update(
            Particulars=Particulars,
            Company_Name=Company_Name,
            Quantity=Quantity,
            Unit=Unit,
            Remarks=Remarks)

        movement_details = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        count = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'Movement_Permit_Livestock/animal_product_details.html', {'import': movement_details,
                                                                                         'count': count})

    # Food Section Edit

    elif identification_type == 'FBR-OP':
        application_no = request.POST.get('edit_op_application_no')
        record_id = request.POST.get('op_record_id')
        BP_Outsourced_To = request.POST.get('edit_name')
        Contact_No = request.POST.get('edit_contact_number')
        Address = request.POST.get('edit_address')
        BAFRA_License_No = request.POST.get('edit_bafra_license_no')

        details = t_food_business_registration_licensing_t2.objects.filter(record_id=record_id)

        details.update(bp_outsourced_to=BP_Outsourced_To, contact_no=Contact_No,
                       address=Address, bafra_license_no=BAFRA_License_No)
        fh_details = t_food_business_registration_licensing_t2.objects.filter(application_no=application_no).order_by(
            'record_id')
        count = t_food_business_registration_licensing_t2.objects.filter(application_no=application_no).count()
        return render(request, 'registration_licensing/details.html', {'fh_details': fh_details,
                                                                       'count': count})
    elif identification_type == 'FBR-FH':
        application_no = request.POST.get('edit_fh_application_no')
        record_id = request.POST.get('fh_record_id')
        fh_name = request.POST.get('edit_fh_name')
        fh_license = request.POST.get('edit_fh_license')

        details = t_food_business_registration_licensing_t3.objects.filter(record_id=record_id)
        details.update(fh_name=fh_name, fh_license_no=fh_license)

        fh_details = t_food_business_registration_licensing_t3.objects.filter(application_no=application_no).order_by(
            'record_id')
        return render(request, 'registration_licensing/food_handler_details.html', {'fh_details': fh_details})
    elif identification_type == 'FIP':
        application_no = request.POST.get('edit_import_app_no')
        record_id = request.POST.get('import_record_id')
        Common_Name = request.POST.get('edit_Common_Name')
        Product_Category = request.POST.get('edit_Product_Category')
        characteristics = request.POST.get('edit_characteristics')
        quantity = request.POST.get('edit_qty')
        unit = request.POST.get('edit_unit')
        exporter_type = request.POST.get('Edit_Export_Type')

        details = t_food_import_permit_t2.objects.filter(Record_Id=record_id)

        details.update(Common_Name=Common_Name, Product_Category=Product_Category,
                       Product_Characteristics=characteristics, Quantity=quantity,
                       Unit=unit, Exporter_Type=exporter_type, Quantity_Balance=quantity)

        import_details = t_food_import_permit_t2.objects.filter(Application_No=application_no).order_by('Record_Id')
        count = t_food_import_permit_t2.objects.filter(Application_No=application_no).count()
        return render(request, 'import_certificate_food/food_permit_details.html', {'import': import_details,
                                                                                    'count': count})

    # certification
    elif identification_type == 'GAP-FG':
        application_no = request.POST.get('edit_farmers_group_application_no')
        record_id = request.POST.get('farmers_group_record_id')
        cid = request.POST.get('edit_farmers_group_cid')
        name = request.POST.get('edit_farmers_group_fullname')
        details = t_certification_gap_t2.objects.filter(Record_Id=record_id)
        details.update(CID=cid, Name=name)
        farmers_group_details = t_certification_gap_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        return render(request, 'GAP_Certification/farmer_group_details.html',
                      {'farmers_group_details': farmers_group_details})
    elif identification_type == 'GAP-CP':
        application_no = request.POST.get('edit_crop_production_app_no')
        record_id = request.POST.get('crop_record_id')
        crop_name = request.POST.get('edit_crop_name')
        area = request.POST.get('edit_area')
        area_unit = request.POST.get('edit_area_unit')
        prev_year = request.POST.get('edit_prev_year')
        to_year = request.POST.get('edit_to_year')
        yields = request.POST.get('edit_yield')
        Yield_Unit = request.POST.get('edit_Yield_Unit')
        harvest_month = request.POST.get('edit_harvest_month')
        sold = request.POST.get('edit_sold')
        balance_stock = request.POST.get('edit_balance_stock')
        current_year = request.POST.get('edit_current_year')
        to_current_year = request.POST.get('edit_to_current_year')
        estimated_yield = request.POST.get('edit_estimated_yield')
        estimated_Yield_Unit = request.POST.get('edit_estimated_Yield_Unit')
        estimated_harvest_month = request.POST.get('edit_estimated_harvest_month')
        p_from = datetime.strptime(prev_year, '%d-%m-%Y').date()
        p_to = datetime.strptime(to_year, '%d-%m-%Y').date()
        c_from = datetime.strptime(current_year, '%d-%m-%Y').date()
        c_to = datetime.strptime(to_current_year, '%d-%m-%Y').date()
        details = t_certification_gap_t4.objects.filter(Record_Id=record_id)
        details.update(
            Crop_Name=crop_name,
            Area_Cultivated=area,
            Unit=area_unit,
            P_From_Date=p_from,
            P_To_Date=p_to,
            P_Yield=yields,
            P_Yield_Unit=Yield_Unit,
            P_Harvest_Month=harvest_month,
            P_Sold=sold,
            P_Balance_Stock=balance_stock,
            C_From_Date=c_from,
            C_To_Date=c_to,
            C_Estimated_Yield=estimated_yield,
            C_Yield_Unit=estimated_Yield_Unit,
            C_Harvest_Month=estimated_harvest_month)

        crop_production_details = t_certification_gap_t4.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        return render(request, 'GAP_Certification/crop_production_details.html',
                      {'crop_production_details': crop_production_details})
    elif identification_type == 'GAP-PH':
        application_no = request.POST.get('edit_pack_house_application_no')
        record_id = request.POST.get('pack_house_record_id')
        pack_house_name = request.POST.get('edit_pack_house_name')
        pack_house_address = request.POST.get('edit_pack_house_address')
        prev_year = request.POST.get('edit_previous_from_date')
        to_year = request.POST.get('edit_previous_to_date')
        production = request.POST.get('edit_production')
        production_unit = request.POST.get('edit_production_unit')
        previous_sold = request.POST.get('edit_previous_sold')
        previous_sold_unit = request.POST.get('edit_previous_sold_unit')
        stock_balance = request.POST.get('edit_stock_balance')
        stock_balance_unit = request.POST.get('edit_stock_balance_unit')
        current_from_date = request.POST.get('edit_current_from_date')
        current_to_date = request.POST.get('edit_current_to_date')
        current_Production = request.POST.get('edit_current_Production')
        current_Production_Unit = request.POST.get('edit_current_Production_unit')
        current_sold = request.POST.get('edit_current_sold')
        current_sold_unit = request.POST.get('edit_current_sold_unit')
        current_stock_balance = request.POST.get('edit_current_stock_balance')
        current_stock_unit = request.POST.get('edit_current_stock_unit')
        p_from = datetime.strptime(prev_year, '%d-%m-%Y').date()
        p_to = datetime.strptime(to_year, '%d-%m-%Y').date()
        c_from = datetime.strptime(current_from_date, '%d-%m-%Y').date()
        c_to = datetime.strptime(current_to_date, '%d-%m-%Y').date()

        details = t_certification_gap_t5.objects.filter(Record_Id=record_id)
        details.update(
            Pack_House_Name=pack_house_name,
            Pack_House_Address=pack_house_address,
            P_From_Date=p_from,
            P_To_Date=p_to,
            P_Production=production,
            P_Production_Unit=production_unit,
            P_Sold=previous_sold,
            P_Sold_Unit=previous_sold_unit,
            P_Balance_Stock=stock_balance,
            P_Balance_Stock_Unit=stock_balance_unit,
            C_From_Date=c_from,
            C_To_Date=c_to,
            C_Production=current_Production,
            C_Production_Unit=current_Production_Unit,
            C_Sold=current_sold,
            C_Sold_Unit=current_sold_unit,
            C_Balance_Stock=current_stock_balance,
            C_Balance_Stock_Unit=current_stock_unit
        )

        pack_house_details = t_certification_gap_t5.objects.filter(Application_No=application_no).order_by('Record_Id')
        return render(request, 'GAP_Certification/pack_house_details.html',
                      {'pack_house_details': pack_house_details})

    elif identification_type == 'OC-CP':
        application_no = request.POST.get('edit_crop_production_app_no')
        record_id = request.POST.get('crop_record_id')
        crop_name = request.POST.get('edit_crop_name')
        area = request.POST.get('edit_area')
        area_unit = request.POST.get('edit_area_unit')
        prev_year = request.POST.get('edit_prev_year')
        to_year = request.POST.get('edit_to_year')
        yields = request.POST.get('edit_yield')
        Yield_Unit = request.POST.get('edit_Yield_Unit')
        harvest_month = request.POST.get('edit_harvest_month')
        sold = request.POST.get('edit_sold')
        balance_stock = request.POST.get('edit_balance_stock')
        current_year = request.POST.get('edit_current_year')
        to_current_year = request.POST.get('edit_to_current_year')
        estimated_yield = request.POST.get('edit_estimated_yield')
        estimated_Yield_Unit = request.POST.get('edit_estimated_Yield_Unit')
        estimated_harvest_month = request.POST.get('edit_estimated_harvest_month')

        p_from = datetime.strptime(prev_year, '%d-%m-%Y').date()
        p_to = datetime.strptime(to_year, '%d-%m-%Y').date()
        c_from = datetime.strptime(current_year, '%d-%m-%Y').date()
        c_to = datetime.strptime(to_current_year, '%d-%m-%Y').date()

        details = t_certification_organic_t4.objects.filter(Record_Id=record_id)
        details.update(
            Crop_Name=crop_name,
            Area_Cultivated=area,
            Unit=area_unit,
            P_From_Date=p_from,
            P_To_Date=p_to,
            P_Yield=yields,
            P_Yield_Unit=Yield_Unit,
            P_Harvest_Month=harvest_month,
            P_Sold=sold,
            P_Balance_Stock=balance_stock,
            C_From_Date=c_from,
            C_To_Date=c_to,
            C_Estimated_Yield=estimated_yield,
            C_Yield_Unit=estimated_Yield_Unit,
            C_Harvest_Month=estimated_harvest_month)
        crop_details = t_certification_organic_t4.objects.filter(Application_No=application_no).order_by('Record_Id')
        return render(request, 'organic_certification/crop_production_details.html',
                      {'crop_details': crop_details})
    elif identification_type == 'OC-WC':
        application_no = request.POST.get('edit_wild_collection_appNo')
        record_id = request.POST.get('wild_record_id')
        print(application_no)
        print(record_id)
        common_name = request.POST.get('edit_common_name')
        botanical_name = request.POST.get('edit_botanical_name')
        part_of_plant = request.POST.get('edit_part_of_plant')
        estimated_harvest = request.POST.get('edit_estimated_harvest')
        estimated_harvest_Yield_Unit = request.POST.get('edit_estimated_harvest_Yield_Unit')
        harvest_season = request.POST.get('edit_harvest_season')
        harvest_acreage = request.POST.get('edit_harvest_acreage')
        harvest_Unit = request.POST.get('edit_harvest_Unit')

        wild_collection_details = t_certification_organic_t6.objects.filter(Record_Id=record_id)
        wild_collection_details.update(
            Common_Name=common_name,
            Botanical_Name=botanical_name,
            Plant_Part=part_of_plant,
            Estimated_Harvest=estimated_harvest,
            Harvest_Unit=estimated_harvest_Yield_Unit,
            Harvest_Season=harvest_season,
            Harvest_Acreage=harvest_acreage,
            Acreage_Unit=harvest_Unit)
        wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_no).order_by('Record_Id')
        return render(request, 'organic_certification/wild_collection_details.html',
                      {'wild_collection': wild_collection})

    elif identification_type == 'OC-AH':
        application_no = request.POST.get('edit_animal_husbandry_application_no')
        print(application_no)
        record_id = request.POST.get('animal_record_id')
        print(record_id)
        livestock_type = request.POST.get('edit_livestock_type')
        male = request.POST.get('edit_male')
        female = request.POST.get('edit_female')
        estimated_production = request.POST.get('edit_estimated_production')
        estimated_production_Unit = request.POST.get('edit_estimated_production_Unit')
        product_sold = request.POST.get('edit_product_sold')

        animal_husbandry_details = t_certification_organic_t7.objects.filter(Record_Id=record_id)
        animal_husbandry_details.update(
            Livestock_Type=livestock_type,
            Male_no=male,
            Female_no=female,
            Estimated_Production=estimated_production,
            Production_Unit=estimated_production_Unit,
            Production_Sold=product_sold)
        animal_husbandry = t_certification_organic_t7.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        return render(request, 'organic_certification/animal_husbandry_details.html',
                      {'animal_husbandry': animal_husbandry})

    elif identification_type == 'OC-AQUA':
        application_no = request.POST.get('edit_aquaculture_application_no')
        record_id = request.POST.get('aqua_record_id')
        Aquaculture_type = request.POST.get('edit_Aquaculture_type')
        Aquaculture_Yield = request.POST.get('edit_Aquaculture_Yield')
        Aquaculture_Yield_Unit = request.POST.get('edit_Aquaculture_Yield_Unit')
        aqua_harvest_month = request.POST.get('edit_aqua_harvest_month')
        aqua_Sold = request.POST.get('edit_aqua_Sold')
        aqua_Sold_unit = request.POST.get('edit_aqua_Sold_unit')
        stock_balance = request.POST.get('edit_stock_balance')
        stock_balance_unit = request.POST.get('edit_stock_balance_unit')

        aquaculture = t_certification_organic_t8.objects.filter(Record_Id=record_id)

        aquaculture.update(
            Aquaculture_Type=Aquaculture_type,
            Estimated_Yield=Aquaculture_Yield,
            Estimated_Yield_Unit=Aquaculture_Yield_Unit,
            Harvest_Month=aqua_harvest_month,
            Sold=aqua_Sold,
            Sold_Unit=aqua_Sold_unit,
            Balance_Stock=stock_balance,
            Balance_Stock_Unit=stock_balance_unit)
        aquaculture_details = t_certification_organic_t8.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        return render(request, 'organic_certification/aquaculture_details.html',
                      {'aquaculture_details': aquaculture_details})

    elif identification_type == 'OC-API':
        application_no = request.POST.get('edit_api_culture_application_no')
        record_id = request.POST.get('api_record_id')
        api_common_name = request.POST.get('edit_api_common_name')
        api_botanical_name = request.POST.get('edit_api_botanical_name')
        api_estimated_harvest = request.POST.get('edit_api_estimated_harvest')
        api_estimated_harvest_Yield_Unit = request.POST.get('edit_api_estimated_harvest_Yield_Unit')
        api_harvest_acreage = request.POST.get('edit_api_harvest_acreage')
        api_Unit = request.POST.get('edit_api_Unit')

        apiculture = t_certification_organic_t9.objects.filter(Record_Id=record_id)

        apiculture.update(
            Common_Name=api_common_name,
            Botanical_Name=api_botanical_name,
            Estimated_Harvest=api_estimated_harvest,
            Harvest_Unit=api_estimated_harvest_Yield_Unit,
            Harvest_Acreage=api_harvest_acreage,
            Acreage_Unit=api_Unit)
        apiculture_details = t_certification_organic_t9.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        return render(request, 'organic_certification/api_culture_details.html',
                      {'apiculture_details': apiculture_details})

    elif identification_type == 'OC-PU':
        application_no = request.POST.get('edit_processing_application_no')
        record_id = request.POST.get('processing_record_id')
        processing_name = request.POST.get('edit_processing_name')
        address_of_Operation = request.POST.get('edit_address_of_Operation')
        processing_type = request.POST.get('edit_processing_type')
        from_date = request.POST.get('edit_from_date')
        to_date = request.POST.get('edit_to_date')
        production = request.POST.get('edit_production')
        production_unit = request.POST.get('edit_production_unit')
        processing_Sold = request.POST.get('edit_processing_Sold')
        processing_balance = request.POST.get('edit_processing_balance')
        current_from_date = request.POST.get('edit_current_from_date')
        current_to_date = request.POST.get('edit_current_to_date')
        current_production = request.POST.get('edit_current_production')
        current_production_unit = request.POST.get('edit_current_production_unit')
        current_processing_Sold = request.POST.get('edit_current_processing_Sold')
        current_processing_balance = request.POST.get('edit_current_processing_balance')

        p_from = datetime.strptime(from_date, '%d-%m-%Y').date()
        p_to = datetime.strptime(to_date, '%d-%m-%Y').date()
        c_from = datetime.strptime(current_from_date, '%d-%m-%Y').date()
        c_to = datetime.strptime(current_to_date, '%d-%m-%Y').date()

        processing = t_certification_organic_t5.objects.filter(Record_Id=record_id)

        processing.update(
            Production_House_Name=processing_name,
            Production_House_Address=address_of_Operation,
            Processing_Type=processing_type,
            P_From_Date=p_from,
            P_To_Date=p_to,
            P_Production=production,
            P_Production_Unit=production_unit,
            P_Sold=processing_Sold,
            P_Balance_Stock=processing_balance,
            C_From_Date=c_from,
            C_To_Date=c_to,
            C_Production=current_production,
            C_Production_Unit=current_production_unit,
            C_Sold=current_processing_Sold,
            C_Balance_Stock=current_processing_balance)
        processing_details = t_certification_organic_t5.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        return render(request, 'organic_certification/processing_unit_details.html',
                      {'processing_details': processing_details})
    elif identification_type == 'OC-FG':
        application_no = request.POST.get('edit_farmers_group_application_no')
        record_id = request.POST.get('farmers_group_record_id')
        cid = request.POST.get('edit_farmers_group_cid')
        name = request.POST.get('edit_farmers_group_fullname')
        farmers_group = t_certification_organic_t2.objects.filter(Record_Id=record_id)
        farmers_group.update(CID=cid, Name=name)
        farmers_group_details = t_certification_organic_t2.objects.filter(Application_No=application_no).order_by(
            'Record_Id')
        return render(request, 'organic_certification/farmer_group_details.html',
                      {'farmers_group_details': farmers_group_details})
    elif identification_type == 'FBR-RM':
        application_no = request.POST.get('edit_raw_application_no')
        record_id = request.POST.get('raw_record_id')
        name = request.POST.get('edit_raw_material_name')
        source_country = request.POST.get('edit_source_country')
        raw_materials_details = t_food_business_registration_licensing_t7.objects.filter(record_id=record_id)
        raw_materials_details.update(name=name, source_country=source_country)
        raw_materials = t_food_business_registration_licensing_t7.objects.filter(
            application_no=application_no).order_by(
            'record_id')
        raw_count = t_food_business_registration_licensing_t7.objects.filter(application_no=application_no).count()
        return render(request, 'registration_licensing/raw_material_details.html', {'raw_materials': raw_materials,
                                                                                    'raw_count': raw_count})
    elif identification_type == 'FBR-RM':
        application_no = request.POST.get('edit_packaging_application_no')
        record_id = request.POST.get('packaging_record_id')
        name = request.POST.get('edit_packaging_name')
        source_country = request.POST.get('edit_packaging_source_country')
        packaging_material_details = t_food_business_registration_licensing_t8.objects.filter(record_id=record_id)
        packaging_material_details.update(name=name, source_Country=source_country)
        packaging_material = t_food_business_registration_licensing_t8.objects.filter(
            application_no=application_no).order_by(
            'record_id')
        packaging_count = t_food_business_registration_licensing_t8.objects.filter(
            application_no=application_no).count()
        return render(request, 'registration_licensing/packaging_material_details.html',
                      {'packaging_material': packaging_material, 'packaging_count': packaging_count})


def view_complain_officer_details(request):
    application_id = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    if service_code == 'OC':
        oc_work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if oc_work_details.exists():
            application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
            details = t_certification_organic_t2.objects.filter(Application_No=application_id)
            audit_team = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=application_id)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_id)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_id)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=application_id)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_id)
            api_details = t_certification_organic_t9.objects.filter(Application_No=application_id)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_id)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            return render(request, 'organic_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details, 'audit_plan': audit_plan,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation})
        else:
            application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
            details = t_certification_organic_t2.objects.filter(Application_No=application_id)
            audit_team = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=application_id)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_id)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_id)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=application_id)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_id)
            api_details = t_certification_organic_t9.objects.filter(Application_No=application_id)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_id)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'organic_certification/team_leader_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details, 'audit_plan': audit_plan,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'file_attach_count': file_attach_count})
    elif service_code == 'GAP':
        work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
            details = t_certification_gap_t2.objects.filter(Application_No=application_id)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=application_id)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id)
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_id)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_id)
            return render(request, 'GAP_Certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details})
        else:
            application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
            details = t_certification_gap_t2.objects.filter(Application_No=application_id)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=application_id)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_id)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_id)
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'GAP_Certification/team_leader_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details, 'audit_plan': audit_plan,
                           'file_attach_count': file_attach_count})
    elif service_code == 'FPC':
        work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
            details = t_certification_food_t2.objects.filter(Application_No=application_id)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id)
            audit_findings = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_observation = t_certification_food_t5.objects.filter(Application_No=application_id)
            return render(request, 'food_product_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details,
                           })
        else:
            application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
            details = t_certification_food_t2.objects.filter(Application_No=application_id)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            audit_findings = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_observation = t_certification_food_t4.objects.filter(Application_No=application_id)
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'food_product_certification/team_leader_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details, 'audit_plan': audit_plan,
                           'file_attach_count': file_attach_count
                           })


def view_chief_details(request):
    application_id = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    if service_code == 'OC':
        oc_work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if oc_work_details.exists():
            application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
            details = t_certification_organic_t2.objects.filter(Application_No=application_id)
            audit_team = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=application_id)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_id)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_id)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=application_id)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_id)
            api_details = t_certification_organic_t9.objects.filter(Application_No=application_id)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_id)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id,
                                                          attachment_type='AP')
            return render(request, 'organic_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details, 'audit_plan': audit_plan,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation})
        else:
            application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
            details = t_certification_organic_t2.objects.filter(Application_No=application_id)
            audit_team = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_organic_t4.objects.filter(Application_No=application_id)
            processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_id)
            wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_id)
            ah_details = t_certification_organic_t7.objects.filter(Application_No=application_id)
            aqua_details = t_certification_organic_t8.objects.filter(Application_No=application_id)
            api_details = t_certification_organic_t9.objects.filter(Application_No=application_id)
            audit_findings = t_certification_organic_t10.objects.filter(Application_No=application_id)
            audit_observation = t_certification_organic_t11.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_No=application_id, attachment_Type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id,
                                                          attachment_type='AP')
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'organic_certification/team_leader_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'crop_production': crop_production, 'audit_team': audit_team,
                           'processing_unit': processing_unit, 'wild_collection': wild_collection,
                           'ah_details': ah_details, 'aqua_details': aqua_details,
                           'api_details': api_details, 'audit_plan': audit_plan,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'file_attach_count': file_attach_count})
    elif service_code == 'GAP':
        work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
            details = t_certification_gap_t2.objects.filter(Application_No=application_id)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=application_id)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_id)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_id)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            return render(request, 'GAP_Certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details, 'audit_plan': audit_plan})
        else:
            application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
            details = t_certification_gap_t2.objects.filter(Application_No=application_id)
            audit_team_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            crop_production = t_certification_gap_t4.objects.filter(Application_No=application_id)
            gap_house_details = t_certification_gap_t5.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id, attachment_type='AP')
            farm_inputs = t_certification_gap_t7.objects.filter(Application_No=application_id)
            audit_observation = t_certification_gap_t8.objects.filter(Application_No=application_id)
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'GAP_Certification/team_leader_details.html',
                          {'application_details': application_details, 'farmer_group': details, 'file_attach': file,
                           'farm_inputs': farm_inputs, 'audit_observation': audit_observation,
                           'crop_production': crop_production, 'pack_house_details': gap_house_details,
                           'audit_team_details': audit_team_details, 'audit_plan': audit_plan,
                           'file_attach_count': file_attach_count})
    elif service_code == 'FPC':
        work_details = t_workflow_details.objects.filter(application_no=application_id, application_status='NCF')
        if work_details.exists():
            application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
            details = t_certification_food_t2.objects.filter(Application_No=application_id)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_findings = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_observation = t_certification_food_t5.objects.filter(Application_No=application_id)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id,
                                                          attachment_type='AP')
            return render(request, 'food_product_certification/team_leader_nc_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details, 'audit_plan': audit_plan
                           })
        else:
            application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
            details = t_certification_food_t2.objects.filter(Application_No=application_id)
            inspection_details = t_certification_food_t3.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id, attachment_type__isnull=True)
            audit_findings = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_observation = t_certification_food_t4.objects.filter(Application_No=application_id)
            audit_plan = t_file_attachment.objects.filter(application_no=application_id,
                                                          attachment_type='AP')
            file_attach_count = t_file_attachment.objects.filter(application_no=application_id,
                                                                 attachment_type='AP').count()
            return render(request, 'food_product_certification/team_leader_details.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'audit_findings': audit_findings, 'audit_observation': audit_observation,
                           'inspection_details': inspection_details,
                           'audit_plan': audit_plan, 'file_attach_count': file_attach_count})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def member_audit_plan(request):
    try:
        login_id = request.session['Login_Id']
        Role = request.session['role']
        Role_Id = request.session['Role_Id']
    except:
        login_id = None
    if login_id:
        if Role == 'Focal Officer':
            section = request.session['section']
            section_details = t_section_master.objects.filter(Section_Id=section)
            for id_section in section_details:
                section_name = id_section.Section_Name
                message_count = (t_workflow_details.objects.filter(
                    assigned_role_id=Role_Id, section=section_name,
                    action_date__isnull=False, application_status='P') | t_workflow_details.objects.filter(
                    assigned_role_id=Role_Id, section=section_name,
                    action_date__isnull=False, application_status='ATA') | t_workflow_details.objects.filter(
                    assigned_role_id=Role_Id, section=section_name,
                    action_date__isnull=False, application_status='FRA') |
                                 t_workflow_details.objects.filter(
                                     assigned_role_id=Role_Id, section=section_name,
                                     action_date__isnull=False, application_status='CA')
                                 ).count()
                application_details = t_certification_food_t3.objects.filter(Login_Id=login_id)
                service_details = t_service_master.objects.all()
                return render(request, 'member_audit_plan_list.html', {'application_details': application_details,
                                                                       'service_details': service_details,
                                                                       'count': message_count})
        elif Role == 'OIC':
            login_id = request.session['Login_Id']
            Field_Office_Id = request.session['field_office_id']
            message_count = (t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                               action_date__isnull=False) |
                             t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                               action_date__isnull=False)).count()
            application_details = t_certification_food_t3.objects.filter(Login_Id=login_id)
            service_details = t_service_master.objects.all()
            return render(request, 'member_audit_plan_list.html', {'application_details': application_details,
                                                                   'service_details': service_details,
                                                                   'count': message_count})
        elif Role == 'Inspector':
            login_id = request.session['Login_Id']
            Field_Office_Id = request.session['field_office_id']
            message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                               action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                                 application_status='I',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                                 application_status='FI',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, Field_Office_Id=Field_Office_Id,
                                                                 application_status='FR',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, Field_Office_Id=Field_Office_Id,
                                                                 application_status='P',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                 action_date__isnull=False)).count()
            application_details = t_certification_food_t3.objects.filter(Login_Id=login_id)
            service_details = t_service_master.objects.all()
            fhc_count = t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                          action_date__isnull=False, service_code='FHC').count()
            return render(request, 'member_audit_plan_list.html', {'application_details': application_details,
                                                                   'service_details': service_details,
                                                                   'ins_count': message_count, 'fhc_count': fhc_count})
    else:
        return render(request, 'redirect_page.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def client_audit_plan(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        application_details = t_workflow_details.objects.filter(application_status__in=['APA', 'NCF', 'CA', 'A'],
                                                                service_code__in=['GAP', 'OC', 'FPC'])
        service_details = t_service_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'client_audit_plan_list.html',
                      {'application_details': application_details, 'service_details': service_details,
                       'count': message_count, 'count_call': inspection_call_count,
                       'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def view_audit_plan(request):
    appNo = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    if service_code == 'OC':
        application_details = t_certification_organic_t1.objects.filter(Application_No=appNo)
        details = t_certification_organic_t2.objects.filter(Application_No=appNo)
        audit_team = t_certification_food_t3.objects.filter(Application_No=appNo)
        crop_production = t_certification_organic_t4.objects.filter(Application_No=appNo)
        processing_unit = t_certification_organic_t5.objects.filter(Application_No=appNo)
        wild_collection = t_certification_organic_t6.objects.filter(Application_No=appNo)
        ah_details = t_certification_organic_t7.objects.filter(Application_No=appNo)
        aqua_details = t_certification_organic_t8.objects.filter(Application_No=appNo)
        api_details = t_certification_organic_t9.objects.filter(Application_No=appNo)
        file = t_file_attachment.objects.filter(application_no=appNo)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        user_details = t_user_master.objects.all()
        audit_plan = t_file_attachment.objects.filter(application_no=appNo, attachment_type="AP")
        return render(request, 'organic_certification/audit_plan_view.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'crop_production': crop_production, 'audit_team': audit_team,
                       'processing_unit': processing_unit, 'wild_collection': wild_collection,
                       'ah_details': ah_details, 'aqua_details': aqua_details, 'api_details': api_details,
                       'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog,
                       'user_details': user_details, 'audit_plan': audit_plan})
    elif service_code == 'GAP':
        application_details = t_certification_gap_t1.objects.filter(Application_No=appNo)
        details = t_certification_gap_t2.objects.filter(Application_No=appNo)
        audit_team_details = t_certification_food_t3.objects.filter(Application_No=appNo)
        crop_production = t_certification_gap_t4.objects.filter(Application_No=appNo)
        gap_house_details = t_certification_gap_t5.objects.filter(Application_No=appNo)
        file = t_file_attachment.objects.filter(application_no=appNo)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        user_details = t_user_master.objects.all()
        audit_plan = t_file_attachment.objects.filter(application_no=appNo, attachment_type="AP")
        return render(request, 'GAP_Certification/audit_plan_view.html',
                      {'application_details': application_details, 'farmer_group': details, 'file': file,
                       'audit_team_details': audit_team_details, 'crop_production': crop_production,
                       'gap_house_details': gap_house_details, 'dzongkhag': dzongkhag, 'village': village,
                       'gewog': gewog, 'user_details': user_details, 'audit_plan': audit_plan})
    elif service_code == 'FPC':
        application_details = t_certification_food_t1.objects.filter(Application_No=appNo)
        details = t_certification_food_t2.objects.filter(Application_No=appNo)
        inspection_details = t_certification_food_t3.objects.filter(Application_No=appNo)
        file = t_file_attachment.objects.filter(application_no=appNo)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        audit_team_details = t_certification_food_t3.objects.filter(Application_No=appNo)
        user_details = t_user_master.objects.all()
        audit_plan = t_file_attachment.objects.filter(application_no=appNo, attachment_type="AP")
        return render(request, 'food_product_certification/audit_plan_view.html',
                      {'application_details': application_details, 'details': details, 'file': file,
                       'inspection_details': inspection_details, 'dzongkhag': dzongkhag, 'village': village,
                       'gewog': gewog, 'audit_team_details': audit_team_details, 'user_details': user_details,
                       'audit_plan': audit_plan})


def load_field_office(request):
    conveyance = request.GET.get('conveyance')
    if conveyance == "By Air":
        location = t_field_office_master.objects.filter(Conveyance_Means="By Air")
        return render(request, 'import_permit/field_office_list.html', {'location': location})
    else:
        location = t_field_office_master.objects.filter(Is_Entry_Point="Y", Conveyance_Means="By Road")
        return render(request, 'import_permit/field_office_list.html', {'location': location})


@csrf_exempt
def bbfss_payment_update(request):
    applicationNo = request.POST.get("applicationNo")
    paymentDate = request.POST.get("paymentDate")
    txnId = request.POST.get("txnId")
    paymentStatus = request.POST.get("paymentStatus")

    if paymentStatus == 'PAID':
        details_pay = t_workflow_details.objects.filter(application_no=applicationNo, application_source='IBLS')
        details_pay.update(receipt_no=txnId)
        details_pay.update(receipt_date=paymentDate)
        details_pay.update(payment_type='Online')
        for payment_details in details_pay:
            service_code = payment_details.service_id
            if service_code == 'CMS':
                meat_shop_details = t_livestock_clearance_meat_shop_t1.objects.filter(
                    application_no=applicationNo,
                    conditional_clearance_no__isnull=False)
                if meat_shop_details.exists():
                    for meat_details in meat_shop_details:
                        x = {
                            "applicationNo": applicationNo,
                            "cleareanceNo": meat_details.conditional_clearance_no,
                            "status": True,
                            "message": "null",
                            "rejectionMessage": "null"
                        }
                        post_data = json.dumps(x)
                        headers = {'Accept': 'application/json'}

                        res = requests.post('https://bpa.test.bhutan.eregistrations.org/mule/api/action/bafra_update',
                                            params=post_data, headers=headers, verify=False)
            elif service_code == 'CMS':
                food_business_details = t_food_business_registration_licensing_t1.objects.filter(
                    application_no=applicationNo,
                    conditional_clearance_no__isnull=False)
                if food_business_details.exists():
                    for meat_details in meat_shop_details:
                        x = {
                            "applicationNo": Application_No,
                            "cleareanceNo": food_business_details.conditional_clearance_no,
                            "status": True,
                            "message": "null",
                            "rejectionMessage": "null"
                        }
                        post_data = json.dumps(x)
                        headers = {'Accept': 'application/json'}

                        res = requests.post('https://bpa.test.bhutan.eregistrations.org/mule/api/action/bafra_update',
                                            params=post_data, headers=headers, verify=False)
    return HttpResponse('<h1>Ok/h1>')
