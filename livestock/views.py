from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_location_field_office_mapping, \
    t_user_master, t_field_office_master, t_unit_master, t_service_master, t_livestock_species_master, \
    t_livestock_species_breed_master, t_meat_item_master
from administrator.views import dashboard
from bbfss import settings
from livestock.forms import ImportFormProduct, MeatShopFeasibilityForm
from livestock.models import t_livestock_clearance_meat_shop_t1, t_livestock_clearance_meat_shop_t2, \
    t_livestock_ante_post_mortem_t1, t_livestock_movement_permit_t1, t_livestock_export_certificate_t1, \
    t_livestock_ante_post_mortem_t2, t_livestock_movement_permit_t2, t_livestock_export_certificate_t2, \
    t_livestock_import_permit_product_t1, t_livestock_import_permit_animal_t1, t_livestock_movement_permit_t3, \
    t_livestock_import_permit_animal_inspection_t1, t_livestock_import_permit_product_inspection_t1, \
    t_livestock_import_permit_animal_t2, t_livestock_import_permit_product_t2, \
    t_livestock_import_permit_product_inspection_t2, t_livestock_import_permit_animal_inspection_t2, \
    t_livestock_clearance_meat_shop_t5, t_livestock_clearance_meat_shop_t4, t_livestock_clearance_meat_shop_t6, \
    t_livestock_clearance_meat_shop_t3
from plant.models import t_workflow_details, t_file_attachment, t_payment_details
from plant.views import inspector_application, resubmit_application, focal_officer_application, oic_application


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


# MEAT SHOP REGISTRATON
def meat_shop_registration_licensing(request):
    unit = t_unit_master.objects.all()
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    meat_item = t_meat_item_master.objects.all()
    return render(request, 'meat_shop_registration/registration_application.html',
                  {'unit': unit, 'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'meat_item': meat_item})


def save_meat_shop_registration(request):
    data = dict()
    service_code = "CMS"
    new_meat_shop_application = meat_shop_registration_application_no(service_code)
    Meat_Shop_Name = request.POST.get('Business_Name')
    CID = request.POST.get('cid')
    name = request.POST.get('Name')
    name_manager = request.POST.get('name_manager')
    License_Criteria = request.POST.get('license_criteria')
    Contact_No = request.POST.get('contactNumber')
    Email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    address = request.POST.get('address')
    t_livestock_clearance_meat_shop_t1.objects.create(
        Application_No=new_meat_shop_application,
        Application_Date=None,
        Applicant_Id=request.session['email'],
        CID=CID,
        Name_Owner=name,
        Contact_No=Contact_No,
        Email=Email,
        Address=address,
        License_Criteria=License_Criteria,
        Inspection_Type=None,
        Desired_FI_Inspection_Date=None,
        Desired_FR_Inspection_Date=None,
        FB_License_No=None,
        FI_Inspection_Date=None,
        FI_Inspection_Leader=None,
        FI_Response=None,
        FI_Recommendation=None,
        FR_Inspection_Date=None,
        FR_Inspection_Leader=None,
        FR_Response=None,
        FR_Recommendation=None,
        Field_Office_Id=None,
        Conditional_Clearance_No=None,
        Clearance_Approve_Date=None,
        Clearance_Validity_Period=None,
        Clearance_Validity=None,
        Approve_Date=None,
        Validity_Period=None,
        Validity=None,
        FR_Inspection_Team=None,
        FI_Inspection_Team=None,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        FO_Remarks=None,
        Representative=name_manager,
        Village_Code=village,
        Meat_Shop_Name=Meat_Shop_Name,
        Location_Code=None
    )

    t_workflow_details.objects.create(Application_No=new_meat_shop_application,
                                      Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Livestock',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = new_meat_shop_application
    return JsonResponse(data)


def meat_shop_registration_application_no(service_code):
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


def meat_shop_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/livestock/meat_shop_licensing")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/livestock/meat_shop_licensing" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def meat_shop_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'meat_shop_registration/file_attachment.html', {'file_attach': file_attach})


def delete_meat_shop_fh_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_business_registration")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'meat_shop_registration/file_attachment.html', {'file_attach': file_attach})


def submit_meat_shop_application(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(meat_shop_registration_licensing)


def meat_shop_fo_approve(request):
    application_no = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    field_office = request.POST.get('forwardTo')

    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_To=None)
    workflow_details.update(Field_Office_Id=field_office)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Assigned_Role_Id='4')
    workflow_details.update(Application_Status='I')  # feasibility inspection
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_no)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    details.update(Field_Office_Id=field_office)
    return redirect(dashboard)


