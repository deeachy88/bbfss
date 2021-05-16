from datetime import date, datetime, timedelta

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_village_master, t_gewog_master, t_dzongkhag_master, t_country_master, \
    t_field_office_master, t_location_field_office_mapping, t_unit_master, t_service_master, t_user_master
from bbfss import settings
from food.forms import ImportFormFood, FeasibilityForm
from food.models import t_food_export_certificate_t1, t_food_licensinf_food_handler_t1, t_food_import_permit_t1, \
    t_food_import_permit_inspection_t2, t_food_import_permit_t2, t_food_import_permit_inspection_t1, \
    t_food_import_permit_inspection_t3, t_food_business_registration_licensing_t1, \
    t_food_business_registration_licensing_t3, t_food_business_registration_licensing_t2, \
    t_food_business_registration_licensing_t4, t_food_business_registration_licensing_t5, \
    t_food_business_registration_licensing_t6
from livestock.models import t_livestock_clearance_meat_shop_t2
from livestock.views import update_payment
from plant.models import t_workflow_details, t_file_attachment
from plant.views import inspector_application, resubmit_application


def food_business_registration_licensing(request):
    unit = t_unit_master.objects.all()
    return render(request, 'registration_licensing/registration_application.html', {'unit': unit})


def save_food_business_registration(request):
    data = dict()
    service_code = "FBR"
    new_food_business_registration_application = food_business_registration_application_no(service_code)
    Business_Name = request.POST.get('Business_Name')
    CID = request.POST.get('cid')
    name = request.POST.get('name')
    Contact_No = request.POST.get('contactNumber')
    Email = request.POST.get('email')
    address = request.POST.get('address')
    current_status = request.POST.get('current_status')
    name_manager = request.POST.get('name_manager')
    license_criteria = request.POST.get('license_criteria')
    product_category = request.POST.get('product_category')
    product_proposed = request.POST.get('product_proposed')
    identified_water_source = request.POST.get('identified_water_source')
    no_of_years = request.POST.get('no_of_years')
    production_volume = request.POST.get('production_volume')
    volume_unit = request.POST.get('volume_unit')
    history = request.POST.get('history')
    previous_business = request.POST.get('previous_business')
    outsourced_process = request.POST.get('outsourced_process')
    legal_status = request.POST.get('legal_status')
    larger_corporation = request.POST.get('larger_corporation')
    relationship = request.POST.get('relationship')
    licensed_before = request.POST.get('relationship')
    license_number = request.POST.get('license_number')
    reason = request.POST.get('license_number')
    judicial_proceedings = request.POST.get('judicial_proceedings')
    provided_details = request.POST.get('provided_details')
    regulatory_proceedings_details = request.POST.get('regulatory_proceedings_details')
    project_proposal = request.POST.get('project_proposal')
    regulatory_proceedings = request.POST.get('regulatory_proceedings')

    t_food_business_registration_licensing_t1.objects.create(
        Application_No=new_food_business_registration_application,
        Application_Date=date.today(),
        Applicant_Id=request.session['email'],
        Business_Name=Business_Name,
        CID=CID,
        Name_Owner=name,
        Contact_No=Contact_No,
        Email=Email,
        Address=address,
        Name_Manager=name_manager,
        License_Criteria=license_criteria,
        Product_Category=product_category,
        Product=product_proposed,
        Current_Status=current_status,
        Years_In_Production=no_of_years,
        Volume_Last_Year=production_volume,
        Volume_Unit=volume_unit,
        Project_Proposal=project_proposal,
        Water_Source=identified_water_source,
        Site_History=history,
        Previous_Business=previous_business,
        Process_Outsource=outsourced_process,
        Legal_Entity=legal_status,
        Large_Corporation=larger_corporation,
        Large_Corporation_Relation=relationship,
        FBO_License_Status=licensed_before,
        FBO_License_No=license_number,
        Invalid_Reason=reason,
        FBO_Judicial_Proceedings=judicial_proceedings,
        Judicial_Proceedings_Details=provided_details,
        FBO_Regulatory_Proceedings=regulatory_proceedings_details,
        Regulatory_Proceedings_Details=regulatory_proceedings,
        Inspection_Type=None,
        Desired_Inspection_Date=None,
        Remarks_Inspection=None,
        FB_License_No=None,
        FI_Inspection_Date=None,
        FI_Inspection_Leader=None,
        FI_Inspection_Team=None,
        FI_Recommendation=None,
        FR_Inspection_Date=None,
        FR_Inspection_Leader=None,
        FR_Inspection_Team=None
    )

    # field = t_location_field_office_mapping.objects.filter(Location_Code=Consignment_Location_Gewog)
    # for field_office in field:
    #  field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(Application_No=new_food_business_registration_application,
                                      Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Food',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = new_food_business_registration_application
    data['outsourced_process'] = outsourced_process
    return JsonResponse(data)


def food_business_registration_application_no(service_code):
    last_application_no = t_food_business_registration_licensing_t1.objects.aggregate(Max('Application_No'))
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


