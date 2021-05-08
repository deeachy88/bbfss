from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_location_field_office_mapping, \
    t_user_master, t_field_office_master, t_plant_crop_master, t_plant_pesticide_master, t_plant_crop_variety_master, \
    t_service_master, t_unit_master
from bbfss import settings
from livestock.forms import ImportFormProduct
from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_clearance_meat_shop_t2, \
    t_livestock_ante_post_mortem_t1, t_livestock_movement_permit_t1, t_livestock_export_certificate_t1, \
    t_livestock_ante_post_mortem_t2, t_livestock_movement_permit_t2, t_livestock_export_certificate_t2, \
    t_livestock_import_permit_product_t1, t_livestock_import_permit_animal_t1, t_livestock_movement_permit_t3, \
    t_livestock_import_permit_animal_inspection_t1, t_livestock_import_permit_product_inspection_t1, \
    t_livestock_import_permit_animal_t2, t_livestock_import_permit_product_t2, \
    t_livestock_import_permit_product_inspection_t2, t_livestock_import_permit_animal_inspection_t2
from plant.forms import ImportFormTwo
from plant.models import t_workflow_details, t_file_attachment, t_payment_details
from plant.views import inspector_application


def apply_clearance_meat_shop(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    return render(request, 'clearance_meat_shop/apply_clearance_meat_shop.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def save_meat_shop_clearance(request):
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
    clearance = request.POST.get('clearance')
    proceeding = request.POST.get('proceeding')
    proceedingReason = request.POST.get('proceedingReason')
    inspectionDate = request.POST.get('inspectionDate')
    date_format_ins = datetime.strptime(inspectionDate, '%d-%m-%Y').date()

    t_livestock_clearance_meat_shop_t1.objects.create(
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
        Establish_Type=None,
        Establishment_Size=None,
        Meat_Type=None,
        Clearance_Type=clearance,
        Any_Proceedings=proceeding,
        Reason_Suspension=proceedingReason,
        Desired_Inspection_Date=date_format_ins,
        Resubmit_Date=None,
        Desired_Reinspection_Date=None,
        Remarks_Reinspection=None,
        Inspection_Date=None,
        Remarks_Inspection=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Application_Status='P',
        Meat_Shop_Clearance_No=None,
        Approved_Date=None,
        Validity_Period=None,
        Validity=None
    )
    field = t_location_field_office_mapping.objects.filter(Location_Code=gewog)
    for field_office in field:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(Application_No=last_application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=field_office_id, Section='Livestock',
                                      Assigned_Role_Id='4', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = last_application_no
    return JsonResponse(data)


def get_meat_shop_application_no(request, service_code):
    last_application_no = t_livestock_clearance_meat_shop_t1.objects.aggregate(Max('Application_No'))
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
    application_details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)
    return render(request, 'clearance_meat_shop/details_meat_shop.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location_code': location})


def load_attachment_details(request):
    application_id = request.GET.get('application_id')
    attachment_details = t_file_attachment.objects.filter(Application_No=application_id)
    return render(request, 'clearance_meat_shop/meat_shop_file_attachment_page.html',
                  {'file_attach': attachment_details})


def meat_shop_clearance_app(request):
    appNo = request.GET.get('appId')
    meat_shop_inspection = t_livestock_clearance_meat_shop_t2.objects.filter(Application_No=appNo)
    return render(request, 'clearance_meat_shop/apply_clearance_meat_shop.html',
                  {'meat_shop_inspection': meat_shop_inspection, 'title': appNo})


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
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/livestock/meat_shop")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'clearance_meat_shop/file_attachment_page.html', {'file_attach': file_attach})


def submit_details(request):
    application_no = request.GET.get('appNo')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'clearance_meat_shop/apply_clearance_meat_shop.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def details_ins_cms(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_livestock_clearance_meat_shop_t2.objects.create(Application_No=application_id,
                                                      Observation=currentObservation,
                                                      Action=decisionConform)
    observation = t_livestock_clearance_meat_shop_t2.objects.filter(Application_No=application_id)
    return render(request, 'clearance_meat_shop/observation_details.html', {'observation': observation})


def approve_application_cms(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    Meat_Shop_Clearance_No = meat_shop_clearance_no(request)
    identification_No = request.GET.get('identification_No')
    revision_no = request.GET.get('revision_no')
    validity = request.GET.get('validity')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)

    if remarks is not None:
        details.update(Remarks_Inspection=remarks)
    else:
        details.update(Remarks_Inspection=None)
    if revision_no is not None:
        details.update(Revision_No=revision_no)
    else:
        details.update(Revision_No=None)

    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Meat_Shop_Clearance_No=Meat_Shop_Clearance_No)
    details.update(Identification_No=identification_No)
    details.update(Validity_Period=validity)
    details.update(Approved_Date=date.today())
    details.update(Application_Status='A')
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    for email_id in details:
        emailId = email_id.Email
        send_cms_approve_email(Meat_Shop_Clearance_No, emailId, validity_date)
    update_payment(application_id, Meat_Shop_Clearance_No, 'CMS', validity_date)
    return redirect(inspector_application)


def reject_application_cms(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    identification_No = request.GET.get('identification_No')
    revision_no = request.GET.get('revision_no')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)
    for email_id in details:
        email = email_id.Email
    if revision_no is not None:
        details.update(Revision_No=revision_no)
    else:
        details.update(Revision_No=None)
    details.update(Remarks_Inspection=remarks)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Identification_No=identification_No)
    details.update(Application_Status='R')
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='R')
    send_cms_reject_email(remarks, details.Email)
    return redirect(inspector_application)