def meat_shop_fo_reject(request):
    application_no = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Application_Status='R')
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_no)
    details.update(FO_Remarks=remarks)
    for email_id in details:
        email = email_id.Email
        send_meat_shop_reject_email(email, remarks)
    return redirect(dashboard)



def send_meat_shop_approve_email(new_import_permit, Email, validity_date):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Meat Shop Licensing Has Been Approved. Your " \
              "Registration No is:" + new_import_permit + " And is Valid TIll " + str(validity_date) + \
              " Please Make Payment Before Validity Expires.  Visit The Nearest Bafra Office For Payment."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_meat_shop_reject_email(Email, remarks):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Meat Shop Licensing Has Been Rejected." \
              " Reason: " + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def meat_shop_inspection_team_details(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    meeting_type = request.GET.get('meeting_type')

    t_livestock_clearance_meat_shop_t6.objects.create(Application_No=application_id,
                                                      Meeting_Type=meeting_type,
                                                      Name=name, Designation=designation)
    application_details = t_livestock_clearance_meat_shop_t6.objects.filter(Application_No=application_id,
                                                                            Meeting_Type=meeting_type)
    return render(request, 'meat_shop_registration/inspection_team_details.html',
                  {'application_details': application_details})


def meat_shop_team_details_feasibility_ins(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    opening_date = request.GET.get('opening_date')
    closing_date = request.GET.get('closing_date')
    date_open = datetime.strptime(opening_date, '%d-%m-%Y').date()
    date_close = datetime.strptime(closing_date, '%d-%m-%Y').date()
    t_livestock_clearance_meat_shop_t4.objects.create(Application_No=application_id,
                                                      Meeting_Type='Feasibility Inspection',
                                                      Name=name, Designation=designation,
                                                      Open_Meeting_Date=date_open,
                                                      Closing_Meeting_Date=date_close)
    application_details = t_livestock_clearance_meat_shop_t4.objects.filter(Application_No=application_id,
                                                                            Meeting_Type='Feasibility Inspection')
    return render(request, 'meat_shop_registration/team_details.html', {'application_details': application_details})


def meat_shop_concern_details_feasibility_ins(request):
    application_id = request.GET.get('application_id')
    Requirement = request.GET.get('Requirement')
    Observation = request.GET.get('Observations')
    Clause_No = request.GET.get('Clause_No')
    Concern = request.GET.get('Concern')
    FBO_Response = request.GET.get('response_fbo')

    t_livestock_clearance_meat_shop_t5.objects.create(Application_No=application_id,
                                                      Inspection_Type='Feasibility Inspection',
                                                      Requirement=Requirement, Observation=Observation,
                                                      Clause_No=Clause_No, Date=date.today(), Concern=Concern,
                                                      FBO_Response=FBO_Response)
    application_details = t_livestock_clearance_meat_shop_t5.objects.filter(Application_No=application_id,
                                                                            Inspection_Type='Feasibility Inspection')
    message_count = t_livestock_clearance_meat_shop_t5.objects.filter(Concern='Yes',
                                                                      Inspection_Type='Feasibility Inspection').count()
    return render(request, 'meat_shop_registration/concern_details.html', {'application_details': application_details,
                                                                           'message_count': message_count})


def approve_meat_shop_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    Clearance_No = feasibility_clearance_no(request)
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)

    if remarks is not None:
        details.update(FI_Recommendation=remarks)
    else:
        details.update(FI_Recommendation=None)

    details.update(FI_Inspection_Date=date_format_ins)
    details.update(Conditional_Clearance_No=Clearance_No)
    details.update(FI_Inspection_Leader=Inspection_Leader)
    details.update(FI_Inspection_Team=Inspection_Team)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='FR')
    application_details.update(Assigned_Role_Id=None)
    for work_details in application_details:
        user_id = work_details.Applicant_Id
        login = t_user_master.objects.filter(Email_Id=user_id)
        for login_id in login:
            id = login_id.Login_Id
            application_details.update(Assigned_To=id)
    for email_id in details:
        emailId = email_id.Email
        send_feasibility_approve_email(Clearance_No, emailId)

    return redirect(inspector_application)


