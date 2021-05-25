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
    #applicant_details = t_common_complaint_t1.objects.filter(Application_Status='P') | t_common_complaint_t1.objects.filter(Application_Status='A')
    complaint_details = t_workflow_details.objects.filter(Application_Status='P', Assigned_Role_Id='3') | t_workflow_details.objects.filter(Application_Status='A', Assigned_Role_Id='3')
    #for application_number in complaint_details:
        #app_no = application_number.Application_No
        #acknowledge_status = t_common_complaint_t1.objects.filter(Application_No=app_no)

    #return render(request, 'focal_officer_pending_list.html', {'complaint_details': complaint_details, 'applicant_details': applicant_details})

    return render(request, 'complaint_officer_pending_list.html', {'complaint_details': complaint_details})

def complaint_closed_list(request):
    complaint_closed_details = t_workflow_details.objects.filter(Application_Status='C', Assigned_Role_Id='3')
    return render(request, 'complaint_closed_list.html', {'complaint_details': complaint_closed_details})

def complaint_closed_details(request):
    Application_No = request.GET.get('application_id')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    for userId in details:
        user_id = userId.Assign_To
        user_details = t_user_master.objects.filter(Login_Id=user_id)

    return render(request, 'complaint_handling/complaint_officer_complaint_close_details.html', {'complaint_details': details, 'user_details': user_details, 'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})

def investigation_report_list(request):   #list of investigation report submitted to the Complaint Officer
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

    return render(request, 'complaint_handling/complaint_officer_complaint_close.html', {'complaint_details': details, 'user_details': user_details, 'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})

def investigation_complaint_list(request):
    Login_Id = request.session['login_id']
    #Role_Id = request.session['Role_Id']
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

