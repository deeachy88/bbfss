from datetime import date, datetime, timedelta
import requests
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.cache import cache_control
from zeep import Client

from administrator.models import t_village_master, t_gewog_master, t_dzongkhag_master, t_country_master, \
    t_field_office_master, t_location_field_office_mapping, t_unit_master, t_service_master, t_user_master, \
    t_food_category_master, t_food_product_category_master
from administrator.views import dashboard
from bbfss import settings
from certification.models import t_certification_organic_t1, t_certification_food_t1, t_certification_gap_t1
from food.forms import ImportFormFood, FeasibilityForm
from food.models import t_food_export_certificate_t1, t_food_licensing_food_handler_t1, t_food_import_permit_t1, \
    t_food_import_permit_inspection_t2, t_food_import_permit_t2, t_food_import_permit_inspection_t1, \
    t_food_import_permit_inspection_t3, t_food_business_registration_licensing_t1, \
    t_food_business_registration_licensing_t3, t_food_business_registration_licensing_t2, \
    t_food_business_registration_licensing_t4, t_food_business_registration_licensing_t5, \
    t_food_business_registration_licensing_t6, t_food_business_registration_licensing_t7, \
    t_food_business_registration_licensing_t8
from livestock.models import t_livestock_clearance_meat_shop_t2, t_livestock_clearance_meat_shop_t1, \
    t_livestock_clearance_meat_shop_t5, t_livestock_clearance_meat_shop_t4, t_livestock_clearance_meat_shop_t6
from plant.models import t_workflow_details, t_file_attachment, t_payment_details, t_payment_details_master
from plant.views import inspector_application, resubmit_application, focal_officer_application, oic_application


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def food_business_registration_licensing(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        unit = t_unit_master.objects.filter(Unit_Type='S')
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        country = t_country_master.objects.all()
        food_product_category = t_food_product_category_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'registration_licensing/registration_application.html',
                      {'unit': unit, 'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village, 'count': message_count,
                       'count_call': inspection_call_count, 'consignment_call_count': consignment_call_count,
                       'food_product_category': food_product_category, 'country': country})
    else:
        return render(request, 'redirect_page.html')


def save_food_business_registration(request):
    data = dict()
    service_code = "FBR"
    new_food_business_registration_application = food_business_registration_application_no(service_code)
    Business_Name = request.POST.get('Business_Name')
    CID = request.POST.get('cid')
    name = request.POST.get('Name')
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
    licensed_before = request.POST.get('licensed_before')
    license_number = request.POST.get('license_number')
    reason = request.POST.get('license_number')
    judicial_proceedings = request.POST.get('judicial_proceedings')
    provided_details = request.POST.get('provided_details')
    regulatory_proceedings_details = request.POST.get('regulatory_proceedings_details')
    project_proposal = request.POST.get('project_proposal')
    regulatory_proceedings = request.POST.get('regulatory_proceedings')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    process_flow = request.POST.get('process_flow')
    quality_assurance = request.POST.get('quality_assurance')

    t_food_business_registration_licensing_t1.objects.create(
        application_no=new_food_business_registration_application,
        application_date=date.today(),
        applicant_id=request.session['email'],
        business_name=Business_Name,
        cid=CID,
        name_owner=name,
        contact_no=Contact_No,
        email=Email,
        address=address,
        name_manager=name_manager,
        license_criteria=license_criteria,
        product_category=product_category,
        product=product_proposed,
        current_status=current_status,
        years_in_production=no_of_years,
        volume_last_year=production_volume,
        volume_unit=volume_unit,
        project_proposal=project_proposal,
        water_source=identified_water_source,
        site_history=history,
        previous_business=previous_business,
        process_outsource=outsourced_process,
        legal_entity=legal_status,
        large_corporation=larger_corporation,
        large_corporation_relation=relationship,
        fbo_license_status=licensed_before,
        fbo_license_no=license_number,
        invalid_reason=reason,
        fbo_judicial_proceedings=judicial_proceedings,
        judicial_proceedings_details=provided_details,
        fbo_regulatory_proceedings=regulatory_proceedings_details,
        regulatory_proceedings_details=regulatory_proceedings,
        inspection_type=None,
        fb_license_no=None,
        fi_inspection_date=None,
        fi_inspection_leader=None,
        fi_recommendation=None,
        fr_inspection_date=None,
        fr_inspection_leader=None,
        fr_inspection_team=None,
        dzongkhag_code=dzongkhag,
        gewog_code=gewog,
        village_code=village,
        process_flow_technology=process_flow,
        quality_assurance_system=quality_assurance
    )

    t_workflow_details.objects.create(application_no=new_food_business_registration_application,
                                      applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=None, section='Food',
                                      assigned_role_id='2', action_date=None, application_status='P',
                                      service_code=service_code)
    data['applNo'] = new_food_business_registration_application
    data['outsourced_process'] = outsourced_process
    return JsonResponse(data)


def update_food_business_registration(request):
    data = dict()
    service_code = "FBR"
    new_food_business_registration_application = request.POST.get('application_no')
    Business_Name = request.POST.get('Business_Name')
    CID = request.POST.get('cid')
    name = request.POST.get('Name')
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
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    process_flow = request.POST.get('process_flow')
    quality_assurance = request.POST.get('quality_assurance')

    food_business_details = t_food_business_registration_licensing_t1.objects.filter(
        application_no=new_food_business_registration_application)

    food_business_details.update(
        application_date=date.today(),
        applicant_id=request.session['email'],
        business_name=Business_Name,
        cid=CID,
        name_owner=name,
        contact_no=Contact_No,
        email=Email,
        address=address,
        name_manager=name_manager,
        license_criteria=license_criteria,
        product_category=product_category,
        product=product_proposed,
        current_status=current_status,
        years_in_production=no_of_years,
        volume_last_year=production_volume,
        volume_unit=volume_unit,
        project_proposal=project_proposal,
        water_source=identified_water_source,
        site_history=history,
        previous_business=previous_business,
        process_outsource=outsourced_process,
        legal_entity=legal_status,
        large_corporation=larger_corporation,
        large_corporation_relation=relationship,
        fbo_license_status=licensed_before,
        fbo_license_no=license_number,
        invalid_reason=reason,
        fbo_judicial_proceedings=judicial_proceedings,
        judicial_proceedings_details=provided_details,
        fbo_regulatory_proceedings=regulatory_proceedings_details,
        regulatory_proceedings_details=regulatory_proceedings,
        inspection_type=None,
        fb_license_no=None,
        fi_inspection_date=None,
        fi_inspection_leader=None,
        fi_recommendation=None,
        fr_inspection_date=None,
        fr_inspection_leader=None,
        fr_inspection_team=None,
        dzongkhag_code=dzongkhag,
        gewog_code=gewog,
        village_code=village,
        process_flow_technology=process_flow,
        quality_assurance_system=quality_assurance

    )

    work_details = t_workflow_details.objects.filter(application_no=new_food_business_registration_application)
    work_details.update(
        applicant_id=request.session['email'],
        assigned_to=None, field_office_id=None, section='Food',
        assigned_role_id='2', action_date=None, application_status='P',
        service_code=service_code)
    data['applNo'] = new_food_business_registration_application
    data['outsourced_process'] = outsourced_process
    return JsonResponse(data)


def food_business_registration_application_no(service_code):
    last_application_no = t_food_business_registration_licensing_t1.objects.aggregate(Max('application_no'))
    lastAppNo = last_application_no['application_no__max']
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