def feasibility_clearance_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_livestock_clearance_meat_shop_t1.objects.aggregate(Max('Conditional_Clearance_No'))
    lastAppNo = last_application_no['Conditional_Clearance_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "FBR" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "FBR" + "/" + str(year) + "/" + AppNo
    return newAppNo


def send_feasibility_approve_email(Clearance_No, Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your  Feasibility Inspection of " \
              "Meat Shop Licensing  Has Been Approved. Your " \
              "Clearance No is:" + Clearance_No + " ."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_feasibility_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Feasibility Inspection of Meat Shop Licensing " \
                                "Has Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def reject_meat_shop_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)

    details.update(FI_Inspection_Date=date_format_ins)
    details.update(FI_Recommendation=remarks)
    details.update(FI_Inspection_Leader=Inspection_Leader)
    details.update(FI_Inspection_Team=Inspection_Team)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='IRS')
    for email_id in application_details:
        email = email_id.Applicant_Id
        login_details = t_user_master.objects.filter(Email_Id=email)
        login = login_details.Login_Id
        application_details.update(Assigned_To=login)
        application_details.update(Assigned_Role_Id=None)
    return redirect(inspector_application)


def resubmit_meat_shop_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)

    details.update(FI_Response=remarks)
    details.update(Desired_FI_Inspection_Date=date_format_ins)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    for det in details:
        field_office = det.Field_Office_Id
        application_details.update(Field_Office_Id=field_office)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_Role_Id='4')
    application_details.update(Application_Status='I')  # feasibility inspection
    application_details.update(Assigned_To=None)
    return redirect(resubmit_application)


def meat_shop_team_details_factory_ins(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    opening_date = request.GET.get('opening_date')
    closing_date = request.GET.get('closing_date')
    date_open = datetime.strptime(opening_date, '%d-%m-%Y').date()
    date_close = datetime.strptime(closing_date, '%d-%m-%Y').date()
    t_livestock_clearance_meat_shop_t4.objects.create(Application_No=application_id,
                                                      Meeting_Type='Factory Inspection',
                                                      Name=name, Designation=designation,
                                                      Open_Meeting_Date=date_open,
                                                      Closing_Meeting_Date=date_close)
    application_details = t_livestock_clearance_meat_shop_t4.objects.filter(Application_No=application_id,
                                                                            Meeting_Type='Factory Inspection')
    return render(request, 'meat_shop_registration/team_details.html', {'application_details': application_details})


def meat_shop_concern_details_factory_ins(request):
    application_id = request.GET.get('application_id')
    Requirement = request.GET.get('Requirement')
    Observation = request.GET.get('Observations')
    Clause_No = request.GET.get('Clause_No')
    Concern = request.GET.get('Concern')
    FBO_Response = request.GET.get('response_fbo')

    t_livestock_clearance_meat_shop_t5.objects.create(Application_No=application_id,
                                                      Inspection_Type='Factory Inspection',
                                                      Requirement=Requirement, Observation=Observation,
                                                      Clause_No=Clause_No, Date=date.today(), Concern=Concern,
                                                      FBO_Response=FBO_Response)
    application_details = t_livestock_clearance_meat_shop_t5.objects.filter(Application_No=application_id,
                                                                            Inspection_Type='Factory Inspection')
    message_count = t_livestock_clearance_meat_shop_t5.objects.filter(Concern='Yes',
                                                                      Inspection_Type='Factory Inspection').count()
    return render(request, 'meat_shop_registration/concern_details.html', {'application_details': application_details,
                                                                           'message_count': message_count})


def approve_meat_shop_factory_inspection(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)

    if remarks is not None:
        details.update(FR_Recommendation=remarks)
    else:
        details.update(FR_Recommendation=None)

    details.update(FR_Inspection_Date=date_format_ins)
    details.update(FR_Inspection_Leader=Inspection_Leader)
    details.update(FR_Inspection_Team=Inspection_Team)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='FRA')
    application_details.update(Assigned_Role_Id='2')
    for email_id in details:
        emailId = email_id.Email
        send_factory_approve_email(emailId)
    return redirect(inspector_application)


