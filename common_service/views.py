from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.cache import cache_control

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_service_master, t_user_master, \
    t_location_field_office_mapping, t_field_office_master, t_unit_master, t_section_master
from bbfss import settings

from common_service.models import t_common_complaint_t1, t_inspection_monitoring_t1, t_inspection_monitoring_t2, \
    t_inspection_monitoring_t3, t_inspection_monitoring_t4, t_commodity_inspection_t1, t_commodity_inspection_t2, \
    t_feebback

from plant.models import t_workflow_details, t_file_attachment
from plant.views import inspector_application


def co_complaint_list(request):
    complaint_details = t_workflow_details.objects.filter(application_status='P', assigned_role_id='3',
                                                          action_date__isnull=False).order_by(
        'Application_No').reverse() | \
                        t_workflow_details.objects.filter(application_status='A', assigned_role_id='3',
                                                          action_date__isnull=False).order_by(
                            'Application_No').reverse()
    return render(request, 'complaint_officer_pending_list.html', {'complaint_details': complaint_details})


def investigation_report_list(request):  # list of investigation report submitted to the Complaint Officer
    complaint_details = t_workflow_details.objects.filter(application_status='IR', assigned_role_id='3')
    return render(request, 'complaint_officer_investigation_report_list.html', {'complaint_details': complaint_details})


def investigation_report_details(request):
    Application_No = request.GET.get('application_id')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    complaint_file = t_file_attachment.objects.filter(application_no=Application_No, role_id='8')
    investigation_file = t_file_attachment.objects.filter(application_no=Application_No, role_id='5')
    for userId in details:
        user_id = userId.Assign_To
        user_details = t_user_master.objects.filter(Login_Id=user_id)

    return render(request, 'complaint_handling/complaint_officer_complaint_close.html',
                  {'complaint_details': details, 'user_details': user_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village, 'complaint_file': complaint_file, 'investigation_file': investigation_file})


def complaint_closed_list(request):
    complaint_closed_details = t_workflow_details.objects.filter(application_status='C', assigned_role_id='3')
    return render(request, 'complaint_closed_list.html', {'complaint_details': complaint_closed_details})


def complaint_closed_details(request):
    Application_No = request.GET.get('application_id')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    file = t_file_attachment.objects.filter(application_no=Application_No)
    for userId in details:
        user_id = userId.Assign_To
        user_details = t_user_master.objects.filter(Login_Id=user_id)

    return render(request, 'complaint_handling/complaint_officer_complaint_close_details.html',
                  {'complaint_details': details, 'user_details': user_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village, 'file': file})


def investigation_complaint_list(request):
    Login_Id = request.session['Login_Id']
    # Role_Id = request.session['Role_Id']
    in_complaint_list = t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='A',
                                                          service_code='COM')

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
            return render(request, 'complaint_investigation_pending_list.html',
                          {'count': message_count, 'in_complaint_list': in_complaint_list})
    elif Role == 'OIC':
        login_id = request.session['Login_Id']
        Field_Office_Id = request.session['field_office_id']
        message_count = (t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                           action_date__isnull=False) |
                         t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                           action_date__isnull=False)).count()

        return render(request, 'complaint_investigation_pending_list.html',
                      {'count': message_count, 'in_complaint_list': in_complaint_list})
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
                         | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                             application_status='FR',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                             application_status='P',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        fhc_count = t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                      action_date__isnull=False, service_code='FHC').count()
        return render(request, 'complaint_investigation_pending_list.html',
                      {'ins_count': message_count, 'in_complaint_list': in_complaint_list, 'fhc_count': fhc_count})
    elif Role == 'Complaint Officer':
        login_id = request.session['Login_Id']
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                           action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        return render(request, 'complaint_investigation_pending_list.html',
                      {'complain_count': message_count, 'in_complaint_list': in_complaint_list})
    elif Role == 'Chief':
        login_id = request.session['Login_Id']
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                           action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        return render(request, 'complaint_investigation_pending_list.html',
                      {'chief_count': message_count, 'in_complaint_list': in_complaint_list})


def co_complaint_details(request):
    Application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    file = t_file_attachment.objects.filter(application_No=application_No)
    inspector_list = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6', ])

    return render(request, 'complaint_handling/complaint_officer_complaint_forward.html', {'complaint_details': details,
                                                                                           'inspector_list': inspector_list,
                                                                                           'dzongkhag': dzongkhag,
                                                                                           'gewog': gewog,
                                                                                           'village': village,
                                                                                           'file': file})


def investigation_complaint_details(request):
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