def resubmit_application_cms(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    identification_No = request.GET.get('identification_No')
    revision_no = request.GET.get('revision_no')

    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)

    if revision_no is not None:
        details.update(Revision_No=revision_no)
    else:
        details.update(Revision_No=None)
    details.update(Remarks_Inspection=remarks)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Identification_No=identification_No)
    details.update(Application_Status='RS')
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='RS')
    for login in application_details:
        login_id = login.Applicant_Id
    app_det = t_user_master.objects.filter(Email_Id=login_id)
    for app in app_det:
        user_id = app.Login_Id
    application_details.update(Assigned_To=user_id)
    for email_id in details:
        email = email_id.Email
        send_cms_resubmit_email(remarks, email)
    return redirect(inspector_application)


def meat_shop_clearance_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_livestock_clearance_meat_shop_t1.objects.aggregate(Max('Meat_Shop_Clearance_No'))
    lastAppNo = last_application_no['Meat_Shop_Clearance_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "CMS" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "CMS" + "/" + str(year) + "/" + AppNo
    return newAppNo


def send_cms_approve_email(new_meat_shop_clearance, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for Clearance of meat shop Has Been Approved. Your " \
              "Registration No is:" + new_meat_shop_clearance + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_cms_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Application for Clearance of meat shop  Has Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_cms_resubmit_email(remarks, Email):
    subject = 'APPLICATION RESUBMIT'
    message = "Dear " + "Sir" + " You Are Required To Resubmit Your Application For Clearance of meat shop Because " + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


# import permit for live animal and fish
def import_permit(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_field_office_master.objects.filter(Is_Entry_Point='Y')

    return render(request, 'Animal_Fish_Import/import_permit_animal_fish.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def save_import_la_fish(request):
    data = dict()
    service_code = "IAF"
    application_no = live_animal_fish_application_no(service_code)
    # applicant_Id = request.session['email']
    Application_Type = request.POST.get('Application_Type')
    Import_Type = request.POST.get('Import_Type')
    Nationality = request.POST.get('Nationality')
    Country = request.POST.get('Country')
    cid = request.POST.get('cid')
    Name = request.POST.get('Name')
    present_address = request.POST.get('present_address')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    license_no = request.POST.get('license_no')
    business_name = request.POST.get('business_name')
    purpose = request.POST.get('purpose')
    Origin_Source_Products = request.POST.get('Origin_Source_Products')
    Exporter_Address = request.POST.get('Exporter_Address')
    Final_Destination = request.POST.get('Final_Destination')
    Expected_Arrival_Date = request.POST.get('Expected_Arrival_Date')
    expected_date = datetime.strptime(Expected_Arrival_Date, '%d-%m-%Y').date()
    conveyanceMeans = request.POST.get('p_conveyanceMeans')
    point_of_entry = request.POST.get('Actual_Point_Of_Entry')
    QF = request.POST.get('QF')

    t_livestock_import_permit_animal_t1.objects.create(
        Application_No=application_no,
        Application_Type=Application_Type,
        Import_Type=Import_Type,
        License_No=license_no,
        Business_Name=business_name,
        Nationality=Nationality,
        Country=Country,
        CID=cid,
        Applicant_Name=Name,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Present_Address=present_address,
        Contact_No=contact_number,
        Email=email,
        Origin_Source_Products=Origin_Source_Products,
        Name_And_Address_Supplier=Exporter_Address,
        Purpose=purpose,
        Means_of_Conveyance=conveyanceMeans,
        Place_Of_Entry=point_of_entry,
        Final_Destination=Final_Destination,
        Expected_Arrival_Date=expected_date,
        FO_Remarks=None,
        Application_Date=date.today(),
        Approve_Date=None,
        Validity_Period=None,
        Validity=None,
        Quarantine_Facilities=QF
    )
    t_workflow_details.objects.create(Application_No=application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Livestock',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = application_no
    return JsonResponse(data)


def import_permit_la_details(request):
    application_no = request.POST.get('applNo')
    Species = request.POST.get('Species')
    Breed = request.POST.get('Breed')
    Age = request.POST.get('Age')
    Sex = request.POST.get('Sex')
    No_Of_Animal = request.POST.get('No_Of_Animal')
    Remarks = request.POST.get('Remarks')
    Description = request.POST.get('Description')

    t_livestock_import_permit_animal_t2.objects.create(Application_No=application_no,
                                                       Species=Species,
                                                       Breed=Breed,
                                                       Age=Age,
                                                       Sex=Sex,
                                                       Particulars=None,
                                                       Company_Name=None,
                                                       Description=Description,
                                                       Quantity=None,
                                                       Quantity_Released=None,
                                                       Remarks=Remarks,
                                                       No_Of_Animal=No_Of_Animal,
                                                       Unit=None)
    import_details = t_livestock_import_permit_animal_t2.objects.filter(Application_No=application_no)
    return render(request, 'Livestock_Import/permit_details.html', {'import': import_details})


def add_la_permit_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/livestock/livestock_import")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/livestock/livestock_import" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def add_la_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
        return render(request, 'Livestock_Import/file_attachment.html', {'file_attach': file_attach})


def submit_import_application(request):
    application_no = request.GET.get('appNo')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(import_permit)


def live_animal_fish_application_no(service_code):
    last_application_no = t_livestock_import_permit_animal_t1.objects.aggregate(Max('Application_No'))
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


def approve_fo_la_import(request):
    service_code = "IAF"
    permit_no = get_la_permit_no(service_code)
    application_no = request.GET.get('application_no')
    remarks = request.POST.get('remarks')
    validity = request.GET.get('validity')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    for app in workflow_details:
        client_login_id = app.Applicant_Id
    client_id = t_user_master.objects.filter(Email_Id=client_login_id)
    for client in client_id:
        login_id = client.Login_Id
        workflow_details.update(Assigned_To=login_id)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Assigned_Role_Id=None)
    details = t_livestock_import_permit_animal_t1.objects.filter(Application_No=application_no)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    for email_id in details:
        email = email_id.Email
        send_la_approve_email(permit_no, email, validity_date)
    update_payment(application_no, permit_no, 'IAF', validity_date)


def reject_fo_la_import(request):
    application_no = request.GET.get('application_no')
    remarks = request.POST.get('remarks')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Application_Status='R')
    details = t_livestock_import_permit_animal_t1.objects.filter(Application_No=application_no)
    details.update(FO_Remarks=remarks)
    for email_id in details:
        email = email_id.Email
        send_la_reject_email(email, remarks)


def send_la_approve_email(new_import_permit, Email, validity_date):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Live Animal And Fish Has Been Approved. Your " \
              "Import Permit No is:" + new_import_permit + " And is Valid TIll " + validity_date + \
              " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_la_reject_email(Email, remarks):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Live Animal And Fish Has Been Rejected." \
              " Reason: " + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def get_la_permit_no(service_code):
    last_import_permit_no = t_livestock_import_permit_animal_t1.objects.aggregate(Max('Import_Permit_No'))
    last_permit_no = last_import_permit_no['Import_Permit_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = service_code + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_permit_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = service_code + "/" + str(year) + "/" + AppNo
    return newPermitNo


def submit_la_application(request):
    application_no = request.GET.get('application_no')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    timeOfInspection = request.GET.get('timeOfInspection')

    clearnace_ref_no = la_clearance_no(request)

    update_details = t_livestock_import_permit_animal_inspection_t1.objects.filter(Application_No=application_no)
    update_details.update(Clearance_Ref_No=clearnace_ref_no)
    update_details.update(Inspection_Leader=Inspection_Leader)
    update_details.update(Inspection_Team=Inspection_Team)
    update_details.update(Inspection_Date=dateOfInspection)
    update_details.update(Inspection_Time=timeOfInspection)
    if remarks is not None:
        update_details.update(Inspection_Remarks=remarks)
    else:
        update_details.update(Inspection_Remarks=None)
    application_details = t_workflow_details.objects.filter(Application_No=application_no)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='C')
    application_list = t_workflow_details.objects.filter(Application_Status='A')

    return render(request, 'inspector_pending_list.html',
                  {'service_name': None, 'application_details': application_list})


def la_clearance_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_clearance_ref_no = t_livestock_import_permit_animal_inspection_t1.objects.aggregate(Max('Clearance_Ref_No'))
    last_permit_no = last_clearance_ref_no['Clearance_Ref_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = Field_Code + "/" + "IAF" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = Field_Code + "/" + "IAF" + "/" + str(year) + "/" + AppNo
    return newPermitNo


def edit_la_inspector_details(request, Record_Id):
    roles = get_object_or_404(t_livestock_import_permit_animal_inspection_t2, pk=Record_Id)
    Quantity_Released = request.POST.get('Quantity_Released')
    Remarks = request.POST.get('Remarks')
    if request.method == 'POST':
        form = ImportFormProduct(request.POST, instance=roles)
    else:
        form = ImportFormProduct(instance=roles)
    return save_lp_inspector_details(request, form, Record_Id, Quantity_Released, Remarks,
                                     'Animal_Fish_Import/edit_inspector_details.html')


def save_la_inspector_details(request, form, Record_Id, Quantity_Released, Remarks, template_name):
    data = dict()
    if request.method == 'POST':
        import_det = t_livestock_import_permit_animal_inspection_t2.objects.filter(pk=Record_Id)
        import_det.update(Quantity_Released=Quantity_Released)
        import_det.update(Remarks=Remarks)
        for import_LP in import_det:
            Product_Record_Id = import_LP.Product_Record_Id
            balance = int(import_LP.Quantity_Balance) - int(import_LP.Quantity_Released)
            product_details = t_livestock_import_permit_animal_t2.objects.filter(pk=Product_Record_Id)
            product_details.update(Quantity_Balance=balance)
        data['form_is_valid'] = True
        roles = t_livestock_import_permit_product_inspection_t2.objects.all()
        data['html_form'] = render_to_string('Animal_Fish_Import/inspector_details.html', {
            'import': roles
        })
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# import permit for livestock products and animal feed
def import_permit_application(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_field_office_master.objects.filter(Is_Entry_Point='Y')
    unit = t_unit_master.objects.all()

    return render(request, 'Livestock_Import/import_permit_livestock.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'unit': unit})


def save_import_lp(request):
    data = dict()
    service_code = "ILP"
    application_no = livestock_product_application_no(service_code)
    Application_Type = request.POST.get('Application_Type')
    Import_Type = request.POST.get('Import_Type')
    Nationality = request.POST.get('nationality')
    Country = request.POST.get('Country')
    cid = request.POST.get('cid')
    Name = request.POST.get('Name')
    present_address = request.POST.get('present_address')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    license_no = request.POST.get('license_no')
    business_name = request.POST.get('business_name')
    Origin_Source_Products = request.POST.get('Origin_Source_Products')
    Name_And_Address_Supplier = request.POST.get('Name_And_Address_Supplier')
    Final_Destination = request.POST.get('Final_Destination')
    Expected_Arrival_Date = request.POST.get('Expected_Arrival_Date')
    expected_date = datetime.strptime(Expected_Arrival_Date, '%d-%m-%Y').date()
    conveyanceMeans = request.POST.get('p_conveyanceMeans')
    point_of_entry = request.POST.get('Actual_Point_Of_Entry')

    t_livestock_import_permit_product_t1.objects.create(
        Application_No=application_no,
        Application_Type=Application_Type,
        Import_Type=Import_Type,
        License_No=license_no,
        Business_Name=business_name,
        Nationality=Nationality,
        Country=Country,
        CID=cid,
        Applicant_Name=Name,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Present_Address=present_address,
        Contact_No=contact_number,
        Email=email,
        Origin_Source_Products=Origin_Source_Products,
        Name_And_Address_Supplier=Name_And_Address_Supplier,
        Means_of_Conveyance=conveyanceMeans,
        Place_Of_Entry=point_of_entry,
        Final_Destination=Final_Destination,
        Expected_Arrival_Date=expected_date,
        FO_Remarks=None,
        Application_Date=date.today(),
        Approve_Date=None,
        Validity_Period=None,
        Validity=None,
        Import_Permit_No=None
    )

    t_workflow_details.objects.create(Application_No=application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Livestock',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = application_no
    return JsonResponse(data)


def livestock_product_application_no(service_code):
    last_application_no = t_livestock_import_permit_product_t1.objects.aggregate(Max('Application_No'))
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


def import_livestock_product_details(request):
    application_id = request.POST.get('appNo')
    Particulars = request.POST.get('Particulars')
    Company_Name = request.POST.get('Company_Name')
    Description = request.POST.get('Description')
    Quantity = request.POST.get('qty')
    Unit = request.POST.get('unit')
    t_livestock_import_permit_product_t2.objects.create(Application_No=application_id, Particulars=Particulars,
                                                        Company_Name=Company_Name, Description=Description,
                                                        Quantity=Quantity, Quantity_Balance=Quantity, Unit=Unit)
    import_details = t_livestock_import_permit_product_t2.objects.filter(Application_No=application_id)
    return render(request, 'Livestock_Import/permit_details.html', {'import': import_details})


def add_livestock_product_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/livestock/livestock_product_import")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/livestock/livestock_product_import" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def add_livestock_product_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
        return render(request, 'Livestock_Import/file_attachment.html', {'file_attach': file_attach})


def submit_livestock_product_application(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(import_permit)


def approve_fo_lp_import(request):
    service_code = "ILP"
    permit_no = get_lp_permit_no(service_code)
    application_no = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    validity = request.POST.get('validity')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    for app in workflow_details:
        client_login_id = app.Applicant_Id
        client_id = t_user_master.objects.filter(Email_Id=client_login_id)
        for client in client_id:
            login_id = client.Login_Id
            workflow_details.update(Assigned_To=login_id)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Assigned_Role_Id=None)
    details = t_livestock_import_permit_product_t1.objects.filter(Application_No=application_no)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    details.update(Validity_Period=validity)
    details.update(Import_Permit_No=permit_no)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    print(validity_date)
    details.update(Validity=validity_date)
    for email_id in details:
        email = email_id.Email
        send_lp_approve_email(permit_no, email, validity_date)
    update_payment(application_no, permit_no, 'ILP', validity_date)
    return render(request, 'focal_officer_pending_list.html')


def reject_fo_lp_import(request):
    application_no = request.GET.get('application_id')
    remarks = request.POST.get('remarks')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Application_Status='R')
    details = t_livestock_import_permit_product_t1.objects.filter(Application_No=application_no)
    details.update(FO_Remarks=remarks)
    for email_id in details:
        email = email_id.Email
        send_lp_reject_email(email, remarks)


def send_lp_approve_email(new_import_permit, Email, validity_date):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Livestock Product And Animal Feeds Has Been Approved. Your " \
              "Import Permit No is:" + new_import_permit + " And is Valid TIll " + str(validity_date) + \
              " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_lp_reject_email(Email, remarks):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Livestock Product And Animal Feeds Has Been Rejected." \
              " Reason: " + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def get_lp_permit_no(service_code):
    last_import_permit_no = t_livestock_import_permit_product_t1.objects.aggregate(Max('Import_Permit_No'))
    last_permit_no = last_import_permit_no['Import_Permit_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = service_code + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_permit_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = service_code + "/" + str(year) + "/" + AppNo
    return newPermitNo


def submit_lp_application(request):
    application_no = request.GET.get('application_no')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    timeOfInspection = request.GET.get('timeOfInspection')
    expected_date = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    clearnace_ref_no = lp_clearance_no(request)

    update_details = t_livestock_import_permit_product_inspection_t1.objects.filter(Application_No=application_no)
    update_details.update(Clearance_Ref_No=clearnace_ref_no)
    update_details.update(Inspection_Leader=Inspection_Leader)
    update_details.update(Inspection_Team=Inspection_Team)
    update_details.update(Inspection_Date=expected_date)
    update_details.update(Inspection_Time=timeOfInspection)
    if remarks is not None:
        update_details.update(Inspection_Remarks=remarks)
    else:
        update_details.update(Inspection_Remarks=None)
    application_details = t_workflow_details.objects.filter(Application_No=application_no)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='C')
    application_list = t_workflow_details.objects.filter(Application_Status='A')

    return render(request, 'inspector_pending_list.html',
                  {'service_name': None, 'application_details': application_list})


def lp_clearance_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_clearance_ref_no = t_livestock_import_permit_product_inspection_t1.objects.aggregate(Max('Clearance_Ref_No'))
    last_permit_no = last_clearance_ref_no['Clearance_Ref_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = Field_Code + "/" + "IAF" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = Field_Code + "/" + "IAF" + "/" + str(year) + "/" + AppNo
    return newPermitNo


def edit_lp_inspector_details(request, Record_Id):
    roles = get_object_or_404(t_livestock_import_permit_product_inspection_t2, pk=Record_Id)
    Quantity_Released = request.POST.get('Quantity_Released')
    Remarks = request.POST.get('Remarks')
    if request.method == 'POST':
        form = ImportFormProduct(request.POST, instance=roles)
    else:
        form = ImportFormProduct(instance=roles)
    return save_lp_inspector_details(request, form, Record_Id, Quantity_Released, Remarks,
                                     'Livestock_Import/edit_inspector_details.html')


def save_lp_inspector_details(request, form, Record_Id, Quantity_Released, Remarks, template_name):
    data = dict()
    if request.method == 'POST':
        import_det = t_livestock_import_permit_product_inspection_t2.objects.filter(pk=Record_Id)
        import_det.update(Quantity_Released=Quantity_Released)
        import_det.update(Remarks=Remarks)
        for import_LP in import_det:
            Product_Record_Id = import_LP.Product_Record_Id
            balance = int(import_LP.Quantity_Balance) - int(import_LP.Quantity_Released)
            product_details = t_livestock_import_permit_product_t2.objects.filter(pk=Product_Record_Id)
            product_details.update(Quantity_Balance=balance)
        roles = t_livestock_import_permit_product_inspection_t2.objects.all()
        data['html_book_list'] = render_to_string('Livestock_Import/details_import.html', {
            'import': roles, 'balance': balance
        })
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# export certificate for animal and animal products
def export_certificate_application(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_field_office_master.objects.filter(Is_Entry_Point='Y')
    unit = t_unit_master.objects.all()
    return render(request, 'Export_Certificate/export_certificate_application.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'unit': unit})


def save_livestock_export(request):
    data = dict()
    service_code = "LEC"
    application_no = livestock_export_application_no(service_code)

    applicant_Id = request.session['email']
    Application_Type = request.POST.get('Application_Type')
    Exporter_Type = request.POST.get('Exporter_Type')
    Nationality = request.POST.get('Nationality')
    Country = request.POST.get('Country')
    cid = request.POST.get('cid')
    Name = request.POST.get('Name')
    present_address = request.POST.get('present_address')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    license_no = request.POST.get('license_no')
    business_name = request.POST.get('business_name')
    purpose = request.POST.get('Purpose')
    Origin_Source_Products = request.POST.get('Origin_Source_Products')
    Importer_Name_Address = request.POST.get('Importer_Name_Address')
    Final_Destination = request.POST.get('Final_Destination')
    Place_of_Exit = request.POST.get('Place_of_Exit')
    Export_Expected_Date = request.POST.get('Export_Expected_Date')
    inspectionDate = request.POST.get('inspectionDate')
    date_format_ins = datetime.strptime(inspectionDate, '%d-%m-%Y').date()
    export_date = datetime.strptime(Export_Expected_Date, '%d-%m-%Y').date()

    t_livestock_export_certificate_t1.objects.create(
        Application_No=application_no,
        Application_Date=date.today(),
        Application_Type=Application_Type,
        Exporter_Type=Exporter_Type,
        Nationality=Nationality,
        Country=Country,
        CID=cid,
        Applicant_Name=Name,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        License_No=license_no,
        Business_Name=business_name,
        Present_Address=present_address,
        Contact_No=contact_number,
        Email=email,
        Origin_Source_Products=Origin_Source_Products,
        Importer_Name_Address=Importer_Name_Address,
        Purpose=purpose,
        Place_of_Exit=Place_of_Exit,
        Final_Destination=Final_Destination,
        Export_Expected_Date=export_date,
        Proposed_Inspection_Date=date_format_ins,
        Inspection_Date=None,
        Inspection_Type=None,
        Inspection_Time=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Inspection_Remarks=None,
        Export_Permit_No=None,
        Approve_Date=None,
        Validity_Period=None,
        Validity=None,
        Applicant_Id=applicant_Id
    )
    field = t_location_field_office_mapping.objects.filter(Location_Code=Place_of_Exit)
    for field_office in field:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(Application_No=application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=field_office_id, Section='Livestock',
                                      Assigned_Role_Id='4', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = application_no
    data['Application_Type'] = Application_Type
    return JsonResponse(data)


def livestock_export_application_no(service_code):
    last_application_no = t_livestock_export_certificate_t1.objects.aggregate(Max('Application_No'))
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


def save_liv_export_details(request):
    if request.method == 'POST':
        Permit_Type = request.POST.get('app_type')
        print(Permit_Type)
        if Permit_Type == 'A':
            application_no = request.POST.get('appNo')
            Species = request.POST.get('Species')
            Breed = request.POST.get('Breed')
            Age = request.POST.get('Age')
            Sex = request.POST.get('Sex')
            No_Of_Animal = request.POST.get('No_Of_Animal')
            Remarks = request.POST.get('Remarks')
            Description = request.POST.get('Description')

            t_livestock_export_certificate_t2.objects.create(
                Application_No=application_no,
                Species=Species,
                Breed=Breed,
                Age=Age,
                Sex=Sex,
                Particulars=None,
                Company_Name=None,
                Description=Description,
                Quantity=None,
                Quantity_Released=None,
                Remarks=Remarks,
                No_Of_Animal=No_Of_Animal,
                Unit=None
            )
            export_details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no)
            return render(request, 'Export_Certificate/animal_details.html', {'export_details': export_details})
        else:
            application_no = request.POST.get('appNo')
            Particulars = request.POST.get('Species')
            Company_Name = request.POST.get('Company_Name')
            Quantity = request.POST.get('Quantity')
            Unit = request.POST.get('Unit')
            Remarks = request.POST.get('Remarks')

            t_livestock_export_certificate_t2.objects.create(
                Application_No=application_no,
                Species=None,
                Breed=None,
                Age=None,
                Sex=None,
                Particulars=Particulars,
                Company_Name=Company_Name,
                Description=None,
                Quantity=Quantity,
                Quantity_Released=None,
                Remarks=Remarks,
                No_Of_Animal=None,
                Unit=Unit
            )
            export_details = t_livestock_export_certificate_t2.objects.filter(Application_No=application_no)
            return render(request, 'Export_Certificate/animal_product_details.html', {'export_details': export_details})


def add_liv_export_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/livestock/export_certificate")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/livestock/export_certificate" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def add_ec_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
        return render(request, 'Export_Certificate/file_attachment.html', {'file_attach': file_attach})


def submit_ec_details(request):
    application_no = request.GET.get('appNo')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(export_certificate_application)


def approve_application_export(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    Export_Permit_No = export_permit_no(request)
    validity = request.GET.get('validity')
    insTime = request.GET.get('insTime')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_export_certificate_t1.objects.filter(Application_No=application_id)

    if remarks is not None:
        details.update(Inspection_Remarks=remarks)
    else:
        details.update(Inspection_Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Export_Permit_No=Export_Permit_No)
    details.update(Validity_Period=validity)
    details.update(Approve_Date=date.today())
    details.update(Inspection_Time=insTime)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    update_payment(application_id, Export_Permit_No, 'LEC', validity_date)
    for email_id in details:
        emailId = email_id.Email
        send_lms_approve_email(Export_Permit_No, emailId, validity_date)
    return redirect(inspector_application)


def reject_application_export(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_export_certificate_t1.objects.filter(Application_No=application_id)

    details.update(Remarks_Inspection=remarks)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Application_Status='R')
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='R')
    for email_id in details:
        email = email_id.Email
        send_lms_reject_email(remarks, email)
    return redirect(inspector_application)


def export_permit_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_livestock_export_certificate_t1.objects.aggregate(Max('Export_Permit_No'))
    lastAppNo = last_application_no['Export_Permit_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "LEC" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "LEC" + "/" + str(year) + "/" + AppNo
    return newAppNo


def send_lec_approve_email(Export_Permit_No, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for Export Certificate of Animal and Animal Products Has Been Approved. " \
              "Your " \
              "Registration No is:" + Export_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_lec_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + "Your Application for Export Certificate of Animal and Animal Products Has" \
                                " Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


# movement permit for animal, animal products and animal feed apply_movement_permit
def movement_permit_application(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'Movement_Permit_Livestock/apply_movement_permit.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'unit': unit})


def save_movement_permit_application(request):
    data = dict()
    service_code = "LMP"
    application_no = livestock_movement_permit_application_no(service_code)
    Permit_Type = request.POST.get('Permit_Type')
    CID = request.POST.get('cid')
    Name = request.POST.get('Name')
    Dzongkhag = request.POST.get('dzongkhag')
    Gewog = request.POST.get('gewog')
    Village = request.POST.get('village')
    contact_no = request.POST.get('contactNumber')
    Email = request.POST.get('email')
    license_no = request.POST.get('license_no')
    business_name = request.POST.get('business_name')
    from_dzongkhag = request.POST.get('from_dzongkhag')
    from_gewog = request.POST.get('from_gewog')
    from_location = request.POST.get('from_location')
    to_dzongkhag = request.POST.get('to_dzongkhag')
    to_gewog = request.POST.get('to_dzongkhag')
    to_exact_location = request.POST.get('to_exact_location')
    route = request.POST.get('route')
    conveyanceMeans = request.POST.get('conveyanceMeans')
    vehicleNo = request.POST.get('vehicleNo')
    movementPurpose = request.POST.get('movementPurpose')
    date_of_movement = request.POST.get('date')
    movement_date = datetime.strptime(date_of_movement, '%d-%m-%Y').date()
    t_livestock_movement_permit_t1.objects.create(
        Application_No=application_no,
        Permit_Type=Permit_Type,
        CID=CID,
        Applicant_Name=Name,
        Dzongkhag_Code=Dzongkhag,
        Gewog_Code=Gewog,
        Village_Code=Village,
        Contact_No=contact_no,
        Email=Email,
        License_No=license_no,
        Business_Name=business_name,
        From_Dzongkhag_Code=from_dzongkhag,
        From_Gewog_Code=from_gewog,
        From_Location=from_location,
        To_Dzongkhag_Code=to_dzongkhag,
        To_Gewog_Code=to_gewog,
        To_Location=to_exact_location,
        Authorized_Route=route,
        Movement_Purpose=movementPurpose,
        Conveyance_Means=conveyanceMeans,
        Vehicle_No=vehicleNo,
        Movement_Date=movement_date,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Application_Status=None,
        Movement_Permit_No=None,
        Remarks=None,
        Application_Date=date.today(),
        Applicant_Id=request.session['email'],
        Approved_Date=None,
        Validity_Period=None,
        Validity=None
    )
    field = t_location_field_office_mapping.objects.filter(Location_Code=from_gewog)
    for field_office in field:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(Application_No=application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=field_office_id, Section='Livestock',
                                      Assigned_Role_Id='4', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = application_no
    data['Permit_Type'] = Permit_Type
    return JsonResponse(data)


def livestock_movement_permit_application_no(service_code):
    last_application_no = t_livestock_movement_permit_t1.objects.aggregate(Max('Application_No'))
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


def save_movement_permit_details(request):
    if request.method == 'POST':
        application_no = request.POST.get('appNo')
        Permit_Type = request.POST.get('permit_type')
        if Permit_Type == 'A':
            Common_Name = request.POST.get('Common_Name')
            Scientific_Name = request.POST.get('Scientific_Name')
            Age = request.POST.get('Age')
            No_Of_Animal = request.POST.get('No_Of_Animal')
            Remarks = request.POST.get('Remarks')

            t_livestock_movement_permit_t2.objects.create(
                Application_No=application_no,
                Common_Name=Common_Name,
                Scientific_Name=Scientific_Name,
                Age=Age,
                Particulars=None,
                Company_Name=None,
                Description=None,
                Quantity=None,
                Unit=None,
                Quantity_Released=None,
                Remarks=Remarks,
                No_Of_Animal=No_Of_Animal)
            mortem_details = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no)
            return render(request, 'Movement_Permit_Livestock/animal_details.html', {'import': mortem_details})
        else:
            Particulars = request.POST.get('Species')
            Company_Name = request.POST.get('Company_Name')
            Quantity = request.POST.get('Quantity')
            Unit = request.POST.get('Unit')
            Remarks = request.POST.get('Remarks')

            t_livestock_movement_permit_t2.objects.create(
                Application_No=application_no,
                Common_Name=None,
                Scientific_Name=None,
                Age=None,
                Particulars=Particulars,
                Company_Name=Company_Name,
                Description=None,
                Quantity=Quantity,
                Unit=Unit,
                Quantity_Released=None,
                Remarks=Remarks,
                No_Of_Animal=None)
            mortem_details = t_livestock_movement_permit_t2.objects.filter(Application_No=application_no)
            return render(request, 'Movement_Permit_Livestock/animal_product_details.html', {'import': mortem_details})


def add_lmp_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/livestock/movement_permit")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/livestock/movement_permit" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def add_lmp_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
        return render(request, 'ante_post_mortem/file_attachment.html', {'file_attach': file_attach})


def submit_lmp_details(request):
    application_no = request.GET.get('appNo')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(movement_permit_application)


def details_ins_lmp(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_livestock_movement_permit_t3.objects.create(Application_No=application_id,
                                                  Current_Observation=currentObservation,
                                                  Decision_Conformity=decisionConform)
    observation = t_livestock_movement_permit_t3.objects.filter(Application_No=application_id)
    return render(request, 'Movement_Permit_Livestock/observation_details.html', {'observation': observation})


def approve_application_lmp(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    Movement_Permit_No = movement_permit_no(request)
    validity = request.GET.get('validity')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_movement_permit_t1.objects.filter(Application_No=application_id)

    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Movement_Permit_No=Movement_Permit_No)
    details.update(Validity_Period=validity)
    details.update(Approved_Date=date.today())
    details.update(Application_Status='A')
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    update_payment(application_id, Movement_Permit_No, 'LMP', validity_date)
    for email_id in details:
        emailId = email_id.Email
        send_lms_approve_email(Movement_Permit_No, emailId, validity_date)
    return redirect(inspector_application)


def reject_application_lmp(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_movement_permit_t1.objects.filter(Application_No=application_id)

    details.update(Remarks=remarks)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Application_Status='R')
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='R')
    for email_id in details:
        email = email_id.Email
        send_lms_reject_email(remarks, email)
    return redirect(inspector_application)


def movement_permit_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_livestock_movement_permit_t1.objects.aggregate(Max('Movement_Permit_No'))
    lastAppNo = last_application_no['Movement_Permit_No__max']
    print(lastAppNo)
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "LMP" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "LMP" + "/" + str(year) + "/" + AppNo
    return newAppNo


def send_lms_approve_email(Export_Permit_No, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for Movement Permit Of Live Animal and Animal Products Has Been Approved. " \
              "Your " \
              "Registration No is:" + Export_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_lms_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + "Your Application for Movement Permit Of Live Animal and Animal Products Has" \
                                " Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


# Ante Mortem And Post Mortem
def application_form(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'ante_post_mortem/ante_post_mortem_application.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def save_application_form(request):
    data = dict()
    service_code = "APM"
    application_no = get_mortem_application_no(service_code)
    Inspection_Type = request.POST.get('Inspection_Type')
    CID = request.POST.get('cid')
    Name = request.POST.get('Name')
    Dzongkhag = request.POST.get('dzongkhag')
    Gewog = request.POST.get('gewog')
    Village = request.POST.get('village')
    Address = request.POST.get('present_address')
    contact_no = request.POST.get('contactNumber')
    Email = request.POST.get('email')
    Location_Dzongkhag_Code = request.POST.get('Location_Dzongkhag_Code')
    location_code = request.POST.get('location_code')
    exact_location = request.POST.get('exact_location')
    inspectionDate = request.POST.get('inspectionDate')
    date_format_ins = datetime.strptime(inspectionDate, '%d-%m-%Y').date()

    t_livestock_ante_post_mortem_t1.objects.create(
        Application_No=application_no,
        Inspection_Type=Inspection_Type,
        CID=CID,
        Applicant_Name=Name,
        Dzongkhag_Code=Dzongkhag,
        Gewog_Code=Gewog,
        Village_Code=Village,
        Address=Address,
        Contact_No=contact_no,
        Email=Email,
        Location_Dzongkhag_Code=Location_Dzongkhag_Code,
        Location_Code=location_code,
        Exact_Location=exact_location,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Application_Status='P',
        Clearance_No=None,
        Remarks=None,
        Application_Date=date.today(),
        Applicant_Id=request.session['email'],
        Approved_Date=None,
        Validity_Period=None,
        Validity=None,
        Inspection_Date_Requested=date_format_ins,
        Respiration_Abnormalities=None,
        Behaviour_Abnormalities=None,
        Structure_Abnormalities=None,
        Abnormal_Gait=None,
        Abnormal_Posture=None,
        Discharge_Abnormalities=None,
        Abnormal_Colour=None,
        Abnormal_Odour=None,
        No_Without_Restrictions=None,
        No_Close_Supervision=None,
        No_Withheld=None,
        No_Emergency=None,
        No_Unfit=None
    )
    field = t_location_field_office_mapping.objects.filter(Location_Code=location_code)
    for field_office in field:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(Application_No=application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=field_office_id, Section='Livestock',
                                      Assigned_Role_Id='4', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = application_no
    return JsonResponse(data)


def get_mortem_application_no(service_code):
    last_application_no = t_livestock_ante_post_mortem_t1.objects.aggregate(Max('Application_No'))
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


def save_mortem_details(request):
    if request.method == 'POST':
        species = request.POST.get('Species')
        Nos = request.POST.get('Nos')
        qty = request.POST.get('qty')
        application_no = request.POST.get('application_no_details')
        remarks = request.POST.get('remarks')
        t_livestock_ante_post_mortem_t2.objects.create(Application_No=application_no, Species=species,
                                                       Nos=Nos, Quantity=qty, Remarks=remarks)
        mortem_details = t_livestock_ante_post_mortem_t2.objects.filter(Application_No=application_no)
    return render(request, 'ante_post_mortem/details.html', {'mortem': mortem_details})


def add_mortem_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/livestock/ante_post_mortem")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/livestock/ante_post_mortem" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def add_mortem_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'ante_post_mortem/file_attachment.html', {'file_attach': file_attach})


def submit_mortem_details(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(application_form)


def approve_application_apm(request):
    application_id = request.POST.get('application_id')
    print(application_id)
    Inspection_Leader = request.POST.get('Inspection_Leader')
    Inspection_Team = request.POST.get('Inspection_Team')
    remarks = request.POST.get('remarks')
    dateOfInspection = request.POST.get('dateOfInspection')
    Clearance_No = clearnace_no_apm(request)
    validity = request.POST.get('validity')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    Respiration_Abnormalities = request.POST.get('Respiration_Abnormalities'),
    Behaviour_Abnormalities = request.POST.getlist('Abnormalities_Behaviour'),
    Structure_Abnormalities = request.POST.getlist('Abnormalities_Structure'),
    Abnormal_Gait = request.POST.get('gait'),
    Abnormal_Posture = request.POST.get('posture'),
    Discharge_Abnormalities = request.POST.getlist('Discharge_Abnormalities'),
    Abnormal_Colour = request.POST.get('colour'),
    Abnormal_Odour = request.POST.get('odour'),
    No_Without_Restrictions = request.POST.get('fit_for_slaughter'),
    No_Close_Supervision = request.POST.get('fit_for_slaughter_supervision'),
    No_Withheld = request.POST.get('withheld_for_slaughter'),
    No_Emergency = request.POST.get('emergency_slaughter'),
    No_Unfit = request.POST.get('unfifit_for_consumption')

    details = t_livestock_ante_post_mortem_t1.objects.filter(Application_No=application_id)

    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Clearance_No=Clearance_No)
    details.update(Validity_Period=validity)
    details.update(Approved_Date=date.today())
    details.update(Application_Status='A')
    details.update(Respiration_Abnormalities=Respiration_Abnormalities)
    details.update(Behaviour_Abnormalities=Behaviour_Abnormalities)
    details.update(Structure_Abnormalities=Structure_Abnormalities)
    details.update(Abnormal_Gait=Abnormal_Gait)
    details.update(Abnormal_Posture=Abnormal_Posture)
    details.update(Discharge_Abnormalities=Discharge_Abnormalities)
    details.update(Abnormal_Colour=Abnormal_Colour)
    details.update(Abnormal_Odour=Abnormal_Odour)
    details.update(No_Without_Restrictions=No_Without_Restrictions)
    details.update(No_Close_Supervision=No_Close_Supervision)
    details.update(No_Withheld=No_Withheld)
    details.update(No_Emergency=No_Emergency)
    details.update(No_Unfit=No_Unfit)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    for email_id in details:
        emailId = email_id.Email
        send_apm_approve_email(Clearance_No, emailId, validity_date)
    update_payment(application_id, Clearance_No, 'APM', validity_date)
    return redirect(inspector_application)


def reject_application_apm(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_ante_post_mortem_t1.objects.filter(Application_No=application_id)

    details.update(Remarks_Inspection=remarks)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Application_Status='R')
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='R')
    for email_id in details:
        email = email_id.Email
        send_apm_approve_email(remarks, email)
    return redirect(inspector_application)


def clearnace_no_apm(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_livestock_ante_post_mortem_t1.objects.aggregate(Max('Clearance_No'))
    lastAppNo = last_application_no['Clearance_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "APM" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "APM" + "/" + str(year) + "/" + AppNo
    return newAppNo


def send_apm_approve_email(Export_Permit_No, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for Movement Permit Of Live Animal and Animal Products Has Been Approved. " \
              "Your " \
              "Registration No is:" + Export_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_apm_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + "Your Application for Movement Permit Of Live Animal and Animal Products Has" \
                                " Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


# Common
def update_payment(application_id, Permit_No, Service_Id, Validity):
    t_payment_details.objects.create(Application_No=application_id,
                                     Application_Date=date.today(),
                                     Permit_No=Permit_No,
                                     Service_Id=Service_Id,
                                     Validity=Validity,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)
