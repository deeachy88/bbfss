from django.core.mail import send_mail
from django.db.models import Max
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime, timedelta
# Organic Certificate.
from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_country_master, \
    t_field_office_master, t_location_field_office_mapping, t_unit_master, t_user_master, t_service_master
from bbfss import settings
from certification.forms import GapForm, FpcForm
from certification.models import t_certification_food_t2, t_certification_organic_t2, t_certification_organic_t4, \
    t_certification_organic_t6, t_certification_organic_t7, t_certification_organic_t8, t_certification_organic_t5, \
    t_certification_organic_t9, t_certification_organic_t1, t_certification_gap_t5, t_certification_gap_t4, \
    t_certification_organic_t3, t_certification_gap_t1, t_certification_food_t4, t_certification_organic_t11, \
    t_certification_food_t1, t_certification_gap_t3, t_certification_food_t3, t_certification_organic_t10, \
    t_certification_food_t5, t_certification_gap_t2, t_certification_gap_t7, t_certification_gap_t8
from plant.models import t_file_attachment, t_workflow_details, t_payment_details
import pandas as pd
# Organic Certification
from plant.views import focal_officer_application, inspector_application


def organic_certificate(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    country = t_country_master.objects.all()
    field_office = t_field_office_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'organic_certification/apply_organic_certification.html',
                  {'dzongkhag': dzongkhag, 'village': village,
                   'gewog': gewog, 'country': country,
                   'field_office': field_office,
                   'location': location, 'unit': unit})


def save_organic_certificate(request):
    data = dict()
    service_code = "OC"
    organic_certificate_app_no = get_organic_certificate_app_no(request, service_code)
    Applicant_Type = request.POST.get('Applicant_Type')
    print(Applicant_Type)
    if Applicant_Type == 'I':
        cid = request.POST.get('cid')
        Name = request.POST.get('Name')
        Farmer_Group_No = None
        Farmer_Group_name = None
    else:
        cid = None
        Name = None
        Farmer_Group_No = request.POST.get('farmers_group_name')
        Farmer_Group_name = request.POST.get('farmers_group_number')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    address = request.POST.get('address')
    farm_location = request.POST.get('farm_location')
    inspectionDate = request.POST.get('inspectionDate')
    farm_name = request.POST.get('farm_name')
    business_license_no = request.POST.get('business_license_no')
    technical_in_charge = request.POST.get('technical_in_charge')
    management_in_charge = request.POST.get('management_in_charge')
    t_certification_organic_t1.objects.create(
        Application_No=organic_certificate_app_no,
        Application_Date=None,
        Application_Type=Applicant_Type,
        CID=cid,
        Applicant_Name=Name,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Present_Address=address,
        Contact_No=contact_number,
        Email=email,
        Farmer_Group_No=Farmer_Group_No,
        Farmer_Group_Name=Farmer_Group_name,
        Crop_Production=None,
        Wild_Collection=None,
        Animal_Husbandry=None,
        Aquaculture=None,
        Apiculture=None,
        Processing_Unit=None,
        Proposed_Standard=None,
        Terms_Bafra_Certification=None,
        Terms_Change_Willingness=None,
        Terms_Abide=None,
        Terms_Agreement=None,
        FO_Remarks=None,
        Acknowledge=None,
        Audit_Team_Leader=None,
        Audit_Team_Acceptance=None,
        Audit_Team_Acceptance_Remarks=None,
        Audit_Plan_Date=None,
        Audit_Plan_Criteria=None,
        Audit_Plan_Type=None,
        Audit_Plan_Scope=None,
        Audit_Plan_Acceptance=None,
        Audit_Plan_Acceptance_Remarks=None,
        Audit_Date=None,
        Audit_Findings_Site_History_OE=None,
        Audit_Findings_Water_Source_OE=None,
        Audit_Findings_Product_Quality_OE=None,
        Audit_Findings_Harvesting_OE=None,
        Audit_Findings_Equipment_OE=None,
        Audit_Findings_Manufacturing_Production_OE=None,
        Audit_Findings_Sampling_Testing_OE=None,
        Audit_Findings_Packing_Marking_OE=None,
        Audit_Findings_Storage_Transport_OE=None,
        Audit_Findings_Traceability_OE=None,
        Audit_Findings_Worker_Health_OE=None,
        Audit_Findings_Group_Requirement_OE=None,
        Audit_Findings_Others_OE=None,
        Audit_Findings_Site_History_Observations=None,
        Audit_Findings_Water_Source_Observations=None,
        Audit_Findings_Product_Quality_Observations=None,
        Audit_Findings_Harvesting_Observations=None,
        Audit_Findings_Equipment_Observations=None,
        Audit_Findings_Manufacturing_Production_Observations=None,
        Audit_Findings_Sampling_Testing_Observations=None,
        Audit_Findings_Packing_Marking_Observations=None,
        Audit_Findings_Storage_Transport_Observations=None,
        Audit_Findings_Traceability_Observations=None,
        Audit_Findings_Worker_Health_Observations=None,
        Audit_Findings_Group_Requirement_Observations=None,
        Audit_Findings_Others_Observations=None,
        Approve_Date=None,
        Certificate_No=None,
        Validity_Period=None,
        Validity=None,
        Farm_Location=farm_location,
        Applicant_Id=request.session['email'],
        Farm_Name=farm_name,
        Audit_Type=None,
        Others_Standards=None,
        Terms_Standards=None,
        License_Number=business_license_no,
        Technical_In_Charge=technical_in_charge,
        Manager_In_Charge=management_in_charge
    )

    t_workflow_details.objects.create(Application_No=organic_certificate_app_no,
                                      Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Certification',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['Applicant_Type'] = Applicant_Type
    data['applNo'] = organic_certificate_app_no
    return JsonResponse(data)


def get_organic_certificate_app_no(request, service_code):
    last_application_no = t_certification_organic_t1.objects.aggregate(Max('Application_No'))
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


def organic_certificate_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/certification/organic_certificate")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/certification/organic_certificate" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def organic_certificate_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'GAP_Certification/file_attachment.html', {'file_attach': file_attach})


def save_farmers_group_details(request):
    application_no = request.POST.get('farmers_group_application_no')
    cid = request.POST.get('farmers_group_cid')
    name = request.POST.get('farmers_group_fullname')
    farmers_group_details = t_certification_organic_t2.objects.filter(Application_No=application_no, CID=cid, Name=name)
    return render(request, 'organic_certification/farmers_group_details.html',
                  {'farmers_group_details': farmers_group_details})


def save_crop_production_details(request):
    application_no = request.POST.get('crop_production_app_no')
    crop_name = request.POST.get('crop_name')
    area = request.POST.get('area')
    area_unit = request.POST.get('area_unit')
    prev_year = request.POST.get('prev_year')
    to_year = request.POST.get('to_year')
    yields = request.POST.get('yield')
    Yield_Unit = request.POST.get('Yield_Unit')
    harvest_month = request.POST.get('harvest_month')
    sold = request.POST.get('sold')
    balance_stock = request.POST.get('balance_stock')
    current_year = request.POST.get('current_year')
    to_current_year = request.POST.get('to_current_year')
    estimated_yield = request.POST.get('estimated_yield')
    estimated_Yield_Unit = request.POST.get('estimated_Yield_Unit')
    estimated_harvest_month = request.POST.get('estimated_harvest_month')

    p_from = datetime.strptime(prev_year, '%d-%m-%Y').date()
    p_to = datetime.strptime(to_year, '%d-%m-%Y').date()
    c_from = datetime.strptime(current_year, '%d-%m-%Y').date()
    c_to = datetime.strptime(to_current_year, '%d-%m-%Y').date()

    t_certification_organic_t4.objects.create(
        Application_No=application_no,
        Crop_Name=crop_name,
        Area_Cultivated=area,
        Unit=area_unit,
        P_From_Date=p_from,
        P_To_Date=p_to,
        P_Yield=yields,
        P_Yield_Unit=Yield_Unit,
        P_Harvest_Month=harvest_month,
        P_Sold=sold,
        P_Balance_Stock=balance_stock,
        C_From_Date=c_from,
        C_To_Date=c_to,
        C_Estimated_Yield=estimated_yield,
        C_Yield_Unit=estimated_Yield_Unit,
        C_Harvest_Month=estimated_harvest_month)
    crop_details = t_certification_organic_t4.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/crop_production_details.html',
                  {'crop_details': crop_details})


def save_wild_collection_details(request):
    application_no = request.POST.get('wild_collection_app_no')
    common_name = request.POST.get('common_name')
    botanical_name = request.POST.get('botanical_name')
    part_of_plant = request.POST.get('part_of_plant')
    estimated_harvest = request.POST.get('estimated_harvest')
    estimated_harvest_Yield_Unit = request.POST.get('estimated_harvest_Yield_Unit')
    harvest_season = request.POST.get('harvest_season')
    harvest_acreage = request.POST.get('harvest_acreage')
    harvest_Unit = request.POST.get('harvest_Unit')

    t_certification_organic_t6.objects.create(
        Application_No=application_no,
        Common_Name=common_name,
        Botanical_Name=botanical_name,
        Plant_Part=part_of_plant,
        Estimated_Harvest=estimated_harvest,
        Harvest_Unit=estimated_harvest_Yield_Unit,
        Harvest_Season=harvest_season,
        Harvest_Acreage=harvest_acreage,
        Acreage_Unit=harvest_Unit)
    wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/wild_collection_details.html',
                  {'wild_collection': wild_collection})


def save_animal_husbandry_details(request):
    application_no = request.POST.get('animal_husbandry_application_no')
    livestock_type = request.POST.get('livestock_type')
    male = request.POST.get('male')
    female = request.POST.get('female')
    estimated_production = request.POST.get('estimated_production')
    estimated_production_Unit = request.POST.get('estimated_production_Unit')
    product_sold = request.POST.get('product_sold')

    t_certification_organic_t7.objects.create(
        Application_No=application_no,
        Livestock_Type=livestock_type,
        Male_no=male,
        Female_no=female,
        Estimated_Production=estimated_production,
        Production_Unit=estimated_production_Unit,
        Production_Sold=product_sold)
    animal_husbandry = t_certification_organic_t7.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/animal_husbandry_details.html',
                  {'animal_husbandry': animal_husbandry})


def save_aquaculture_details(request):
    application_no = request.POST.get('aquaculture_application_no')
    Aquaculture_type = request.POST.get('Aquaculture_type')
    Aquaculture_Yield = request.POST.get('Aquaculture_Yield')
    Aquaculture_Yield_Unit = request.POST.get('Aquaculture_Yield_Unit')
    aqua_harvest_month = request.POST.get('aqua_harvest_month')
    aqua_Sold = request.POST.get('aqua_Sold')
    aqua_Sold_unit = request.POST.get('aqua_Sold')
    stock_balance = request.POST.get('stock_balance')
    stock_balance_unit = request.POST.get('stock_balance')

    t_certification_organic_t8.objects.create(
        Application_No=application_no,
        Aquaculture_Type=Aquaculture_type,
        Estimated_Yield=Aquaculture_Yield,
        Estimated_Yield_Unit=Aquaculture_Yield_Unit,
        Harvest_Month=aqua_harvest_month,
        Sold=aqua_Sold,
        Sold_Unit=aqua_Sold_unit,
        Balance_Stock=stock_balance,
        Balance_Stock_Unit=stock_balance_unit)
    aquaculture_details = t_certification_organic_t8.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/aquaculture_details.html',
                  {'aquaculture_details': aquaculture_details})