def apply_complaint_form(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    return render(request, 'complaint_handling/submit_complaint.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})


def save_complaint(request):
    data = dict()
    service_code = "COM"
    last_application_no = get_complaint_application_no(request, service_code)
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
        Applicant_Id=email,
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

    t_workflow_details.objects.create(application_no=last_application_no, applicant_id=email,
                                      assigned_to=None, field_office_id=None, section='Complaint',
                                      assigned_role_id='3', action_date=None, application_status='P',
                                      service_code=service_code)
    data['applNo'] = last_application_no
    data['email'] = email
    return JsonResponse(data)


def update_complaint_application(request):
    data = dict()
    application_no = request.POST.get('applicationNo')
    cid = request.POST.get('cid')
    complainantName = request.POST.get('complainantName')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    address = request.POST.get('address')
    complaint_description = request.POST.get('complainDescription')

    complaintDetails = t_common_complaint_t1.objects.filter(Application_No=application_no)
    complaintDetails.update(
        CID=cid,
        Name=complainantName,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Contact_No=contact_number,
        Email=email,
        Address=address,
        Complaint_Description=complaint_description,
    )
    data['applNo'] = application_no
    data['email'] = email
    return JsonResponse(data)


def load_complaint_attachment_details(request):
    application_id = request.GET.get('application_id')
    attachment_details = t_file_attachment.objects.filter(application_no=application_id, role_id='8')
    return render(request, 'complaint_handling/complaint_file_attachment_page.html',
                  {'file_attach': attachment_details})


def save_complaint_file(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/common_service/complaint_handling")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/common_service/complaint_handling" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def add_complaint_file_name(request):
    app_no = request.POST.get('appNo')
    fileName = request.POST.get('filename')
    file_url = request.POST.get('file_url')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
    t_file_attachment.objects.create(application_no=app_no, applicant_id=None,
                                     role_id=None, file_path=file_url,
                                     attachment=file_name)
    complaint_file = t_file_attachment.objects.filter(application_no=app_no)
    return render(request, 'complaint_handling/complaint_file_attachment_page.html', {'complaint_file': complaint_file})


def delete_complaint_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')
    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/common_service/complaint_handling")
        fs.delete(str(fileName))
    file.delete()

    complaint_file = t_file_attachment.objects.filter(application_no=Application_No, role_id='8')
    return render(request, 'complaint_handling/complaint_file_attachment_page.html', {'complaint_file': complaint_file})


def load_investigation_attachment_details(request):
    application_id = request.GET.get('application_id')
    attachment_details = t_file_attachment.objects.filter(application_no=application_id, role_id='5')
    return render(request, 'complaint_handling/investigation_file_attachment_page.html',
                  {'file_attach': attachment_details})


def save_investigation_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/common_service/complaint_handling")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def add_investigation_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        fs = ("attachments" + "/" + str(timezone.now().year) + "/common_service/complaint_handling/" + fileName)
        t_file_attachment.objects.create(application_no=Application_No, applicant_id=Applicant_Id,
                                         role_id='5', file_path=fs, attachment=fileName)
        investigation_file = t_file_attachment.objects.filter(application_no=Application_No, role_id='5')
    return render(request, 'complaint_handling/investigation_file_attachment_page.html',
                  {'investigation_file': investigation_file})


def delete_investigation_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')
    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/common_service/complaint_handling")
        fs.delete(str(fileName))
    file.delete()
    investigation_file = t_file_attachment.objects.filter(application_no=Application_No, role_id='5')
    return render(request, 'complaint_handling/investigation_file_attachment_page.html',
                  {'investigation_file': investigation_file})


def submit_complaint(request):
    application_no = request.GET.get('appNo')
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    workflow_details.update(action_date=date.today())
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()

    return render(request, 'complaint_handling/submit_complaint.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})


def complaint_details(request):
    Application_No = request.GET.get('application_id')
    service_code = request.GET.get('service_code')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    complaint_details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    file = t_file_attachment.objects.filter(application_no=Application_No)

    inspector_list = t_user_master.objects.filter(Role_Id__in=['2', '3', '4', '5', '6'])

    return render(request, 'complaint_handling/complaint_officer_complaint_acknowledge.html',
                  {'complaint_details': complaint_details, 'inspector_list': inspector_list, 'dzongkhag': dzongkhag,
                   'gewog': gewog, 'village': village, 'file': file})


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

    workflow_details = t_workflow_details.objects.filter(application_no=app_no)
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

    application_details = t_workflow_details.objects.filter(application_no=app_no)
    application_details.update(action_date=date.today())
    application_details.update(assigned_to=forward_to)
    application_details.update(assigned_role_id=None)
    return redirect(co_complaint_list)


def forward_complaint_to_co(request):
    app_no = request.POST.get('applicationNo')
    investigation_report = request.POST.get('investigationReport')
    investigation_date = request.POST.get('investigationDate')
    forward_details = t_common_complaint_t1.objects.filter(Application_No=app_no)

    forward_details.update(Investigation_Report=investigation_report)
    forward_details.update(Investigation_Date=investigation_date)
    forward_details.update(Application_Status='IR')

    application_details = t_workflow_details.objects.filter(application_no=app_no)
    application_details.update(action_date=date.today())
    application_details.update(assigned_to=None)
    application_details.update(assigned_role_id='3')
    application_details.update(application_status='IR')  # IR - Investigation Report complete
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

    application_details = t_workflow_details.objects.filter(application_no=app_no)
    application_details.update(action_date=date.today())
    application_details.update(assigned_to=None)
    # application_details.update(Assigned_Role_Id=None)
    application_details.update(application_status='C')
    send_close_email(app_no, application_date, closure_remarks, email, investigation_report, investigation_date)
    return redirect(investigation_report_list)


def send_acknowledge_email(app_no, app_date, ack_remarks, email_id):
    subject = 'COMPLAINT APPLICATION ACCEPTED'
    message = "Dear Sir/Madam, This has reference to your application number " + app_no + " dated: " + str(
        app_date) + ", regarding your complaint on " + ack_remarks + ". Kindly quote this complaint registration number in all your future correspondence. We will inform you of the outcome of the complaint as soon as investigation is over."
    recipient_list = [email_id]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_close_email(app_no, app_date, close_remarks, email_id, in_report, in_date):
    subject = 'COMPLAINT CLOSED'
    message = "Dear " + "Sir/Madam, This has reference to your complaint registered with us Registration No." \
                        "" + app_no + " dated " + str(app_date) + ". Please find below our decision or findings here :" \
                                                                  "" + close_remarks + ".Thank You"

    recipient_list = [email_id]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def get_complaint_application_no(request, service_code):
    last_application_no = t_common_complaint_t1.objects.aggregate(Max('Application_No'))
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


# Establishment Inspection and Monitoring
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def establishment_inspection_form(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        unit = t_unit_master.objects.filter(Unit_Type='S')
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
                return render(request, 'inspection_establishment/application_form.html',
                              {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                               'count': message_count, 'unit': unit})
        elif Role == 'OIC':
            login_id = request.session['Login_Id']
            Field_Office_Id = request.session['field_office_id']
            message_count = (t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                               action_date__isnull=False) |
                             t_workflow_details.objects.filter(Assigned_To=login_id, application_status='NCF',
                                                               action_date__isnull=False)).count()

            return render(request, 'inspection_establishment/application_form.html',
                          {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'count': message_count, 'unit': unit})
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
                             | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                                 application_status='FR',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                                 application_status='P',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                 action_date__isnull=False)).count()
            fhc_count = t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                          action_date__isnull=False, service_code='FHC').count()
            return render(request, 'inspection_establishment/application_form.html',
                          {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'ins_count': message_count, 'unit': unit, 'fhc_count': fhc_count})
        elif Role == 'Complain Officer':
            login_id = request.session['Login_Id']
            message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                               action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                 action_date__isnull=False)).count()
            return render(request, 'inspection_establishment/application_form.html',
                          {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'complain_count': message_count, 'unit': unit})
        elif Role == 'Chief':
            login_id = request.session['Login_Id']
            message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                               action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                 action_date__isnull=False)).count()
            return render(request, 'inspection_establishment/application_form.html',
                          {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'chief_count': message_count, 'unit': unit})
    else:
        return render(request, 'redirect_page.html')


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
    observations = request.POST.get('observations')
    Login_Id = request.session['Login_Id']
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
        Service_Code=service_code,
        Observation=observations,
        Created_Date=None,
        Created_By=Login_Id
    )
    data['applNo'] = monitoring_ref_no
    return JsonResponse(data)