def food_business_file(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_business_registration")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/food_business_registration" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def food_business_file_name(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
        return render(request, 'registration_licensing/file_attachment.html', {'file_attach': file_attach})


def delete_fbr_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_business_registration")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'registration_licensing/file_attachment.html', {'file_attach': file_attach})


def save_fbr_details(request):
    Application_No = request.POST.get('fh_details_application_no')
    BP_Outsourced_To = request.POST.get('details_name')
    Contact_No = request.POST.get('contact_number')
    Address = request.POST.get('details_address')
    BAFRA_License_No = request.POST.get('bafra_license_no')

    t_food_business_registration_licensing_t2.objects.create(application_no=Application_No,
                                                             bp_outsourced_to=BP_Outsourced_To,
                                                             contact_no=Contact_No,
                                                             address=Address, bafra_license_no=BAFRA_License_No)
    fh_details = t_food_business_registration_licensing_t2.objects.filter(application_no=Application_No)
    count = t_food_business_registration_licensing_t2.objects.filter(application_no=Application_No).count()
    return render(request, 'registration_licensing/details.html', {'fh_details': fh_details, 'count': count})


def save_fh_details(request):
    Application_No = request.POST.get('fh_application_no')
    fh_name = request.POST.get('fh_name')
    fh_license = request.POST.get('fh_license')

    t_food_business_registration_licensing_t3.objects.create(application_no=Application_No, fh_name=fh_name,
                                                             fh_license_no=fh_license)
    fh_details = t_food_business_registration_licensing_t3.objects.filter(application_no=Application_No)
    fh_details_count = t_food_business_registration_licensing_t3.objects.filter(application_no=Application_No).count()
    return render(request, 'registration_licensing/food_handler_details.html', {'fh_details': fh_details,
                                                                                'count': fh_details_count})


def load_outsourced_details(request):
    Application_No = request.GET.get('appNo')
    fh_details = t_food_business_registration_licensing_t2.objects.filter(application_no=Application_No)
    count = t_food_business_registration_licensing_t2.objects.filter(application_no=Application_No).count()
    return render(request, 'registration_licensing/details.html', {'fh_details': fh_details, 'count': count})


def food_handler_details(request):
    Application_No = request.GET.get('appNo')
    fh_details = t_food_business_registration_licensing_t3.objects.filter(application_no=Application_No)
    fh_details_count = t_food_business_registration_licensing_t3.objects.filter(application_no=Application_No).count()
    return render(request, 'registration_licensing/food_handler_details.html', {'fh_details': fh_details,
                                                                                'fh_details_count': fh_details_count})


def load_fbr_attachment(request):
    Application_No = request.GET.get('appNo')
    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'registration_licensing/file_attachment.html', {'file_attach': file_attach})


def submit_food_business_application(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    workflow_details.update(action_date=date.today())
    application_details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_no)
    application_details.update(application_date=date.today())
    return redirect(food_business_registration_licensing)


def fbr_fo_approve(request):
    application_no = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    field_office = request.POST.get('forwardTo')

    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    workflow_details.update(assigned_to=None)
    workflow_details.update(field_office_id=field_office)
    workflow_details.update(action_date=date.today())
    workflow_details.update(assigned_role_id='4')
    workflow_details.update(application_status='I')  # feasibility inspection
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_no)
    if remarks is not None:
        details.update(fo_remarks=remarks)
    else:
        details.update(fo_remarks=None)
    details.update(field_office_id=field_office)
    return redirect(focal_officer_application)


def fbr_fo_reject(request):
    application_no = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    workflow_details.update(action_date=date.today())
    workflow_details.update(application_status='R')
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_no)
    details.update(fo_remarks=remarks)
    for email_id in details:
        email = email_id.email
        send_fbr_reject_email(email, remarks)
    return redirect(focal_officer_application)


def send_fbr_approve_email(new_import_permit, Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir," \
              "" \
              "Your Application for Food Business Registration Has Been Approved. Your " \
              "Registration No is:" + new_import_permit + \
              " Please Make Payment To Download The Certificate. Visit The Nearest Bafra Office For Payment" \
              "or Pay Online at https://tinyurl.com/y3m7wa3c Thank you!"
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_fbr_reject_email(Email, remarks):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Food Business Registration Has Been Rejected." \
              " Because: " + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def inspection_team_details(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')

    t_food_business_registration_licensing_t6.objects.create(application_no=application_id,
                                                             meeting_type='Feasibility Inspection',
                                                             name=name, designation=designation)
    application_details = t_food_business_registration_licensing_t6.objects.filter(
        application_no=application_id, meeting_type='Feasibility Inspection')
    return render(request, 'registration_licensing/inspection_team_details.html',
                  {'application_details': application_details})


def team_details_feasibility_ins(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    meeting_date = request.GET.get('meeting_date')
    meeting_type_value = request.GET.get('meeting_type')
    t_food_business_registration_licensing_t4.objects.create(application_no=application_id,
                                                             meeting_type='Feasibility Inspection',
                                                             name=name, designation=designation,
                                                             meeting_date=meeting_date,
                                                             type=meeting_type_value)
    application_details = t_food_business_registration_licensing_t4.objects.filter(
        application_no=application_id, meeting_type='Feasibility Inspection')
    return render(request, 'registration_licensing/team_details.html', {'application_details': application_details})


def concern_details_feasibility_ins(request):
    application_id = request.GET.get('application_id')
    Requirement = request.GET.get('Requirement')
    Observation = request.GET.get('Observations')
    Clause_No = request.GET.get('Clause_No')
    Concern = request.GET.get('Concern')
    response_fbo = request.GET.get('response_fbo')
    t_food_business_registration_licensing_t5.objects.create(application_no=application_id,
                                                             inspection_type='Feasibility Inspection',
                                                             requirement=Requirement, observation=Observation,
                                                             clause_no=Clause_No, date=date.today(), concern=Concern,
                                                             fbo_response=response_fbo, nc=None, nc_category=None)
    application_details = t_food_business_registration_licensing_t5.objects.filter(application_no=application_id,
                                                                                   inspection_type='Feasibility '
                                                                                                   'Inspection') \
        .order_by('record_id')
    message_count = t_food_business_registration_licensing_t5.objects.filter(
        concern='Yes', inspection_type='Feasibility Inspection').count()
    return render(request, 'registration_licensing/concern_details.html', {'application_details': application_details,
                                                                           'message_count': message_count})


def approve_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    inspection_leader = request.GET.get('Inspection_Leader')
    inspection_team = request.GET.get('Inspection_Team')
    date_format_ins = request.GET.get('dateOfInspection')
    Clearance_No = feasibility_clearance_no(request)
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)

    if remarks is not None:
        details.update(fi_recommendation=remarks)
    else:
        details.update(fi_recommendation=None)

    details.update(fi_inspection_date=date_format_ins)
    details.update(fi_inspection_team=inspection_team)
    details.update(fi_inspection_leader=inspection_leader)
    details.update(conditional_clearance_no=Clearance_No)
    details.update(clearance_approve_date=date.today())
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='FR')
    application_details.update(assigned_role_id=None)
    for work_details in application_details:
        user_id = work_details.applicant_id
        login = t_user_master.objects.filter(Email_Id=user_id)
        for login_id in login:
            id = login_id.Login_Id
            application_details.update(assigned_to=id)
    for email_id in details:
        emailId = email_id.email
        send_feasibility_approve_email(Clearance_No, emailId)
    update_payment(application_id, Clearance_No, 'FBR', None, 'Feasibility', '131110039')
    return redirect(inspector_application)


def feasibility_clearance_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_food_business_registration_licensing_t1.objects.aggregate(Max('conditional_clearance_no'))
    lastAppNo = last_application_no['Conditional_Clearance_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "-" + "FBR-CLR" + "-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "-" + "FBR-CLR" + "-" + str(year) + "-" + AppNo
    return newAppNo


def send_feasibility_approve_email(Clearance_No, Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for Feasibility Inspection of " \
              "Food Business Registration And Licensing Has Been Approved. Your " \
              "Clearance No is :" + Clearance_No + "Please Make Payment To Download The Clearance." \
                                                   " Visit The Nearest Bafra Office For Payment."
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_feasibility_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Feasibility Inspection of Food Business Registration " \
                                "And Licensing " \
                                "Has Been Rejected Because" + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def reject_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)

    details.update(fi_recommendation=remarks)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='IRS')
    for email_id in application_details:
        email = email_id.applicant_id
        login_details = t_user_master.objects.filter(Email_Id=email)
        for det_login in login_details:
            login = det_login.Login_Id
            application_details.update(assigned_to=login)
            application_details.update(assigned_role_id=None)
    return redirect(inspector_application)


def resubmit_feasibility_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    date_format_ins = request.GET.get('dateOfInspection')
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)

    details.update(fi_response=remarks)
    details.update(desired_fi_inspection_date=date_format_ins)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(assigned_role_id='4')
    application_details.update(application_status='I')  # feasibility inspection
    application_details.update(assigned_to=None)
    return redirect(resubmit_application)