def save_api_culture_details(request):
    application_no = request.POST.get('api_culture_application_no')
    api_common_name = request.POST.get('api_common_name')
    api_botanical_name = request.POST.get('api_botanical_name')
    api_estimated_harvest = request.POST.get('api_estimated_harvest')
    api_estimated_harvest_Yield_Unit = request.POST.get('api_estimated_harvest_Yield_Unit')
    api_harvest_acreage = request.POST.get('api_harvest_acreage')
    api_Unit = request.POST.get('api_Unit')

    t_certification_organic_t9.objects.create(
        Application_No=application_no,
        Common_Name=api_common_name,
        Botanical_Name=api_botanical_name,
        Estimated_Harvest=api_estimated_harvest,
        Harvest_Unit=api_estimated_harvest_Yield_Unit,
        Harvest_Acreage=api_harvest_acreage,
        Acreage_Unit=api_Unit)
    apiculture_details = t_certification_organic_t9.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/api_culture_details.html',
                  {'apiculture_details': apiculture_details})


def save_processing_unit_details(request):
    application_no = request.POST.get('processing_application_no')
    processing_name = request.POST.get('processing_name')
    address_of_Operation = request.POST.get('address_of_Operation')
    processing_type = request.POST.get('processing_type')
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    production = request.POST.get('production')
    production_unit = request.POST.get('production_unit')
    processing_Sold = request.POST.get('processing_Sold')
    processing_balance = request.POST.get('processing_balance')
    current_from_date = request.POST.get('current_from_date')
    current_to_date = request.POST.get('current_to_date')
    current_production = request.POST.get('current_production')
    current_production_unit = request.POST.get('current_production_unit')
    current_processing_Sold = request.POST.get('current_processing_Sold')
    current_processing_balance = request.POST.get('current_processing_balance')

    p_from = datetime.strptime(from_date, '%d-%m-%Y').date()
    p_to = datetime.strptime(to_date, '%d-%m-%Y').date()
    c_from = datetime.strptime(current_from_date, '%d-%m-%Y').date()
    c_to = datetime.strptime(current_to_date, '%d-%m-%Y').date()

    t_certification_organic_t5.objects.create(
        Application_No=application_no,
        Production_House_Name=processing_name,
        Production_House_Address=address_of_Operation,
        Processing_Type=processing_type,
        P_From_Date=p_from,
        P_To_Date=p_to,
        P_Production=production,
        P_Production_Unit=production_unit,
        P_Sold=processing_Sold,
        P_Balance_Stock=processing_balance,
        C_From_Date=c_from,
        C_To_Date=c_to,
        C_Production=current_production,
        C_Production_Unit=current_production_unit,
        C_Sold=current_processing_Sold,
        C_Balance_Stock=current_processing_balance)
    processing_details = t_certification_organic_t5.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/processing_unit_details.html',
                  {'processing_details': processing_details})


def submit_organic_certificate(request):
    application_no = request.POST.get('application_no')
    Terms_Bafra_Certification = request.POST.get('Terms_Bafra_Certification')
    Terms_Change_Willingness = request.POST.get('Terms_Change_Willingness')
    Terms_Abide = request.POST.get('Terms_Abide')
    Terms_Agreement = request.POST.get('Terms_Agreement')
    Standards = request.POST.get('Standards')
    Others_Standards = request.POST.get('other_standard')
    app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    app_details.update(Terms_Bafra_Certification=Terms_Bafra_Certification)
    app_details.update(Terms_Change_Willingness=Terms_Change_Willingness)
    app_details.update(Terms_Abide=Terms_Abide)
    app_details.update(Terms_Agreement=Terms_Agreement)
    app_details.update(Terms_Standards=Standards)
    if Others_Standards is not None:
        app_details.update(Others_Standards=Others_Standards)
    else:
        app_details.update(Others_Standards=None)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(organic_certificate)


def add_audit_team_details(request):
    application_no = request.GET.get('application_id')
    audit_team_member = request.GET.get('name')
    role = request.GET.get('role')
    details = t_user_master.objects.filter(Login_Id=audit_team_member)
    for name in details:
        app_name = name.Name
        t_certification_organic_t3.objects.create(Application_No=application_no, Login_Id=audit_team_member,
                                                  Name=app_name, Role=role)
    audit_team = t_certification_organic_t3.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/audit_team_details.html',
                  {'audit_team': audit_team})


def send_acknowledge(request):
    application_no = request.POST.get('application_no')
    service_id = request.POST.get('service_id')
    if service_id == 'OC':
        app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
        app_details.update(Acknowledge='Y')
        workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
        for email_id in workflow_details:
            email = email_id.Applicant_Id
            send_acknowledge_email(email)
    elif service_id == 'FPC':
        app_details = t_certification_food_t1.objects.filter(Application_No=application_no)
        app_details.update(Acknowledge='Y')
        workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
        for email_id in workflow_details:
            email = email_id.Applicant_Id
            send_acknowledge_email(email)
    else:
        app_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
        app_details.update(Acknowledge='Y')
        workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
        for email_id in workflow_details:
            email = email_id.Applicant_Id
            send_acknowledge_email(email)
    return redirect(organic_certificate)


def send_acknowledge_email(Email):
    subject = 'APPLICATION ACCEPTED'
    message = "Dear Sir, Your Application for Organic Certificate Has Been Accepted. You Can Check Your Application " \
              "Status By Loggin Into BBFSS"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


# audit_team_acceptance
def send_for_acceptance(request):
    application_no = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    audit_team_leader = request.GET.get('audit_team_leader')
    app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    app_details.update(Audit_Team_Leader=audit_team_leader)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='ATR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(focal_officer_application)


def accept_reject_audit_team(request):
    application_no = request.POST.get('application_id')
    acceptance = request.POST.get('acceptance')
    remarks = request.POST.get('remarks')
    app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    app_details.update(Audit_Team_Acceptance=acceptance)
    app_details.update(Audit_Team_Acceptance_Remarks=remarks)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id='2')
    workflow_details.update(Action_Date=date.today())


def forward_application_team_leader(request):
    application_no = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    team_leader = request.GET.get('audit_team_leader')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Application_Status='AP')
    workflow_details.update(Assigned_Role_Id=None)
    app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    workflow_details.update(Assigned_To=team_leader)
    return redirect(focal_officer_application)


def approve_application(request):
    application_no = request.POST.get('application_no')
    remarks = request.POST.get('remarks')
    app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id='2')
    workflow_details.update(Application_Status='FP')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    return render(request, 'inspector_pending_list.html', {'application_details': workflow_details})


def resubmit_application(request):
    application_no = request.GET.get('application_no')
    Corrective_Action_Proposed_Auditee = request.GET.get('Corrective_Action_Proposed_Auditee')
    Corrective_Action_Taken_Auditee = request.GET.get('Corrective_Action_Taken_Auditee')
    Corrective_Action_Date = request.GET.get('Corrective_Action_Date')
    details = t_certification_organic_t11.objects.filter(Application_No=application_no)
    details.update(Corrective_Action_Proposed_Auditee=Corrective_Action_Proposed_Auditee)
    details.update(Corrective_Action_Taken_Auditee=Corrective_Action_Taken_Auditee)
    details.update(Corrective_Action_Date=Corrective_Action_Date)
    work_flow = t_workflow_details.objects.filter(Application_No=application_no)
    work_flow.update(Action_Date=date.today())
    work_flow.update(Application_Status='AP')
    return redirect(resubmit_application)


def approve_leader_application(request):
    application_no = request.GET.get('application_no')
    remarks = request.GET.get('remarks')
    Audit_Findings_Site_History = request.GET.get('Audit_Findings_Site_History')
    Audit_Findings_Water_Source = request.GET.get('Audit_Findings_Water_Source')
    Audit_Findings_Product_Quality = request.GET.get('Audit_Findings_Product_Quality')
    Audit_Findings_Harvesting = request.GET.get('Audit_Findings_Harvesting')
    Audit_Findings_Equipment = request.GET.get('Audit_Findings_Equipment')
    Audit_Findings_Manufacturing_Production = request.GET.get('Audit_Findings_Manufacturing_Production')
    Audit_Findings_Sampling_Testing = request.GET.get('Audit_Findings_Sampling_Testing')
    Audit_Findings_Packing_Marking = request.GET.get('Audit_Findings_Packing_Marking')
    Audit_Findings_Storage_Transport = request.GET.get('Audit_Findings_Storage_Transport')
    Audit_Findings_Traceability = request.GET.get('Audit_Findings_Traceability')
    Audit_Findings_Worker_Health = request.GET.get('Audit_Findings_Worker_Health')
    Audit_Findings_Group_Requirement = request.GET.get('Audit_Findings_Group_Requirement')
    Audit_Findings_Others = request.GET.get('Audit_Findings_Others')
    Audit_Type = request.GET.get('Audit_Type')
    Audit_Date = request.GET.get('audit_date')
    app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    app_details.update(Audit_Findings_Site_History=Audit_Findings_Site_History)
    app_details.update(Audit_Findings_Water_Source=Audit_Findings_Water_Source)
    app_details.update(Audit_Findings_Product_Quality=Audit_Findings_Product_Quality)
    app_details.update(Audit_Findings_Harvesting=Audit_Findings_Harvesting)
    app_details.update(Audit_Findings_Equipment=Audit_Findings_Equipment)
    app_details.update(Audit_Findings_Manufacturing_Production=Audit_Findings_Manufacturing_Production)
    app_details.update(Audit_Findings_Sampling_Testing=Audit_Findings_Sampling_Testing)
    app_details.update(Audit_Findings_Packing_Marking=Audit_Findings_Packing_Marking)
    app_details.update(Audit_Findings_Storage_Transport=Audit_Findings_Storage_Transport)
    app_details.update(Audit_Findings_Traceability=Audit_Findings_Traceability)
    app_details.update(Audit_Findings_Worker_Health=Audit_Findings_Worker_Health)
    app_details.update(Audit_Findings_Group_Requirement=Audit_Findings_Group_Requirement)
    app_details.update(Audit_Findings_Others=Audit_Findings_Others)
    app_details.update(Audit_Type=Audit_Type)
    app_details.update(Audit_Date=Audit_Date)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='AA')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assign_To=login)
    return redirect(focal_officer_application)


# audit_plan_acceptance
def send_audit_plan_acceptance(request):
    application_no = request.GET.get('application_no')

    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='AA')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assign_To=login)


def send_audit_plan_resubmit(request):
    application_no = request.GET.get('audit_application_no')

    Audit_Type = request.GET.get('Audit_Type')
    Audit_Date = request.GET.get('Audit_Date')
    app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    app_details.update(Audit_Type=Audit_Type)
    app_details.update(Audit_Date=Audit_Date)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='APR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(inspector_application)


def farm_input_observation(request):
    application_no = request.GET.get('application_no')
    Audit_Findings_Farm_Inputs = request.GET.get('Audit_Findings_Farm_Inputs')
    Audit_Findings_Farm_Supplier = request.GET.get('Audit_Findings_Farm_Supplier')
    Audit_Findings_Farm_Invoice = request.GET.get('Audit_Findings_Farm_Invoice')
    t_certification_organic_t10.objects.create(Application_No=application_no,
                                               Audit_Findings_Farm_Inputs=Audit_Findings_Farm_Inputs,
                                               Audit_Findings_Farm_Supplier=Audit_Findings_Farm_Supplier,
                                               Audit_Findings_Farm_Invoice=Audit_Findings_Farm_Invoice)
    details = t_certification_organic_t10.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/farm_input_details.html', {'farm_inputs': details})


def conform_observation(request):
    application_no = request.GET.get('appl_nos')
    Clause_Number = request.GET.get('Clause_Number')
    Non_Conformity = request.GET.get('Non_Conformity')
    Non_Conformity_Category = request.GET.get('Non_Conformity_Category')
    Non_Conformity_Description = request.GET.get('Non_Conformity_Description')
    t_certification_organic_t11.objects.create(
        Application_No=application_no,
        Clause_Number=Clause_Number,
        Non_Conformity=Non_Conformity,
        Non_Conformity_Category=Non_Conformity_Category,
        Non_Conformity_Description=Non_Conformity_Description,
        Corrective_Action_Proposed_Auditee=None,
        Corrective_Action_Taken_Auditee=None,
        Corrective_Action_Date=None,
        Corrective_Action_Verified_Auditor=None,
        Non_Conformity_Closure=None
    )
    conform_details = t_certification_organic_t11.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/non_conform_details.html', {'conform_details': conform_details})


