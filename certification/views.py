from django.core.mail import send_mail
from django.db.models import Max
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
# Organic Certificate.
from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_country_master, \
    t_field_office_master, t_location_field_office_mapping, t_unit_master, t_user_master
from bbfss import settings
from certification.models import t_certification_Food_t2, t_certification_Organic_t2, t_certification_Organic_t4, \
    t_certification_Organic_t6, t_certification_Organic_t7, t_certification_Organic_t8, t_certification_Organic_t5, \
    t_certification_Organic_t9, t_certification_Organic_t1, t_certification_GAP_t5, t_certification_GAP_t4, \
    t_certification_Organic_t3, t_certification_GAP_t1
from plant.models import t_file_attachment, t_workflow_details

# Organic Certification
from plant.views import focal_officer_application


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

    t_certification_Organic_t1.objects.create(
        Application_No=organic_certificate_app_no,
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
        Audit_Findings_Site_History=None,
        Audit_Findings_Water_Source=None,
        Audit_Findings_Product_Quality=None,
        Audit_Findings_Harvesting=None,
        Audit_Findings_Equipment=None,
        Audit_Findings_Manufacturing_Production=None,
        Audit_Findings_Sampling_Testing=None,
        Audit_Findings_Packing_Marking=None,
        Audit_Findings_Storage_Transport=None,
        Audit_Findings_Traceability=None,
        Audit_Findings_Worker_Health=None,
        Audit_Findings_Group_Requirement=None,
        Audit_Findings_Others=None,
        Feasibility_Inspection_Date=None,
        Feasibility_Inspection_Conformity=None,
        Feasibility_Inspection_Remarks=None,
        Factory_Inspection_Date=None,
        Factory_Inspection_Conformity=None,
        Factory_Inspection_Remarks=None,
        Approve_Date=None,
        Certificate_No=None,
        Validity_Period=None,
        Validity=None,
        Farm_Location=farm_location
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
    last_application_no = t_certification_Organic_t1.objects.aggregate(Max('Application_No'))
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
    farmers_group_details = t_certification_Organic_t2.objects.filter(Application_No=application_no, CID=cid, Name=name)
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

    crop_production_details = t_certification_Organic_t4.objects.create(
        Application_No=application_no,
        Crop_Name=crop_name,
        Area_Cultivated=area,
        Unit=area_unit,
        P_From_Date=prev_year,
        P_To_Date=to_year,
        P_Yield=yields,
        P_Yield_Unit=Yield_Unit,
        P_Harvest_Month=harvest_month,
        P_Sold=sold,
        P_Balance_Stock=balance_stock,
        C_From_Date=current_year,
        C_To_Date=to_current_year,
        C_Estimated_Yield=estimated_yield,
        C_Yield_Unit=estimated_Yield_Unit,
        C_Harvest_Month=estimated_harvest_month)
    return render(request, 'organic_certification/crop_production_details.html',
                  {'crop_production_details': crop_production_details})


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

    crop_production_details = t_certification_Organic_t6.objects.filter(
        Application_No=application_no,
        Common_Name=common_name,
        Botanical_Name=botanical_name,
        Plant_Part=part_of_plant,
        Estimated_Harvest=estimated_harvest,
        Harvest_Unit=estimated_harvest_Yield_Unit,
        Harvest_Season=harvest_season,
        Harvest_Acreage=harvest_acreage,
        Acreage_Unit=harvest_Unit)
    return render(request, 'organic_certification/farmers_group_details.html',
                  {'crop_production_details': crop_production_details})


def save_animal_husbandry_details(request):
    application_no = request.POST.get('animal_husbandry_application_no')
    livestock_type = request.POST.get('livestock_type')
    male = request.POST.get('male')
    female = request.POST.get('female')
    estimated_production = request.POST.get('estimated_production')
    estimated_production_Unit = request.POST.get('estimated_production_Unit')
    product_sold = request.POST.get('product_sold')

    crop_production_details = t_certification_Organic_t7.objects.filter(
        Application_No=application_no,
        Livestock_Type=livestock_type,
        Male_no=male,
        Female_no=female,
        Estimated_Production=estimated_production,
        Production_Unit=estimated_production_Unit,
        Production_Sold=product_sold)
    return render(request, 'organic_certification/animal_husbandry_details.html',
                  {'crop_production_details': crop_production_details})


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

    crop_production_details = t_certification_Organic_t8.objects.filter(
        Application_No=application_no,
        Aquaculture_Type=Aquaculture_type,
        Estimated_Yield=Aquaculture_Yield,
        Estimated_Yield_Unit=Aquaculture_Yield_Unit,
        Harvest_Month=aqua_harvest_month,
        Sold=aqua_Sold,
        Sold_Unit=aqua_Sold_unit,
        Balance_Stock=stock_balance,
        Balance_Stock_Unit=stock_balance_unit)
    return render(request, 'organic_certification/farmers_group_details.html',
                  {'crop_production_details': crop_production_details})


def save_api_culture_details(request):
    application_no = request.POST.get('api_culture_application_no')
    api_common_name = request.POST.get('api_common_name')
    api_botanical_name = request.POST.get('api_botanical_name')
    api_estimated_harvest = request.POST.get('api_estimated_harvest')
    api_estimated_harvest_Yield_Unit = request.POST.get('api_estimated_harvest_Yield_Unit')
    api_harvest_acreage = request.POST.get('api_harvest_acreage')
    api_Unit = request.POST.get('api_Unit')

    apiculture_details = t_certification_Organic_t9.objects.create(
        Application_No=application_no,
        Common_Name=api_common_name,
        Botanical_Name=api_botanical_name,
        Estimated_Harvest=api_estimated_harvest,
        Harvest_Unit=api_estimated_harvest_Yield_Unit,
        Harvest_Acreage=api_harvest_acreage,
        Acreage_Unit=api_Unit)
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

    crop_production_details = t_certification_Organic_t5.objects.create(
        Application_No=application_no,
        Production_House_Name=processing_name,
        Production_House_Address=address_of_Operation,
        Processing_Type=processing_type,
        P_From_Date=from_date,
        P_To_Date=to_date,
        P_Production=production,
        P_Production_Unit=production_unit,
        P_Sold=processing_Sold,
        P_Balance_Stock=processing_balance,
        C_From_Date=current_from_date,
        C_To_Date=current_to_date,
        C_Production=current_production,
        C_Production_Unit=current_production_unit,
        C_Sold=current_processing_Sold,
        C_Balance_Stock=current_processing_balance)
    return render(request, 'organic_certification/processing_unit_details.html',
                  {'crop_production_details': crop_production_details})


def submit_organic_certificate(request):
    application_no = request.POST.get('application_no')
    Terms_Bafra_Certification = request.POST.get('Terms_Bafra_Certification')
    Terms_Change_Willingness = request.POST.get('Terms_Change_Willingness')
    Terms_Abide = request.POST.get('Terms_Abide')
    Terms_Agreement = request.POST.get('Terms_Agreement')
    app_details = t_certification_Organic_t1.objects.filter(Application_No=application_no)
    app_details.update(Terms_Bafra_Certification=Terms_Bafra_Certification)
    app_details.update(Terms_Change_Willingness=Terms_Change_Willingness)
    app_details.update(Terms_Abide=Terms_Abide)
    app_details.update(Terms_Agreement=Terms_Agreement)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(gap_certificate)


def add_audit_team_details(request):
    application_no = request.GET.get('application_id')
    audit_team_member = request.GET.get('name')

    details = t_user_master.objects.filter(Login_Id=audit_team_member)
    for name in details:
        app_name = name.Name
        t_certification_Organic_t3.objects.create(Application_No=application_no, Login_Id=audit_team_member,
                                                  Name=app_name)
    audit_team = t_certification_Organic_t3.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/audit_team_details.html',
                  {'audit_team': audit_team})


