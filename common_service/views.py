from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_service_master, t_user_master, \
    t_location_field_office_mapping, t_field_office_master
from bbfss import settings

from common_service.models import t_common_complaint_t1, t_Inspection_monitoring_t2, t_Inspection_monitoring_t3, \
    t_Inspection_monitoring_t4
from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_clearance_meat_shop_t2
from livestock.views import meat_shop_clearance_no, update_payment

from plant.models import t_workflow_details, t_file_attachment
from plant.views import inspector_application


def co_complaint_list(request):
    # Role_Id = request.session['Role_Id']
    service_details = t_service_master.objects.all()
    complaint_details = t_workflow_details.objects.filter(Application_Status='P', Assigned_Role_Id='3')

    return render(request, 'complaint_officer_pending_list.html',
                  {'service_details': service_details, 'complaint_details': complaint_details})


def co_complaint_details(request):
    Application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    complaint_details = t_common_complaint_t1.objects.filter(Application_No=Application_No)

    inspector_list = t_user_master.objects.filter(Login_Type='I')

    return render(request, 'complaint_handling/complaint_officer_complaint_details.html',
                  {'complaint_details': complaint_details, 'inspector_list': inspector_list, 'dzongkhag': dzongkhag,
                   'gewog': gewog,
                   'village': village})


def apply_complaint_form(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    return render(request, 'complaint_handling/submit_complaint.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})


def submit_complaint(request):
    data = dict()
    service_code = "COM"
    last_application_no = get_complaint_application_no(request, service_code)
    applicant_Id = request.session['email']
    cid = request.POST.get('cid')
    complainantName = request.POST.get('complainantName')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    address = request.POST.get('address')
    complaint_description = request.POST.get('complainDescription')

    t_common_complaint_t1.objects.create(
        Application_No=last_application_no,
        Applicant_Id=applicant_Id,
        Application_Date=date.today(),
        CID=cid,
        Name=complainantName,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Contact_No=contact_number,
        Email=email,
        Address=address,
        Complaint_Description=complaint_description

    )

    t_workflow_details.objects.create(Application_No=last_application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Complaint',
                                      Assigned_Role_Id='3', Action_Date=date.today(), Application_Status='P',
                                      Service_Code=service_code)
    return JsonResponse(data)


def acknowledge_complaint(request):
    Application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    complaint_details = t_common_complaint_t1.objects.filter(Application_No=Application_No)

    inspector_list = t_user_master.objects.filter(Login_Type='I')

    return render(request, 'complaint_handling/complaint_officer_complaint_acknowledge.html',
                  {'complaint_details': complaint_details, 'inspector_list': inspector_list, 'dzongkhag': dzongkhag,
                   'gewog': gewog,
                   'village': village})


def get_complaint_no(request, service_code):
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


def complaint_app(request):
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


def clearance_print(request):
    return render(request, 'clearance_printing.html')


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


def complaint_no(request):
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


def get_complaint_application_no(request, service_code):
    last_application_no = t_common_complaint_t1.objects.aggregate(Max('Application_No'))
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


def inspection_and_monitoring_form(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    return render(request, 'inspection_monitoring/application_form.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})


def save_owner_manager_details(request):
    Reference_No = request.POST.get('owner_manager_app_no')
    Inspection_Date = request.POST.get('Inspection_Date')
    Inspector_Name = request.POST.get('Inspector_Name')
    Observation = request.POST.get('Observation')
    Correction_Proposed = request.POST.get('Correction_Proposed')
    Date_Line_Correction = request.POST.get('Date_Line_Correction')
    Correction_Taken = request.POST.get('Correction_Taken')
    Fine_Imposed = request.POST.get('Fine_Imposed')
    Revenue_Receipt = request.POST.get('Revenue_Receipt')
    Receipt_Date = request.POST.get('Receipt_Date')

    t_Inspection_monitoring_t2.objects.create(
        Reference_No=Reference_No,
        Inspection_Date=Inspection_Date,
        Inspector_Name=Inspector_Name,
        Observation=Observation,
        Correction_Proposed=Correction_Proposed,
        Date_Line_Correction=Date_Line_Correction,
        Correction_Taken=Correction_Taken,
        Fine_Imposed=Fine_Imposed,
        Revenue_Receipt=Revenue_Receipt,
        Receipt_Date=Receipt_Date
    )
    details = t_Inspection_monitoring_t2.objects.filter(Reference_No=Reference_No)
    return render(request, 'inspection_monitoring/owner_manager_details.html', {'details': details})


def save_item_details(request):
    Reference_No = request.POST.get('details_application_no')
    Inspection_Date = request.POST.get('item_Inspection_Date')
    Inspector_Name = request.POST.get('Item_Inspector_Name')
    Items_Seized = request.POST.get('Items_Seized')
    Qty_Seized = request.POST.get('Qty_Seized')
    Unit = request.POST.get('Unit')
    Reason = request.POST.get('reason')
    Fine_Imposed = request.POST.get('Item_Fine_Imposed')
    Revenue_Receipt = request.POST.get('Item_Revenue_Receipt')
    Receipt_Date = request.POST.get('Item_Receipt_Date')

    t_Inspection_monitoring_t3.objects.create(
        Reference_No=Reference_No,
        Inspection_Date=Inspection_Date,
        Inspector_Name=Inspector_Name,
        Items_Seized=Items_Seized,
        Qty_Seized=Qty_Seized,
        Unit=Unit,
        Reason=Reason,
        Fine_Imposed=Fine_Imposed,
        Revenue_Receipt=Revenue_Receipt,
        Receipt_Date=Receipt_Date
    )
    details = t_Inspection_monitoring_t3.objects.filter(Reference_No=Reference_No)
    return render(request, 'inspection_monitoring/item_details.html', {'details': details})


def save_sample_details(request):
    Reference_No = request.POST.get('sample_collection_application_no')
    Collection_Type = request.POST.get('Collection_Type')
    Collection_Date = request.POST.get('Collection_Date')
    Submission_Date = request.POST.get('Submission_Date')
    HS_Code_Imp = request.POST.get('HS_Code_Imp')
    HS_Code_Local = request.POST.get('HS_Code_Local')
    Sample_Type = request.POST.get('Sample_Type')
    Qty = request.POST.get('Qty')
    Batch_No_Date = request.POST.get('Batch_No_Date')
    Test_Requested = request.POST.get('Test_Requested')
    Test_Report = request.POST.get('Test_Report')
    t_Inspection_monitoring_t4.objects.create(
        Reference_No=Reference_No,
        Collection_Type=Collection_Type,
        Collection_Date=Collection_Date,
        Submission_Date=Submission_Date,
        HS_Code_Imp=HS_Code_Imp,
        HS_Code_Local=HS_Code_Local,
        Sample_Type=Sample_Type,
        Qty=Qty,
        Batch_No_Date=Batch_No_Date,
        Test_Requested=Test_Requested,
        Test_Report=Test_Report
    )
    details = t_Inspection_monitoring_t4.objects.filter(Reference_No=Reference_No)
    return render(request, 'inspection_monitoring/sample_collection_details.html', {'details': details})