def team_details_factory_ins(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    meeting_date = request.GET.get('meeting_date')
    meeting_type_value = request.GET.get('meeting_type')
    t_food_business_registration_licensing_t4.objects.create(application_no=application_id,
                                                             meeting_type='Factory Inspection',
                                                             name=name, designation=designation,
                                                             meeting_date=meeting_date,
                                                             type=meeting_type_value)
    application_details = t_food_business_registration_licensing_t4.objects.filter(application_no=application_id,
                                                                                   meeting_type='Factory Inspection')
    return render(request, 'registration_licensing/team_details.html', {'application_details': application_details})


def concern_details_factory_ins(request):
    application_id = request.GET.get('application_id')
    Requirement = request.GET.get('Requirement')
    Observation = request.GET.get('Observations')
    Clause_No = request.GET.get('Clause_No')
    Concern = request.GET.get('Concern')
    NC_Category = request.GET.get('NC_Category')
    t_food_business_registration_licensing_t5.objects.create(application_no=application_id,
                                                             inspection_type='Factory Inspection',
                                                             requirement=Requirement, observation=Observation,
                                                             clause_no=Clause_No, date=date.today(), concern=None,
                                                             fbo_response=None, nc=Concern, nc_category=NC_Category)
    application_details = t_food_business_registration_licensing_t5.objects.filter(application_no=application_id,
                                                                                   inspection_type='Factory Inspection') \
        .order_by('record_id')
    message_count = t_food_business_registration_licensing_t5.objects.filter(
        nc='Yes', inspection_type='Factory Inspection').count()
    return render(request, 'registration_licensing/nc_details.html', {'application_details': application_details,
                                                                      'message_count': message_count})


def fbr_factory_team_details(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')

    t_food_business_registration_licensing_t6.objects.create(application_no=application_id,
                                                             meeting_type='Factory Inspection',
                                                             name=name, designation=designation)
    application_details = t_food_business_registration_licensing_t6.objects.filter(
        application_no=application_id, meeting_type='Factory Inspection').order_by('Record_Id')
    return render(request, 'registration_licensing/inspection_team_details.html',
                  {'application_details': application_details})


def approve_factory_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    inspection_leader = request.GET.get('Inspection_Leader')
    inspection_team = request.GET.get('Inspection_Team')
    date_format_ins = request.GET.get('dateOfInspection')
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)

    if remarks is not None:
        details.update(fr_recommendation=remarks)
    else:
        details.update(fr_recommendation=None)

    details.update(fr_inspection_date=date_format_ins)
    details.update(fr_inspection_leader=inspection_leader)
    details.update(fr_inspection_team=inspection_team)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='FRA')
    application_details.update(assigned_role_id='2')
    for email_id in details:
        emailId = email_id.email
        send_factory_approve_email(emailId)
    return redirect(inspector_application)


def fbr_submit(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')

    clearance = factory_clearance_no(request, application_id)
    print(clearance)
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)
    details.update(fb_license_no=clearance)
    details.update(approve_date=date.today())
    # d = timedelta(days=int(validity))
    # validity_date = date.today() + d
    # details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='A')
    update_payment(application_id, clearance, 'FBR', None, 'Final', '131110038')
    for email_id in details:
        emailId = email_id.email
        send_fbr_approve_email(clearance, emailId)
    return redirect(focal_officer_application)


def factory_clearance_no(request, application_id):
    global Field_Code
    details = t_workflow_details.objects.filter(application_no=application_id)
    for details in details:
        Field_office_Code = details.Field_Office_Id
        code = t_field_office_master.objects.filter(Field_Office_Id=Field_office_Code)
        for code in code:
            Field_Code = code.Field_Office_Code
            last_application_no = t_food_business_registration_licensing_t1.objects.aggregate(Max('fb_license_no'))
            lastAppNo = last_application_no['fb_license_no__max']
            if not lastAppNo:
                year = timezone.now().year
                newAppNo = Field_Code + "-" + "FBR" + "-" + str(year) + "-" + "0001"
            else:
                substring = str(lastAppNo)[14:17]
                substring = int(substring) + 1
                AppNo = str(substring).zfill(4)
                year = timezone.now().year
                newAppNo = Field_Code + "-" + "FBR" + "-" + str(year) + "-" + AppNo
            return newAppNo


def send_factory_approve_email(Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Factory Inspection of " \
              "Food Business Registration And Licensing Has Been Approved. "
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_factory_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Factory Inspection of Food Business Registration And Licensing " \
                                "Has Been Rejected Because" + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def reject_factory_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)

    details.update(fr_recommendation=remarks)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='RS')
    application_details.update(assigned_role_id=None)
    for applicant in application_details:
        email_id = applicant.applicant_id
        print(email_id)
        login_details = t_user_master.objects.filter(Email_Id=email_id)
        for applicant_login in login_details:
            login = applicant_login.Login_Id
            print(login)
            application_details.update(assigned_to=login)
    # send_feasibility_reject_email(remarks, details.Email)
    return redirect(inspector_application)


def resubmit_factory_inspection(request):
    application_id = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    date_format_ins = request.GET.get('dateOfInspection')
    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)

    details.update(fr_response=remarks)
    details.update(desired_fr_inspection_date=date_format_ins)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(assigned_to=None)
    application_details.update(assigned_role_id='4')
    application_details.update(application_status='FR')  # Factory inspection
    return redirect(resubmit_application)


def edit_fbr_feasibility_details(request):
    record_id = request.GET.get('record_id')
    application_id = request.GET.get('app_no')
    edit_Concern = request.GET.get('edit_Concern')
    edit_response_fbo = request.GET.get('edit_response_fbo')
    app_details = t_food_business_registration_licensing_t5.objects.filter(record_id=record_id)
    app_details.update(concern=edit_Concern)
    app_details.update(fbo_response=edit_response_fbo)
    if edit_response_fbo is not None:
        app_details.update(fbo_response=edit_response_fbo)
    else:
        app_details.update(fbo_response=None)
    application_details = t_food_business_registration_licensing_t5.objects.filter(application_no=application_id,
                                                                                   inspection_type='Feasibility Inspection') \
        .order_by('record_id')
    message_count = t_food_business_registration_licensing_t5.objects.filter(
        concern='Yes', inspection_type='Feasibility Inspection').count()
    return render(request, 'registration_licensing/concern_details.html', {'application_details': application_details,
                                                                           'message_count': message_count})


def edit_fbr_factory_details(request):
    record_id = request.GET.get('record_id')
    application_id = request.GET.get('app_no')
    print(record_id)
    print(application_id)
    edit_Concern = request.GET.get('edit_Concern')
    NC_Category = request.GET.get('edit_nc_category')
    edit_Observations = request.GET.get('edit_Observations')
    app_details = t_food_business_registration_licensing_t5.objects.filter(record_id=record_id)
    app_details.update(nc=edit_Concern)
    app_details.update(observation=edit_Observations)
    if edit_Observations is not None:
        app_details.update(observation=edit_Observations)
    else:
        app_details.update(observation=None)
    if NC_Category is not None:
        app_details.update(nc_category=NC_Category)
    else:
        app_details.update(nc_category=None)
    application_details = t_food_business_registration_licensing_t5.objects.filter(application_no=application_id,
                                                                                   inspection_type='Factory Inspection') \
        .order_by('record_id')
    message_count = t_food_business_registration_licensing_t5.objects.filter(
        nc='Yes', inspection_type='Factory Inspection').count()
    return render(request, 'registration_licensing/nc_details.html', {'application_details': application_details,
                                                                      'message_count': message_count})


def forward_fbr_application(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')

    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(assigned_to=forwardTo)
    application_details.update(action_date=date.today())
    application_details.update(assigned_role_id='5')
    return redirect(oic_application)


def view_factory_inspection_application(request):
    application_id = request.GET.get('application_id')
    work_details = t_workflow_details.objects.filter(application_no=application_id)
    for app_status in work_details:
        service_code = app_status.service_code
        if service_code == 'CMS':
            application_details = t_livestock_clearance_meat_shop_t1.objects.filter(Application_No=application_id)
            details = t_livestock_clearance_meat_shop_t2.objects.filter(Application_No=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id)
            unit = t_unit_master.objects.all()
            inspection_details = t_livestock_clearance_meat_shop_t5.objects.filter(Application_No=application_id)
            team_details = t_livestock_clearance_meat_shop_t4.objects.filter(Application_No=application_id)
            inspection_team_details = t_livestock_clearance_meat_shop_t6.objects.filter(Application_No=application_id)
            oic_list = t_field_office_master.objects.filter()
            dzongkhag = t_dzongkhag_master.objects.all()
            gewog = t_gewog_master.objects.all()
            village = t_village_master.objects.all()
            return render(request, 'meat_shop_registration/client_factory_inspect.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'oic_list': oic_list, 'unit': unit, 'inspection_details': inspection_details,
                           'team_details': team_details, 'inspection_team_details': inspection_team_details,
                           'dzongkhag': dzongkhag, 'village': village, 'gewog': gewog})
        else:
            application_details = t_food_business_registration_licensing_t1.objects.filter(
                application_no=application_id)
            details = t_food_business_registration_licensing_t2.objects.filter(application_no=application_id)
            fh_details = t_food_business_registration_licensing_t3.objects.filter(application_no=application_id)
            file = t_file_attachment.objects.filter(application_no=application_id)
            unit = t_unit_master.objects.all()
            inspection_details = t_food_business_registration_licensing_t5.objects.filter(
                application_no=application_id)
            team_details = t_food_business_registration_licensing_t4.objects.filter(application_no=application_id)
            inspection_team_details = t_food_business_registration_licensing_t6.objects.filter(
                application_no=application_id)
            oic_list = t_field_office_master.objects.filter()
            raw_materials = t_food_business_registration_licensing_t7.objects.filter(application_no=application_id)
            packaging_material = t_food_business_registration_licensing_t8.objects.filter(application_no=application_id)
            dzongkhag = t_dzongkhag_master.objects.all()
            gewog = t_gewog_master.objects.all()
            village = t_village_master.objects.all()
            return render(request, 'registration_licensing/client_factory_inspect.html',
                          {'application_details': application_details, 'details': details, 'file': file,
                           'oic_list': oic_list, 'unit': unit, 'inspection_details': inspection_details,
                           'team_details': team_details, 'inspection_team_details': inspection_team_details,
                           'fh_details': fh_details, 'raw_materials': raw_materials,
                           'packaging_material': packaging_material, 'dzongkhag': dzongkhag, 'village': village,
                           'gewog': gewog})