def audit_team_accept(request):
    application_no = request.GET.get('application_id')
    acceptance = request.GET.get('acceptance')
    remarks = request.GET.get('remarks')

    details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    details.update(Audit_Team_Acceptance_Remarks=remarks)
    details.update(Audit_Team_Acceptance=acceptance)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_To=None)
    workflow_details.update(Assigned_Role_Id='2')
    workflow_details.update(Application_Status='ATA')
    return redirect(focal_officer_application)


def approve_oc_application(request):
    application_id = request.GET.get('application_no')
    validity = request.GET.get('validity')
    remarks = request.GET.get('remarks')
    Certificate_No = oc_certificate_no(request)
    details = t_certification_organic_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    details.update(Certificate_No=Certificate_No)
    details.update(Validity_Period=validity)
    details.update(Approve_Date=date.today())
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    update_payment(application_id, Certificate_No, 'OC', validity_date)
    for email_id in details:
        emailId = email_id.Email
        send_oc_approve_email(Certificate_No, emailId, validity_date)
    return redirect(focal_officer_application)


def send_oc_approve_email(Export_Permit_No, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for GAP Certificate Has Been Approved. " \
              "Your " \
              "Registration No is:" + Export_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def oc_certificate_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_certification_organic_t1.objects.aggregate(Max('Certificate_No'))
    lastAppNo = last_application_no['Certificate_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "OC" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "OC" + "/" + str(year) + "/" + AppNo
    return newAppNo


def oc_application_team_leader(request):
    application_no = request.GET.get('oc_application_id')
    acceptance = request.GET.get('acceptance')
    remarks = request.GET.get('remarks')
    team_leader = request.GET.get('Leader')

    details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    details.update(Audit_Plan_Acceptance_Remarks=remarks)
    details.update(Audit_Plan_Acceptance=acceptance)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_To=team_leader)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='APA')
    workflow_details.update(Action_Date=date.today())
    return redirect(resubmit_application)


def save_oc_audit_plan(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/organic_certificate/audit_plan")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/organic_certificate/audit_plan" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def save_oc_audit_plan_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('application_no')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'organic_certification/audit_plan_details.html', {'file_attach': file_attach})


def resubmit_oc_nc_details(request):
    application_no = request.GET.get('det_application_no')
    Audit_Findings_Site_History = request.GET.get('Audit_Findings_Site_History')
    Audit_Findings_Water_Source = request.GET.get('Audit_Findings_Water_Source')
    Audit_Findings_Product_Quality = request.GET.get('Audit_Findings_Product_Quality')
    Audit_Findings_Harvesting = request.GET.get('Audit_Findings_Harvesting')
    Audit_Findings_Equipment = request.GET.get('Audit_Findings_Equipment')
    Audit_Findings_Manufacturing_Production = request.GET.get('Audit_Findings_Manufacturing_Production')
    Audit_Findings_Sampling_Testing = request.GET.get('Audit_Findings_Sampling_Testing')
    Audit_Findings_Packing_Marking = request.GET.get('Audit_Findings_Packing_Marking')
    Audit_Findings_Storage_Transport = request.GET.get('Audit_Findings_Storage_Transport')
    Audit_Findings_Traceability = request.GET.get('Audit_Findings_Traceability')
    Audit_Findings_Worker_Health = request.GET.get('Audit_Findings_Worker_Health')
    Audit_Findings_Group_Requirement = request.GET.get('Audit_Findings_Group_Requirement')
    Audit_Findings_Others = request.GET.get('Audit_Findings_Others')
    Audit_Findings_Site_History_O = request.GET.get('Audit_Findings_Site_History_O')
    Audit_Findings_Water_Source_O = request.GET.get('Audit_Findings_Water_Source_O')
    Audit_Findings_Product_Quality_O = request.GET.get('Audit_Findings_Product_Quality_O')
    Audit_Findings_Harvesting_O = request.GET.get('Audit_Findings_Harvesting_O')
    Audit_Findings_Equipment_O = request.GET.get('Audit_Findings_Equipment_O')
    Audit_Findings_Manufacturing_Production_O = request.GET.get('Audit_Findings_Manufacturing_Production_O')
    Audit_Findings_Sampling_Testing_O = request.GET.get('Audit_Findings_Sampling_Testing_O')
    Audit_Findings_Packing_Marking_O = request.GET.get('Audit_Findings_Packing_Marking_O')
    Audit_Findings_Storage_Transport_O = request.GET.get('Audit_Findings_Storage_Transport_O')
    Audit_Findings_Traceability_O = request.GET.get('Audit_Findings_Traceability_O')
    Audit_Findings_Worker_Health_O = request.GET.get('Audit_Findings_Worker_Health_O')
    Audit_Findings_Group_Requirement_O = request.GET.get('Audit_Findings_Group_Requirement_O')
    Audit_Findings_Others_O = request.GET.get('Audit_Findings_Others_O')
    Audit_Type = request.GET.get('Audit_Type')
    app_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    app_details.update(Audit_Findings_Site_History_OE=Audit_Findings_Site_History)
    app_details.update(Audit_Findings_Water_Source_OE=Audit_Findings_Water_Source)
    app_details.update(Audit_Findings_Product_Quality_OE=Audit_Findings_Product_Quality)
    app_details.update(Audit_Findings_Harvesting_OE=Audit_Findings_Harvesting)
    app_details.update(Audit_Findings_Equipment_OE=Audit_Findings_Equipment)
    app_details.update(Audit_Findings_Manufacturing_Production_OE=Audit_Findings_Manufacturing_Production)
    app_details.update(Audit_Findings_Sampling_Testing_OE=Audit_Findings_Sampling_Testing)
    app_details.update(Audit_Findings_Packing_Marking_OE=Audit_Findings_Packing_Marking)
    app_details.update(Audit_Findings_Storage_Transport_OE=Audit_Findings_Storage_Transport)
    app_details.update(Audit_Findings_Traceability_OE=Audit_Findings_Traceability)
    app_details.update(Audit_Findings_Worker_Health_OE=Audit_Findings_Worker_Health)
    app_details.update(Audit_Findings_Group_Requirement_OE=Audit_Findings_Group_Requirement)
    app_details.update(Audit_Findings_Others_OE=Audit_Findings_Others)

    app_details.update(Audit_Findings_Site_History_Observations=Audit_Findings_Site_History_O)
    app_details.update(Audit_Findings_Water_Source_Observations=Audit_Findings_Water_Source_O)
    app_details.update(Audit_Findings_Product_Quality_Observations=Audit_Findings_Product_Quality_O)
    app_details.update(Audit_Findings_Harvesting_Observations=Audit_Findings_Harvesting_O)
    app_details.update(Audit_Findings_Equipment_Observations=Audit_Findings_Equipment_O)
    app_details.update(Audit_Findings_Manufacturing_Production_Observations=Audit_Findings_Manufacturing_Production_O)
    app_details.update(Audit_Findings_Sampling_Testing_Observations=Audit_Findings_Sampling_Testing_O)
    app_details.update(Audit_Findings_Packing_Marking_Observations=Audit_Findings_Packing_Marking_O)
    app_details.update(Audit_Findings_Storage_Transport_Observations=Audit_Findings_Storage_Transport_O)
    app_details.update(Audit_Findings_Traceability_Observations=Audit_Findings_Traceability_O)
    app_details.update(Audit_Findings_Worker_Health_Observations=Audit_Findings_Worker_Health_O)
    app_details.update(Audit_Findings_Group_Requirement_Observations=Audit_Findings_Group_Requirement_O)
    app_details.update(Audit_Findings_Others_Observations=Audit_Findings_Others_O)
    app_details.update(Audit_Type=Audit_Type)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='NCR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(inspector_application)


def edit_oc_nc_details(request, Record_Id):
    gap = get_object_or_404(t_certification_gap_t8, pk=Record_Id)
    if request.method == 'POST':
        form = GapForm(request.POST, instance=gap)
    else:
        form = GapForm(instance=gap)
    return save_oc_nc_details(request, form, 'organic_certification/edit_gap_nc_details.html')