def get_monitoring_ref_no(service_code):
    last_application_no = t_inspection_monitoring_t1.objects.aggregate(Max('Reference_No'))
    lastAppNo = last_application_no['Reference_No__max']
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

    if not Inspection_Date:
        date_format_ins = None
    else:
        date_format_ins = datetime.strptime(Inspection_Date, '%d-%m-%Y').date()
    if not Receipt_Date:
        date_of_receipt = None
    else:
        date_of_receipt = datetime.strptime(Receipt_Date, '%d-%m-%Y').date()
    if not Date_Line_Correction:
        date_line = None
    else:
        date_line = datetime.strptime(Date_Line_Correction, '%d-%m-%Y').date()

    if not Fine_Imposed:
        fine_amt = None
    else:
        fine_amt = Fine_Imposed

    t_inspection_monitoring_t2.objects.create(
        Reference_No=Reference_No,
        Inspection_Date=date_format_ins,
        Inspector_Name=Inspector_Name,
        Observation=Observation,
        Correction_Proposed=Correction_Proposed,
        Date_Line_Correction=date_line,
        Correction_Taken=Correction_Taken,
        Fine_Imposed=fine_amt,
        Revenue_Receipt=Revenue_Receipt,
        Receipt_Date=date_of_receipt
    )
    details = t_inspection_monitoring_t2.objects.filter(Reference_No=Reference_No)
    return render(request, 'inspection_establishment/owner_manager_details.html', {'details': details})


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
    Detention_Destruction_No = request.POST.get('Detaintion_Destruction_No')

    if not Inspection_Date:
        date_format_ins = None
    else:
        date_format_ins = datetime.strptime(Inspection_Date, '%d-%m-%Y').date()

    if not Receipt_Date:
        date_of_receipt = None
    else:
        date_of_receipt = datetime.strptime(Receipt_Date, '%d-%m-%Y').date()

    if not Fine_Imposed:
        fine_amt = None
    else:
        fine_amt = Fine_Imposed

    if not Detention_Destruction_No:
        destruction_no = None
    else:
        destruction_no = Detention_Destruction_No

    t_inspection_monitoring_t3.objects.create(
        Reference_No=Reference_No,
        Inspection_Date=date_format_ins,
        Inspector_Name=Inspector_Name,
        Items_Seized=Items_Seized,
        Qty_Seized=Qty_Seized,
        Unit=Unit,
        Reason=Reason,
        Fine_Imposed=fine_amt,
        Revenue_Receipt=Revenue_Receipt,
        Receipt_Date=date_of_receipt,
        Detention_Destruction_No=destruction_no
    )
    details = t_inspection_monitoring_t3.objects.filter(Reference_No=Reference_No)
    return render(request, 'inspection_establishment/item_details.html', {'details': details})


def save_sample_details(request):
    Reference_No = request.POST.get('sample_collection_application_no')
    Collection_Type = request.POST.get('Collection_Type')
    Collection_Date = request.POST.get('Collection_Date')
    Submission_Date = request.POST.get('Submission_Date')
    HS_Code_Imp = request.POST.get('HS_Code_Imp')
    HS_Code_Local = request.POST.get('HS_Code_Local')
    Sample_Type = request.POST.get('Sample_Type')
    Qty = request.POST.get('Qty')
    Batch_No = request.POST.get('Batch_No')
    Batch_Date = request.POST.get('Batch_Date')
    Test_Requested = request.POST.get('Test_Requested')
    Test_Report = request.POST.get('Test_Report')

    if not Collection_Date:
        date_format_collection = None
    else:
        date_format_collection = datetime.strptime(Collection_Date, '%d-%m-%Y').date()

    if not Submission_Date:
        date_of_submission = None
    else:
        date_of_submission = datetime.strptime(Submission_Date, '%d-%m-%Y').date()

    if not Batch_Date:
        BatchDate = None
    else:
        BatchDate = datetime.strptime(Batch_Date, '%d-%m-%Y').date()

    if not Qty:
        qty_collected = None
    else:
        qty_collected = Qty

    t_inspection_monitoring_t4.objects.create(
        Reference_No=Reference_No,
        Collection_Type=Collection_Type,
        Collection_Date=date_format_collection,
        Submission_Date=date_of_submission,
        HS_Code_Imp=HS_Code_Imp,
        HS_Code_Local=HS_Code_Local,
        Sample_Type=Sample_Type,
        Qty=qty_collected,
        Batch_No=Batch_No,
        Batch_Date=BatchDate,
        Test_Requested=Test_Requested,
        Test_Report=Test_Report
    )
    details = t_inspection_monitoring_t4.objects.filter(Reference_No=Reference_No)
    return render(request, 'inspection_establishment/sample_collection_details.html', {'details': details})