def food_business_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_business_registration")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/food/food_business_registration" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def food_business_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'registration_licensing/file_attachment.html', {'file_attach': file_attach})


def delete_fh_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_business_registration")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'registration_licensing/file_attachment.html', {'file_attach': file_attach})


def save_fbr_details(request):
    Application_No = request.POST.get('fh_details_application_no')
    BP_Outsourced_To = request.POST.get('details_name')
    Contact_No = request.POST.get('contact_number')
    Address = request.POST.get('details_address')
    BAFRA_License_No = request.POST.get('bafra_license_no')

    t_food_business_registration_licensing_t2.objects.create(Application_No=Application_No,
                                                             BP_Outsourced_To=BP_Outsourced_To,
                                                             Contact_No=Contact_No,
                                                             Address=Address, BAFRA_License_No=BAFRA_License_No)
    fh_details = t_food_business_registration_licensing_t2.objects.filter(Application_No=Application_No)
    return render(request, 'registration_licensing/details.html', {'fh_details': fh_details})


def save_fh_details(request):
    Application_No = request.POST.get('fh_application_no')
    fh_name = request.POST.get('fh_name')
    fh_license = request.POST.get('fh_license')

    t_food_business_registration_licensing_t3.objects.create(Application_No=Application_No, FH_Name=fh_name,
                                                             FH_License_No=fh_license)
    fh_details = t_food_business_registration_licensing_t3.objects.filter(Application_No=Application_No)
    return render(request, 'registration_licensing/food_handler_details.html', {'fh_details': fh_details})


def submit_food_business_application(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(food_business_registration_licensing)


def fbr_fo_approve(request):
    application_no = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    field_office = request.POST.get('forwardTo')

    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_To=field_office)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Assigned_Role_Id='4')
    workflow_details.update(Application_Status='I')  # feasibility inspection
    details = t_food_business_registration_licensing_t1.objects.filter(Application_No=application_no)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    details.update(Field_Office_Id=field_office)
    for email_id in details:
        email = email_id.Email
        send_fip_approve_email(email)

    return render(request, 'focal_officer_pending_list.html')


def fbr_fo_reject(request):
    application_no = request.GET.get('application_id')
    remarks = request.POST.get('remarks')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Application_Status='R')
    details = t_food_import_permit_t1.objects.filter(Application_No=application_no)
    details.update(FO_Remarks=remarks)
    for email_id in details:
        email = email_id.Email
        send_fbr_reject_email(email, remarks)


def send_fbr_approve_email(new_import_permit, Email, validity_date):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Food Products Has Been Approved. Your " \
              "Import Permit No is:" + new_import_permit + " And is Valid TIll " + str(validity_date) + \
              " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_fbr_reject_email(Email, remarks):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Food Business And Registration Has Been Rejected." \
              " Reason: " + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def inspection_team_details(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')

    t_food_business_registration_licensing_t6.objects.create(Application_No=application_id,
                                                             Meeting_Type='Feasibility Inspection ',
                                                             Name=name, Designation=designation)
    application_details = t_food_business_registration_licensing_t6.objects.filter(Application_No=application_id)
    return render(request, 'registration_licensing/inspection_team_details.html',
                  {'application_details': application_details})


def team_details_feasibility_ins(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    opening_date = request.GET.get('opening_date')
    closing_date = request.GET.get('closing_date')
    date_open = datetime.strptime(opening_date, '%d-%m-%Y').date()
    date_close = datetime.strptime(closing_date, '%d-%m-%Y').date()
    t_food_business_registration_licensing_t4.objects.create(Application_No=application_id,
                                                             Meeting_Type='Feasibility Inspection ',
                                                             Name=name, Designation=designation,
                                                             Open_Meeting_Date=date_open,
                                                             Closing_Meeting_Date=date_close)
    application_details = t_food_business_registration_licensing_t4.objects.filter(Application_No=application_id)
    return render(request, 'registration_licensing/team_details.html', {'application_details': application_details})


def concern_details_feasibility_ins(request):
    application_id = request.GET.get('application_id')
    Requirement = request.GET.get('Requirement')
    Observation = request.GET.get('Observations')
    Clause_No = request.GET.get('Clause_No')
    Concern = request.GET.get('Concern')
    Date = request.GET.get('Date')
    date_chosen = datetime.strptime(Date, '%d-%m-%Y').date()
    t_food_business_registration_licensing_t5.objects.create(Application_No=application_id,
                                                             Meeting_Type='Feasibility Inspection ',
                                                             Requirement=Requirement, Observation=Observation,
                                                             Clause_No=Clause_No, Date=date_chosen, Concern=Concern)
    application_details = t_food_business_registration_licensing_t5.objects.filter(Application_No=application_id)
    return render(request, 'registration_licensing/concern_details.html', {'application_details': application_details})


def approve_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    Clearance_No = feasibility_clearance_no(request)
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_food_business_registration_licensing_t1.objects.filter(Application_No=application_id)

    if remarks is not None:
        details.update(FI_Recommendation=remarks)
    else:
        details.update(FI_Recommendation=None)

    details.update(Inspection_Date=date_format_ins)
    details.update(Meat_Shop_Clearance_No=Clearance_No)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='IA')
    for email_id in details:
        emailId = email_id.Email
        send_feasibility_approve_email(Clearance_No, emailId)
    # update_payment(application_id, Meat_Shop_Clearance_No, 'CMS', validity_date)
    return redirect(inspector_application)