def send_acknowledge(request):
    application_no = request.POST.get('application_no')
    app_details = t_certification_Organic_t1.objects.filter(Application_No=application_no)
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
    app_details = t_certification_Organic_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    app_details.update(Audit_Team_Leader=audit_team_leader)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='AT')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assign_To=login)
    return redirect(focal_officer_application)


def accept_reject_audit_team(request):
    application_no = request.POST.get('application_id')
    acceptance = request.POST.get('acceptance')
    remarks = request.POST.get('remarks')
    app_details = t_certification_Organic_t1.objects.filter(Application_No=application_no)
    app_details.update(Audit_Team_Acceptance=acceptance)
    app_details.update(Audit_Team_Acceptance_Remarks=remarks)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id='2')
    workflow_details.update(Action_Date=date.today())


def forward_application_team_leader(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Application_Status='P')
    app_details = t_certification_Organic_t1.objects.filter(Application_No=application_no)
    for app in app_details:
        team_leader = app.Audit_Team_Leader
    workflow_details.update(Assigned_To=team_leader)


def approve_application(request):
    application_no = request.POST.get('application_no')
    remarks = request.POST.get('remarks')
    app_details = t_certification_Organic_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='A')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assign_To=login)
    return redirect(focal_officer_application)


def resubmit_application(request):
    application_no = request.POST.get('application_no')
    remarks = request.POST.get('remarks')
    app_details = t_certification_Organic_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='AT')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assign_To=login)
    return redirect(focal_officer_application)