def meat_shop_submit(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    validity = request.GET.get('validity')

    clearance = factory_clearance_no(request, application_id)
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    details.update(Meat_Shop_Clearance_No=clearance)
    details.update(Approve_Date=date.today())
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    t_payment_details.objects.create(Application_No=application_id,
                                     Application_Date=date.today(),
                                     Permit_No=clearance,
                                     Service_Id='CMS',
                                     Validity=validity_date,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)
    for email_id in details:
        emailId = email_id.Email
        send_meat_shop_approve_email(clearance, emailId, validity_date)
    return redirect(focal_officer_application)


def factory_clearance_no(request, application_id):
    global Field_Code
    details = t_workflow_details.objects.filter(Application_No=application_id)
    for details in details:
        Field_office_Code = details.Field_Office_Id
        code = t_field_office_master.objects.filter(Field_Office_Id=Field_office_Code)
        for code in code:
            Field_Code = code.Field_Office_Code
            last_application_no = t_livestock_clearance_meat_shop_t1.objects.aggregate(Max('FB_License_No'))
            lastAppNo = last_application_no['FB_License_No__max']
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


def send_factory_approve_email(Clearance_No, Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Factory Inspection of " \
              "Meat Shop Licensing  Has Been Approved."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_factory_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Factory Inspection of Meat Shop Licensing " \
                                "Has Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def reject_meat_shop_factory_inspection(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)

    details.update(FR_Recommendation=remarks)
    details.update(FR_Inspection_Date=date_format_ins)
    details.update(FR_Inspection_Leader=Inspection_Leader)
    details.update(FR_Inspection_Team=Inspection_Team)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='RS')
    application_details.update(Assigned_Role_Id=None)
    for applicant in application_details:
        email_id = applicant.Applicant_Id
        login_details = t_user_master.objects.filter(Email_Id=email_id)
        for applicant_login in login_details:
            login = applicant_login.Login_Id
            print(login)
            application_details.update(Assigned_To=login)
    # send_feasibility_reject_email(remarks, details.Email)
    return redirect(inspector_application)


def resubmit_meat_shop_factory_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)

    details.update(FR_Response=remarks)
    details.update(Desired_FR_Inspection_Date=date_format_ins)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_To=None)
    application_details.update(Assigned_Role_Id='4')
    application_details.update(Application_Status='FR')  # Factory inspection
    return redirect(resubmit_application)


def edit_meat_shop_feasibility_details(request):
    record_id = request.GET.get('record_id')
    application_id = request.GET.get('app_no')
    edit_Concern = request.GET.get('edit_Concern')
    edit_response_fbo = request.GET.get('edit_response_fbo')
    app_details = t_livestock_clearance_meat_shop_t5.objects.filter(Record_Id=record_id)
    app_details.update(Concern=edit_Concern)
    app_details.update(FBO_Response=edit_response_fbo)
    if edit_response_fbo is not None:
        app_details.update(FBO_Response=edit_response_fbo)
    else:
        app_details.update(FBO_Response=None)
    application_details = t_livestock_clearance_meat_shop_t5.objects.filter(Application_No=application_id,
                                                                            Inspection_Type='Feasibility Inspection')
    message_count = t_livestock_clearance_meat_shop_t5.objects.filter(Concern='Yes').count()
    return render(request, 'meat_shop_registration/concern_details.html', {'application_details': application_details,
                                                                           'message_count': message_count})


