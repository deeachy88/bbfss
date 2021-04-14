from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.dateparse import parse_date
from django.utils.formats import date_format

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_location_field_office_mapping, \
    t_user_master, t_field_office_master, t_plant_crop_master, t_plant_pesticide_master, t_plant_crop_variety_master, \
    t_service_master
from bbfss import settings
from livestock.forms import MeatShopClearanceFormOne, MeatShopClearanceFormTwo
from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_clearance_meat_shop_t2
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
        Conformity=None,
        Conformity_Statement=None,
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
    print(application_id)
    return render(request, 'clearance_meat_shop/details_meat_shop.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location_code': location})


def load_attachment_details(request):
    application_id = request.GET.get('application_id')
    print(application_id)
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
    return render(request, 'movement_permit/ile_attachment_page.html', {'file_attach': file_attach})


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


def update_payment(application_id, Meat_Shop_Clearance_No, Service_Id, Validity):
    t_payment_details.objects.create(Application_No=application_id,
                                     Application_Date=date.today(),
                                     Permit_No=Meat_Shop_Clearance_No,
                                     Service_Id=Service_Id,
                                     Validity=Validity,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)
