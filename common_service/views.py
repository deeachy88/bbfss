from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_service_master, t_user_master, \
    t_location_field_office_mapping, t_field_office_master, t_unit_master
from bbfss import settings

from common_service.models import t_common_complaint_t1, t_inspection_monitoring_t1, t_inspection_monitoring_t2, \
    t_inspection_monitoring_t3, t_inspection_monitoring_t4
from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_clearance_meat_shop_t2
from livestock.views import meat_shop_clearance_no, update_payment

from plant.models import t_workflow_details, t_file_attachment
from plant.views import inspector_application


def co_complaint_list(request):
    # Role_Id = request.session['Role_Id']
    # global acknowledge_status
    # service_details = t_service_master.objects.all()
    complaint_details = t_workflow_details.objects.filter(Application_Status='P',
                                                          Assigned_Role_Id='3') | t_workflow_details.objects.filter(
        Application_Status='A', Assigned_Role_Id='3')
    # for application_number in complaint_details:
    # app_no = application_number.Application_No
    # acknowledge_status = t_common_complaint_t1.objects.filter(Application_No=app_no)
    return render(request, 'complaint_officer_pending_list.html', {'complaint_details': complaint_details})


def investigation_report_list(request):  # list of investigation report submitted to the Complaint Officer
    complaint_details = t_workflow_details.objects.filter(Application_Status='IR', Assigned_Role_Id='3')
    return render(request, 'complaint_officer_investigation_report_list.html', {'complaint_details': complaint_details})


def investigation_report_details(request):
    Application_No = request.GET.get('application_id')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    for userId in details:
        user_id = userId.Assign_To
        user_details = t_user_master.objects.filter(Login_Id=user_id)

    return render(request, 'complaint_handling/complaint_officer_complaint_close.html',
                  {'complaint_details': details, 'user_details': user_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village})


def investigation_complaint_list(request):
    Login_Id = request.session['login_id']
    # Role_Id = request.session['Role_Id']
    global investigation_list
    in_complaint_list = t_workflow_details.objects.filter(Assigned_To=Login_Id, Application_Status='A')

    return render(request, 'complaint_investigation_pending_list.html', {'in_complaint_list': in_complaint_list})


def co_complaint_details(request):
    Application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)

    inspector_list = t_user_master.objects.all()

    return render(request, 'complaint_handling/complaint_officer_complaint_forward.html', {'complaint_details': details, 'inspector_list': inspector_list, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village})

def investigation_complaint_details(request):
    Application_No = request.GET.get('application_id')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    return render(request, 'complaint_handling/investigation_complaint_update.html', {'complaint_details': details, 'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})

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
        Complaint_Description=complaint_description,
        Application_Status='P'

    )

    t_workflow_details.objects.create(Application_No=last_application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Complaint',
                                      Assigned_Role_Id='3', Action_Date=date.today(), Application_Status='P',
                                      Service_Code=service_code)
    return JsonResponse(data)


def complaint_details(request):
    Application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    complaint_details = t_common_complaint_t1.objects.filter(Application_No=Application_No)

    inspector_list = t_user_master.objects.filter(Login_Type='I')

    return render(request, 'complaint_handling/complaint_officer_complaint_acknowledge.html', {'complaint_details': complaint_details, 'inspector_list': inspector_list, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village})

def load_gewog(request):
    dzongkhag_id = request.GET.get('dzongkhag_id')
    gewog_list = t_gewog_master.objects.filter(Dzongkhag_Code_id=dzongkhag_id).order_by('Gewog_Name')
    return render(request, 'gewog_list.html', {'gewog_list': gewog_list})

def load_village(request):
    gewog_id = request.GET.get('gewog_id')
    village_list = t_village_master.objects.filter(Gewog_Code_id=gewog_id).order_by('Village_Name')
    return render(request, 'village_list.html', {'village_list': village_list})

def acknowledge_complaint(request):
    app_no = request.POST.get('applicationNo')
    remarks = request.POST.get('acknowledgeRemarks')
    c_details = t_common_complaint_t1.objects.filter(Application_No=app_no)
    for email_id in c_details:
        email = email_id.Email
        application_date = email_id.Application_Date

    workflow_details = t_workflow_details.objects.filter(Application_No = app_no)
    c_details.update(Acknowledge='Y')
    c_details.update(Acknowledge_Remarks=remarks)
    c_details.update(Acknowledge_Date=date.today())
    c_details.update(Application_Status='A')

    workflow_details.update(Application_Status='A')
    send_acknowledge_email(app_no, application_date, remarks, email)
    return redirect(co_complaint_list)

def forward_complaint_by_co(request):
    app_no = request.POST.get('applicationNo')
    remarks = request.POST.get('forwardRemarks')
    forward_to = request.POST.get('forwardTo')
    forward_details = t_common_complaint_t1.objects.filter(Application_No=app_no)

    forward_details.update(Assign_To=forward_to)
    forward_details.update(Assign_Remarks=remarks)
    forward_details.update(Assign_Date=date.today())

    application_details = t_workflow_details.objects.filter(Application_No=app_no)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_To=forward_to)
    application_details.update(Assigned_Role_Id=None)
    return redirect(co_complaint_list)