def feasibility_clearance_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_food_business_registration_licensing_t1.objects.aggregate(Max('Meat_Shop_Clearance_No'))
    lastAppNo = last_application_no['Meat_Shop_Clearance_No__max']
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
    message = "Dear Sir, Your Application for Feasibility Inspection of " \
              "Food Business And License Registration  Has Been Approved. Your " \
              "Registration No is:" + Clearance_No + " And is Valid Till " \
                                                     "."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_feasibility_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Application for Feasibility Inspection of Food Business And License " \
                                "Registration Has Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def reject_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_food_business_registration_licensing_t1.objects.filter(Application_No=application_id)

    details.update(FI_Recommendation=remarks)
    details.update(FI_Inspection_Date=date_format_ins)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='RS')
    for email_id in application_details:
        email = email_id.Applicant_Id
        login_details = t_user_master.objects.filter(Email_Id=email)
        login = login_details.Login_Id
        application_details.update(Assigned_To=login)
        application_details.update(Assigned_Role_Id=None)
    send_feasibility_reject_email(remarks, details.Email)
    return redirect(inspector_application)


def resubmit_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_food_business_registration_licensing_t1.objects.filter(Application_No=application_id)

    details.update(FI_Recommendation=remarks)
    details.update(FI_Inspection_Date=date_format_ins)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    for det in details:
        field_office = det.Field_Office_Id
        application_details.update(Field_Office_Id=field_office)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_Role_Id='4')
    application_details.update(Application_Status='I')  # feasibility inspection
    application_details.update(Assigned_To=None)
    return redirect(resubmit_application)


def team_details_factory_ins(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    opening_date = request.GET.get('opening_date')
    closing_date = request.GET.get('closing_date')
    date_open = datetime.strptime(opening_date, '%d-%m-%Y').date()
    date_close = datetime.strptime(closing_date, '%d-%m-%Y').date()
    t_food_business_registration_licensing_t4.objects.create(Application_No=application_id,
                                                             Meeting_Type='Feasibility Inspection ',
                                                             Name=name, Designation=designation,
                                                             Open_Meeting_Date=date_open,
                                                             Closing_Meeting_Date=date_close)
    application_details = t_food_business_registration_licensing_t4.objects.filter(Application_No=application_id)
    return render(request, 'registration_licensing/team_details.html', {'application_details': application_details})


def concern_details_factory_ins(request):
    application_id = request.GET.get('application_id')
    Requirement = request.GET.get('Requirement')
    Observation = request.GET.get('Observations')
    Clause_No = request.GET.get('Clause_No')
    Concern = request.GET.get('Concern')
    Date = request.GET.get('Date')
    date_chosen = datetime.strptime(Date, '%d-%m-%Y').date()
    t_food_business_registration_licensing_t5.objects.create(Application_No=application_id,
                                                             Meeting_Type='Feasibility Inspection ',
                                                             Requirement=Requirement, Observation=Observation,
                                                             Clause_No=Clause_No, Date=date_chosen, Concern=Concern)
    application_details = t_food_business_registration_licensing_t5.objects.filter(Application_No=application_id)
    return render(request, 'registration_licensing/concern_details.html', {'application_details': application_details})


def approve_factory_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    Clearance_No = feasibility_clearance_no(request)
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_food_business_registration_licensing_t1.objects.filter(Application_No=application_id)

    if remarks is not None:
        details.update(FI_Recommendation=remarks)
    else:
        details.update(FI_Recommendation=None)

    details.update(Inspection_Date=date_format_ins)
    details.update(Meat_Shop_Clearance_No=Clearance_No)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='IA')
    for email_id in details:
        emailId = email_id.Email
        send_feasibility_approve_email(Clearance_No, emailId)
    # update_payment(application_id, Meat_Shop_Clearance_No, 'CMS', validity_date)
    return redirect(inspector_application)


def factory_clearance_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_food_business_registration_licensing_t1.objects.aggregate(Max('Meat_Shop_Clearance_No'))
    lastAppNo = last_application_no['Meat_Shop_Clearance_No__max']
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