# audit_plan_acceptance
def send_audit_plan_acceptance(request):
    application_no = request.POST.get('application_no')
    remarks = request.POST.get('remarks')
    app_details = t_certification_Organic_t1.objects.filter(Application_No=application_no)
    app_details.update(FO_Remarks=remarks)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Assigned_Role_Id=None)
    workflow_details.update(Application_Status='AP')
    for email_id in workflow_details:
        email = email_id.Applicant_Id
        user_details = t_user_master.objects.filter(Email_Id=email)
        for user in user_details:
            login = user.Login_Id
            workflow_details.update(Assign_To=login)
    return redirect(gap_certificate)


# gap_certificate
def gap_certificate(request):
    return render(request, 'GAP_Certification/apply_gap_certification.html')


def save_gap_certificate(request):
    data = dict()
    service_code = "OC"
    gap_certificate_app_no = get_gap_certificate_app_no(request, service_code)
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
        Audit_Findings_Site_History=None,
        Audit_Findings_Water_Source=None,
        Audit_Findings_Product_Quality=None,
        Audit_Findings_Harvesting=None,
        Audit_Findings_Equipment=None,
        Audit_Findings_Manufacturing_Production=None,
        Audit_Findings_Sampling_Testing=None,
        Audit_Findings_Packing_Marking=None,
        Audit_Findings_Storage_Transport=None,
        Audit_Findings_Traceability=None,
        Audit_Findings_Worker_Health=None,
        Audit_Findings_Group_Requirement=None,
        Audit_Findings_Others=None,
        Feasibility_Inspection_Date=None,
        Feasibility_Inspection_Conformity=None,
        Feasibility_Inspection_Remarks=None,
        Factory_Inspection_Date=None,
        Factory_Inspection_Conformity=None,
        Factory_Inspection_Remarks=None,
        Approve_Date=None,
        Certificate_No=None,
        Validity_Period=None,
        Validity=None,
        Farm_Location=farm_location
    )

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


def gap_farmers_group_details(request):
    application_no = request.POST.get('farmers_group_application_no')
    cid = request.POST.get('farmers_group_cid')
    name = request.POST.get('farmers_group_fullname')
    farmers_group_details = t_certification_Organic_t2.objects.filter(Application_No=application_no, CID=cid, Name=name)
    return render(request, 'organic_certification/farmers_group_details.html',
                  {'farmers_group_details': farmers_group_details})


def gap_crop_production_details(request):
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

    t_certification_GAP_t4.objects.create(
        Application_No=application_no,
        Crop_Name=crop_name,
        Area_Cultivated=area,
        Unit=area_unit,
        P_From_Date=prev_year,
        P_To_Date=to_year,
        P_Yield=yields,
        P_Yield_Unit=Yield_Unit,
        P_Harvest_Month=harvest_month,
        P_Sold=sold,
        P_Balance_Stock=balance_stock,
        C_From_Date=current_year,
        C_To_Date=to_current_year,
        C_Estimated_Yield=estimated_yield,
        C_Yield_Unit=estimated_Yield_Unit,
        C_Harvest_Month=estimated_harvest_month)

    crop_production_details = t_certification_GAP_t4.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/crop_production_details.html',
                  {'crop_production_details': crop_production_details})


def get_gap_certificate_app_no(request, service_code):
    last_application_no = t_certification_GAP_t1.objects.aggregate(Max('Application_No'))
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
    application_no = request.POST.get('packhouse_application_no')
    pack_house_details = t_certification_GAP_t5.objects.filter(Application_No=application_no)
    return render(request, 'organic_certification/crop_production_details.html',
                  {'packhouse_details': pack_house_details})


def submit_gap_certificate(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(gap_certificate)


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
    return JsonResponse(data)


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
    return render(request, 'GAP_Certification/file_attachment.html', {'file_attach': file_attach})


def submit_food_product_certificate(request):
    application_no = request.POST.get('application_no')
    workflow_details = t_workflow_details.objects.filter(Application_No=application_no)
    workflow_details.update(Action_Date=date.today())
    return redirect(gap_certificate)