def forward_complaint_to_co(request):
    app_no = request.POST.get('applicationNo')
    investigation_report = request.POST.get('investigationReport')
    investigation_date = request.POST.get('investigationDate')
    #forward_to = request.POST.get('forwardTo')
    forward_details = t_common_complaint_t1.objects.filter(Application_No=app_no)

    forward_details.update(Investigation_Report=investigation_report)
    forward_details.update(Investigation_Date=investigation_date)
    forward_details.update(Application_Status='IR')

    application_details = t_workflow_details.objects.filter(Application_No=app_no)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_To=None)
    application_details.update(Assigned_Role_Id='3')
    application_details.update(Application_Status='IR')  #IR - Investigation Report complete
    return redirect(investigation_complaint_list)

def close_complaint(request):
    app_no = request.POST.get('applicationNo')
    closure_remarks = request.POST.get('closeRemarks')
    c_details = t_common_complaint_t1.objects.filter(Application_No=app_no)
    for email_id in c_details:
        email = email_id.Email
        application_date = email_id.Application_Date
        investigation_report = email_id.Investigation_Report
        investigation_date = email_id.Investigation_Date

    c_details.update(Closure_Remarks=closure_remarks)
    c_details.update(Closure_Date=date.today())
    c_details.update(Application_Status='C')

    application_details = t_workflow_details.objects.filter(Application_No=app_no)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_To=None)
    #application_details.update(Assigned_Role_Id=None)
    application_details.update(Application_Status='C')
    send_close_email(app_no, application_date, closure_remarks, email, investigation_report, investigation_date)
    return redirect(investigation_report_list)


def send_acknowledge_email(app_no, app_date,ack_remarks, email_id):
    subject = 'COMPLAINT APPLICATION ACCEPTED'
    message = "Dear Sir/Madam, This has reference to your application number " + app_no + " dated: " + str(app_date) + ", regarding your complaint on " + ack_remarks + ". Kindly quote this complaint registration number in all your future correspondence. We will inform you of the outcome of the complaint as soon as investigation is over."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_id]
    send_mail(subject, message, email_from, recipient_list)


def send_close_email(app_no, app_date, close_remarks, email_id, in_report, in_date):
    subject = 'COMPLAINT CLOSED'
    message = "Dear " + "Sir/Madam, This has reference to your complaint registered with us Registration No." \
                        "" + app_no + " dated " + str(app_date) + ". Please find below our decision or findings here :"\
                        "" + close_remarks + ".Thank You"

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_id]
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
    unit = t_unit_master.objects.all()
    return render(request, 'inspection_monitoring/application_form.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village, 'unit': unit})


def save_monitoring_form(request):
    data = dict()
    service_code = "IAM"
    monitoring_ref_no = get_monitoring_ref_no(service_code)
    Inspection_Type = request.POST.get('Inspection_Type')
    inspection_report_date = request.POST.get('inspection_report_date')
    FBO_Name = request.POST.get('FBO_Name')
    License_No = request.POST.get('License_No')
    Address = request.POST.get('Address')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    cid = request.POST.get('cid')
    owner_name = request.POST.get('owner_name')
    email = request.POST.get('email')
    contactNumber = request.POST.get('contactNumber')
    date_format_ins = datetime.strptime(inspection_report_date, '%d-%m-%Y').date()

    t_inspection_monitoring_t1.objects.create(
        Reference_No=monitoring_ref_no,
        Inspection_Type=Inspection_Type,
        FBO_Name=FBO_Name,
        License_No=License_No,
        Address=Address,
        Email=email,
        Contact_No=contactNumber,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        CID=cid,
        Inspection_Report_Date=date_format_ins,
        Name_Of_Owner=owner_name,
        Service_Code=service_code
    )
    data['applNo'] = monitoring_ref_no
    return JsonResponse(data)


def get_monitoring_ref_no(service_code):
    last_application_no = t_inspection_monitoring_t1.objects.aggregate(Max('Reference_No'))
    lastAppNo = last_application_no['Reference_No__max']
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
    date_format_ins = datetime.strptime(Inspection_Date, '%d-%m-%Y').date()
    date_of_receipt = datetime.strptime(Receipt_Date, '%d-%m-%Y').date()
    date_line = datetime.strptime(Date_Line_Correction, '%d-%m-%Y').date()

    t_inspection_monitoring_t2.objects.create(
        Reference_No=Reference_No,
        Inspection_Date=date_format_ins,
        Inspector_Name=Inspector_Name,
        Observation=Observation,
        Correction_Proposed=Correction_Proposed,
        Date_Line_Correction=date_line,
        Correction_Taken=Correction_Taken,
        Fine_Imposed=Fine_Imposed,
        Revenue_Receipt=Revenue_Receipt,
        Receipt_Date=date_of_receipt
    )
    details = t_inspection_monitoring_t2.objects.filter(Reference_No=Reference_No)
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
    Detaintion_Destruction_No = request.POST.get('Detaintion_Destruction_No')
    date_format_ins = datetime.strptime(Inspection_Date, '%d-%m-%Y').date()
    date_of_receipt = datetime.strptime(Receipt_Date, '%d-%m-%Y').date()

    t_inspection_monitoring_t3.objects.create(
        Reference_No=Reference_No,
        Inspection_Date=date_format_ins,
        Inspector_Name=Inspector_Name,
        Items_Seized=Items_Seized,
        Qty_Seized=Qty_Seized,
        Unit=Unit,
        Reason=Reason,
        Fine_Imposed=Fine_Imposed,
        Revenue_Receipt=Revenue_Receipt,
        Receipt_Date=date_of_receipt,
        Detaintion_Destruction_No=Detaintion_Destruction_No
    )
    details = t_inspection_monitoring_t3.objects.filter(Reference_No=Reference_No)
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
    date_format_collection = datetime.strptime(Collection_Date, '%d-%m-%Y').date()
    date_of_submission = datetime.strptime(Submission_Date, '%d-%m-%Y').date()

    t_inspection_monitoring_t4.objects.create(
        Reference_No=Reference_No,
        Collection_Date=date_format_collection,
        Submission_Date=date_of_submission,
        HS_Code_Imp=HS_Code_Imp,
        HS_Code_Local=HS_Code_Local,
        Sample_Type=Sample_Type,
        Qty=Qty,
        Batch_No_Date=Batch_No_Date,
        Test_Requested=Test_Requested,
        Test_Report=Test_Report
    )
    details = t_inspection_monitoring_t4.objects.filter(Reference_No=Reference_No)
    return render(request, 'inspection_monitoring/sample_collection_details.html', {'details': details})


def inspection_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/common_service/inspection_monitoring")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/common_service/inspection_monitoring" + "/" \
                   + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def inspection_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'inspection_monitoring/file_attachment.html', {'file_attach': file_attach})