def save_oc_nc_details(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        form.save()
        data['form_is_valid'] = True
        books = t_certification_gap_t8.objects.all()
        message_count = t_certification_gap_t8.objects.filter(Non_Conformity='Yes').count()
        data['html_book_list'] = render_to_string('organic_certification/nc_update_details.html', {
            'audit_observation': books, 'message_count': message_count
        })
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def oc_nc_response(request):
    application_no = request.GET.get('application_id')
    action_taken = request.GET.get('action_taken')
    Corrective_Action_Date = request.GET.get('Corrective_Action_Date')
    Team_Leader = request.GET.get('Team_Leader')
    date_action = datetime.strptime(Corrective_Action_Date, '%d-%m-%Y').date()
    nc_details = t_certification_gap_t8.objects.filter(Application_No=application_no)
    nc_details.update(Corrective_Action_Taken_Auditee=action_taken)
    nc_details.update(Corrective_Action_Date=date_action)
    details = t_workflow_details.objects.filter(Application_No=application_no)
    details.update(Assigned_To=Team_Leader)
    details.update(Action_Date=date.today())
    details.update(Application_Status='NCF')
    return redirect(resubmit_application)


# gap_certificate
def gap_certificate(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    country = t_country_master.objects.all()
    field_office = t_field_office_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'GAP_Certification/apply_gap_certification.html',
                  {'dzongkhag': dzongkhag, 'village': village,
                   'gewog': gewog, 'country': country,
                   'field_office': field_office,
                   'location': location, 'unit': unit})


def save_gap_certificate(request):
    data = dict()
    service_code = "GAP"
    gap_certificate_app_no = get_gap_certificate_app_no(request, service_code)
    Applicant_Type = request.POST.get('Applicant_Type')
    if Applicant_Type == 'I':
        cid = request.POST.get('cid')
        Name = request.POST.get('Name')
        Farmer_Group_No = None
        Farmer_Group_name = None
    else:
        cid = None
        Name = None
        Farmer_Group_No = request.POST.get('farmers_group_name')
        Farmer_Group_name = request.POST.get('farmers_group_number')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    address = request.POST.get('address')
    farm_location = request.POST.get('farm_location')
    farm_name = request.POST.get('farm_name')

    t_certification_gap_t1.objects.create(
        Application_No=gap_certificate_app_no,
        Application_Date=date.today(),
        Application_Type=Applicant_Type,
        CID=cid,
        Applicant_Name=Name,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Present_Address=address,
        Contact_No=contact_number,
        Email=email,
        Farmer_Group_No=Farmer_Group_No,
        Farmer_Group_Name=Farmer_Group_name,
        Pack_House=None,
        Crop_Production=None,
        Proposed_Standard=None,
        Terms_Bafra_Certification=None,
        Terms_Change_Willingness=None,
        Terms_Abide=None,
        Terms_Agreement=None,
        Acknowledge=None,
        FO_Remarks=None,
        Audit_Team_Leader=None,
        Audit_Team_Acceptance=None,
        Audit_Team_Acceptance_Remarks=None,
        Audit_Plan_Date=None,
        Audit_Plan_Criteria=None,
        Audit_Plan_Type=None,
        Audit_Plan_Scope=None,
        Audit_Plan_Acceptance=None,
        Audit_Plan_Acceptance_Remarks=None,
        Audit_Date=None,
        Audit_Findings_Site_History_OE=None,
        Audit_Findings_Water_Source_OE=None,
        Audit_Findings_Product_Quality_OE=None,
        Audit_Findings_Harvesting_OE=None,
        Audit_Findings_Equipment_OE=None,
        Audit_Findings_Manufacturing_Production_OE=None,
        Audit_Findings_Sampling_Testing_OE=None,
        Audit_Findings_Packing_Marking_OE=None,
        Audit_Findings_Storage_Transport_OE=None,
        Audit_Findings_Traceability_OE=None,
        Audit_Findings_Worker_Health_OE=None,
        Audit_Findings_Group_Requirement_OE=None,
        Audit_Findings_Others_OE=None,
        Audit_Findings_Site_History_Observations=None,
        Audit_Findings_Water_Source_Observations=None,
        Audit_Findings_Product_Quality_Observations=None,
        Audit_Findings_Harvesting_Observations=None,
        Audit_Findings_Equipment_Observations=None,
        Audit_Findings_Manufacturing_Production_Observations=None,
        Audit_Findings_Sampling_Testing_Observations=None,
        Audit_Findings_Packing_Marking_Observations=None,
        Audit_Findings_Storage_Transport_Observations=None,
        Audit_Findings_Traceability_Observations=None,
        Audit_Findings_Worker_Health_Observations=None,
        Audit_Findings_Group_Requirement_Observations=None,
        Audit_Findings_Others_Observations=None,
        Approve_Date=None,
        Certificate_No=None,
        Validity_Period=None,
        Validity=None,
        Farm_Location=farm_location,
        Applicant_Id=request.session['email'],
        Farm_Name=farm_name,
        Audit_Type=None,
        Others_Standards=None,
        Terms_Standards=None
    )
    t_workflow_details.objects.create(Application_No=gap_certificate_app_no,
                                      Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Certification',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['Applicant_Type'] = Applicant_Type
    data['applNo'] = gap_certificate_app_no
    return JsonResponse(data)


def gap_certificate_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/certification/gap_certificate")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/certification/gap_certificate" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def gap_certificate_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'GAP_Certification/file_attachment.html', {'file_attach': file_attach})


def save_gap_audit_plan(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/gap_certificate/audit_plan")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/gap_certificate/audit_plan" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def save_gap_audit_plan_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
        return render(request, 'GAP_Certification/audit_plan_details.html', {'file_attach': file_attach})


def gap_farmers_group_details(request):
    application_no = request.POST.get('farmers_group_application_no')
    cid = request.POST.get('farmers_group_cid')
    name = request.POST.get('farmers_group_fullname')
    t_certification_gap_t2.objects.create(Application_No=application_no, CID=cid, Name=name)
    farmers_group_details = t_certification_gap_t2.objects.filter(Application_No=application_no)
    return render(request, 'GAP_Certification/farmers_group_details.html',
                  {'farmers_group_details': farmers_group_details})


def gap_crop_production_details(request):
    application_no = request.GET.get('crop_production_app_no')
    crop_name = request.GET.get('crop_name')
    area = request.GET.get('area')
    area_unit = request.GET.get('area_unit')
    prev_year = request.GET.get('prev_year')
    to_year = request.GET.get('to_year')
    yields = request.GET.get('yield')
    Yield_Unit = request.GET.get('Yield_Unit')
    harvest_month = request.GET.get('harvest_month')
    sold = request.GET.get('sold')
    balance_stock = request.GET.get('balance_stock')
    current_year = request.GET.get('current_year')
    to_current_year = request.GET.get('to_current_year')
    estimated_yield = request.GET.get('estimated_yield')
    estimated_Yield_Unit = request.GET.get('estimated_Yield_Unit')
    estimated_harvest_month = request.GET.get('estimated_harvest_month')
    p_from = datetime.strptime(prev_year, '%d-%m-%Y').date()
    p_to = datetime.strptime(to_year, '%d-%m-%Y').date()
    c_from = datetime.strptime(current_year, '%d-%m-%Y').date()
    c_to = datetime.strptime(to_current_year, '%d-%m-%Y').date()

    t_certification_gap_t4.objects.create(
        Application_No=application_no,
        Crop_Name=crop_name,
        Area_Cultivated=area,
        Unit=area_unit,
        P_From_Date=p_from,
        P_To_Date=p_to,
        P_Yield=yields,
        P_Yield_Unit=Yield_Unit,
        P_Harvest_Month=harvest_month,
        P_Sold=sold,
        P_Balance_Stock=balance_stock,
        C_From_Date=c_from,
        C_To_Date=c_to,
        C_Estimated_Yield=estimated_yield,
        C_Yield_Unit=estimated_Yield_Unit,
        C_Harvest_Month=estimated_harvest_month)

    crop_production_details = t_certification_gap_t4.objects.filter(Application_No=application_no)
    return render(request, 'GAP_Certification/crop_production_details.html',
                  {'crop_production_details': crop_production_details})


def get_gap_certificate_app_no(request, service_code):
    last_application_no = t_certification_gap_t1.objects.aggregate(Max('Application_No'))
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


def add_pack_house_details(request):
    application_no = request.GET.get('packhouse_application_no')
    pack_house_name = request.GET.get('pack_house_name')
    pack_house_address = request.GET.get('pack_house_address')
    prev_year = request.GET.get('previous_from_date')
    to_year = request.GET.get('previous_to_date')
    production = request.GET.get('production')
    production_unit = request.GET.get('production_unit')
    previous_sold = request.GET.get('previous_sold')
    # previous_sold_unit = request.GET.get('previous_sold_unit')
    stock_balance = request.GET.get('stock_balance')
    # stock_balance_unit = request.GET.get('stock_balance_unit')
    current_from_date = request.GET.get('current_from_date')
    current_to_date = request.GET.get('current_to_date')
    current_Production = request.GET.get('current_Production')
    current_sold = request.GET.get('current_sold')
    # current_sold_unit = request.GET.get('current_sold_unit')
    current_stock_balance = request.GET.get('current_stock_balance')
    current_stock_unit = request.GET.get('current_stock_unit')
    p_from = datetime.strptime(prev_year, '%d-%m-%Y').date()
    p_to = datetime.strptime(to_year, '%d-%m-%Y').date()
    c_from = datetime.strptime(current_from_date, '%d-%m-%Y').date()
    c_to = datetime.strptime(current_to_date, '%d-%m-%Y').date()

    t_certification_gap_t5(
        Application_No=application_no,
        Pack_House_Name=pack_house_name,
        Pack_House_Address=pack_house_address,
        P_From_Date=p_from,
        P_To_Date=p_to,
        P_Production=production,
        P_Production_Unit=production_unit,
        P_Sold=previous_sold,
        P_Balance_Stock=stock_balance,
        C_From_Date=c_from,
        C_To_Date=c_to,
        C_Production=current_Production,
        C_Sold=current_sold,
        C_Balance_Stock=current_stock_balance
    )

    pack_house_details = t_certification_gap_t5.objects.filter(Application_No=application_no)
    return render(request, 'GAP_Certification/pack_house_details.html',
                  {'pack_house_details': pack_house_details})


def gap_audit_team_details(request):
    application_no = request.GET.get('application_id')
    audit_team_member = request.GET.get('name')
    role = request.GET.get('role')

    details = t_user_master.objects.filter(Login_Id=audit_team_member)
    for name in details:
        app_name = name.Name
        t_certification_gap_t3.objects.create(Application_No=application_no, Login_Id=audit_team_member,
                                              Name=app_name, Role=role)
    audit_team = t_certification_gap_t3.objects.filter(Application_No=application_no)
    return render(request, 'GAP_Certification/audit_team_details.html',
                  {'audit_team': audit_team})


def submit_gap_certificate(request):
    application_no = request.POST.get('application_no')
    print(application_no)
    Terms_Bafra_Certification = request.POST.get('Terms_Bafra_Certification')
    Terms_Change_Willingness = request.POST.get('Terms_Change_Willingness')
    Terms_Abide = request.POST.get('Terms_Abide')
    Terms_Agreement = request.POST.get('Terms_Agreement')
    Standards = request.POST.get('Standards')
    Others_Standards = request.POST.get('other_standard')
    app_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    app_details.update(Terms_Bafra_Certification=Terms_Bafra_Certification)
    app_details.update(Terms_Change_Willingness=Terms_Change_Willingness)
    app_details.update(Terms_Abide=Terms_Abide)
    app_details.update(Terms_Agreement=Terms_Agreement)
    app_details.update(Terms_Standards=Standards)
    if Others_Standards is not None:
        app_details.update(Others_Standards=Others_Standards)
    else:
        app_details.update(Others_Standards=None)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(gap_certificate)


def gap_for_acceptance(request):
    application_no = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    audit_team_leader = request.GET.get('audit_team_leader')
    app_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    app_details.update(Audit_Team_Leader=audit_team_leader)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='ATR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(focal_officer_application)


def gap_application_team_leader(request):
    application_no = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    team_leader = request.GET.get('audit_team_leader')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Application_Status='AP')
    workflow_details.update(Assigned_Role_Id=None)
    app_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    workflow_details.update(Assigned_To=team_leader)
    return redirect(focal_officer_application)


def gap_audit_team_accept(request):
    application_no = request.GET.get('application_id')
    acceptance = request.GET.get('acceptance')
    remarks = request.GET.get('remarks')

    details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    details.update(Audit_Team_Acceptance_Remarks=remarks)
    details.update(Audit_Team_Acceptance=acceptance)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_To=None)
    workflow_details.update(Assigned_Role_Id='2')
    workflow_details.update(Application_Status='ATA')
    workflow_details.update(Action_Date=date.today())
    return redirect(focal_officer_application)


def gap_farm_input_observation(request):
    application_no = request.GET.get('application_no')
    Audit_Findings_Farm_Inputs = request.GET.get('Audit_Findings_Farm_Inputs')
    Audit_Findings_Farm_Supplier = request.GET.get('Audit_Findings_Farm_Supplier')
    Audit_Findings_Farm_Invoice = request.GET.get('Audit_Findings_Farm_Invoice')
    t_certification_gap_t7.objects.create(Application_No=application_no,
                                          Audit_Findings_Farm_Inputs=Audit_Findings_Farm_Inputs,
                                          Audit_Findings_Farm_Supplier=Audit_Findings_Farm_Supplier,
                                          Audit_Findings_Farm_Invoice=Audit_Findings_Farm_Invoice)
    details = t_certification_food_t4.objects.filter(Application_No=application_no)
    return render(request, 'GAP_Certification/farm_input_details.html', {'farm_inputs': details})


def gap_audit_plan_acceptance(request):
    application_no = request.GET.get('application_id')
    acceptance = request.GET.get('acceptance')
    remarks = request.GET.get('remarks')
    team_leader = request.GET.get('Leader')

    details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    details.update(Audit_Plan_Acceptance_Remarks=remarks)
    details.update(Audit_Plan_Acceptance=acceptance)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_To=team_leader)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='APA')
    workflow_details.update(Action_Date=date.today())
    return redirect(resubmit_application)


def gap_audit_plan_resubmit(request):
    application_no = request.GET.get('audit_date_application_no')
    Audit_Date = request.GET.get('date_of_audit')
    app_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    app_details.update(Audit_Date=Audit_Date)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='APR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(inspector_application)