def send_factory_approve_email(Clearance_No, Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for Factory Inspection of " \
              "Food Business And License Registration  Has Been Approved. Your " \
              "Registration No is:" + Clearance_No + " And is Valid Till " \
                                                     "."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_factory_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Application for Factory Inspection of Food Business And License " \
                                "Registration Has Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def reject_factory_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_food_business_registration_licensing_t1.objects.filter(Application_No=application_id)

    details.update(FI_Recommendation=remarks)
    details.update(FI_Inspection_Date=date_format_ins)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='RS')
    for email_id in application_details:
        email = email_id.Applicant_Id
        login_details = t_user_master.objects.filter(Email_Id=email)
        login = login_details.Login_Id
        application_details.update(Assigned_To=login)
        application_details.update(Assigned_Role_Id=None)
    send_feasibility_reject_email(remarks, details.Email)
    return redirect(inspector_application)


def resubmit_factory_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    details = t_food_business_registration_licensing_t1.objects.filter(Application_No=application_id)

    details.update(FI_Recommendation=remarks)
    details.update(FI_Inspection_Date=date_format_ins)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='I')  # feasibility inspection
    return redirect(resubmit_application)


def edit_feasibility_details(request, Record_Id):
    roles = get_object_or_404(t_food_business_registration_licensing_t5, pk=Record_Id)
    Concern_val = request.POST.get('Concern_val')
    if request.method == 'POST':
        form = FeasibilityForm(request.POST, instance=roles)
    else:
        form = FeasibilityForm(instance=roles)
    return save_feasibility_details(request, form, Record_Id, Concern_val,
                                    'registration_licensing/edit_feasibility_details.html')


def save_feasibility_details(request, form, Record_Id, Concern_val, template_name):
    data = dict()
    if request.method == 'POST':
        print(Concern_val)
        import_det = t_food_business_registration_licensing_t5.objects.filter(pk=Record_Id)
        import_det.update(Concern=Concern_val)
        data['form_is_valid'] = True
        roles = t_food_business_registration_licensing_t5.objects.all()
        data['html_book_list'] = render_to_string('registration_licensing/feasibility_inspection.html', {
            'roles': roles
        })
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# Export OF Food
def food_export_certificate_application(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    country = t_country_master.objects.all()
    field_office = t_field_office_master.objects.filter(Is_Entry_Point='Y')
    location = t_location_field_office_mapping.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'export_certificate_food/food_export_certificate.html',
                  {'dzongkhag': dzongkhag, 'village': village,
                   'gewog': gewog, 'country': country,
                   'field_office': field_office,
                   'location': location, 'unit': unit})


def save_food_export_details(request):
    data = dict()
    service_code = "FEC"
    food_export_application = food_export_application_no(service_code)
    License_No = request.POST.get('license_no')
    CID = request.POST.get('cid')
    Exporters_Name = request.POST.get('name')
    Dzongkhag_Code = request.POST.get('dzongkhag')
    Gewog_Code = request.POST.get('gewog')
    Village_Code = request.POST.get('village')
    Exporters_Address = request.POST.get('Exporter_Address')
    Contact_No = request.POST.get('contactNumber')
    Email = request.POST.get('email')
    Importer_Name = request.POST.get('importers_name')
    Importer_Address = request.POST.get('Importers_Address')
    Importing_Country = request.POST.get('importing_country')
    Product_Name = request.POST.get('Product_name')
    No_Of_Packages = request.POST.get('no_of_packages')
    Description_Of_Packages = request.POST.get('description_of_packages')
    Quantity = request.POST.get('quantity')
    Unit = request.POST.get('unit')
    Declared_Point_of_Exit = request.POST.get('Place_of_Exit')
    Export_Expected_Date = request.POST.get('Export_Expected_Date')
    Proposed_Inspection_Date = request.POST.get('inspectionDate')
    Purpose_Of_Export = request.POST.get('export_purpose')
    Consignment_Location_Dzongkhag = request.POST.get('consignment_location_dzongkhag')
    Consignment_Location_Gewog = request.POST.get('consignment_location_gewog')
    Consignment_Location = request.POST.get('consignment_location')
    date_format_ins = datetime.strptime(Proposed_Inspection_Date, '%d-%m-%Y').date()
    date_of_export = datetime.strptime(Export_Expected_Date, '%d-%m-%Y').date()
    additional_info = request.POST.get('additional_info')
    t_food_export_certificate_t1.objects.create(
        Application_No=food_export_application,
        Application_Date=date.today(),
        License_No=License_No,
        CID=CID,
        Exporters_Name=Exporters_Name,
        Dzongkhag_Code=Dzongkhag_Code,
        Gewog_Code=Gewog_Code,
        Village_Code=Village_Code,
        Exporters_Address=Exporters_Address,
        Contact_No=Contact_No,
        Email=Email,
        Importer_Name=Importer_Name,
        Importer_Address=Importer_Address,
        Product_Name=Product_Name,
        No_Of_Packages=No_Of_Packages,
        Description_Of_Packages=Description_Of_Packages,
        Quantity=Quantity,
        Unit=Unit,
        Declared_Point_of_Exit=Declared_Point_of_Exit,
        Export_Expected_Date=date_of_export,
        Proposed_Inspection_Date=date_format_ins,
        Purpose_Of_Export=Purpose_Of_Export,
        Consignment_Location_Dzongkhag=Consignment_Location_Dzongkhag,
        Consignment_Location_Gewog=Consignment_Location_Gewog,
        Consignment_Location=Consignment_Location,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Inspection_Remarks=None,
        Quantity_Net=None,
        Unit_Net=None,
        Export_Permit_No=None,
        Approve_Date=None,
        Validity_Period=None,
        Validity=None,
        Applicant_Id=request.session['email'],
        Importing_Country=Importing_Country,
        Additional_Information=additional_info
    )
    field = t_location_field_office_mapping.objects.filter(Location_Code=Consignment_Location_Gewog)
    for field_office in field:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(Application_No=food_export_application, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=field_office_id, Section='Food',
                                      Assigned_Role_Id='4', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = food_export_application
    return JsonResponse(data)


def food_export_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/export_certificate")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/export_certificate" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def food_export_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'export_certificate_food/file_attachment.html', {'file_attach': file_attach})