def inspection_file(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/common_service/inspection_establishment")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/common_service/inspection_establishment" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def inspection_file_name(request):
    app_no = request.POST.get('appNo')
    fileName = request.POST.get('filename')
    Applicant_Id = request.session['email']
    file_url = request.POST.get('file_url')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
    t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                     role_id=None, file_path=file_url,
                                     attachment=file_name)

    file_attach = t_file_attachment.objects.filter(application_no=app_no)
    return render(request, 'inspection_establishment/file_attachment.html', {'file_attach': file_attach})


def submit_establishment_inspection_form(request):
    Application_No = request.POST.get('applicationNo')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    print(Application_No)
    details = t_inspection_monitoring_t1.objects.filter(Reference_No=Application_No)
    details.update(Created_Date=date.today())
    return render(request, 'inspection_establishment/application_form.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})


def draft_application_list(request):
    application_details = t_inspection_monitoring_t1.objects.filter(Application_Flag='P')
    service_details = t_service_master.objects.all()
    return render(request, 'inspection_establishment/draft_application.html',
                  {'application_details': application_details, 'service_details': service_details})


def view_draft_details(request):
    reference_no = request.GET.get('reference_no')
    application_details = t_inspection_monitoring_t1.objects.filter(Reference_No=reference_no)
    details = t_inspection_monitoring_t2.objects.filter(Reference_No=reference_no)
    t3_details = t_inspection_monitoring_t3.objects.filter(Reference_No=reference_no)
    t4_details = t_inspection_monitoring_t4.objects.filter(Reference_No=reference_no)
    file_attach = t_file_attachment.objects.filter(application_no=reference_no)
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'inspection_establishment/draft_application_details.html',
                  {'application_details': application_details, 'details': details, 't3_details': t3_details,
                   't4_details': t4_details, 'file_attach': file_attach, 'dzongkhag': dzongkhag,
                   'gewog': gewog, 'village': village, 'unit': unit})


def update_inspection_establishment_application(request):
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
    details.update(Created_Date=date.today())
    return redirect(draft_application_list)


def load_establishment_nc_details(request):
    reference_no = request.GET.get('refNo')
    details = t_inspection_monitoring_t2.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_commodity/owner_manager_details.html', {'details': details})


def load_establishment_seized_details(request):
    reference_no = request.GET.get('refNo')
    details = t_inspection_monitoring_t3.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_commodity/item_details.html', {'details': details})


def load_establishment_sample_details(request):
    reference_no = request.GET.get('refNo')
    details = t_inspection_monitoring_t4.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_commodity/sample_collection_details.html', {'details': details})


def load_establishment_attachment_details(request):
    referenceNo = request.GET.get('refNo')
    attachment_details = t_file_attachment.objects.filter(application_no=referenceNo)
    return render(request, 'inspection_commodity/file_attachment.html',
                  {'file_attach': attachment_details})


def delete_establishment_file(request):
    File_Id = request.GET.get('file_id')
    referenceNo = request.GET.get('refNo')
    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage(
            "attachments" + "/" + str(timezone.now().year) + "/common_service/inspection_establishment")
        fs.delete(str(fileName))
    file.delete()
    file_attach = t_file_attachment.objects.filter(application_no=referenceNo)
    return render(request, 'inspection_establishment/file_attachment.html', {'file_attach': file_attach})


def delete_nc_details(request):
    record_id = request.GET.get('record_id')
    reference_no = request.GET.get('refNo')
    record = t_inspection_monitoring_t2.objects.filter(Record_Id=record_id)
    record.delete()
    nc_inspection = t_inspection_monitoring_t2.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_establishment/owner_manager_details.html',
                  {'details': nc_inspection})


def delete_seized_details(request):
    record_id = request.GET.get('record_id')
    reference_no = request.GET.get('refNo')
    record = t_inspection_monitoring_t3.objects.filter(Record_Id=record_id)
    record.delete()
    details = t_inspection_monitoring_t3.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_establishment/item_details.html',
                  {'details': details})


def delete_collection_details(request):
    record_id = request.GET.get('record_id')
    reference_no = request.GET.get('refNo')
    record = t_inspection_monitoring_t4.objects.filter(Record_Id=record_id)
    record.delete()
    details = t_inspection_monitoring_t4.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_establishment/sample_collection_details.html',
                  {'details': details})


def view_establishment_inspection_list(request):
    application_details = t_inspection_monitoring_t1.objects.filter(Created_Date__isnull=False)

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
            return render(request, 'inspection_establishment/establishment_inspection_list.html',
                          {'count': message_count, 'application_details': application_details})
    elif Role == 'OIC':
        login_id = request.session['Login_Id']
        Field_Office_Id = request.session['field_office_id']
        message_count = (t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                           action_date__isnull=False) |
                         t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                           action_date__isnull=False)).count()

        return render(request, 'inspection_establishment/establishment_inspection_list.html',
                      {'count': message_count, 'application_details': application_details})
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
                         | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                             application_status='FR',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                             application_status='P',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        fhc_count = t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                      action_date__isnull=False, service_code='FHC').count()
        return render(request, 'inspection_establishment/establishment_inspection_list.html',
                      {'ins_count': message_count, 'application_details': application_details, 'fhc_count': fhc_count})
    elif Role == 'Complain Officer':
        login_id = request.session['Login_Id']
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                           action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        return render(request, 'inspection_establishment/establishment_inspection_list.html',
                      {'complain_count': message_count, 'application_details': application_details})
    elif Role == 'Chief':
        login_id = request.session['Login_Id']
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                           action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        return render(request, 'inspection_establishment/establishment_inspection_list.html',
                      {'chief_count': message_count, 'application_details': application_details})