def resubmit_nc_details(request):
    application_no = request.GET.get('det_application_no')
    Audit_Findings_Site_History = request.GET.get('Audit_Findings_Site_History')
    Audit_Findings_Water_Source = request.GET.get('Audit_Findings_Water_Source')
    Audit_Findings_Product_Quality = request.GET.get('Audit_Findings_Product_Quality')
    Audit_Findings_Harvesting = request.GET.get('Audit_Findings_Harvesting')
    Audit_Findings_Equipment = request.GET.get('Audit_Findings_Equipment')
    Audit_Findings_Manufacturing_Production = request.GET.get('Audit_Findings_Manufacturing_Production')
    Audit_Findings_Sampling_Testing = request.GET.get('Audit_Findings_Sampling_Testing')
    Audit_Findings_Packing_Marking = request.GET.get('Audit_Findings_Packing_Marking')
    Audit_Findings_Storage_Transport = request.GET.get('Audit_Findings_Storage_Transport')
    Audit_Findings_Traceability = request.GET.get('Audit_Findings_Traceability')
    Audit_Findings_Worker_Health = request.GET.get('Audit_Findings_Worker_Health')
    Audit_Findings_Group_Requirement = request.GET.get('Audit_Findings_Group_Requirement')
    Audit_Findings_Others = request.GET.get('Audit_Findings_Others')
    Audit_Findings_Site_History_O = request.GET.get('Audit_Findings_Site_History_O')
    Audit_Findings_Water_Source_O = request.GET.get('Audit_Findings_Water_Source_O')
    Audit_Findings_Product_Quality_O = request.GET.get('Audit_Findings_Product_Quality_O')
    Audit_Findings_Harvesting_O = request.GET.get('Audit_Findings_Harvesting_O')
    Audit_Findings_Equipment_O = request.GET.get('Audit_Findings_Equipment_O')
    Audit_Findings_Manufacturing_Production_O = request.GET.get('Audit_Findings_Manufacturing_Production_O')
    Audit_Findings_Sampling_Testing_O = request.GET.get('Audit_Findings_Sampling_Testing_O')
    Audit_Findings_Packing_Marking_O = request.GET.get('Audit_Findings_Packing_Marking_O')
    Audit_Findings_Storage_Transport_O = request.GET.get('Audit_Findings_Storage_Transport_O')
    Audit_Findings_Traceability_O = request.GET.get('Audit_Findings_Traceability_O')
    Audit_Findings_Worker_Health_O = request.GET.get('Audit_Findings_Worker_Health_O')
    Audit_Findings_Group_Requirement_O = request.GET.get('Audit_Findings_Group_Requirement_O')
    Audit_Findings_Others_O = request.GET.get('Audit_Findings_Others_O')
    Audit_Type = request.GET.get('Audit_Type')
    app_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    app_details.update(Audit_Findings_Site_History_OE=Audit_Findings_Site_History)
    app_details.update(Audit_Findings_Water_Source_OE=Audit_Findings_Water_Source)
    app_details.update(Audit_Findings_Product_Quality_OE=Audit_Findings_Product_Quality)
    app_details.update(Audit_Findings_Harvesting_OE=Audit_Findings_Harvesting)
    app_details.update(Audit_Findings_Equipment_OE=Audit_Findings_Equipment)
    app_details.update(Audit_Findings_Manufacturing_Production_OE=Audit_Findings_Manufacturing_Production)
    app_details.update(Audit_Findings_Sampling_Testing_OE=Audit_Findings_Sampling_Testing)
    app_details.update(Audit_Findings_Packing_Marking_OE=Audit_Findings_Packing_Marking)
    app_details.update(Audit_Findings_Storage_Transport_OE=Audit_Findings_Storage_Transport)
    app_details.update(Audit_Findings_Traceability_OE=Audit_Findings_Traceability)
    app_details.update(Audit_Findings_Worker_Health_OE=Audit_Findings_Worker_Health)
    app_details.update(Audit_Findings_Group_Requirement_OE=Audit_Findings_Group_Requirement)
    app_details.update(Audit_Findings_Others_OE=Audit_Findings_Others)

    app_details.update(Audit_Findings_Site_History_Observations=Audit_Findings_Site_History_O)
    app_details.update(Audit_Findings_Water_Source_Observations=Audit_Findings_Water_Source_O)
    app_details.update(Audit_Findings_Product_Quality_Observations=Audit_Findings_Product_Quality_O)
    app_details.update(Audit_Findings_Harvesting_Observations=Audit_Findings_Harvesting_O)
    app_details.update(Audit_Findings_Equipment_Observations=Audit_Findings_Equipment_O)
    app_details.update(Audit_Findings_Manufacturing_Production_Observations=Audit_Findings_Manufacturing_Production_O)
    app_details.update(Audit_Findings_Sampling_Testing_Observations=Audit_Findings_Sampling_Testing_O)
    app_details.update(Audit_Findings_Packing_Marking_Observations=Audit_Findings_Packing_Marking_O)
    app_details.update(Audit_Findings_Storage_Transport_Observations=Audit_Findings_Storage_Transport_O)
    app_details.update(Audit_Findings_Traceability_Observations=Audit_Findings_Traceability_O)
    app_details.update(Audit_Findings_Worker_Health_Observations=Audit_Findings_Worker_Health_O)
    app_details.update(Audit_Findings_Group_Requirement_Observations=Audit_Findings_Group_Requirement_O)
    app_details.update(Audit_Findings_Others_Observations=Audit_Findings_Others_O)
    app_details.update(Audit_Type=Audit_Type)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='NCR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(inspector_application)


def edit_nc_details(request, Record_Id):
    gap = get_object_or_404(t_certification_gap_t8, pk=Record_Id)
    if request.method == 'POST':
        form = GapForm(request.POST, instance=gap)
    else:
        form = GapForm(instance=gap)
    return save_nc_details(request, form, 'GAP_Certification/edit_gap_nc_details.html')