def submit_inspection_details(request):
    Application_No = request.POST.get('application_no')
    details = t_inspection_monitoring_t1.objects.filter(Reference_No=Application_No)
    details.update(Application_Flag='C')
    details.update(Application_Date=date.today())
    return redirect(inspection_and_monitoring_form)


def draft_application_list(request):
    application_details = t_inspection_monitoring_t1.objects.filter(Application_Flag='P')
    service_details = t_service_master.objects.all()
    return render(request, 'inspection_monitoring/draft_application.html',
                  {'application_details': application_details, 'service_details': service_details})


def view_draft_details(request):
    reference_no = request.GET.get('reference_no')
    application_details = t_inspection_monitoring_t1.objects.filter(Reference_No=reference_no)
    details = t_inspection_monitoring_t2.objects.filter(Reference_No=reference_no)
    t3_details = t_inspection_monitoring_t3.objects.filter(Reference_No=reference_no)
    t4_details = t_inspection_monitoring_t4.objects.filter(Reference_No=reference_no)
    file_attach = t_file_attachment.objects.filter(Application_No=reference_no)
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'inspection_monitoring/draft_application_details.html',
                  {'application_details': application_details, 'details': details, 't3_details': t3_details,
                   't4_details': t4_details, 'file_attach': file_attach, 'dzongkhag': dzongkhag,
                   'gewog': gewog, 'village': village, 'unit': unit})


def update_inspection_details(request):
    data = dict()
    reference_no = request.POST.get('reference_no')
    Inspection_Type = request.POST.get('Inspection_Type')
    inspection_report_date = request.POST.get('inspection_report_date')
    FBO_Name = request.POST.get('FBO_Name')
    License_No = request.POST.get('License_No')
    Address = request.POST.get('Address')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    cid = request.POST.get('cid')
    owner_name = request.POST.get('owner_name')
    email = request.POST.get('email')
    contactNumber = request.POST.get('contactNumber')
    date_format_ins = datetime.strptime(inspection_report_date, '%d-%m-%Y').date()

    details = t_inspection_monitoring_t1.objects.filter(Reference_No=reference_no)
    details.update(
        Inspection_Type=Inspection_Type,
        FBO_Name=FBO_Name,
        License_No=License_No,
        Address=Address,
        Email=email,
        Contact_No=contactNumber,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        CID=cid,
        Inspection_Report_Date=date_format_ins,
        Name_Of_Owner=owner_name
    )
    data['applNo'] = reference_no
    return JsonResponse(data)


def submit_draft_inspection_details(request):
    Application_No = request.POST.get('application_no')
    details = t_inspection_monitoring_t1.objects.filter(Reference_No=Application_No)
    details.update(Application_Flag='C')
    details.update(Application_Date=date.today())
    return redirect(draft_application_list)