def edit_meat_shop_factory_details(request):
    record_id = request.GET.get('record_id')
    application_id = request.GET.get('app_no')
    edit_Concern = request.GET.get('edit_Concern')
    edit_response_fbo = request.GET.get('edit_response_fbo')
    app_details = t_livestock_clearance_meat_shop_t5.objects.filter(Record_Id=record_id)
    app_details.update(Concern=edit_Concern)
    app_details.update(FBO_Response=edit_response_fbo)
    if edit_response_fbo is not None:
        app_details.update(FBO_Response=edit_response_fbo)
    else:
        app_details.update(FBO_Response=None)
    application_details = t_livestock_clearance_meat_shop_t5.objects.filter(Application_No=application_id,
                                                                            Inspection_Type='Factory Inspection')
    message_count = t_livestock_clearance_meat_shop_t5.objects.filter(Concern='Yes').count()
    return render(request, 'meat_shop_registration/concern_details.html', {'application_details': application_details,
                                                                           'message_count': message_count})


def forward_meat_shop_application(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')

    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Assigned_To=forwardTo)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_Role_Id='5')
    return redirect(oic_application)


def view_meat_shop_factory_inspection_application(request):
    application_id = request.GET.get('application_id')
    service_code = request.GET.get('service_code')

    application_details = t_livestock_clearance_meat_shop_t1.objects.filter(
        Application_No=application_id)
    details = t_livestock_clearance_meat_shop_t2.objects.filter(Application_No=application_id)
    file = t_file_attachment.objects.filter(Application_No=application_id)
    unit = t_unit_master.objects.all()
    inspection_details = t_livestock_clearance_meat_shop_t5.objects.filter(
        Application_No=application_id)
    team_details = t_livestock_clearance_meat_shop_t4.objects.filter(Application_No=application_id)
    inspection_team_details = t_livestock_clearance_meat_shop_t6.objects.filter(
        Application_No=application_id)
    oic_list = t_field_office_master.objects.filter()
    return render(request, 'meat_shop_registration/client_factory_inspect.html',
                  {'application_details': application_details, 'details': details, 'file': file,
                   'oic_list': oic_list, 'unit': unit, 'inspection_details': inspection_details,
                   'team_details': team_details, 'inspection_team_details': inspection_team_details})


def forward_meat_shop_factory_application(request):
    application_id = request.POST.get('application_id')
    Desired_FR_Inspection_Date = request.POST.get('date')
    date_format_ins = datetime.strptime(Desired_FR_Inspection_Date, '%d-%m-%Y').date()

    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Assigned_To=None)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_Role_Id='4')

    details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)
    details.update(Desired_FR_Inspection_Date=date_format_ins)

    return redirect(meat_factory_inspection_list)


def save_meat_shop_details(request):
    Application_No = request.POST.get('fh_application_no')
    print(Application_No)

    meat_name = request.POST.get('meat_name')

    t_livestock_clearance_meat_shop_t2.objects.create(Application_No=Application_No,
                                                      Meat_Item=meat_name)
    meat_details = t_livestock_clearance_meat_shop_t2.objects.filter(Application_No=Application_No)
    return render(request, 'meat_shop_registration/details.html', {'meat_details': meat_details})


def save_meat_shop_fh_details(request):
    Application_No = request.POST.get('fh_application_no')

    fh_name = request.POST.get('fh_name')
    fh_license = request.POST.get('fh_license')

    t_livestock_clearance_meat_shop_t3.objects.create(Application_No=Application_No, FH_Name=fh_name,
                                                      FH_License_No=fh_license)
    fh_details = t_livestock_clearance_meat_shop_t3.objects.filter(Application_No=Application_No)
    return render(request, 'meat_shop_registration/food_handler_details.html', {'fh_details': fh_details})


def send_meat_shop_acknowledge(request):
    application_id = request.GET.get('application_id')
    work_details = t_workflow_details.objects.filter(Application_No=application_id)
    work_details.update(Application_Status='ACK')
    application_details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)
    for app in application_details:
        mail_id = app.Email
        send_meat_shop_acknowledgement_mail(mail_id)
    return redirect(focal_officer_application)


def send_meat_shop_acknowledgement_mail(Email):
    subject = 'APPLICATION ACKNOWLEGED'
    message = "Dear Sir/Madam, Your Application for Meat Shop Licensing Has Been Accepted. " \
              "You will Be Informed About The Inspection Later."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