def save_nc_details(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        form.save()
        data['form_is_valid'] = True
        books = t_certification_gap_t8.objects.all()
        message_count = t_certification_gap_t8.objects.filter(Non_Conformity='Yes').count()
        data['html_book_list'] = render_to_string('GAP_Certification/nc_update_details.html', {
            'audit_observation': books, 'message_count': message_count
        })
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def gap_conform_observation(request):
    application_no = request.GET.get('appl_no')
    Clause_Number = request.GET.get('Clause_Number')
    Non_Conformity = request.GET.get('Non_Conformity')
    Non_Conformity_Category = request.GET.get('Non_Conformity_Category')
    Non_Conformity_Description = request.GET.get('Non_Conformity_Description')
    Corrective_Action_Proposed_Auditee = request.GET.get('Corrective_Action_Proposed_Auditee')
    t_certification_gap_t8.objects.create(
        Application_No=application_no,
        Clause_Number=Clause_Number,
        Non_Conformity=Non_Conformity,
        Non_Conformity_Category=Non_Conformity_Category,
        Non_Conformity_Description=Non_Conformity_Description,
        Corrective_Action_Proposed_Auditee=Corrective_Action_Proposed_Auditee,
        Corrective_Action_Taken_Auditee=None,
        Corrective_Action_Date=None,
        Corrective_Action_Verified_Auditor=None,
        Non_Conformity_Closure=None
    )
    conform_details = t_certification_gap_t8.objects.filter(Application_No=application_no)
    message_count = t_certification_gap_t8.objects.filter(Non_Conformity='Yes').count()
    return render(request, 'GAP_Certification/non_conform_details.html', {'conform_details': conform_details,
                                                                          'message_count': message_count})


def forward_application_head_office(request):
    application_no = request.POST.get('approved_application_no')
    print(application_no)
    details = t_workflow_details.objects.filter(Application_No=application_no)
    details.update(Assigned_To=None)
    details.update(Assigned_Role_Id='2')
    details.update(Action_Date=date.today())
    details.update(Application_Status='CA')
    return redirect(inspector_application)


def gap_nc_response(request):
    application_no = request.GET.get('application_id')
    action_taken = request.GET.get('action_taken')
    Corrective_Action_Date = request.GET.get('Corrective_Action_Date')
    Team_Leader = request.GET.get('Team_Leader')
    date_action = datetime.strptime(Corrective_Action_Date, '%d-%m-%Y').date()
    nc_details = t_certification_gap_t8.objects.filter(Application_No=application_no)
    nc_details.update(Corrective_Action_Taken_Auditee=action_taken)
    nc_details.update(Corrective_Action_Date=date_action)
    details = t_workflow_details.objects.filter(Application_No=application_no)
    details.update(Assigned_To=Team_Leader)
    details.update(Action_Date=date.today())
    details.update(Application_Status='NCF')
    return redirect(resubmit_application)


def approve_gap_application(request):
    application_id = request.GET.get('application_no')
    validity = request.GET.get('validity')
    remarks = request.POST.get('remarks')
    certificate_no = gap_certificate_no(request)
    details = t_certification_gap_t1.objects.filter(Application_No=application_id)
    details.update(Certificate_No=certificate_no)
    details.update(Validity_Period=validity)
    details.update(Approve_Date=date.today())
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    update_payment(application_id, certificate_no, 'GAP', validity_date)
    for email_id in details:
        emailId = email_id.Email
        send_gap_approve_email(certificate_no, emailId, validity_date)
    return redirect(focal_officer_application)


def send_gap_approve_email(Export_Permit_No, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for GAP Certificate Has Been Approved. " \
              "Your " \
              "Registration No is:" + Export_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def gap_certificate_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_certification_gap_t1.objects.aggregate(Max('Certificate_No'))
    lastAppNo = last_application_no['Certificate_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "GAP" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "GAP" + "/" + str(year) + "/" + AppNo
    return newAppNo


# Food Product certificate
def food_product_certificate(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    country = t_country_master.objects.all()
    field_office = t_field_office_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    unit = t_unit_master.objects.all()
    return render(request, 'food_product_certification/apply_food_product_certification.html',
                  {'dzongkhag': dzongkhag, 'village': village,
                   'gewog': gewog, 'country': country,
                   'field_office': field_office,
                   'location': location, 'unit': unit})


def save_food_product_certificate(request):
    data = dict()
    service_code = "FPC"
    food_product_certificate_app_no = food_product_application_no(request, service_code)

    Firm_Name = request.POST.get('Firm_Name')
    Firm_Address = request.POST.get('Firm_Address')
    Firm_Contact_No = request.POST.get('Firm_Contact_No')
    Firm_Email = request.POST.get('Firm_Email')
    Factory_Name = request.POST.get('Factory_Name')
    Factory_Address = request.POST.get('Factory_Address')
    Factory_Contact_No = request.POST.get('Factory_Contact_No')
    Factory_Email = request.POST.get('Factory_Email')
    Product_Description = request.POST.get('Product_Description')
    Product_Trade_Mark = request.POST.get('Product_Trade_Mark')
    P_From_Date = request.POST.get('P_From_Date')
    P_To_Date = request.POST.get('P_To_Date')
    P_Production = request.POST.get('P_Production')
    P_Production_Unit = request.POST.get('P_Production_Unit')
    P_Production_Value = request.POST.get('P_Production_Value')
    P_Export = request.POST.get('P_Export')
    P_Export_Unit = request.POST.get('P_Export_Unit')
    C_From_Date = request.POST.get('C_From_Date')
    C_To_Date = request.POST.get('C_To_Date')
    C_Production = request.POST.get('C_Production')
    C_Production_Unit = request.POST.get('C_Production_Unit')
    C_Production_Value = request.POST.get('C_Production_Value')
    C_Export = request.POST.get('C_Export')
    C_Export_Unit = request.POST.get('C_Export_Unit')
    C_Export_From_Date = request.POST.get('C_Export_From_Date')
    C_Export_To_Date = request.POST.get('C_Export_To_Date')
    C_Export_Value = request.POST.get('C_Export_Value')
    P_Export_From_Date = request.POST.get('P_Export_From_Date')
    P_Export_To_Date = request.POST.get('P_Export_To_Date')
    P_Export_Value = request.POST.get('P_Export_Value')

    date_from_p = datetime.strptime(P_From_Date, '%d-%m-%Y').date()
    date_to_p = datetime.strptime(P_To_Date, '%d-%m-%Y').date()
    date_from_c = datetime.strptime(C_From_Date, '%d-%m-%Y').date()
    date_to_c = datetime.strptime(C_To_Date, '%d-%m-%Y').date()
    date_export_f = datetime.strptime(C_Export_From_Date, '%d-%m-%Y').date()
    date_export_t = datetime.strptime(C_Export_To_Date, '%d-%m-%Y').date()
    date_export_pf = datetime.strptime(P_Export_From_Date, '%d-%m-%Y').date()
    date_export_pt = datetime.strptime(P_Export_To_Date, '%d-%m-%Y').date()

    t_certification_food_t1.objects.create(
        Application_No=food_product_certificate_app_no,
        Application_Date=date.today(),
        Firm_Name=Firm_Name,
        Firm_Address=Firm_Address,
        Firm_Contact_No=Firm_Contact_No,
        Firm_Email=Firm_Email,
        Factory_Name=Factory_Name,
        Factory_Address=Factory_Address,
        Factory_Contact_No=Factory_Contact_No,
        Factory_Email=Factory_Email,
        Product_Description=Product_Description,
        Product_Trade_Mark=Product_Trade_Mark,
        P_From_Date=date_from_p,
        P_To_Date=date_to_p,
        P_Production=P_Production,
        P_Production_Unit=P_Production_Unit,
        P_Production_Value=P_Production_Value,
        P_Export=P_Export,
        P_Export_Unit=P_Export_Unit,
        C_From_Date=date_from_c,
        C_To_Date=date_to_c,
        C_Production=C_Production,
        C_Production_Unit=C_Production_Unit,
        C_Production_Value=C_Production_Value,
        C_Export=C_Export,
        C_Export_Unit=C_Export_Unit,
        Proposed_Standard=None,
        Terms_Bafra_Certification=None,
        Terms_Change_Willingness=None,
        Terms_Abide=None,
        Terms_Agreement=None,
        Acknowledge=None,
        FO_Remarks=None,
        Audit_Team_Leader=None,
        Audit_Team_Acceptance=None,
        Audit_Team_Acceptance_Remarks=None,
        Audit_Plan_Date=None,
        Audit_Plan_Criteria=None,
        Audit_Plan_Type=None,
        Audit_Plan_Scope=None,
        Audit_Plan_Acceptance=None,
        Audit_Plan_Acceptance_Remarks=None,
        Audit_Date=None,
        Audit_Findings_Site_History_OE=None,
        Audit_Findings_Water_Source_OE=None,
        Audit_Findings_Product_Quality_OE=None,
        Audit_Findings_Harvesting_OE=None,
        Audit_Findings_Equipment_OE=None,
        Audit_Findings_Manufacturing_Production_OE=None,
        Audit_Findings_Sampling_Testing_OE=None,
        Audit_Findings_Packing_Marking_OE=None,
        Audit_Findings_Storage_Transport_OE=None,
        Audit_Findings_Traceability_OE=None,
        Audit_Findings_Worker_Health_OE=None,
        Audit_Findings_Group_Requirement_OE=None,
        Audit_Findings_Others_OE=None,
        Audit_Findings_Site_History_Observations=None,
        Audit_Findings_Water_Source_Observations=None,
        Audit_Findings_Product_Quality_Observations=None,
        Audit_Findings_Harvesting_Observations=None,
        Audit_Findings_Equipment_Observations=None,
        Audit_Findings_Manufacturing_Production_Observations=None,
        Audit_Findings_Sampling_Testing_Observations=None,
        Audit_Findings_Packing_Marking_Observations=None,
        Audit_Findings_Storage_Transport_Observations=None,
        Audit_Findings_Traceability_Observations=None,
        Audit_Findings_Worker_Health_Observations=None,
        Audit_Findings_Group_Requirement_Observations=None,
        Audit_Findings_Others_Observations=None,
        Approve_Date=None,
        Certificate_No=None,
        Validity_Period=None,
        Validity=None,
        Applicant_Id=request.session['email'],
        Audit_Type=None,
        C_Export_From_Date=date_export_f,
        C_Export_To_Date=date_export_t,
        C_Export_Value=C_Export_Value,
        P_Export_From_Date=date_export_pf,
        P_Export_To_Date=date_export_pt,
        P_Export_Value=P_Export_Value,
        Others_Standards=None,
        Terms_Standards=None
    )
    t_workflow_details.objects.create(Application_No=food_product_certificate_app_no,
                                      Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Certification',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)

    data['applNo'] = food_product_certificate_app_no
    return JsonResponse(data)


def food_product_application_no(request, service_code):
    last_application_no = t_certification_food_t1.objects.aggregate(Max('Application_No'))
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


def food_product_certificate_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/certification/food_product_certificate")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/certification/food_product_certificate" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def food_product_certificate_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'food_product_certification/file_attachment.html', {'file_attach': file_attach})


def submit_food_product_certificate(request):
    application_no = request.POST.get('application_no')
    Terms_Bafra_Certification = request.POST.get('Terms_Bafra_Certification')
    Terms_Change_Willingness = request.POST.get('Terms_Change_Willingness')
    Terms_Abide = request.POST.get('Terms_Abide')
    Terms_Agreement = request.POST.get('Terms_Agreement')
    Standards = request.POST.get('Standards')
    Others_Standards = request.POST.get('other_standard')

    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    app_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    app_details.update(Terms_Bafra_Certification=Terms_Bafra_Certification)
    app_details.update(Terms_Change_Willingness=Terms_Change_Willingness)
    app_details.update(Terms_Abide=Terms_Abide)
    app_details.update(Terms_Agreement=Terms_Agreement)
    app_details.update(Terms_Standards=Standards)
    if Others_Standards is not None:
        app_details.update(Others_Standards=Others_Standards)
    else:
        app_details.update(Others_Standards=None)
    return redirect(food_product_certificate)


def fpc_audit_team_details(request):
    application_no = request.GET.get('application_id')
    audit_team_member = request.GET.get('name')
    role = request.GET.get('role')

    details = t_user_master.objects.filter(Login_Id=audit_team_member)
    for name in details:
        app_name = name.Name
        t_certification_food_t3.objects.create(Application_No=application_no, Login_Id=audit_team_member,
                                               Name=app_name, Role=role)
    audit_team = t_certification_food_t3.objects.filter(Application_No=application_no)
    return render(request, 'food_product_certification/audit_team_details.html',
                  {'audit_team': audit_team})


def fpc_for_acceptance(request):
    application_no = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    audit_team_leader = request.GET.get('audit_team_leader')
    app_details = t_certification_food_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    app_details.update(Audit_Team_Leader=audit_team_leader)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='ATR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(focal_officer_application)


def fpc_application_team_leader(request):
    application_no = request.GET.get('application_id')
    remarks = request.GET.get('remarks')
    team_leader = request.GET.get('audit_team_leader')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Application_Status='AP')
    workflow_details.update(Assigned_Role_Id=None)
    app_details = t_certification_food_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    workflow_details.update(Assigned_To=team_leader)
    return redirect(focal_officer_application)


def fpc_audit_team_accept(request):
    application_no = request.GET.get('application_id')
    acceptance = request.GET.get('acceptance')
    remarks = request.GET.get('remarks')

    details = t_certification_food_t1.objects.filter(Application_No=application_no)
    details.update(Audit_Team_Acceptance_Remarks=remarks)
    details.update(Audit_Team_Acceptance=acceptance)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_To=None)
    workflow_details.update(Assigned_Role_Id='2')
    workflow_details.update(Application_Status='ATA')
    return redirect(focal_officer_application)


def fpc_farm_input_observation(request):
    application_no = request.GET.get('application_no')
    Audit_Findings_Farm_Inputs = request.GET.get('Audit_Findings_Farm_Inputs')
    Audit_Findings_Farm_Supplier = request.GET.get('Audit_Findings_Farm_Supplier')
    Audit_Findings_Farm_Invoice = request.GET.get('Audit_Findings_Farm_Invoice')
    t_certification_food_t4.objects.create(Application_No=application_no,
                                           Audit_Findings_Farm_Inputs=Audit_Findings_Farm_Inputs,
                                           Audit_Findings_Farm_Supplier=Audit_Findings_Farm_Supplier,
                                           Audit_Findings_Farm_Invoice=Audit_Findings_Farm_Invoice)
    details = t_certification_food_t4.objects.filter(Application_No=application_no)
    return render(request, 'food_product_certification/farm_input_details.html', {'farm_inputs': details})


def fpc_audit_plan_acceptance(request):
    application_no = request.GET.get('application_id')
    acceptance = request.GET.get('acceptance')
    remarks = request.GET.get('remarks')
    team_leader = request.GET.get('Leader')

    details = t_certification_food_t1.objects.filter(Application_No=application_no)
    details.update(Audit_Plan_Acceptance_Remarks=remarks)
    details.update(Audit_Plan_Acceptance=acceptance)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_To=team_leader)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='APA')
    workflow_details.update(Action_Date=date.today())
    return redirect(resubmit_application)


def fpc_audit_plan_resubmit(request):
    application_no = request.GET.get('audit_date_application_no')
    Audit_Type = request.GET.get('Audit_Type')
    Audit_Date = request.GET.get('Audit_Date')
    app_details = t_certification_food_t1.objects.filter(Application_No=application_no)
    app_details.update(Audit_Type=Audit_Type)
    app_details.update(Audit_Date=Audit_Date)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='APR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(inspector_application)


def fpc_conform_observation(request):
    application_no = request.GET.get('appl_no')
    Clause_Number = request.GET.get('Clause_Number')
    Non_Conformity = request.GET.get('Non_Conformity')
    Non_Conformity_Category = request.GET.get('Non_Conformity_Category')
    Non_Conformity_Description = request.GET.get('Non_Conformity_Description')
    Corrective_Action_Proposed_Auditee = request.GET.get('Corrective_Action_Proposed_Auditee')
    t_certification_food_t5.objects.create(
        Application_No=application_no,
        Clause_Number=Clause_Number,
        Non_Conformity=Non_Conformity,
        Non_Conformity_Category=Non_Conformity_Category,
        Non_Conformity_Description=Non_Conformity_Description,
        Corrective_Action_Proposed_Auditee=Corrective_Action_Proposed_Auditee,
        Corrective_Action_Taken_Auditee=None,
        Corrective_Action_Date=None,
        Corrective_Action_Verified_Auditor=None,
        Non_Conformity_Closure=None
    )
    conform_details = t_certification_food_t5.objects.filter(Application_No=application_no)
    message_count = t_certification_food_t5.objects.filter(Non_Conformity='Yes').count()
    return render(request, 'food_product_certification/non_conform_details.html',
                  {'conform_details': conform_details, 'message_count': message_count})


def approve_fpc_application(request):
    application_id = request.GET.get('application_no')

    validity = request.GET.get('validity')
    remarks = request.GET.get('remarks')

    Export_Permit_No = fpc_certificate_no(request)
    details = t_certification_food_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    details.update(Certificate_No=Export_Permit_No)
    details.update(Validity_Period=validity)
    details.update(Approve_Date=date.today())
    d = timedelta(days=int(validity))
    validity_date = date.today() + d
    details.update(Validity=validity_date)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    update_payment(application_id, Export_Permit_No, 'GAP', validity_date)
    for email_id in details:
        emailId = email_id.Firm_Email
        send_fpc_approve_email(Export_Permit_No, emailId, validity_date)
    return redirect(focal_officer_application)