def view_establishment_inspection_details(request):
    reference_no = request.GET.get('reference_no')
    application_details = t_inspection_monitoring_t1.objects.filter(Reference_No=reference_no)
    details = t_inspection_monitoring_t2.objects.filter(Reference_No=reference_no)
    seized_details = t_inspection_monitoring_t3.objects.filter(Reference_No=reference_no)
    sample_details = t_inspection_monitoring_t4.objects.filter(Reference_No=reference_no)
    file_attach = t_file_attachment.objects.filter(application_no=reference_no)
    for dzoCode in application_details:
        dzo_code = dzoCode.Dzongkhag_Code
    for gewogCode in application_details:
        gewog_code = gewogCode.Gewog_Code
    for vilCode in application_details:
        vil_code = vilCode.Village_Code
    dzongkhag = t_dzongkhag_master.objects.filter(Dzongkhag_Code=dzo_code)
    gewog = t_gewog_master.objects.filter(Gewog_Code=gewog_code)
    village = t_village_master.objects.filter(Village_Code=vil_code)
    return render(request, 'inspection_establishment/establishment_inspection_details.html',
                  {'application_details': application_details, 'details': details, 'seized_details': seized_details,
                   'sample_details': sample_details, 'file_attach': file_attach, 'dzongkhag': dzongkhag,
                   'gewog': gewog, 'village': village})


# Commodity Inspection and Monitoring
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def commodity_inspection_form(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        inspector_list = t_user_master.objects.filter(Login_Type='I')
        unit = t_unit_master.objects.filter(Unit_Type='S')
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
                return render(request, 'inspection_commodity/application_commodity.html',
                              {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                               'count': message_count, 'inspector_list': inspector_list, 'unit': unit})
        elif Role == 'OIC':
            login_id = request.session['Login_Id']
            Field_Office_Id = request.session['field_office_id']
            message_count = (t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                               action_date__isnull=False) |
                             t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                               action_date__isnull=False)).count()

            return render(request, 'inspection_commodity/application_commodity.html',
                          {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'count': message_count, 'inspector_list': inspector_list, 'unit': unit})
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
                             | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                                 application_status='FR',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                                 application_status='P',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                 action_date__isnull=False)).count()
            fhc_count = t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                          action_date__isnull=False, service_code='FHC').count()
            return render(request, 'inspection_commodity/application_commodity.html',
                          {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'ins_count': message_count, 'inspector_list': inspector_list, 'unit': unit,
                           'fhc_count': fhc_count})
        elif Role == 'Complain Officer':
            login_id = request.session['Login_Id']
            message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                               action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                 action_date__isnull=False)).count()
            return render(request, 'inspection_commodity/application_commodity.html',
                          {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'complain_count': message_count, 'inspector_list': inspector_list, 'unit': unit})
        elif Role == 'Chief':
            login_id = request.session['Login_Id']
            message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                               action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                 action_date__isnull=False)
                             | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                 action_date__isnull=False)).count()
            return render(request, 'inspection_commodity/application_commodity.html',
                          {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                           'chief_count': message_count, 'inspector_list': inspector_list, 'unit': unit})
    else:
        return render(request, 'redirect_page.html')


def load_commodity_attachment_details(request):
    application_id = request.GET.get('application_id')
    attachment_details = t_file_attachment.objects.filter(application_no=application_id, role_id='5')
    return render(request, 'complaint_handling/investigation_file_attachment_page.html',
                  {'file_attach': attachment_details})


def add_commodity_file(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/common_service/inspection_commodity")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/common_service/inspection_commodity" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def add_commodity_file_name(request):
    app_no = request.POST.get('refNo')
    fileName = request.POST.get('filename')
    Applicant_Id = request.session['email']
    file_url = request.POST.get('file_url')
    Role_Id = request.session['Role_Id']
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
    t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                     role_id=Role_Id, file_path=file_url, attachment=fileName)
    file_attach = t_file_attachment.objects.filter(application_no=app_no)
    return render(request, 'inspection_commodity/commodity_file_attachment.html', {'file_attach': file_attach})


def delete_commodity_file(request):
    File_Id = request.GET.get('file_id')
    referenceNo = request.GET.get('refNo')
    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/common_service/inspection_commodity")
        fs.delete(str(fileName))
    file.delete()
    file_attach = t_file_attachment.objects.filter(application_no=referenceNo)
    return render(request, 'inspection_commodity/commodity_file_attachment.html', {'file_attach': file_attach})


def delete_commodity_details(request):
    record_id = request.GET.get('record_id')
    reference_no = request.GET.get('refNo')
    record = t_commodity_inspection_t2.objects.filter(Record_Id=record_id)
    record.delete()
    commodity_inspection = t_commodity_inspection_t2.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_commodity/commodity_details.html',
                  {'commodity_inspection': commodity_inspection})


def load_commodity_attachment_details(request):
    referenceNo = request.GET.get('refNo')
    attachment_details = t_file_attachment.objects.filter(application_no=referenceNo)
    return render(request, 'inspection_commodity/commodity_file_attachment.html',
                  {'file_attach': attachment_details})


def load_commodity_application(request):
    reference_no = request.GET.get('refNo')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    application_details = t_commodity_inspection_t1.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_commodity/application_commodity.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village})


def load_commodity_application_details(request):
    reference_no = request.GET.get('refNo')
    commodity_inspection = t_commodity_inspection_t2.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_commodity/commodity_details.html',
                  {'commodity_inspection': commodity_inspection})