# import permit for live animal and fish
def import_permit(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_field_office_master.objects.filter(Is_Entry_Point='Y')
    species = t_livestock_species_master.objects.all()
    breed = t_livestock_species_breed_master.objects.all()
    return render(request, 'Animal_Fish_Import/import_permit_animal_fish.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'species': species, 'breed': breed})


def save_import_la_fish(request):
    data = dict()
    service_code = "IAF"
    application_no = live_animal_fish_application_no(service_code)
    # applicant_Id = request.session['email']
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
        Quarantine_Facilities=QF,
        Applicant_Id=request.session['email']
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
    No_Of_Animal = request.POST.get('no')
    Remarks = request.POST.get('AP_Remarks')
    Description = request.POST.get('animal_Description')

    t_livestock_import_permit_animal_t2.objects.create(Application_No=application_no,
                                                       Species=Species,
                                                       Breed=Breed,
                                                       Age=Age,
                                                       Sex=Sex,
                                                       Description=Description,
                                                       Quantity=No_Of_Animal,
                                                       Quantity_Balance=No_Of_Animal,
                                                       Remarks=Remarks
                                                       )
    import_details = t_livestock_import_permit_animal_t2.objects.filter(Application_No=application_no)
    return render(request, 'Animal_Fish_Import/animal_details.html', {'import': import_details})


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
    application_no = request.POST.get('application_no')
    print(application_no)
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
    t_payment_details.objects.create(Application_No=application_no,
                                     Application_Date=date.today(),
                                     Permit_No=permit_no,
                                     Service_Id='IAF',
                                     Validity=validity_date,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)
    return redirect(focal_officer_application)

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
              "Import Permit No is:" + new_import_permit + " And is Valid TIll " + str(validity_date) + \
              " Please Make Payment Before Validity Expires. Visit Nearest Bafra Office For Payment."
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

    return redirect(inspector_application)


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


def update_details_la(request):
    application_no = request.POST.get('applicationNo')
    record_id = request.POST.get('import_record_id')
    approved_quantity = request.POST.get('number_released')
    balance_number = request.POST.get('agro_qty_balance')
    remarks = request.POST.get('import_Remarks')

    import_det = t_livestock_import_permit_animal_inspection_t2.objects.filter(pk=record_id)
    if remarks is not None:
        import_det.update(Remarks=remarks)
    else:
        import_det.update(Remarks=None)
    import_det.update(Quantity_Released=approved_quantity)
    import_det.update(Quantity_Balance=balance_number)
    for import_ILA in import_det:
        Product_Record_Id = import_ILA.Product_Record_Id
        balance = int(import_ILA.Quantity_Balance) - int(import_ILA.Quantity_Released)
        product_details = t_livestock_import_permit_animal_t2.objects.filter(pk=Product_Record_Id)
        product_details.update(Quantity_Balance=balance)
        if balance == 0:
            import_details = t_livestock_import_permit_animal_inspection_t1.objects.filter(
                Application_No=application_no)
            for import_det in import_details:
                la_details = t_livestock_import_permit_animal_t1.objects.filter(
                    Import_Permit_No=import_det.Import_Permit_No)
                for la in la_details:
                    work_details = t_workflow_details.objects.filter(Application_No=la.Application_No)
                    work_details.update(Application_Status='C')
    application_details = t_livestock_import_permit_animal_inspection_t2.objects.filter(Application_No=application_no)
    return render(request, 'Animal_Fish_Import/animal_import_details.html', {'import': application_details})


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
    t_payment_details.objects.create(Application_No=application_no,
                                     Application_Date=date.today(),
                                     Permit_No=permit_no,
                                     Service_Id='ILP',
                                     Validity=validity_date,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)
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
              " Please Make Payment Before Validity Expires. Visit Nearest Bafra Office For Payment."
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
    clearnace_ref_no = lp_clearance_no(request)

    update_details = t_livestock_import_permit_product_inspection_t1.objects.filter(Application_No=application_no)
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

    return redirect(inspector_application)


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


def update_details_lp(request):
    application_no = request.POST.get('applicationNo')
    record_id = request.POST.get('import_record_id')
    approved_quantity = request.POST.get('number_released')
    balance_number = request.POST.get('balance')
    remarks = request.POST.get('import_Remarks')

    import_det = t_livestock_import_permit_product_inspection_t2.objects.filter(pk=record_id)
    if remarks is not None:
        import_det.update(Remarks=remarks)
    else:
        import_det.update(Remarks=None)
    import_det.update(Quantity_Released=approved_quantity)
    import_det.update(Quantity_Balance=balance_number)
    for import_ILA in import_det:
        Product_Record_Id = import_ILA.Product_Record_Id
        balance = int(import_ILA.Quantity_Balance) - int(import_ILA.Quantity_Released)
        product_details = t_livestock_import_permit_product_t2.objects.filter(pk=Product_Record_Id)
        product_details.update(Quantity_Balance=balance)
        if balance == 0:
            import_details = t_livestock_import_permit_product_inspection_t1.objects.filter(
                Application_No=application_no)
            for import_det in import_details:
                la_details = t_livestock_import_permit_product_t1.objects.filter(
                    Import_Permit_No=import_det.Import_Permit_No)
                for la in la_details:
                    work_details = t_workflow_details.objects.filter(Application_No=la.Application_No)
                    work_details.update(Application_Status='C')
    application_details = t_livestock_import_permit_product_inspection_t2.objects.filter(Application_No=application_no)
    return render(request, 'Livestock_Import/livestock_import_details.html', {'import': application_details})


# export certificate for animal and animal products
def export_certificate_application(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_field_office_master.objects.filter(Is_Entry_Point='Y')
    unit = t_unit_master.objects.all()
    species = t_livestock_species_master.objects.all()
    breed = t_livestock_species_breed_master.objects.all()
    return render(request, 'Export_Certificate/export_certificate_application.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'unit': unit, 'species': species, 'breed': breed})


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
    Name = request.POST.get('name')
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
    passport = request.POST.get('passport')

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
        Applicant_Id=applicant_Id,
        Passport_No=passport
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
            Particulars = request.POST.get('Particulars')
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
        return render(request, 'Export_Certificate/EC_file_attachment.html', {'file_attach': file_attach})


def submit_ec_details(request):
    application_no = request.POST.get('application_no')
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
    t_payment_details.objects.create(Application_No=application_id,
                                     Application_Date=date.today(),
                                     Permit_No=Export_Permit_No,
                                     Service_Id='LEC',
                                     Validity=validity_date,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)
    for email_id in details:
        emailId = email_id.Email
        send_lec_approve_email(Export_Permit_No, emailId, validity_date)
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
              "Export Permit No is:" + Export_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. Visit Nearest Bafra Office For Payment."
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
    Application_Type = request.POST.get('Permit_Type')
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
        Application_Type=Application_Type,
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
    t_payment_details.objects.create(Application_No=application_id,
                                     Application_Date=date.today(),
                                     Permit_No=Movement_Permit_No,
                                     Service_Id='LMP',
                                     Validity=validity_date,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)
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


def send_lms_approve_email(Movement_Permit_No, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for Movement Permit Of Live Animal and Animal Products Has Been Approved. " \
              "Your " \
              "Movement Permit No is:" + Movement_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. Visit Nearest Bafra Office For Payment."
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
    species = t_livestock_species_master.objects.all()

    return render(request, 'ante_post_mortem/ante_post_mortem_application.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'species': species})


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
    t_payment_details.objects.create(Application_No=application_id,
                                     Application_Date=date.today(),
                                     Permit_No=Clearance_No,
                                     Service_Id='APM',
                                     Validity=validity_date,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)
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
def meat_factory_inspection_list(request):
    Login_Id = request.session['Login_Id']
    new_import_app = t_workflow_details.objects.filter(Application_Status='FR', Action_Date__isnull=False)
    service_details = t_service_master.objects.all()
    return render(request, 'factory_inspection_list.html',
                  {'service_details': service_details, 'application_details': new_import_app})
