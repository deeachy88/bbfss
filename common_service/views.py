from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_service_master, t_user_master
from bbfss import settings

from common_service.models import t_common_complaint_t1

from plant.models import t_workflow_details, t_file_attachment
from plant.views import inspector_application


def co_complaint_list(request):
    #Role_Id = request.session['Role_Id']
    service_details = t_service_master.objects.all()
    complaint_details = t_workflow_details.objects.filter(Application_Status='P', Assigned_Role_Id='3')

    return render(request, 'complaint_officer_pending_list.html', {'service_details': service_details, 'complaint_details': complaint_details})

def co_complaint_details(request):
    Application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)

    inspector_list = t_user_master.objects.filter(Login_Type='I')

    return render(request, 'complaint_handling/complaint_officer_complaint_forward.html', {'complaint_details': details, 'inspector_list': inspector_list, 'dzongkhag': dzongkhag, 'gewog': gewog,
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

def load_attachment_details(request):
    application_id = request.GET.get('application_id')
    attachment_details = t_file_attachment.objects.filter(Application_No=application_id)
    return render(request, 'clearance_meat_shop/meat_shop_file_attachment_page.html',
                  {'file_attach': attachment_details})

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

    c_details.update(Acknowledge='Y')
    c_details.update(Acknowledge_Remarks=remarks)
    c_details.update(Acknowledge_Date=date.today())
    send_acknowledge_email(app_no, application_date, remarks, email)
    return redirect(co_complaint_list)

def forward_complaint_by_co(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    identification_No = request.GET.get('identification_No')
    revision_no = request.GET.get('revision_no')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_common_complaint_t1.objects.filter(Application_No=application_id)
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
    return redirect(co_complaint_list)


def forward_complaint_to_co(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    identification_No = request.GET.get('identification_No')
    revision_no = request.GET.get('revision_no')

    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_common_complaint_t1.objects.filter(Application_No=application_id)

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
    return redirect(co_complaint_list)


def close_complaint(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    revision_no = request.GET.get('revision_no')

    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_common_complaint_t1.objects.filter(Application_No=application_id)

    if revision_no is not None:
        details.update(Revision_No=revision_no)
    else:
        details.update(Revision_No=None)
    details.update(Remarks_Inspection=remarks)
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
        send_close_email(remarks, email)
    return redirect(co_complaint_list)

def send_acknowledge_email(app_no, app_date,ack_remarks, email_id):
    subject = 'COMPLAINT APPLICATION ACCEPTED'
    message = "Dear Sir/Madam, This has reference to your application number " + app_no + " dated: " + str(app_date) + ", regarding your complaint on " + ack_remarks + ". Kindly quote this complaint registration number in all your future correspondence. We will inform you of the outcome of the complaint as soon as investigation is over."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_id]
    send_mail(subject, message, email_from, recipient_list)


def send_close_email(remarks, Email):
    subject = 'COMPLAINT CLOSED'
    message = "Dear " + "Sir" + " Your Complaint has been closed" + remarks + ""
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
