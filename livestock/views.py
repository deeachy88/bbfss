from datetime import date
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_location_field_office_mapping,\
    t_user_master, t_field_office_master, t_plant_crop_master, t_plant_pesticide_master, t_plant_crop_variety_master,\
    t_service_master
from bbfss import settings
from livestock.forms import MeatShopClearanceFormOne, MeatShopClearanceFormTwo
from livestock.models import t_livestock_clearence_meat_shop_t1, t_livestock_clearence_meat_shop_t2
from plant.models import t_workflow_details, t_file_attachment

def apply_clearance_meat_shop(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    return render(request, 'clearance_meat_shop/apply_clearance_meat_shop.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})

def save_meat_shop_clearance(request):
    print("inside")
    data = dict()
    service_code = "CMS"
    last_application_no = get_meat_shop_application_no(request, service_code)

    applicant_Id = request.session['email']
    scope = request.POST.get('scope')
    purpose = request.POST.get('purpose')
    shopName = request.POST.get('shopName')
    ownership = request.POST.get('ownership')
    cid = request.POST.get('cid')
    Name = request.POST.get('Name')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location = request.POST.get('location_code')
    clearance = request.POST.get('clearance')
    proceeding = request.POST.get('proceeding')
    proceedingReason = request.POST.get('proceedingReason')
    inspectionDate = request.POST.get('inspectionDate')

    t_livestock_clearence_meat_shop_t1.objects.create(
        Application_No=last_application_no,
        Applicant_Id=applicant_Id,
        Scope=scope,
        Purpose=purpose,
        Name_Meat_Shop=shopName,
        Ownership_Type=ownership,
        CID=cid,
        Name_Owner=Name,
        Contact_No=contact_number,
        Email=email,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Location_Code=location,
        Establish_Type=None,
        Establishment_Size=None,
        Meat_Type=None,
        Clearance_Type=clearance,
        Any_Proceedings=proceeding,
        Reason_Suspension=proceedingReason,
        Desired_Inspection_Date=inspectionDate,
        Resubmit_Date=None,
        Desired_Reinspection_Date=None,
        Remarks_Reinspection=None,
        Inspection_Date=None,
        Remarks_Inspection=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Application_Status='P',
        Meat_Shop_Clearance_No=None,
        Conformity=None,
        Conformity_Statement=None
        )
    t_workflow_details.objects.create(Application_No=last_application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Plant',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = last_application_no
    return JsonResponse(data)

def get_meat_shop_application_no(request, service_code):
    last_application_no = t_livestock_clearence_meat_shop_t1.objects.aggregate(Max('Application_No'))
    lastAppNo = last_application_no['Application_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = service_code + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = service_code + "/" + str(year) + "/" + AppNo
    return newAppNo

def load_application_details(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_livestock_clearence_meat_shop_t1.objects.filter(Application_No=application_id)
    print(application_id)
    return render(request, 'clearance_meat_shop/details_meat_shop.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location_code': location})

def load_attachment_details(request):
    application_id = request.GET.get('application_id')
    print(application_id)
    attachment_details = t_file_attachment.objects.filter(Application_No=application_id)
    return render(request, 'clearance_meat_shop/meat_shop_file_attachment_page.html', {'file_attach': attachment_details})


def meat_shop_clearance_app(request):
    appNo = request.GET.get('appId')
    meat_shop_inspection = t_livestock_clearence_meat_shop_t2.objects.filter(Application_No=appNo)
    return render(request, 'clearance_meat_shop/apply_clearance_meat_shop.html', {'meat_shop_inspection': meat_shop_inspection, 'title': appNo})

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
    return render(request, 'location_list.html', {'location_list': location_list})


def clearance_print(request):
    return render(request, 'clearance_printing.html')



def save_meat_shop_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/livestock/meat_shop")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)



def add_meat_shop_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'clearance_meat_shop/meat_shop_file_attachment_page.html', {'file_attach': file_attach})


def delete_meat_shop_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'movement_permit/ile_attachment_page.html', {'file_attach': file_attach})

def submit_details(request):
    application_no = request.GET.get('appNo')
    print(application_no)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'clearance_meat_shop/apply_clearance_meat_shop.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})