def send_fpc_approve_email(Export_Permit_No, Email, validity_date):
    valid_till = validity_date.strftime('%d-%m-%Y')

    subject = 'APPLICATION APPROVED'
    message = "Dear Sir, Your Application for GAP Certificate Has Been Approved. " \
              "Your " \
              "Registration No is:" + Export_Permit_No + " And is Valid Till " + str(valid_till) + \
              "." + " Please Make Payment Before Validity Expires. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def fpc_certificate_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_certification_food_t1.objects.aggregate(Max('Certificate_No'))
    lastAppNo = last_application_no['Certificate_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "FPC" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[14:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "/" + "FPC" + "/" + str(year) + "/" + AppNo
    return newAppNo


def save_fpc_audit_plan(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/food_product_certificate/audit_plan")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(
            timezone.now().year) + "/food_product_certificate/audit_plan" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def save_fpc_audit_plan_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
        return render(request, 'food_product_certification/audit_plan_details.html', {'file_attach': file_attach})


def resubmit_fpc_nc_details(request):
    application_no = request.GET.get('det_application_no')
    Audit_Findings_Site_History = request.GET.get('Audit_Findings_Site_History')
    Audit_Findings_Water_Source = request.GET.get('Audit_Findings_Water_Source')
    Audit_Findings_Product_Quality = request.GET.get('Audit_Findings_Product_Quality')
    Audit_Findings_Harvesting = request.GET.get('Audit_Findings_Harvesting')
    Audit_Findings_Equipment = request.GET.get('Audit_Findings_Equipment')
    Audit_Findings_Manufacturing_Production = request.GET.get('Audit_Findings_Manufacturing_Production')
    Audit_Findings_Sampling_Testing = request.GET.get('Audit_Findings_Sampling_Testing')
    Audit_Findings_Packing_Marking = request.GET.get('Audit_Findings_Packing_Marking')
    Audit_Findings_Storage_Transport = request.GET.get('Audit_Findings_Storage_Transport')
    Audit_Findings_Traceability = request.GET.get('Audit_Findings_Traceability')
    Audit_Findings_Worker_Health = request.GET.get('Audit_Findings_Worker_Health')
    Audit_Findings_Group_Requirement = request.GET.get('Audit_Findings_Group_Requirement')
    Audit_Findings_Others = request.GET.get('Audit_Findings_Others')
    Audit_Findings_Site_History_O = request.GET.get('Audit_Findings_Site_History_O')
    Audit_Findings_Water_Source_O = request.GET.get('Audit_Findings_Water_Source_O')
    Audit_Findings_Product_Quality_O = request.GET.get('Audit_Findings_Product_Quality_O')
    Audit_Findings_Harvesting_O = request.GET.get('Audit_Findings_Harvesting_O')
    Audit_Findings_Equipment_O = request.GET.get('Audit_Findings_Equipment_O')
    Audit_Findings_Manufacturing_Production_O = request.GET.get('Audit_Findings_Manufacturing_Production_O')
    Audit_Findings_Sampling_Testing_O = request.GET.get('Audit_Findings_Sampling_Testing_O')
    Audit_Findings_Packing_Marking_O = request.GET.get('Audit_Findings_Packing_Marking_O')
    Audit_Findings_Storage_Transport_O = request.GET.get('Audit_Findings_Storage_Transport_O')
    Audit_Findings_Traceability_O = request.GET.get('Audit_Findings_Traceability_O')
    Audit_Findings_Worker_Health_O = request.GET.get('Audit_Findings_Worker_Health_O')
    Audit_Findings_Group_Requirement_O = request.GET.get('Audit_Findings_Group_Requirement_O')
    Audit_Findings_Others_O = request.GET.get('Audit_Findings_Others_O')
    Audit_Type = request.GET.get('Audit_Type')
    app_details = t_certification_food_t1.objects.filter(Application_No=application_no)
    app_details.update(Audit_Findings_Site_History_OE=Audit_Findings_Site_History)
    app_details.update(Audit_Findings_Water_Source_OE=Audit_Findings_Water_Source)
    app_details.update(Audit_Findings_Product_Quality_OE=Audit_Findings_Product_Quality)
    app_details.update(Audit_Findings_Harvesting_OE=Audit_Findings_Harvesting)
    app_details.update(Audit_Findings_Equipment_OE=Audit_Findings_Equipment)
    app_details.update(Audit_Findings_Manufacturing_Production_OE=Audit_Findings_Manufacturing_Production)
    app_details.update(Audit_Findings_Sampling_Testing_OE=Audit_Findings_Sampling_Testing)
    app_details.update(Audit_Findings_Packing_Marking_OE=Audit_Findings_Packing_Marking)
    app_details.update(Audit_Findings_Storage_Transport_OE=Audit_Findings_Storage_Transport)
    app_details.update(Audit_Findings_Traceability_OE=Audit_Findings_Traceability)
    app_details.update(Audit_Findings_Worker_Health_OE=Audit_Findings_Worker_Health)
    app_details.update(Audit_Findings_Group_Requirement_OE=Audit_Findings_Group_Requirement)
    app_details.update(Audit_Findings_Others_OE=Audit_Findings_Others)

    app_details.update(Audit_Findings_Site_History_Observations=Audit_Findings_Site_History_O)
    app_details.update(Audit_Findings_Water_Source_Observations=Audit_Findings_Water_Source_O)
    app_details.update(Audit_Findings_Product_Quality_Observations=Audit_Findings_Product_Quality_O)
    app_details.update(Audit_Findings_Harvesting_Observations=Audit_Findings_Harvesting_O)
    app_details.update(Audit_Findings_Equipment_Observations=Audit_Findings_Equipment_O)
    app_details.update(Audit_Findings_Manufacturing_Production_Observations=Audit_Findings_Manufacturing_Production_O)
    app_details.update(Audit_Findings_Sampling_Testing_Observations=Audit_Findings_Sampling_Testing_O)
    app_details.update(Audit_Findings_Packing_Marking_Observations=Audit_Findings_Packing_Marking_O)
    app_details.update(Audit_Findings_Storage_Transport_Observations=Audit_Findings_Storage_Transport_O)
    app_details.update(Audit_Findings_Traceability_Observations=Audit_Findings_Traceability_O)
    app_details.update(Audit_Findings_Worker_Health_Observations=Audit_Findings_Worker_Health_O)
    app_details.update(Audit_Findings_Group_Requirement_Observations=Audit_Findings_Group_Requirement_O)
    app_details.update(Audit_Findings_Others_Observations=Audit_Findings_Others_O)
    app_details.update(Audit_Type=Audit_Type)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='NCR')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assigned_To=login)
    return redirect(inspector_application)


def edit_fpc_nc_details(request, Record_Id):
    gap = get_object_or_404(t_certification_food_t5, pk=Record_Id)
    if request.method == 'POST':
        form = FpcForm(request.POST, instance=gap)
    else:
        form = FpcForm(instance=gap)
    return save_fpc_nc_details(request, form, 'food_product_certification/edit_fpc_nc_details.html')