def draft_inspection_application_details(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    reference_no = request.GET.get('referenceNo')
    application_details = t_inspection_monitoring_t1.objects.filter(Reference_No=reference_no)
    commodity_details = t_inspection_monitoring_t2.objects.filter(Reference_No=reference_no)
    return render(request, 'inspection_commodity/draft_application_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village, 'commodity_details': commodity_details})


def save_inspection_report_application(request):
    data = dict()
    service_code = "CIM"
    reference_no = get_commodity_Inspection_ref_no(request, service_code)
    ownerName = request.POST.get('ownerName')
    regNumber = request.POST.get('regNumber')
    Dzongkhag = request.POST.get('dzongkhag')
    Gewog = request.POST.get('gewog')
    Village = request.POST.get('village')
    address = request.POST.get('address')
    contact_no = request.POST.get('contactNumber')
    email = request.POST.get('email')
    commodity = request.POST.get('commodity')
    inspectionDate = request.POST.get('inspectionDate')
    inspectionTeam = request.POST.get('inspectionTeam')
    inspectionPurpose = request.POST.get('inspectionPurpose')
    observation = request.POST.get('observation')
    teamLeader = request.POST.get('teamLeader')
    Login_Id = request.session['Login_Id']
    date_of_inspection = datetime.strptime(inspectionDate, '%d-%m-%Y').date()

    t_commodity_inspection_t1.objects.create(
        Reference_No=reference_no,
        FBO_Name=ownerName,
        Registration_No=regNumber,
        Dzongkhag_Code=Dzongkhag,
        Gewog_Code=Gewog,
        Village_Code=Village,
        Address=address,
        Contact_No=contact_no,
        Email=email,
        Inspection_Date=date_of_inspection,
        Inspection_Team=inspectionTeam,
        Team_Leader=teamLeader,
        Commodity=commodity,
        Purpose=inspectionPurpose,
        Observation=observation,
        Created_Date=None,
        Created_By=Login_Id
    )
    data['refNo'] = reference_no
    return JsonResponse(data)


def get_commodity_Inspection_ref_no(request, service_code):
    last_reference_no = t_commodity_inspection_t1.objects.aggregate(Max('Reference_No'))
    lastRefNo = last_reference_no['Reference_No__max']
    if not lastRefNo:
        year = timezone.now().year
        newRefNo = service_code + "-" + str(year) + "-" + "0001"
    else:
        substring = str(lastRefNo)[9:13]
        substring = int(substring) + 1
        RefNo = str(substring).zfill(4)
        year = timezone.now().year
        newRefNo = service_code + "-" + str(year) + "-" + RefNo
    return newRefNo


def save_commodity_details(request):
    if request.method == 'POST':
        reference_no = request.POST.get('refNo')
        commodityDesc = request.POST.get('commodity_desc')
        commodityRequirement = request.POST.get('commodity_requirement')
        qtyInspected = request.POST.get('qty_inspected')
        unit = request.POST.get('unit')
        qtyCleared = request.POST.get('qty_cleared')
        qtyRejected = request.POST.get('qty_rejected')
        reasonReject = request.POST.get('reason_rejected')

        t_commodity_inspection_t2.objects.create(
            Reference_No=reference_no,
            Commodity=commodityDesc,
            Commodity_Requirement=commodityRequirement,
            Qty_Inspected=qtyInspected,
            Unit=unit,
            Qty_Cleared=qtyCleared,
            Qty_Rejected=qtyRejected,
            Reason_For_Rejection=reasonReject)

        commodity_inspection = t_commodity_inspection_t2.objects.filter(Reference_No=reference_no)
        return render(request, 'inspection_commodity/commodity_details.html',
                      {'commodity_inspection': commodity_inspection})


def submit_commodity_inspection_form(request):
    reference_no = request.POST.get('referenceNo')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_commodity_inspection_t1.objects.filter(Reference_No=reference_no)
    details.update(Created_Date=date.today())

    return render(request, 'inspection_commodity/application_commodity.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village})


def draft_commodity_inspection_list(request):
    application_details = t_commodity_inspection_t1.objects.filter(Created_Date__isnull=True)
    return render(request, 'inspection_commodity/draft_application_list.html',
                  {'application_details': application_details})


def view_draft_commodity_inspection_details(request):
    reference_no = request.GET.get('reference_no')
    application_details = t_commodity_inspection_t1.objects.filter(Reference_No=reference_no)
    details = t_commodity_inspection_t2.objects.filter(Reference_No=reference_no)
    file_attach = t_file_attachment.objects.filter(application_no=reference_no)
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    unit = t_unit_master.objects.all()
    inspector_list = t_user_master.objects.filter(Login_Type='I')
    return render(request, 'inspection_commodity/draft_application_details.html',
                  {'application_details': application_details, 'details': details, 'file_attach': file_attach,
                   'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village, 'unit': unit,
                   'inspector_list': inspector_list})


def update_inspection_commodity_application(request):
    data = dict()
    reference_no = request.POST.get('referenceNo')
    ownerName = request.POST.get('ownerName')
    regNumber = request.POST.get('regNumber')
    Dzongkhag = request.POST.get('dzongkhag')
    Gewog = request.POST.get('gewog')
    Village = request.POST.get('village')
    address = request.POST.get('address')
    contact_no = request.POST.get('contactNumber')
    email = request.POST.get('email')
    commodity = request.POST.get('commodity')
    inspectionDate = request.POST.get('inspectionDate')
    inspectionTeam = request.POST.get('inspectionTeam')
    inspectionPurpose = request.POST.get('inspectionPurpose')
    observation = request.POST.get('observation')
    teamLeader = request.POST.get('teamLeader')
    Login_Id = request.session['Login_Id']
    date_of_inspection = datetime.strptime(inspectionDate, '%d-%m-%Y').date()

    application_details = t_commodity_inspection_t1.objects.filter(Reference_No=reference_no)
    application_details.update(Reference_No=reference_no)
    application_details.update(FBO_Name=ownerName)
    application_details.update(Registration_No=regNumber)
    application_details.update(Dzongkhag_Code=Dzongkhag)
    application_details.update(Gewog_Code=Gewog)
    application_details.update(Village_Code=Village)
    application_details.update(Address=address)
    application_details.update(Contact_No=contact_no)
    application_details.update(Email=email)
    application_details.update(Inspection_Date=date_of_inspection)
    application_details.update(Inspection_Team=inspectionTeam)
    application_details.update(Team_Leader=teamLeader)
    application_details.update(Commodity=commodity)
    application_details.update(Purpose=inspectionPurpose)
    application_details.update(Observation=observation)
    application_details.update(Created_Date=None)
    application_details.update(Created_By=Login_Id)

    data['refNo'] = reference_no
    return JsonResponse(data)


def update_commodity_details(request):
    if request.method == 'POST':
        reference_no = request.POST.get('refNo')
        record_id = request.POST.get('recordId')
        commodityDesc = request.POST.get('commodity_desc')
        commodityRequirement = request.POST.get('commodity_requirement')
        qtyInspected = request.POST.get('qty_inspected')
        unit = request.POST.get('unit')
        qtyCleared = request.POST.get('qty_cleared')
        qtyRejected = request.POST.get('qty_rejected')
        reasonReject = request.POST.get('reason_rejected')

        commodity_details = t_commodity_inspection_t2.objects.filter(Record_id=record_id)

        t_commodity_inspection_t2.objects.create(
            Reference_No=reference_no,
            Commodity=commodityDesc,
            Commodity_Requirement=commodityRequirement,
            Qty_Inspected=qtyInspected,
            Unit=unit,
            Qty_Cleared=qtyCleared,
            Qty_Rejected=qtyRejected,
            Reason_For_Rejection=reasonReject)

        commodity_inspection = t_commodity_inspection_t2.objects.filter(Reference_No=reference_no)
        return render(request, 'inspection_commodity/commodity_details.html',
                      {'commodity_inspection': commodity_inspection})


def view_commodity_inspection_list(request):
    application_details = t_commodity_inspection_t1.objects.filter(Created_Date__isnull=False)
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
            return render(request, 'inspection_commodity/commodity_inspection_list.html',
                          {'count': message_count, 'application_details': application_details})
    elif Role == 'OIC':
        login_id = request.session['Login_Id']
        Field_Office_Id = request.session['field_office_id']
        message_count = (t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                           action_date__isnull=False) |
                         t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                           action_date__isnull=False)).count()

        return render(request, 'inspection_commodity/commodity_inspection_list.html',
                      {'count': message_count, 'application_details': application_details})
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
                         | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                             application_status='FR',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, field_office_id=Field_Office_Id,
                                                             application_status='P',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        fhc_count = t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                      action_date__isnull=False, service_code='FHC').count()
        return render(request, 'inspection_commodity/commodity_inspection_list.html',
                      {'ins_count': message_count, 'application_details': application_details, 'fhc_count': fhc_count})
    elif Role == 'Complain Officer':
        login_id = request.session['Login_Id']
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                           action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        return render(request, 'inspection_commodity/commodity_inspection_list.html',
                      {'complain_count': message_count, 'application_details': application_details})
    elif Role == 'Chief':
        login_id = request.session['Login_Id']
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                           action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                             action_date__isnull=False)
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                             action_date__isnull=False)).count()
        return render(request, 'inspection_commodity/commodity_inspection_list.html',
                      {'chief_count': message_count, 'application_details': application_details})