def submit_food_export_application(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(food_business_registration_licensing)


def food_export_application_no(service_code):
    last_application_no = t_food_export_certificate_t1.objects.aggregate(Max('Application_No'))
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


def approve_food_export(request):
    application_id = request.POST.get('application_id')
    Inspection_Leader = request.POST.get('Inspection_Leader')
    Inspection_Team = request.POST.get('Inspection_Team')
    Inspection_Date = request.POST.get('dateOfInspection')
    certified_qty = request.POST.get('certified_qty')
    Unit_Net = request.POST.get('Unit_Net')
    rejected_qty = request.POST.get('rejected_qty')
    Unit_Rejected = request.POST.get('Unit_Rejected')
    validity = request.POST.get('validity')
    date_format_ins = datetime.strptime(Inspection_Date, '%d-%m-%Y').date()
    remarks = request.POST.get('remarks')
    Export_Permit_No = food_export_permit_no(request)
    details = t_food_export_certificate_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Inspection_Remarks=remarks)
    else:
        details.update(Inspection_Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Export_Permit_No=Export_Permit_No)
    details.update(Validity_Period=validity)
    details.update(Approved_Date=date.today())
    details.update(Quantity_Certified=certified_qty)
    details.update(Unit_Certified=Unit_Net)
    details.update(Quantity_Rejected=rejected_qty)
    details.update(Unit_Rejected=Unit_Rejected)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    update_payment(application_id, Export_Permit_No, 'FEC', validity_date)
    for email_id in details:
        emailId = email_id.Email
        send_fec_approve_email(Export_Permit_No, emailId, validity_date)
    return redirect(inspector_application)


def food_export_permit_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_food_export_certificate_t1.objects.aggregate(Max('Export_Permit_No'))
    lastAppNo = last_application_no['Export_Permit_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "FEC" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "FEC" + "/" + str(year) + "/" + AppNo
    return newAppNo


def reject_food_export(request):
    application_id = request.POST.get('application_id')
    Inspection_Leader = request.POST.get('Inspection_Leader')
    Inspection_Team = request.POST.get('Inspection_Team')
    Inspection_Date = request.POST.get('dateOfInspection')
    certified_qty = request.POST.get('certified_qty')
    Unit_Net = request.POST.get('Unit_Net')
    rejected_qty = request.POST.get('rejected_qty')
    Unit_Rejected = request.POST.get('Unit_Rejected')
    validity = request.POST.get('validity')
    date_format_ins = datetime.strptime(Inspection_Date, '%d-%m-%Y').date()
    remarks = request.POST.get('remarks')

    details = t_food_export_certificate_t1.objects.filter(Application_No=application_id)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=date_format_ins)
    details.update(Validity_Period=validity)
    details.update(Approved_Date=date.today())
    details.update(Quantity_Certified=certified_qty)
    details.update(Unit_Certified=Unit_Net)
    details.update(Quantity_Rejected=rejected_qty)
    details.update(Unit_Rejected=Unit_Rejected)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='R')
    for email_id in details:
        emailId = email_id.Email
        send_fec_reject_email(remarks, emailId)
    return redirect(inspector_application)