def save_fpc_nc_details(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        form.save()
        data['form_is_valid'] = True
        books = t_certification_food_t5.objects.all()
        message_count = t_certification_food_t5.objects.filter(Non_Conformity='Yes').count()
        data['html_book_list'] = render_to_string('food_product_certification/nc_update_details.html', {
            'audit_observation': books, 'message_count': message_count
        })
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def fpc_nc_response(request):
    application_no = request.GET.get('application_id')
    action_taken = request.GET.get('action_taken')
    Corrective_Action_Date = request.GET.get('Corrective_Action_Date')
    Team_Leader = request.GET.get('Team_Leader')
    date_action = datetime.strptime(Corrective_Action_Date, '%d-%m-%Y').date()
    nc_details = t_certification_gap_t8.objects.filter(Application_No=application_no)
    nc_details.update(Corrective_Action_Taken_Auditee=action_taken)
    nc_details.update(Corrective_Action_Date=date_action)
    details = t_workflow_details.objects.filter(Application_No=application_no)
    details.update(Assigned_To=Team_Leader)
    details.update(Action_Date=date.today())
    details.update(Application_Status='NCF')
    return redirect(resubmit_application)


# Common
def certificate_pending_list(request):
    Login_Id = request.session['email']

    application_details = t_workflow_details.objects.filter(Applicant_Id=Login_Id, Service_Code='OC',
                                                            Action_Date__isnull=True) \
                          | t_workflow_details.objects.filter(Applicant_Id=Login_Id, Service_Code='FPC',
                                                              Action_Date__isnull=True) \
                          | t_workflow_details.objects.filter(Applicant_Id=Login_Id, Service_Code='GAP',
                                                              Action_Date__isnull=True)
    service_details = t_service_master.objects.all()
    return render(request, 'certification_draft_list.html', {'application_details': application_details,
                                                             'service_details': service_details})


def view_certificate_draft_details(request):
    application_no = request.GET.get('application_no')
    service_code = request.GET.get('service_code')

    if service_code == 'GAP':
        application_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
        farmer_group = t_certification_gap_t2.objects.filter(Application_No=application_no)
        crop_production = t_certification_gap_t4.objects.filter(Application_No=application_no)
        pack_house = t_certification_gap_t5.objects.filter(Application_No=application_no)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()

        return render(request, 'GAP_Certification/gap_draft_details.html', {'application_details': application_details,
                                                                            'farmer_group': farmer_group,
                                                                            'crop_production': crop_production,
                                                                            'pack_house': pack_house,
                                                                            'dzongkhag': dzongkhag,
                                                                            'village': village,
                                                                            'gewog': gewog
                                                                            })
    elif service_code == 'OC':
        application_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
        farmer_group = t_certification_organic_t2.objects.filter(Application_No=application_no)
        crop_production = t_certification_organic_t4.objects.filter(Application_No=application_no)
        processing_unit = t_certification_organic_t5.objects.filter(Application_No=application_no)
        wild_collection = t_certification_organic_t6.objects.filter(Application_No=application_no)
        ah_details = t_certification_organic_t7.objects.filter(Application_No=application_no)
        aqua_culture = t_certification_organic_t8.objects.filter(Application_No=application_no)
        api_culture = t_certification_organic_t9.objects.filter(Application_No=application_no)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        return render(request, 'organic_certification/oc_draft_details.html',
                      {'application_details': application_details,
                       'farmer_group': farmer_group,
                       'crop_production': crop_production,
                       'processing_unit': processing_unit,
                       'wild_collection': wild_collection,
                       'ah_details': ah_details,
                       'aqua_culture': aqua_culture,
                       'api_culture': api_culture,
                       'dzongkhag': dzongkhag,
                       'village': village,
                       'gewog': gewog})
    else:
        application_details = t_certification_food_t1.objects.filter(Application_No=application_no)
        farmer_group = t_certification_food_t2.objects.filter(Application_No=application_no)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        unit = t_unit_master.objects.all()
        return render(request, 'food_product_certification/fpc_draft_details.html',
                      {'application_details': application_details,
                       'farmer_group': farmer_group, 'dzongkhag': dzongkhag,
                       'village': village, 'gewog': gewog, 'unit': unit})


def update_food_product_form(request):
    application_no = request.POST.get('application_no')
    application_details = t_certification_food_t1.objects.filter(Application_No=application_no)
    data = dict()
    Firm_Name = request.POST.get('Firm_Name')
    Firm_Address = request.POST.get('Firm_Address')
    Firm_Contact_No = request.POST.get('Firm_Contact_No')
    Firm_Email = request.POST.get('Firm_Email')
    Factory_Name = request.POST.get('Factory_Name')
    Factory_Address = request.POST.get('Factory_Address')
    Factory_Contact_No = request.POST.get('Factory_Contact_No')
    Factory_Email = request.POST.get('Factory_Email')
    Product_Description = request.POST.get('Product_Description')
    Product_Trade_Mark = request.POST.get('Product_Trade_Mark')
    P_From_Date = request.POST.get('P_From_Date')
    P_To_Date = request.POST.get('P_To_Date')
    P_Production = request.POST.get('P_Production')
    P_Production_Unit = request.POST.get('P_Production_Unit')
    P_Production_Value = request.POST.get('P_Production_Value')
    P_Export = request.POST.get('P_Export')
    P_Export_Unit = request.POST.get('P_Export_Unit')
    C_From_Date = request.POST.get('C_From_Date')
    C_To_Date = request.POST.get('C_To_Date')
    C_Production = request.POST.get('C_Production')
    C_Production_Unit = request.POST.get('C_Production_Unit')
    C_Production_Value = request.POST.get('C_Production_Value')
    C_Export = request.POST.get('C_Export')
    C_Export_Unit = request.POST.get('C_Export_Unit')
    C_Export_From_Date = request.POST.get('C_Export_From_Date')
    C_Export_To_Date = request.POST.get('C_Export_To_Date')
    C_Export_Value = request.POST.get('C_Export_Value')
    P_Export_From_Date = request.POST.get('P_Export_From_Date')
    P_Export_To_Date = request.POST.get('P_Export_To_Date')
    P_Export_Value = request.POST.get('P_Export_Value')

    date_from_p = datetime.strptime(P_From_Date, '%d-%m-%Y').date()
    date_to_p = datetime.strptime(P_To_Date, '%d-%m-%Y').date()
    date_from_c = datetime.strptime(C_From_Date, '%d-%m-%Y').date()
    date_to_c = datetime.strptime(C_To_Date, '%d-%m-%Y').date()
    date_export_f = datetime.strptime(C_Export_From_Date, '%d-%m-%Y').date()
    date_export_t = datetime.strptime(C_Export_To_Date, '%d-%m-%Y').date()
    date_export_pf = datetime.strptime(P_Export_From_Date, '%d-%m-%Y').date()
    date_export_pt = datetime.strptime(P_Export_To_Date, '%d-%m-%Y').date()

    application_details.update(
        Application_Date=date.today(),
        Firm_Name=Firm_Name,
        Firm_Address=Firm_Address,
        Firm_Contact_No=Firm_Contact_No,
        Firm_Email=Firm_Email,
        Factory_Name=Factory_Name,
        Factory_Address=Factory_Address,
        Factory_Contact_No=Factory_Contact_No,
        Factory_Email=Factory_Email,
        Product_Description=Product_Description,
        Product_Trade_Mark=Product_Trade_Mark,
        P_From_Date=date_from_p,
        P_To_Date=date_to_p,
        P_Production=P_Production,
        P_Production_Unit=P_Production_Unit,
        P_Production_Value=P_Production_Value,
        P_Export=P_Export,
        P_Export_Unit=P_Export_Unit,
        C_From_Date=date_from_c,
        C_To_Date=date_to_c,
        C_Production=C_Production,
        C_Production_Unit=C_Production_Unit,
        C_Production_Value=C_Production_Value,
        C_Export=C_Export,
        C_Export_Unit=C_Export_Unit,
        Proposed_Standard=None,
        Terms_Bafra_Certification=None,
        Terms_Change_Willingness=None,
        Terms_Abide=None,
        Terms_Agreement=None,
        Acknowledge=None,
        FO_Remarks=None,
        Audit_Team_Leader=None,
        Audit_Team_Acceptance=None,
        Audit_Team_Acceptance_Remarks=None,
        Audit_Plan_Date=None,
        Audit_Plan_Criteria=None,
        Audit_Plan_Type=None,
        Audit_Plan_Scope=None,
        Audit_Plan_Acceptance=None,
        Audit_Plan_Acceptance_Remarks=None,
        Audit_Date=None,
        Audit_Findings_Site_History_OE=None,
        Audit_Findings_Water_Source_OE=None,
        Audit_Findings_Product_Quality_OE=None,
        Audit_Findings_Harvesting_OE=None,
        Audit_Findings_Equipment_OE=None,
        Audit_Findings_Manufacturing_Production_OE=None,
        Audit_Findings_Sampling_Testing_OE=None,
        Audit_Findings_Packing_Marking_OE=None,
        Audit_Findings_Storage_Transport_OE=None,
        Audit_Findings_Traceability_OE=None,
        Audit_Findings_Worker_Health_OE=None,
        Audit_Findings_Group_Requirement_OE=None,
        Audit_Findings_Others_OE=None,
        Audit_Findings_Site_History_Observations=None,
        Audit_Findings_Water_Source_Observations=None,
        Audit_Findings_Product_Quality_Observations=None,
        Audit_Findings_Harvesting_Observations=None,
        Audit_Findings_Equipment_Observations=None,
        Audit_Findings_Manufacturing_Production_Observations=None,
        Audit_Findings_Sampling_Testing_Observations=None,
        Audit_Findings_Packing_Marking_Observations=None,
        Audit_Findings_Storage_Transport_Observations=None,
        Audit_Findings_Traceability_Observations=None,
        Audit_Findings_Worker_Health_Observations=None,
        Audit_Findings_Group_Requirement_Observations=None,
        Audit_Findings_Others_Observations=None,
        Approve_Date=None,
        Certificate_No=None,
        Validity_Period=None,
        Validity=None,
        Applicant_Id=request.session['email'],
        Audit_Type=None,
        C_Export_From_Date=date_export_f,
        C_Export_To_Date=date_export_t,
        C_Export_Value=C_Export_Value,
        P_Export_From_Date=date_export_pf,
        P_Export_To_Date=date_export_pt,
        P_Export_Value=P_Export_Value,
        Others_Standards=None,
        Terms_Standards=None
    )
    data['applNo'] = application_no
    return JsonResponse(data)


def update_oc_form(request):
    data = dict()
    application_no = request.POST.get('application_no')
    application_details = t_certification_organic_t1.objects.filter(Application_No=application_no)
    Applicant_Type = request.POST.get('Applicant_Type')
    if Applicant_Type == 'I':
        cid = request.POST.get('cid')
        Name = request.POST.get('Name')
        Farmer_Group_No = None
        Farmer_Group_name = None
    else:
        cid = None
        Name = None
        Farmer_Group_No = request.POST.get('farmers_group_name')
        Farmer_Group_name = request.POST.get('farmers_group_number')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    address = request.POST.get('address')
    farm_location = request.POST.get('farm_location')
    farm_name = request.POST.get('farm_name')
    application_details.update(
        Application_Date=None,
        Application_Type=Applicant_Type,
        CID=cid,
        Applicant_Name=Name,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Present_Address=address,
        Contact_No=contact_number,
        Email=email,
        Farmer_Group_No=Farmer_Group_No,
        Farmer_Group_Name=Farmer_Group_name,
        Crop_Production=None,
        Wild_Collection=None,
        Animal_Husbandry=None,
        Aquaculture=None,
        Apiculture=None,
        Processing_Unit=None,
        Proposed_Standard=None,
        Terms_Bafra_Certification=None,
        Terms_Change_Willingness=None,
        Terms_Abide=None,
        Terms_Agreement=None,
        FO_Remarks=None,
        Acknowledge=None,
        Audit_Team_Leader=None,
        Audit_Team_Acceptance=None,
        Audit_Team_Acceptance_Remarks=None,
        Audit_Plan_Date=None,
        Audit_Plan_Criteria=None,
        Audit_Plan_Type=None,
        Audit_Plan_Scope=None,
        Audit_Plan_Acceptance=None,
        Audit_Plan_Acceptance_Remarks=None,
        Audit_Date=None,
        Audit_Findings_Site_History_OE=None,
        Audit_Findings_Water_Source_OE=None,
        Audit_Findings_Product_Quality_OE=None,
        Audit_Findings_Harvesting_OE=None,
        Audit_Findings_Equipment_OE=None,
        Audit_Findings_Manufacturing_Production_OE=None,
        Audit_Findings_Sampling_Testing_OE=None,
        Audit_Findings_Packing_Marking_OE=None,
        Audit_Findings_Storage_Transport_OE=None,
        Audit_Findings_Traceability_OE=None,
        Audit_Findings_Worker_Health_OE=None,
        Audit_Findings_Group_Requirement_OE=None,
        Audit_Findings_Others_OE=None,
        Audit_Findings_Site_History_Observations=None,
        Audit_Findings_Water_Source_Observations=None,
        Audit_Findings_Product_Quality_Observations=None,
        Audit_Findings_Harvesting_Observations=None,
        Audit_Findings_Equipment_Observations=None,
        Audit_Findings_Manufacturing_Production_Observations=None,
        Audit_Findings_Sampling_Testing_Observations=None,
        Audit_Findings_Packing_Marking_Observations=None,
        Audit_Findings_Storage_Transport_Observations=None,
        Audit_Findings_Traceability_Observations=None,
        Audit_Findings_Worker_Health_Observations=None,
        Audit_Findings_Group_Requirement_Observations=None,
        Audit_Findings_Others_Observations=None,
        Approve_Date=None,
        Certificate_No=None,
        Validity_Period=None,
        Validity=None,
        Farm_Location=farm_location,
        Applicant_Id=request.session['email'],
        Farm_Name=farm_name,
        Audit_Type=None,
        Others_Standards=None,
        Terms_Standards=None
    )
    data['Applicant_Type'] = Applicant_Type
    data['applNo'] = application_no
    return JsonResponse(data)


def update_gap_form(request):
    data = dict()
    application_no = request.POST.get('application_no')
    application_details = t_certification_gap_t1.objects.filter(Application_No=application_no)
    Applicant_Type = request.POST.get('Applicant_Type')
    if Applicant_Type == 'I':
        cid = request.POST.get('cid')
        Name = request.POST.get('Name')
        Farmer_Group_No = None
        Farmer_Group_name = None
    else:
        cid = None
        Name = None
        Farmer_Group_No = request.POST.get('farmers_group_name')
        Farmer_Group_name = request.POST.get('farmers_group_number')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    address = request.POST.get('address')
    farm_location = request.POST.get('farm_location')
    farm_name = request.POST.get('farm_name')

    application_details.update(
        Application_Date=date.today(),
        Application_Type=Applicant_Type,
        CID=cid,
        Applicant_Name=Name,
        Dzongkhag_Code=dzongkhag,
        Gewog_Code=gewog,
        Village_Code=village,
        Present_Address=address,
        Contact_No=contact_number,
        Email=email,
        Farmer_Group_No=Farmer_Group_No,
        Farmer_Group_Name=Farmer_Group_name,
        Pack_House=None,
        Crop_Production=None,
        Proposed_Standard=None,
        Terms_Bafra_Certification=None,
        Terms_Change_Willingness=None,
        Terms_Abide=None,
        Terms_Agreement=None,
        Acknowledge=None,
        FO_Remarks=None,
        Audit_Team_Leader=None,
        Audit_Team_Acceptance=None,
        Audit_Team_Acceptance_Remarks=None,
        Audit_Plan_Date=None,
        Audit_Plan_Criteria=None,
        Audit_Plan_Type=None,
        Audit_Plan_Scope=None,
        Audit_Plan_Acceptance=None,
        Audit_Plan_Acceptance_Remarks=None,
        Audit_Date=None,
        Audit_Findings_Site_History_OE=None,
        Audit_Findings_Water_Source_OE=None,
        Audit_Findings_Product_Quality_OE=None,
        Audit_Findings_Harvesting_OE=None,
        Audit_Findings_Equipment_OE=None,
        Audit_Findings_Manufacturing_Production_OE=None,
        Audit_Findings_Sampling_Testing_OE=None,
        Audit_Findings_Packing_Marking_OE=None,
        Audit_Findings_Storage_Transport_OE=None,
        Audit_Findings_Traceability_OE=None,
        Audit_Findings_Worker_Health_OE=None,
        Audit_Findings_Group_Requirement_OE=None,
        Audit_Findings_Others_OE=None,
        Audit_Findings_Site_History_Observations=None,
        Audit_Findings_Water_Source_Observations=None,
        Audit_Findings_Product_Quality_Observations=None,
        Audit_Findings_Harvesting_Observations=None,
        Audit_Findings_Equipment_Observations=None,
        Audit_Findings_Manufacturing_Production_Observations=None,
        Audit_Findings_Sampling_Testing_Observations=None,
        Audit_Findings_Packing_Marking_Observations=None,
        Audit_Findings_Storage_Transport_Observations=None,
        Audit_Findings_Traceability_Observations=None,
        Audit_Findings_Worker_Health_Observations=None,
        Audit_Findings_Group_Requirement_Observations=None,
        Audit_Findings_Others_Observations=None,
        Approve_Date=None,
        Certificate_No=None,
        Validity_Period=None,
        Validity=None,
        Farm_Location=farm_location,
        Applicant_Id=request.session['email'],
        Farm_Name=farm_name,
        Audit_Type=None,
        Others_Standards=None,
        Terms_Standards=None
    )
    data['Applicant_Type'] = Applicant_Type
    data['applNo'] = application_no
    return JsonResponse(data)


def update_payment(application_no, permit_no, service_code, validity_date):
    t_payment_details.objects.create(Application_No=application_no,
                                     Application_Date=date.today(),
                                     Permit_No=permit_no,
                                     Service_Id=service_code,
                                     Validity=validity_date,
                                     Payment_Type=None,
                                     Instrument_No=None,
                                     Amount=None,
                                     Receipt_No=None,
                                     Receipt_Date=None,
                                     Updated_By=None,
                                     Updated_On=None)


def date_month(request):
    date1 = request.GET.get('from_date')
    date2 = request.GET.get('to_date')
    d1 = datetime.strptime(date1, "%d-%m-%Y").date()
    d2 = datetime.strptime(date2, "%d-%m-%Y").date()
    month_list = [i.strftime("%B") for i in pd.date_range(start=d1, end=d2, freq='MS')]
    return render(request, 'GAP_Certification/month_list.html', {'month_list': month_list})