def view_commodity_inspection_details(request):
    reference_no = request.GET.get('reference_no')
    application_details = t_commodity_inspection_t1.objects.filter(Reference_No=reference_no)
    details = t_commodity_inspection_t2.objects.filter(Reference_No=reference_no)
    file_attach = t_file_attachment.objects.filter(application_no=reference_no)
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    unit = t_unit_master.objects.all()
    inspector_list = t_user_master.objects.filter(Login_Type='I')
    return render(request, 'inspection_commodity/commodity_inspection_details.html',
                  {'application_details': application_details, 'details': details, 'file_attach': file_attach,
                   'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village, 'unit': unit,
                   'inspector_list': inspector_list})


def view_commodity_inspection_details(request):
    reference_no = request.GET.get('reference_no')
    application_details = t_commodity_inspection_t1.objects.filter(Reference_No=reference_no)
    details = t_commodity_inspection_t2.objects.filter(Reference_No=reference_no)
    file_attach = t_file_attachment.objects.filter(application_no=reference_no)
    for dzoCode in application_details:
        dzo_code = dzoCode.Dzongkhag_Code
    for gewogCode in application_details:
        gewog_code = gewogCode.Gewog_Code
    for vilCode in application_details:
        vil_code = vilCode.Village_Code
    for inspectorCode in application_details:
        inspector_code = inspectorCode.Team_Leader
    dzongkhag = t_dzongkhag_master.objects.filter(Dzongkhag_Code=dzo_code)
    gewog = t_gewog_master.objects.filter(Gewog_Code=gewog_code)
    village = t_village_master.objects.filter(Village_Code=vil_code)
    team_leader = t_user_master.objects.filter(Login_Id=inspector_code)
    return render(request, 'inspection_commodity/commodity_inspection_details.html',
                  {'application_details': application_details, 'details': details, 'file_attach': file_attach,
                   'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village, 'team_leader': team_leader})


def view_FHC_inspection_details(request):
    reference_no = request.GET.get('reference_no')
    application_details = t_commodity_inspection_t1.objects.filter(Reference_No=reference_no)
    details = t_commodity_inspection_t2.objects.filter(Reference_No=reference_no)
    file_attach = t_file_attachment.objects.filter(application_no=reference_no)
    for dzoCode in application_details:
        dzo_code = dzoCode.Dzongkhag_Code
    for gewogCode in application_details:
        gewog_code = gewogCode.Gewog_Code
    for vilCode in application_details:
        vil_code = vilCode.Village_Code
    for inspectorCode in application_details:
        inspector_code = inspectorCode.Team_Leader
    dzongkhag = t_dzongkhag_master.objects.filter(Dzongkhag_Code=dzo_code)
    gewog = t_gewog_master.objects.filter(Gewog_Code=gewog_code)
    village = t_village_master.objects.filter(Village_Code=vil_code)
    team_leader = t_user_master.objects.filter(Login_Id=inspector_code)

    return render(request, 'inspection_commodity/fit_for_human_consumption_certificate.html',
                  {'application_details': application_details, 'details': details, 'file_attach': file_attach,
                   'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village, 'team_leader': team_leader})


# FEEDBACK
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submit_feedback_form(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        login_type = request.session['Login_Type']
        service = t_service_master.objects.all().order_by('Service_Id')
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
                    return render(request, 'feedback/submit_feedback.html',
                                  {'count': message_count, 'service': service})
            elif Role == 'OIC':
                login_id = request.session['Login_Id']
                Field_Office_Id = request.session['field_office_id']
                message_count = (
                        t_workflow_details.objects.filter(assigned_role_id='4', field_office_id=Field_Office_Id,
                                                          action_date__isnull=False) |
                        t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                          action_date__isnull=False)).count()

                return render(request, 'feedback/submit_feedback.html', {'count': message_count, 'service': service})
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
                return render(request, 'feedback/submit_feedback.html',
                              {'ins_count': message_count, 'fhc_count': fhc_count, 'service': service})
            elif Role == 'Complain Officer':
                login_id = request.session['Login_Id']
                message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                                   action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                     action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                     action_date__isnull=False)).count()
                return render(request, 'feedback/submit_feedback.html', {'complain_count': message_count,
                                                                         'service': service})
            elif Role == 'Chief':
                login_id = request.session['Login_Id']
                message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='AP',
                                                                   action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APA',
                                                                     action_date__isnull=False)
                                 | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCF',
                                                                     action_date__isnull=False)).count()
                return render(request, 'feedback/submit_feedback.html', {'chief_count': message_count,
                                                                         'service': service})
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
            return render(request, 'feedback/submit_feedback.html',
                          {'count': message_count, 'count_call': inspection_call_count,
                           'consignment_call_count': consignment_call_count, 'service': service})
    else:
        return render(request, 'redirect_page.html')