def send_fec_approve_email(Export_Permit_No, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for Export Certificate for Food Products Has Been Approved. " \
              "Your " \
              "Registration No is:" + Export_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_fec_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + "Your Application for Export Certificate for Food Products Has" \
                                " Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


# Licensing of Food Handler
def food_handler_licensing(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    country = t_country_master.objects.all()
    field_office = t_field_office_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'food_handler/application_form.html',
                  {'dzongkhag': dzongkhag, 'village': village,
                   'gewog': gewog, 'country': country,
                   'field_office': field_office,
                   'location': location, 'unit': unit})


def save_food_handler_details(request):
    data = dict()
    service_code = "FHC"
    application_no = food_handler_application_no(service_code)
    Nationality = request.POST.get('Nationality')
    if Nationality == "Bhutanese":
        CID = request.POST.get('cid')
        Permit_No = None
    else:
        CID = None
        Permit_No = request.POST.get('Permit_No')
    Applicant_Name = request.POST.get('name')
    Contact_No = request.POST.get('contactNumber')
    if Nationality == "Bhutanese":
        Email = request.POST.get('email')
        Country_Code = None
        Dzongkhag_Code = request.POST.get('dzongkhag')
        Gewog_Code = request.POST.get('gewog')
        Village_Code = request.POST.get('village')
    else:
        Email = request.POST.get('f_email')
        Country_Code = request.POST.get('country')
        Dzongkhag_Code = None
        Gewog_Code = None
        Village_Code = None
    Training_Request = request.POST.get('Training_Type')
    Preferred_Place = request.POST.get('preferred_place')
    Proposed_Inspection_Date = request.POST.get('preferred_Date')
    Associated_Food_Establishment = request.POST.get('associated_establishment')
    date_format_ins = datetime.strptime(Proposed_Inspection_Date, '%d-%m-%Y').date()
    t_food_licensinf_food_handler_t1.objects.create(
        Application_No=application_no,
        Application_Date=date.today(),
        Nationality=Nationality,
        CID=CID,
        Permit_No=Permit_No,
        Applicant_Name=Applicant_Name,
        Dzongkhag_Code=Dzongkhag_Code,
        Gewog_Code=Gewog_Code,
        Village_Code=Village_Code,
        Country_Code=Country_Code,
        Contact_No=Contact_No,
        Email=Email,
        Training_Request=Training_Request,
        Preferred_Inspection_Place=Preferred_Place,
        Proposed_Inspection_Date=date_format_ins,
        Associated_Food_Establishment=Associated_Food_Establishment,
        Training_Batch_No=None,
        Training_From_Date=None,
        Training_To_Date=None,
        License_Status=None,
        Assessment_Score=None,
        Minimum_Score=None,
        Trainer=None,
        FH_License_No=None,
        Approved_Date=None,
        FH_License_Validity_Period=None,
        FH_License_Validity=None,
        Applicant_Id=request.session['email'],
        OIC_Remarks=None,
        Inspection_Remarks=None
    )
    t_workflow_details.objects.create(Application_No=application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=Preferred_Place, Section='Food',
                                      Assigned_Role_Id='4', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = application_no
    return JsonResponse(data)


def food_handler_application_no(service_code):
    last_application_no = t_food_licensinf_food_handler_t1.objects.aggregate(Max('Application_No'))
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


def food_handler_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_handler_certificate")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/food_handler_certificate" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def food_handler_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'food_handler/file_attachment.html', {'file_attach': file_attach})


def submit_food_handler_application(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(food_handler_licensing)


def food_handler_forward_application(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')
    remarks = request.POST.get('remarks')
    details = t_food_licensinf_food_handler_t1.objects.filter(Application_No=application_id)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Assigned_To=forwardTo)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_Role_Id='5')
    application_details.update(Application_Status='A')
    if remarks is not None:
        details.update(OIC_Remarks=remarks)
    else:
        details.update(OIC_Remarks=None)
    Field_Office_Id = request.session['field_office_id']
    Role_Id = request.session['Role_Id']
    application_Lists = t_workflow_details.objects.filter(Assigned_To=Role_Id, Field_Office_Id=Field_Office_Id)
    for application in application_details:
        email = application.Applicant_Id
        send_acknowledgement_mail(email)
    return render(request, 'oic_pending_list.html', {'application_details': application_Lists})


def reject_food_handler_application(request):
    application_id = request.GET.get('application_id')
    remarks = request.POST.get('remarks')
    details = t_food_licensinf_food_handler_t1.objects.filter(Application_No=application_id)
    work_details = t_workflow_details.objects.filter(Application_No=application_id)
    work_details.update(Action_Date=date.today())
    work_details.update(Application_Status='R')
    for application in details:
        email = application.Applicant_Id
        send_reject_mail(email)
    details.update(OIC_Remarks=remarks)


def send_acknowledgement_mail(Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir/Madam, Your Application for Food Handler Certificate Has Been Accepted. " \
              "You will Be Informed About The Training Programme Later."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_reject_mail(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir/Madam" + "Your Application for Food Handler Certificate Has" \
                                      " Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


# Common
def food_handler_application(request):
    service_code = "FHC"
    Login_Id = request.session['login_id']

    application_details = t_workflow_details.objects.filter(Assigned_Role_Id='5', Assigned_To=Login_Id,
                                                            Application_Status='A', Service_Code=service_code)
    details = t_food_licensinf_food_handler_t1.objects.all()
    return render(request, 'food_handler_list.html',
                  {'details': details, 'application_details': application_details})


def update_batch_no(request):
    app = request.POST.getlist('checkedVals')
    batchNo = request.POST.get('batch_no')
    from_training_Date = request.POST.get('from_training_Date')
    to_training_Date = request.POST.get('from_training_Date')
    remarks = request.POST.get('Remarks')
    Minimum_Score = request.POST.get('min_mark')

    from_Date = datetime.strptime(from_training_Date, '%d-%m-%Y').date()
    to_Date = datetime.strptime(to_training_Date, '%d-%m-%Y').date()

    strings = app[0].split("#")
    for tempArr in strings:
        checkboxArr = tempArr.split("~")
        email = checkboxArr[0]
        app_no = checkboxArr[1]
        details = t_food_licensinf_food_handler_t1.objects.filter(Application_No=app_no)
        details.update(Minimum_Score=Minimum_Score, Training_Batch_No=batchNo, Training_From_Date=from_Date,
                       Training_To_Date=to_Date, Inspection_Remarks=remarks)
        send_batch_mail(batchNo, from_training_Date, to_training_Date, remarks, email)


def send_batch_mail(batchNo, from_training_Date, to_training_Date, remarks, Email):
    subject = 'TRAINING CONFIRMATION'
    message = "Dear " + "Sir/Madam" + "Your Application for Food Handler Certificate Has" \
                                      " Been Accepted. You Are Requested To Attend The Following Training" \
                                      " Training Batch No: " + batchNo + " Training From" + from_training_Date + \
              " To " + to_training_Date + "." + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def result_update_list(request):
    result_details = t_food_licensinf_food_handler_t1.objects.filter(Training_Batch_No__isnull=False).distinct(
        'Training_Batch_No')
    return render(request, 'food_handler/food_handler_result_list.html',
                  {'application_details': result_details})


def update_list(request):
    batch_no = request.POST.get('Training_Batch_No')
    result_details = t_food_licensinf_food_handler_t1.objects.filter(Training_Batch_No=batch_no)
    return render(request, 'food_handler/result_list.html',
                  {'application_details': result_details})


def result_update(request):
    app = request.POST.getlist('checkedVals')
    strings = app[0].split("#")
    for tempArr in strings:
        checkboxArr = tempArr.split("~")
        score = checkboxArr[0]
        app_no = checkboxArr[1]
        att = checkboxArr[2]
        details = t_food_licensinf_food_handler_t1.objects.filter(Application_No=app_no)
        details.update(Assessment_Score=score)
        details.update(Attendance=att)
        for detail in details:
            min_mark = detail.Minimum_Score
            if int(score) > int(min_mark):
                FH_License_no = generate_fh_license_no(request)
                details.update(FH_License_No=FH_License_no)


def generate_fh_license_no(request):
    last_application_no = t_food_licensinf_food_handler_t1.objects.aggregate(Max('FH_License_No'))
    lastAppNo = last_application_no['FH_License_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = "FHC" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = "FHC" + "/" + str(year) + "/" + AppNo
    return newAppNo


# Licensing of Food Handler
def food_import_application(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    country = t_country_master.objects.all()
    field_office = t_field_office_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'import_certificate_food/application_form.html',
                  {'dzongkhag': dzongkhag, 'village': village,
                   'gewog': gewog, 'country': country,
                   'field_office': field_office,
                   'location': location, 'unit': unit})


def save_food_import(request):
    data = dict()
    service_code = "FIP"
    application_no = generate_food_import_app_no(service_code)
    Import_Type = request.POST.get('Import_Type')
    cid = request.POST.get('cid')
    Name = request.POST.get('Name')
    present_address = request.POST.get('present_address')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    license_no = request.POST.get('license_no')
    Operation = request.POST.get('Operation')
    Country_Of_Origin = request.POST.get('Country_Of_Origin')
    country_of_transit = request.POST.get('country_of_transit')
    Country_Name = request.POST.get('Country_Name')
    conveyanceMeans = request.POST.get('conveyanceMeans')
    Place_of_Entry = request.POST.get('Place_of_Entry')
    Final_Destination = request.POST.get('Final_Destination')
    expectedArrivalDate = request.POST.get('expectedArrivalDate')
    date_format_ins = datetime.strptime(expectedArrivalDate, '%d-%m-%Y').date()

    t_food_import_permit_t1.objects.create(
        Application_No=application_no,
        Import_Type=Import_Type,
        License_No=license_no,
        CID=cid,
        Applicant_Name=Name,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Present_Address=present_address,
        Contact_No=contact_number,
        Email=email,
        Operation_Type=Operation,
        Origin_Country_Food=Country_Of_Origin,
        Transit_Country=country_of_transit,
        Country_Of_Transit=Country_Name,
        Means_of_Conveyance=conveyanceMeans,
        Place_Of_Entry=Place_of_Entry,
        Final_Destination=Final_Destination,
        Expected_Arrival_Date=date_format_ins,
        FO_Remarks=None,
        Application_Date=date.today(),
        Approve_Date=None,
        Validity_Period=None,
        Validity=None,
        Import_Permit_No=None
    )
    t_workflow_details.objects.create(Application_No=application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Food',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = application_no
    return JsonResponse(data)


def generate_food_import_app_no(service_code):
    last_application_no = t_food_import_permit_t1.objects.aggregate(Max('Application_No'))
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


def save_food_import_details(request):
    application_no = request.POST.get('appNo')
    Description = request.POST.get('Description')
    quantity = request.POST.get('qty')
    unit = request.POST.get('unit')
    exporter_type = request.POST.getlist('exporter_type')

    t_food_import_permit_t2.objects.create(Application_No=application_no, Product_Name_Description=Description,
                                           Quantity=quantity, Unit=unit, Exporter_Type=exporter_type,
                                           Quantity_Balance=quantity, Remarks=None)
    import_details = t_food_import_permit_t2.objects.filter(Application_No=application_no)
    return render(request, 'import_certificate_food/food_permit_details.html', {'import': import_details})


def food_import_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/import_permit")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/import_permit" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def food_import_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'import_certificate_food/file_attachment.html', {'file_attach': file_attach})


def delete_import_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/import_permit")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'import_certificate_food/file_attachment.html', {'file_attach': file_attach})


def submit_food_import(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(food_import_application)


def approve_fo_fip_import(request):
    service_code = "FIP"
    permit_no = get_fip_permit_no(service_code)
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
    details = t_food_import_permit_t1.objects.filter(Application_No=application_no)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    details.update(Validity_Period=validity)
    details.update(Import_Permit_No=permit_no)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    for email_id in details:
        email = email_id.Email
        send_fip_approve_email(permit_no, email, validity_date)
    update_payment(application_no, permit_no, 'FIP', validity_date)
    return render(request, 'focal_officer_pending_list.html')


def reject_fo_fip_import(request):
    application_no = request.GET.get('application_id')
    remarks = request.POST.get('remarks')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Application_Status='R')
    details = t_food_import_permit_t1.objects.filter(Application_No=application_no)
    details.update(FO_Remarks=remarks)
    for email_id in details:
        email = email_id.Email
        send_fip_reject_email(email, remarks)


def send_fip_approve_email(new_import_permit, Email, validity_date):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Food Products Has Been Approved. Your " \
              "Import Permit No is:" + new_import_permit + " And is Valid TIll " + str(validity_date) + \
              " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def send_fip_reject_email(Email, remarks):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Food Products Has Been Rejected." \
              " Reason: " + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def get_fip_permit_no(service_code):
    last_import_permit_no = t_food_import_permit_t1.objects.aggregate(Max('Import_Permit_No'))
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


def edit_food_inspector_details(request, Record_Id):
    roles = get_object_or_404(t_food_import_permit_inspection_t2, pk=Record_Id)
    Quantity_Released = request.POST.get('Quantity_Released')
    Remarks = request.POST.get('Remarks')
    if request.method == 'POST':
        form = ImportFormFood(request.POST, instance=roles)
    else:
        form = ImportFormFood(instance=roles)
    return save_fip_inspector_details(request, form, Record_Id, Quantity_Released, Remarks,
                                      'import_certificate_food/edit_inspector_details.html')


def save_fip_inspector_details(request, form, Record_Id, Quantity_Released, Remarks, template_name):
    data = dict()
    if request.method == 'POST':
        import_det = t_food_import_permit_inspection_t2.objects.filter(pk=Record_Id)
        import_det.update(Quantity_Released=Quantity_Released)
        import_det.update(Remarks=Remarks)
        for import_LP in import_det:
            Product_Record_Id = import_LP.Product_Record_Id
            balance = int(import_LP.Quantity_Balance) - int(import_LP.Quantity_Released)
            product_details = t_food_import_permit_t2.objects.filter(pk=Product_Record_Id)
            product_details.update(Quantity_Balance=balance)
        data['form_is_valid'] = True
        roles = t_food_import_permit_inspection_t2.objects.all()
        data['html_form'] = render_to_string('import_certificate_food/inspector_details.html', {
            'import': roles
        })
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def food_details_ins_import(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_food_import_permit_inspection_t3.objects.create(Application_No=application_id,
                                                      Current_Observation=currentObservation,
                                                      Decision_Conformity=decisionConform)
    observation = t_food_import_permit_inspection_t3.objects.filter(Application_No=application_id)
    return render(request, 'import_certificate_food/observation_details.html', {'observation': observation})


def submit_fip_application(request):
    application_no = request.GET.get('application_no')
    print(application_no)
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    timeOfInspection = request.GET.get('timeOfInspection')
    date_format_ins = datetime.strptime(dateOfInspection, '%d-%m-%Y').date()
    clearnace_ref_no = fip_clearance_no(request)

    update_details = t_food_import_permit_inspection_t1.objects.filter(Application_No=application_no)
    update_details.update(Clearance_Ref_No=clearnace_ref_no)
    update_details.update(Inspection_Leader=Inspection_Leader)
    update_details.update(Inspection_Team=Inspection_Team)
    update_details.update(Inspection_Date=date_format_ins)
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


def fip_clearance_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_clearance_ref_no = t_food_import_permit_inspection_t1.objects.aggregate(Max('Clearance_Ref_No'))
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