def forward_factory_application(request):
    application_id = request.POST.get('application_id')
    Desired_FR_Inspection_Date = request.POST.get('date')
    print(application_id)
    print(Desired_FR_Inspection_Date)

    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(assigned_to=None)
    application_details.update(action_date=date.today())
    application_details.update(assigned_role_id='4')

    details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)
    details.update(desired_fr_inspection_date=Desired_FR_Inspection_Date)

    return redirect(factory_inspection_list)


def update_fbr_team_details_feasibility_ins(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    meeting_date = request.GET.get('meeting_date')
    meeting_type_value = request.GET.get('meeting_type')
    record_id = request.GET.get('record_id')
    details = t_food_business_registration_licensing_t4.objects.filter(record_id=record_id)
    details.update(name=name, designation=designation, meeting_date=meeting_date, type=meeting_type_value)
    application_details = t_food_business_registration_licensing_t4.objects.filter(application_no=application_id,
                                                                                   meeting_type='Feasibility Inspection') \
        .order_by('record_id')
    return render(request, 'registration_licensing/team_details.html', {'application_details': application_details})


def update_fbr_inspection_team_details(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    record_id = request.GET.get('record_id')

    details = t_food_business_registration_licensing_t6.objects.filter(record_id=record_id)
    details.update(name=name, designation=designation)
    application_details = t_food_business_registration_licensing_t6.objects.filter(application_no=application_id,
                                                                                   meeting_type='Feasibility Inspection') \
        .order_by('record_id')
    return render(request, 'registration_licensing/inspection_team_details.html',
                  {'application_details': application_details})


def delete_fbr_fi_inspection_team_details(request):
    application_id = request.GET.get('Application_No')
    record_id = request.GET.get('Record_Id')
    details = t_food_business_registration_licensing_t6.objects.filter(record_id=record_id)
    details.delete()
    application_details = t_food_business_registration_licensing_t6.objects.filter(application_no=application_id,
                                                                                   meeting_type='Feasibility Inspection') \
        .order_by('record_id')
    return render(request, 'registration_licensing/inspection_team_details.html',
                  {'application_details': application_details})


def delete_fbr_fi_team_details(request):
    application_id = request.GET.get('Application_No')
    record_id = request.GET.get('Record_Id')
    details = t_food_business_registration_licensing_t4.objects.filter(record_id=record_id)
    details.delete()
    application_details = t_food_business_registration_licensing_t4.objects.filter(application_no=application_id,
                                                                                   meeting_type='Feasibility Inspection') \
        .order_by('record_id')
    return render(request, 'registration_licensing/team_details.html', {'application_details': application_details})


def update_fbr_team_details_factory_ins(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    meeting_date = request.GET.get('meeting_date')
    meeting_type_value = request.GET.get('meeting_type')
    record_id = request.GET.get('record_id')
    details = t_food_business_registration_licensing_t4.objects.filter(record_id=record_id)
    details.update(name=name, designation=designation, meeting_date=meeting_date, type=meeting_type_value)
    application_details = t_food_business_registration_licensing_t4.objects.filter(application_no=application_id,
                                                                                   meeting_type='Factory Inspection') \
        .order_by('record_id')
    return render(request, 'registration_licensing/team_details.html', {'application_details': application_details})


def update_fbr_factory_inspection_team_details(request):
    application_id = request.GET.get('application_id')
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    record_id = request.GET.get('record_id')

    details = t_food_business_registration_licensing_t6.objects.filter(record_id=record_id)
    details.update(name=name, designation=designation)
    application_details = t_food_business_registration_licensing_t6.objects.filter(application_no=application_id,
                                                                                   meeting_type='Factory Inspection') \
        .order_by('record_id')
    return render(request, 'registration_licensing/inspection_team_details.html',
                  {'application_details': application_details})


def delete_fbr_factory_inspection_team_details(request):
    application_id = request.GET.get('application_id')
    record_id = request.GET.get('record_id')
    details = t_food_business_registration_licensing_t4.objects.filter(record_id=record_id)
    details.delete()
    application_details = t_food_business_registration_licensing_t4.objects.filter(application_no=application_id,
                                                                                   meeting_type='Factory Inspection') \
        .order_by('record_id')
    return render(request, 'registration_licensing/inspection_team_details.html',
                  {'application_details': application_details})


def delete_fbr_factory_team_details(request):
    application_id = request.GET.get('application_id')
    record_id = request.GET.get('record_id')
    details = t_food_business_registration_licensing_t4.objects.filter(record_id=record_id)
    details.delete()
    application_details = t_food_business_registration_licensing_t4.objects.filter(application_no=application_id,
                                                                                   meeting_type='Factory Inspection') \
        .order_by('record_id')
    return render(request, 'registration_licensing/team_details.html', {'application_details': application_details})


def save_raw_materials_details(request):
    application_no = request.POST.get('application_no')
    name = request.POST.get('raw_material_name')
    source_country = request.POST.get('source_country')
    t_food_business_registration_licensing_t7.objects.create(application_no=application_no, name=name,
                                                             source_country=source_country)
    raw_materials = t_food_business_registration_licensing_t7.objects.filter(application_no=application_no) \
        .order_by('record_id')
    raw_count = t_food_business_registration_licensing_t7.objects.filter(application_no=application_no).count()
    return render(request, 'registration_licensing/raw_material_details.html', {'raw_materials': raw_materials,
                                                                                'raw_count': raw_count})


def save_packaging_materials_details(request):
    application_no = request.POST.get('application_no')
    name = request.POST.get('packaging_name')
    source_country = request.POST.get('packaging_source_country')
    t_food_business_registration_licensing_t8.objects.create(application_no=application_no, name=name,
                                                             source_country=source_country)
    packaging_material = t_food_business_registration_licensing_t8.objects.filter(application_no=application_no) \
        .order_by('record_id')
    packaging_count = t_food_business_registration_licensing_t8.objects.filter(application_no=application_no).count()
    return render(request, 'registration_licensing/packaging_material_details.html',
                  {'packaging_material': packaging_material, 'packaging_count': packaging_count})


# Export OF Food
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def food_export_certificate_application(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        country = t_country_master.objects.all()
        field_office = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        location = t_location_field_office_mapping.objects.all()
        unit = t_unit_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'export_certificate_food/food_export_certificate.html',
                      {'dzongkhag': dzongkhag, 'village': village,
                       'gewog': gewog, 'country': country,
                       'field_office': field_office,
                       'location': location, 'unit': unit, 'count': message_count, 'count_call': inspection_call_count,
                       'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def save_food_export_details(request):
    data = dict()
    service_code = "FEC"
    food_export_application = food_export_application_no(service_code)
    Application_Type = request.POST.get('Application_Type')
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
    date_of_export = request.POST.get('Export_Expected_Date')
    date_format_ins = request.POST.get('inspectionDate')
    Purpose_Of_Export = request.POST.get('export_purpose')
    Consignment_Location_Dzongkhag = request.POST.get('consignment_location_dzongkhag')
    Consignment_Location_Gewog = request.POST.get('consignment_location_gewog')
    Consignment_Location = request.POST.get('consignment_location')
    additional_info = request.POST.get('additional_info')
    t_food_export_certificate_t1.objects.create(
        Application_No=food_export_application,
        Application_Date=date.today(),
        Application_Type=Application_Type,
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
        Export_Permit_No=None,
        Approved_Date=None,
        Validity_Period=None,
        Validity=None,
        Applicant_Id=request.session['email'],
        Importing_Country=Importing_Country,
        Additional_Information=additional_info,
        Rejection_Reason=None,
        Terms=None
    )
    field = t_location_field_office_mapping.objects.filter(Location_Code=Consignment_Location_Gewog)
    for field_office in field:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(application_no=food_export_application, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=field_office_id, section='Food',
                                      assigned_role_id='4', action_date=None, application_status='P',
                                      service_code=service_code)
    data['applNo'] = food_export_application
    return JsonResponse(data)


def update_food_export_details(request):
    data = dict()
    service_code = "FEC"
    food_export_application = request.POST.get('application_no')
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
    additional_info = request.POST.get('additional_info')

    food_export_details = t_food_export_certificate_t1.objects.filter(Application_No=food_export_application)

    food_export_details.update(
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
        Export_Expected_Date=Export_Expected_Date,
        Proposed_Inspection_Date=Proposed_Inspection_Date,
        Purpose_Of_Export=Purpose_Of_Export,
        Consignment_Location_Dzongkhag=Consignment_Location_Dzongkhag,
        Consignment_Location_Gewog=Consignment_Location_Gewog,
        Consignment_Location=Consignment_Location,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Inspection_Remarks=None,
        Export_Permit_No=None,
        Approved_Date=None,
        Validity_Period=None,
        Validity=None,
        Applicant_Id=request.session['email'],
        Importing_Country=Importing_Country,
        Additional_Information=additional_info,
        Rejection_Reason=None,
        Terms=None
    )
    field = t_location_field_office_mapping.objects.filter(Location_Code=Consignment_Location_Gewog)
    for field_office in field:
        field_office_id = field_office.Field_Office_Id_id
        work_details = t_workflow_details.objects.filter(application_no=food_export_application)
        work_details.update(application_no=food_export_application, applicant_id=request.session['email'],
                            assigned_to=None, field_office_id=field_office_id, section='Food',
                            assigned_role_id='4', action_date=None, application_status='P',
                            service_code=service_code)
    data['applNo'] = food_export_application
    return JsonResponse(data)


def food_export_file(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/export_certificate")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/export_certificate" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def food_export_file_name(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
        return render(request, 'export_certificate_food/file_attachment.html', {'file_attach': file_attach})


def delete_export_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/export_certificate")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'export_certificate_food/file_attachment.html', {'file_attach': file_attach})


def load_fec_attachment(request):
    Application_No = request.GET.get('appNo')
    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'export_certificate_food/file_attachment.html', {'file_attach': file_attach})


def submit_food_export_application(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    application_details = t_food_export_certificate_t1.objects.filter(Application_No=application_no)
    application_details.update(Application_Date=date.today())
    workflow_details.update(action_date=date.today())
    return redirect(food_business_registration_licensing)


def food_export_application_no(service_code):
    last_application_no = t_food_export_certificate_t1.objects.aggregate(Max('Application_No'))
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


def approve_food_export(request):
    application_id = request.POST.get('application_id')
    Inspection_Leader = request.POST.get('Inspection_Leader')
    Inspection_Team = request.POST.get('Inspection_Team')
    date_format_ins = request.POST.get('dateOfInspection')
    certified_qty = request.POST.get('certified_qty')
    Unit_Net = request.POST.get('Unit_Certified')
    rejected_qty = request.POST.get('rejected_qty')
    Unit_Rejected = request.POST.get('Unit_Rejected')
    validity = request.POST.get('validity')
    remarks = request.POST.get('remarks')
    rejection_reason = request.POST.get('rejection_reason')
    terms = request.POST.get('terms')
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
    details.update(Rejection_Reason=rejection_reason)
    details.update(Terms=terms)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='A')
    update_payment(application_id, Export_Permit_No, 'FEC', validity_date, 'Final', '131110049')
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
        newAppNo = Field_Code + "-" + "FEC" + "-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "-" + "FEC" + "-" + str(year) + "-" + AppNo
    return newAppNo


def reject_food_export(request):
    application_id = request.POST.get('application_id')
    remarks = request.POST.get('remarks')

    details = t_food_export_certificate_t1.objects.filter(Application_No=application_id)
    details.update(Inspection_Remarks=remarks)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(action_date=date.today())
    application_details.update(application_status='R')
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
              "." + " Please Make Payment Before Validity Expires. Visit The Nearest Bafra Office For Payment" \
                    "or Pay Online at https://tinyurl.com/y3m7wa3c Thank you!"
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_fec_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + "Your Application for Export Certificate for Food Products Has" \
                                " Been Rejected Because" + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


# Licensing of Food Handler
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def food_handler_licensing(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        country = t_country_master.objects.all()
        field_office = t_field_office_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        unit = t_unit_master.objects.filter(Unit_Type='S')
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'food_handler/application_form.html',
                      {'dzongkhag': dzongkhag, 'village': village,
                       'gewog': gewog, 'country': country,
                       'field_office': field_office,
                       'location': location, 'unit': unit, 'count': message_count, 'count_call': inspection_call_count,
                       'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def save_food_handler_details(request):
    data = dict()
    service_code = "FHL"
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
    date_format_ins = request.POST.get('preferred_Date')
    Associated_Food_Establishment = request.POST.get('associated_establishment')
    t_food_licensing_food_handler_t1.objects.create(
        Application_No=application_no,
        Application_Date=None,
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
        Inspection_Remarks=None,
        Attendance=None,
        Training_Venue=None,
        Training_Batch=None,
        App_Status=None
    )
    t_workflow_details.objects.create(application_no=application_no, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=Preferred_Place, section='Food',
                                      assigned_role_id='4', action_date=None, application_status='P',
                                      service_code=service_code)
    data['applNo'] = application_no
    return JsonResponse(data)


def update_food_handler_details(request):
    data = dict()
    service_code = "FHC"
    application_no = request.POST.get('application_no')
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

    food_det = t_food_licensing_food_handler_t1.objects.filter(Application_No=application_no)

    food_det.update(
        Application_Date=None,
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
        Proposed_Inspection_Date=Proposed_Inspection_Date,
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
        Inspection_Remarks=None,
        Attendance=None,
        Training_Venue=None,
        Training_Batch=None,
        App_Status=None
    )
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    workflow_details.update(applicant_id=request.session['email'],
                            assigned_to=None, field_office_id=Preferred_Place, section='Food',
                            assigned_role_id='4', action_date=None, application_status='P',
                            service_code=service_code)
    data['applNo'] = application_no
    return JsonResponse(data)


def food_handler_application_no(service_code):
    last_application_no = t_food_licensing_food_handler_t1.objects.aggregate(Max('Application_No'))
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


def food_handler_file(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_handler_certificate")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/food_handler_certificate" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def food_handler_file_name(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
        return render(request, 'food_handler/file_attachment.html', {'file_attach': file_attach})


def delete_fh_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_handler_certificate")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'food_handler/file_attachment.html', {'file_attach': file_attach})


def load_fh_attachment(request):
    Application_No = request.GET.get('appNo')
    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'food_handler/file_attachment.html', {'file_attach': file_attach})


def submit_food_handler_application(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    workflow_details.update(action_date=date.today())
    details = t_food_licensing_food_handler_t1.objects.filter(Application_No=application_no)
    details.update(Application_Date=date.today())
    return redirect(food_handler_licensing)


def food_handler_forward_application(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')
    remarks = request.POST.get('remarks')
    details = t_food_licensing_food_handler_t1.objects.filter(Application_No=application_id)
    application_details = t_workflow_details.objects.filter(application_no=application_id)
    application_details.update(assigned_to=forwardTo)
    application_details.update(action_date=date.today())
    application_details.update(assigned_role_id='5')
    application_details.update(application_status='A')
    if remarks is not None:
        details.update(OIC_Remarks=remarks)
    else:
        details.update(OIC_Remarks=None)
    for application in details:
        email = application.Email
        send_acknowledgement_mail(email)
    Field_Office_Id = request.session['field_office_id']
    Role_Id = request.session['Role_Id']
    application_Lists = t_workflow_details.objects.filter(assigned_to=Role_Id, field_office_id=Field_Office_Id)
    return redirect(dashboard)


def reject_food_handler_application(request):
    application_id = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    details = t_food_licensing_food_handler_t1.objects.filter(Application_No=application_id)
    work_details = t_workflow_details.objects.filter(application_no=application_id)
    work_details.update(action_date=date.today())
    work_details.update(application_status='R')
    for application in details:
        email = application.Email
        send_reject_mail(remarks, email)
    details.update(OIC_Remarks=remarks)
    return redirect(dashboard)


def send_acknowledge(request):
    application_id = request.GET.get('application_id')
    service_code = request.GET.get('Service_Code')
    work_details = t_workflow_details.objects.filter(application_no=application_id)
    work_details.update(application_status='ACK')
    if service_code == "FBR":
        application_details = t_food_business_registration_licensing_t1.objects.filter(application_no=application_id)
        for app in application_details:
            mail_id = app.email
            send_fbr_acknowledgement_mail(mail_id)
    elif service_code == "OC":
        application_details = t_certification_organic_t1.objects.filter(Application_No=application_id)
        for app in application_details:
            mail_id = app.Email
            send_oc_acknowledgement_mail(mail_id)
    elif service_code == "FPC":
        application_details = t_certification_food_t1.objects.filter(Application_No=application_id)
        for app in application_details:
            mail_id = app.Firm_Email
            send_fpc_acknowledgement_mail(mail_id)
    elif service_code == "GAP":
        application_details = t_certification_gap_t1.objects.filter(Application_No=application_id)
        for app in application_details:
            mail_id = app.Email
            send_gap_acknowledgement_mail(mail_id)
    elif service_code == "CMS":
        application_details = t_livestock_clearance_meat_shop_t1.objects.filter(application_no=application_id)
        for app in application_details:
            mail_id = app.email
            send_cms_acknowledgement_mail(mail_id)
    return redirect(focal_officer_application)


def send_fbr_acknowledgement_mail(Email):
    subject = 'APPLICATION ACKNOWLEDGED'
    message = "Dear Sir/Madam, Your Application for Food Business Registration And Licensing Has Been Accepted. " \
              "You will Be Informed About The Inspection Later."
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_cms_acknowledgement_mail(Email):
    subject = 'APPLICATION ACKNOWLEDGED'
    message = "Dear Sir/Madam, Your Application for Meat ShopLicensing Has Been Accepted. " \
              "You will Be Informed About The Inspection Later."
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_gap_acknowledgement_mail(Email):
    subject = 'APPLICATION ACKNOWLEDGED'
    message = "Dear Sir/Madam, Your Application for GAP Certification Has Been Accepted. " \
              "You will Be Informed About The Inspection Later."
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_fpc_acknowledgement_mail(Email):
    subject = 'APPLICATION ACKNOWLEDGED'
    message = "Dear Sir/Madam, Your Application for Food Product Certification Has Been Accepted. " \
              "You will Be Informed About The Inspection Later."
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_oc_acknowledgement_mail(Email):
    subject = 'APPLICATION ACKNOWLEDGED'
    message = "Dear Sir/Madam, Your Application for Organic Certification Has Been Accepted. " \
              "You will Be Informed About The Inspection Later."
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_acknowledgement_mail(Email):
    subject = 'APPLICATION ACKNOWLEDGED'
    message = "Dear Sir/Madam, Your Application for Food Handler Certificate Has Been Accepted. " \
              "You will Be Informed About The Training Programme Later."
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_reject_mail(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir/Madam" + "Your Application for Food Handler Certificate Has" \
                                      " Been Rejected Because" + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def food_handler_image(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_handlers")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/food_handlers" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def food_handler_image_name(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        batch_no = request.POST.get('batch_No')
        score = request.POST.get('score')
        attendance = request.POST.get('attendance')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         file_path=file_url, role_id=None,
                                         attachment=file_name, attachment_type='FH')

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
        details = t_food_licensing_food_handler_t1.objects.filter(Application_No=app_no, Attachment_Type='FH')
        details.update(Attendance=attendance)
        details.update(Assessment_Score=score)
        app_details = t_food_licensing_food_handler_t1.objects.filter(Training_Batch_No=batch_no)
    return render(request, 'food_handler/result_list.html', {'application_details': app_details,
                                                             'file_attach': file_attach})


def food_handler_image_update(request):
    data = dict()
    myFile = request.FILES['image']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_handlers")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/food_handlers" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def food_handler_image_name_update(request):
    app_no = request.GET.get('Application_No')
    fileName = request.GET.get('filename')
    Applicant_Id = request.session['email']
    file_url = request.GET.get('file_url')
    batch_no = request.GET.get('batch_No')
    score = request.GET.get('score')
    attendance = request.GET.get('attendance')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
    t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                     file_path=file_url, role_id=None, attachment=file_name, attachment_type='FH')
    details = t_food_licensing_food_handler_t1.objects.filter(Application_No=app_no)
    details.update(Attendance=attendance)
    details.update(Assessment_Score=score)
    result_details = t_food_licensing_food_handler_t1.objects.filter(Training_Batch_No=batch_no)
    file_attach = t_file_attachment.objects.filter(attachment_type='FH')
    return render(request, 'food_handler/result_details_edit.html',
                  {'application_details': result_details, 'file_attach': file_attach})


def food_handler_update(request):
    Application_No = request.GET.get('Application_No')
    Applicant_Id = request.session['email']
    batch_no = request.GET.get('batch_No')
    score = request.GET.get('score')
    attendance = request.GET.get('attendance')

    details = t_food_licensing_food_handler_t1.objects.filter(Application_No=Application_No)
    details.update(Attendance=attendance)
    details.update(Assessment_Score=score)
    app_details = t_food_licensing_food_handler_t1.objects.filter(Training_Batch_No=batch_no)
    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'food_handler/result_list.html', {'application_details': details,
                                                             'file_attach': file_attach})


# Common
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def food_handler_application(request):
    service_code = "FHC"
    try:
        Login_Id = request.session['Login_Id']
    except:
        Login_Id = None
    if Login_Id:
        # Application Status A is forwarded from OIC
        application_details = t_workflow_details.objects.filter(assigned_role_id='5', assigned_to=Login_Id,
                                                                application_status='A', service_code=service_code)
        details = t_food_licensing_food_handler_t1.objects.filter(Training_Batch_No__isnull=True)
        message_count = (t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=Login_Id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=Login_Id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        fhc_count = (t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='B',
                                                       action_date__isnull=False, service_code='FHC') |
                     t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='A',
                                                       action_date__isnull=False, service_code='FHC')).count()
        return render(request, 'food_handler_list.html',
                      {'application_details': application_details, 'details': details,
                       'count': message_count, 'count_call': inspection_call_count,
                       'consignment_call_count': consignment_call_count,
                       'fhc_count': fhc_count})
    else:
        return render(request, 'redirect_page.html')


def update_batch_no(request):
    app = request.POST.getlist('checkedVals')
    batchNo = request.POST.get('batch_no')
    from_Date = request.POST.get('from_training_Date')
    to_Date = request.POST.get('to_training_Date')
    remarks = request.POST.get('Remarks')
    Minimum_Score = request.POST.get('min_mark')
    training_batch = request.POST.get('Training_Batch')
    Training_Venue = request.POST.get('Training_Venue')

    strings = app[0].split("#")
    for tempArr in strings:
        checkboxArr = tempArr.split("~")
        email = checkboxArr[0]
        app_no = checkboxArr[1]
        details = t_food_licensing_food_handler_t1.objects.filter(Application_No=app_no)
        details.update(Minimum_Score=Minimum_Score, Training_Batch_No=batchNo, Training_From_Date=from_Date,
                       Training_To_Date=to_Date, Inspection_Remarks=remarks, Training_Venue=Training_Venue,
                       Training_Batch=training_batch)
        work_details = t_workflow_details.objects.filter(application_no=app_no)
        work_details.update(application_status='B')  # Batch No Updated
        send_batch_mail(batchNo, from_Date, to_Date, remarks, email)
    return redirect(food_handler_application)


def send_batch_mail(batchNo, from_training_Date, to_training_Date, remarks, Email):
    subject = 'TRAINING CONFIRMATION'
    message = "Dear " + "Sir/Madam" + "Your Application for Food Handler Certificate Has" \
                                      " Been Accepted. You Are Requested To Attend The Following Training" \
                                      " Training Batch No: " + batchNo + " Training From" + from_training_Date + \
              " To " + to_training_Date + "." + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def result_update_list(request):
    result_details = t_food_licensing_food_handler_t1.objects.filter(Training_Batch_No__isnull=False,
                                                                     App_Status__isnull=True
                                                                     ).distinct('Training_Batch_No')

    return render(request, 'food_handler/food_handler_result_list.html',
                  {'application_details': result_details})


def update_list(request):
    batch_no = request.POST.get('Training_Batch_No')
    result_details = t_food_licensing_food_handler_t1.objects.filter(Training_Batch_No=batch_no,
                                                                     FH_License_No__isnull=True)
    file_attach = t_file_attachment.objects.filter(attachment_type='FH')
    return render(request, 'food_handler/result_list.html',
                  {'application_details': result_details, 'file_attach': file_attach})


def result_update(request):
    app = request.POST.getlist('checkedVals')

    strings = app[0].split("#")
    for tempArr in strings:
        checkboxArr = tempArr.split("~")
        score = checkboxArr[0]
        app_no = checkboxArr[1]
        att = checkboxArr[2]
        details = t_food_licensing_food_handler_t1.objects.filter(Application_No=app_no)
        details.update(Assessment_Score=score)
        details.update(Attendance=att)

        for detail in details:
            min_mark = detail.Minimum_Score
            if int(score) > int(min_mark):
                FH_License_no = generate_fh_license_no(request)
                details.update(FH_License_No=FH_License_no)


def generate_fh_license_no(request):
    last_application_no = t_food_licensing_food_handler_t1.objects.aggregate(Max('FH_License_No'))
    lastAppNo = last_application_no['FH_License_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = "FHC" + "-" + str(year) + "-" + "0001"
    else:
        substring = str(lastAppNo)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = "FHC" + "-" + str(year) + "-" + AppNo
    return newAppNo


# Licensing of Food Handler
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def food_import_application(request):
    try:
        login_id = request.session['Login_Id']
    except:
        login_id = None
    if login_id:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        country = t_country_master.objects.all()
        field_office = t_field_office_master.objects.filter(Is_Entry_Point='Y')
        location = t_location_field_office_mapping.objects.all()
        unit = t_unit_master.objects.all()
        category = t_food_category_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_to=login_id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=login_id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(application_status='FR', assigned_to=login_id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=login_id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        return render(request, 'import_certificate_food/application_form.html',
                      {'dzongkhag': dzongkhag, 'village': village,
                       'gewog': gewog, 'country': country,
                       'field_office': field_office,
                       'location': location, 'unit': unit, 'category': category, 'count': message_count,
                       'count_call': inspection_call_count, 'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


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
    date_format_ins = request.POST.get('expectedArrivalDate')

    if Import_Type == "Individual":
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
            Import_Permit_No=None,
            Applicant_Id=request.session['email'],
            Terms=None
        )
    else:
        t_food_import_permit_t1.objects.create(
            Application_No=application_no,
            Import_Type=Import_Type,
            License_No=license_no,
            CID=None,
            Applicant_Name=Name,
            Dzongkhag_Code=None,
            Gewog_Code=None,
            Village_Code=None,
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
            Import_Permit_No=None,
            Applicant_Id=request.session['email'],
            Terms=None
        )
    t_workflow_details.objects.create(application_no=application_no, applicant_id=request.session['email'],
                                      assigned_to=None, field_office_id=Place_of_Entry, section='Food',
                                      assigned_role_id='2', action_date=None, application_status='P',
                                      service_code=service_code)
    data['applNo'] = application_no
    return JsonResponse(data)


def update_food_import(request):
    data = dict()
    service_code = "FIP"
    application_no = request.POST.get('application_no')
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
    date_format_ins = request.POST.get('expectedArrivalDate')

    if Import_Type == "Individual":
        fip_details = t_food_import_permit_t1.objects.filter(Application_No=application_no)
        fip_details.update(
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
            Import_Permit_No=None,
            Applicant_Id=request.session['email'],
            Terms=None
        )
    else:
        fip_details = t_food_import_permit_t1.objects.filter(Application_No=application_no)
        fip_details.update(
            Application_No=application_no,
            Import_Type=Import_Type,
            License_No=license_no,
            CID=None,
            Applicant_Name=Name,
            Dzongkhag_Code=None,
            Gewog_Code=None,
            Village_Code=None,
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
            Import_Permit_No=None,
            Applicant_Id=request.session['email'],
            Terms=None
        )
    work_details = t_workflow_details.objects.filter(application_no=application_no)
    work_details.update(application_no=application_no, applicant_id=request.session['email'],
                        assigned_to=None, field_office_id=Place_of_Entry, section='Food',
                        assigned_role_id='2', action_date=None, application_status='P',
                        service_code=service_code)
    data['applNo'] = application_no
    food_import_details = t_food_import_permit_t2.objects.filter(Application_No=application_no)
    if food_import_details.exists():
        count = t_food_import_permit_t2.objects.filter(Application_No=application_no).count()
    else:
        count = 0
    data['count'] = count
    return JsonResponse(data)


def generate_food_import_app_no(service_code):
    last_application_no = t_food_import_permit_t1.objects.aggregate(Max('Application_No'))
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


def save_food_import_details(request):
    application_no = request.POST.get('appNo')
    Common_Name = request.POST.get('Common_Name')
    Product_Category = request.POST.get('Product_Category')
    characteristics = request.POST.get('characteristics')
    quantity = request.POST.get('qty')
    unit = request.POST.get('unit')
    exporter_type = request.POST.get('Export_Type')

    t_food_import_permit_t2.objects.create(Application_No=application_no, Common_Name=Common_Name,
                                           Product_Category=Product_Category,
                                           Product_Characteristics=characteristics,
                                           Quantity=quantity, Unit=unit, Exporter_Type=exporter_type,
                                           Quantity_Balance=quantity, Remarks=None)
    import_details = t_food_import_permit_t2.objects.filter(Application_No=application_no)
    count = t_food_import_permit_t2.objects.filter(Application_No=application_no).count()
    return render(request, 'import_certificate_food/food_permit_details.html',
                  {'import': import_details, 'count': count})


def load_fip_details(request):
    application_no = request.GET.get('appNo')
    import_details = t_food_import_permit_t2.objects.filter(Application_No=application_no)
    count = t_food_import_permit_t2.objects.filter(Application_No=application_no).count()
    return render(request, 'import_certificate_food/food_permit_details.html', {'import': import_details,
                                                                                'count': count})


def load_fip_attachment(request):
    application_no = request.GET.get('appNo')
    file_attach = t_file_attachment.objects.filter(application_no=application_no)
    return render(request, 'import_certificate_food/file_attachment.html', {'file_attach': file_attach})


def food_import_file(request):
    data = dict()
    myFile = request.FILES['document']
    app_no = request.POST.get('appNo')
    file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + myFile.name
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/import_permit")
    if fs.exists(file_name):
        data['form_is_valid'] = False
    else:
        fs.save(file_name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/food/import_permit" + "/" + file_name
        data['form_is_valid'] = True
        data['file_url'] = file_url
        data['file_name'] = file_name
    return JsonResponse(data)


def food_import_file_name(request):
    if request.method == 'POST':
        app_no = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')
        file_name = str(app_no)[0:3] + "_" + str(app_no)[4:8] + "_" + str(app_no)[9:13] + "_" + fileName
        t_file_attachment.objects.create(application_no=app_no, applicant_id=Applicant_Id,
                                         role_id=None, file_path=file_url,
                                         attachment=file_name)

        file_attach = t_file_attachment.objects.filter(application_no=app_no)
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

    file_attach = t_file_attachment.objects.filter(application_no=Application_No)
    return render(request, 'import_certificate_food/file_attachment.html', {'file_attach': file_attach})


def submit_food_import(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    application_details = t_food_import_permit_t1.objects.filter(Application_No=application_no)
    application_details.update(Application_Date=date.today())
    workflow_details.update(action_date=date.today())
    return redirect(food_import_application)


def approve_fo_fip_import(request):
    service_code = "FIP"
    permit_no = get_fip_permit_no(service_code)
    application_no = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    validity = request.POST.get('validity')
    terms = request.POST.get('terms')
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    for app in workflow_details:
        client_login_id = app.applicant_id
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
    details.update(Approve_Date=date.today())
    details.update(Validity_Period=validity)
    details.update(Import_Permit_No=permit_no)
    details.update(Terms=terms)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    for ap_details in details:
        import_type = ap_details.Import_Type
        if import_type == 'P':
            update_payment(application_no, permit_no, 'FIP', validity_date, 'Final', 'account_head_name')
        else:
            update_payment(application_no, permit_no, 'FIP', validity_date, 'Final', '131110011')
    for email_id in details:
        email = email_id.Email
        send_fip_approve_email(permit_no, email, validity_date)
    return render(request, 'focal_officer_pending_list.html')


def reject_fo_fip_import(request):
    application_no = request.GET.get('application_id')
    remarks = request.POST.get('remarks')
    workflow_details = t_workflow_details.objects.filter(application_no=application_no)
    workflow_details.update(action_date=date.today())
    workflow_details.update(application_status='R')
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
              " Please Make Payment Before Validity Expires. Visit The Nearest Bafra Office For Payment" \
              "or Pay Online at https://tinyurl.com/y3m7wa3c Thank you!"
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def send_fip_reject_email(Email, remarks):
    subject = 'APPLICATION REJECTED'
    message = "Dear Sir," \
              "" \
              "Your Application for Import Permit for Food Products Has Been Rejected." \
              " Reason: " + remarks + ""
    recipient_list = [Email]
    send_mail(subject, message, 'bafrabbfss@moaf.gov.bt', recipient_list, fail_silently=False,
              auth_user='systems@moaf.gov.bt', auth_password='hchqbgeeqvawkceg',
              connection=None, html_message=None)


def get_fip_permit_no(service_code):
    last_import_permit_no = t_food_import_permit_t1.objects.aggregate(Max('Import_Permit_No'))
    last_permit_no = last_import_permit_no['Import_Permit_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = service_code + "-" + str(year) + "-" + "0001"
    else:
        substring = str(last_permit_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = service_code + "-" + str(year) + "-" + AppNo
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
            if balance == 0:
                import_details = t_food_import_permit_inspection_t1.objects.filter(
                    Application_No=import_det.Application_No)
                for import_det in import_details:
                    la_details = t_food_import_permit_t1.objects.filter(
                        Import_Permit_No=import_det.Import_Permit_No)
                    for la in la_details:
                        work_details = t_workflow_details.objects.filter(application_no=la.Application_No)
                        work_details.update(application_status='C')
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
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    date_format_ins = request.GET.get('dateOfInspection')
    clearnace_ref_no = fip_clearance_no(request)

    update_details = t_food_import_permit_inspection_t1.objects.filter(Application_No=application_no)
    update_details.update(Clearance_Ref_No=clearnace_ref_no)
    update_details.update(Inspection_Leader=Inspection_Leader)
    update_details.update(Inspection_Team=Inspection_Team)
    update_details.update(Inspection_Date=date_format_ins)
    update_details.update(Approve_Date=date.today())
    if remarks is not None:
        update_details.update(Inspection_Remarks=remarks)
    else:
        update_details.update(Inspection_Remarks=None)
    application_details = t_workflow_details.objects.filter(application_no=application_no)
    application_details.update(action_date=date.today())
    application_details.update(application_status='C')
    return redirect(inspector_application)


def update_import_details_food(request):
    application_no = request.POST.get('applicationNo')
    record_id = request.POST.get('import_record_id')
    approved_quantity = request.POST.get('qty_approved')
    qty_balance = request.POST.get('qty_balance')
    remarks = request.POST.get('import_remarks')
    print(application_no)

    import_det = t_food_import_permit_inspection_t2.objects.filter(pk=record_id)
    if remarks is not None:
        import_det.update(Remarks=remarks)
    else:
        import_det.update(Remarks=None)
    import_det.update(Quantity_Released=approved_quantity)
    import_det.update(Quantity_Balance=qty_balance)
    for import_IPP in import_det:
        Product_Record_Id = import_IPP.Product_Record_Id
        balance = int(import_IPP.Quantity_Balance) - int(import_IPP.Quantity_Released)
        product_details = t_food_import_permit_t2.objects.filter(pk=Product_Record_Id)
        product_details.update(Quantity_Balance=balance)
        if balance == 0:
            import_details = t_food_import_permit_inspection_t1.objects.filter(
                Application_No=application_no)
            for import_det in import_details:
                la_details = t_food_import_permit_t1.objects.filter(
                    Import_Permit_No=import_det.Import_Permit_No)
                for la in la_details:
                    work_details = t_workflow_details.objects.filter(application_no=la.Application_No)
                    work_details.update(application_status='C')
        else:
            import_details = t_food_import_permit_inspection_t1.objects.filter(
                Application_No=application_no)
            for import_det in import_details:
                la_details = t_food_import_permit_t1.objects.filter(
                    Import_Permit_No=import_det.Import_Permit_No)
                for la in la_details:
                    work_details = t_workflow_details.objects.filter(application_no=la.Application_No)
                    work_details.update(application_status='P')
    application_details = t_food_import_permit_inspection_t2.objects.filter(Application_No=application_no)
    return render(request, 'import_certificate_food/import_details.html', {'import': application_details})


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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def factory_inspection_list(request):
    try:
        Login_Id = request.session['Login_Id']
    except:
        Login_Id = None
    if Login_Id:
        new_import_app = t_workflow_details.objects.filter(application_status='FR', assigned_to=Login_Id,
                                                           action_date__isnull=False)
        service_details = t_service_master.objects.all()
        message_count = (t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='RS')
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='IRS')
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='ATR')
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='APR')
                         | t_workflow_details.objects.filter(assigned_to=Login_Id, application_status='NCR')).count()

        inspection_call_count = t_workflow_details.objects.filter(Application_Status='FR', assigned_to=Login_Id,
                                                                  action_date__isnull=False).count()
        consignment_call_count = t_workflow_details.objects.filter(assigned_to=Login_Id,
                                                                   action_date__isnull=False, application_status='P') \
            .count()
        payment_details = t_payment_details.objects.all()
        return render(request, 'factory_inspection_list.html',
                      {'service_details': service_details, 'application_details': new_import_app,
                       'count': message_count,
                       'count_call': inspection_call_count, 'payment_details': payment_details,
                       'consignment_call_count': consignment_call_count})
    else:
        return render(request, 'redirect_page.html')


def update_payment(application_no, permit_no, service_code, validity_date, Permit_Type, account_head_code):
    account_details = t_payment_details_master.objects.filter(account_head_code=account_head_code)
    for pay_details in account_details:
        fees = pay_details.service_fee
        service_name = pay_details.service_name
        t_payment_details.objects.create(application_no=application_no,
                                         application_date=date.today(),
                                         permit_no=permit_no,
                                         service_id=service_code,
                                         validity=validity_date,
                                         payment_type=None,
                                         instrument_no=None,
                                         amount=fees,
                                         receipt_no=None,
                                         receipt_date=None,
                                         updated_by=None,
                                         updated_on=None,
                                         permit_type=Permit_Type,
                                         account_head_code=account_head_code)
        cl = Client('https://www.citizenservices.gov.bt/G2CPaymentAggregator/services/G2CPaymentInitiatorBusiness?wsdl')
        order_type = cl.get_type('ns1:PaymentDTO')
        paymentList = order_type(accountHeadId=account_head_code, serviceFee=fees)
        post_data = {'agencyCode': "BAFRA", 'applicationNo': application_no,
                     'serviceName': service_name,
                     'paymentList': paymentList}
        cl.service.insertPaymentDetailsOnApproval(post_data)


def food_handler_application_details(request):
    app_id = request.GET.get('application_id')
    application_details = t_food_licensing_food_handler_t1.objects.filter(Application_No=app_id)
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    field_office = t_field_office_master.objects.all()
    country = t_country_master.objects.all()
    return render(request, 'food_handler/food_handler_application_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village, 'field_office': field_office, 'country': country})


def get_food_handler_details(request):
    app_id = request.GET.get('application_id')
    application_details = t_food_licensing_food_handler_t1.objects.filter(Application_No=app_id)
    attachment = t_file_attachment.objects.filter(application_no=app_id, attachment_type='FH')
    count = t_file_attachment.objects.filter(application_no=app_id, attachment_type='FH').count()
    return render(request, 'food_handler/edit_food_handler_details.html',
                  {'application_details': application_details, 'attachment': attachment, 'count': count})


def delete_food_handler_photo(request):
    data = dict()
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo')

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_handlers")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(application_no=Application_No, attachment_type='FH').count()
    data['Count'] = file_attach
    return JsonResponse(data)


def food_handler(request):
    Application_No = request.GET.get('Application_No')
    attendance = request.GET.get('attendance')
    file = t_file_attachment.objects.filter(application_no=Application_No)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food/food_handlers")
        fs.delete(str(fileName))
    file.delete()
    details = t_food_licensing_food_handler_t1.objects.filter(Application_No=Application_No)
    details.update(Assessment_Score=None)
    details.update(Attendance=attendance)
    file_attach = t_file_attachment.objects.filter(application_no=Application_No, attachment_type='FH')
    application_details = t_food_licensing_food_handler_t1.objects.filter(Application_No=Application_No)
    return render(request, 'food_handler/result_list.html', {'application_details': application_details,
                                                             'file_attach': file_attach})


def update_food_handler_status(request):
    Application_No = request.GET.get('batch')
    d = timedelta(days=int(730))
    validity_date = date.today() + d
    details = t_food_licensing_food_handler_t1.objects.filter(Training_Batch_No=Application_No)
    details.update(App_Status='Yes')
    details.update(Approved_Date=date.today())
    details_fh = t_food_licensing_food_handler_t1.objects.filter(Assessment_Score__gt=F('Minimum_Score'))
    for app_details in details_fh:
        app_no = app_details.Application_No
        food_handler_license_no = fh_license_no()
        update_details = t_food_licensing_food_handler_t1.objects.filter(Application_No=app_no)
        update_details.update(FH_License_No=food_handler_license_no)
        update_details.update(FH_License_Validity_Period=int(730))
        update_details.update(FH_License_Validity=validity_date)
        update_details.update(Approved_Date=date.today())
        update_payment(app_no, food_handler_license_no, 'FHL', validity_date, 'Final', '131110021')
        details = t_workflow_details.objects.filter(application_no=app_no)
        details.update(application_status='FHC')  # food handler license complete
    return redirect(update_list)


def fh_license_no():
    last_clearance_ref_no = t_food_licensing_food_handler_t1.objects.aggregate(Max('FH_License_No'))
    last_permit_no = last_clearance_ref_no['FH_License_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = "FH" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_permit_no)[10:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = "FH" + "/" + str(year) + "/" + AppNo
    return newPermitNo