def submit_feedback(request):
    data = dict()
    service_code = "FED"
    last_reference_no = get_feedback_reference_no(request, service_code)
    applicant_Id = request.session['email']
    complainantName = request.POST.get('complainantName')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    address = request.POST.get('address')
    feedbackCategory = request.POST.get('feedbackCategory')
    feedback = request.POST.get('feedback')
    service = request.POST.get('service')

    if feedbackCategory == 'General':
        t_feebback.objects.create(
            Reference_No=last_reference_no,
            Created_By=applicant_Id,
            Created_Date=date.today(),
            Name=complainantName,
            Contact_No=contact_number,
            Email=email,
            Address=address,
            Feedback_Category=feedbackCategory,
            Feedback=feedback
        )
    else:
        service_details = t_service_master.objects.filter(Service_Code=service)
        for service_name in service_details:
            t_feebback.objects.create(
                Reference_No=last_reference_no,
                Created_By=applicant_Id,
                Created_Date=date.today(),
                Name=complainantName,
                Contact_No=contact_number,
                Email=email,
                Address=address,
                Feedback_Category=feedbackCategory,
                Feedback=feedback,
                Service=service_name.Service_Name,
                Service_Code=service
            )
    return render(request, 'feedback/submit_feedback.html')


def feedback_list(request):
    Role = request.session['role']
    print(Role)
    if Role == 'Complaint Handling Officer':
        feedback_details = (t_feebback.objects.filter(Service_Code__in=['COM', 'IAM'])
                            | t_feebback.objects.filter(Feedback_Category='General')) \
            .order_by('Created_Date').reverse()
        service_details = t_service_master.objects.all()
        return render(request, 'feedback/feedback_list.html', {'feedback_details': feedback_details,
                                                               'service_details': service_details})
    else:
        section = request.session['section']
        section_details = t_section_master.objects.filter(Section_Id=section)
        for id_section in section_details:
            section_name = id_section.Section_Name

            if section_name == 'Plant':
                feedback_details = t_feebback.objects.filter(Service_Code__in=['MPP', 'IPP', 'EPP', 'RNS', 'RSC', ]) \
                    .order_by('Created_Date').reverse()
                service_details = t_service_master.objects.all()
                return render(request, 'feedback/feedback_list.html', {'feedback_details': feedback_details,
                                                                       'service_details': service_details})
            elif section_name == 'Livestock':
                feedback_details = t_feebback.objects.filter(
                    Service_Code__in=['CMS', 'APM', 'LMP', 'ILP', 'IAF', 'LEC']) \
                    .order_by('Created_Date').reverse()
                service_details = t_service_master.objects.all()
                return render(request, 'feedback/feedback_list.html', {'feedback_details': feedback_details,
                                                                       'service_details': service_details})
            elif section_name == 'Food':
                feedback_details = t_feebback.objects.filter(Service_Code__in=['FPC', 'OC', 'GAP']) \
                    .order_by('Created_Date').reverse()
                service_details = t_service_master.objects.all()
                return render(request, 'feedback/feedback_list.html', {'feedback_details': feedback_details,
                                                                       'service_details': service_details})
            else:
                feedback_details = t_feebback.objects.filter(Service_Code__in=['FEC', 'FHL', 'FIP', 'FBR']) \
                    .order_by('Created_Date').reverse()
                service_details = t_service_master.objects.all()
                return render(request, 'feedback/feedback_list.html', {'feedback_details': feedback_details,
                                                                       'service_details': service_details})


def get_feedback_reference_no(request, service_code):
    last_reference_no = t_feebback.objects.aggregate(Max('Reference_No'))
    lastRefNo = last_reference_no['Reference_No__max']
    if not lastRefNo:
        year = timezone.now().year
        newRefNo = service_code + "-" + str(year) + "-" + "0001"
    else:
        substring = str(lastRefNo)[9:13]
        substring = int(substring) + 1
        RefNo = str(substring).zfill(4)
        year = timezone.now().year
        newRefNo = service_code + "-" + str(year) + "-" + RefNo
    return newRefNo
