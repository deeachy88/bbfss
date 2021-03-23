from datetime import date

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_location_field_office_mapping, \
    t_user_master, t_field_office_master, t_plant_crop_master, t_plant_pesticide_master, t_plant_crop_variety_master, \
    t_service_master
from bbfss import settings
from plant.forms import ImportFormThree, ImportFormTwo
from plant.models import t_workflow_details, t_plant_movement_permit_t2, t_plant_movement_permit_t1, \
    t_plant_movement_permit_t3, t_file_attachment, t_plant_import_permit_t1, t_plant_import_permit_t2, \
    t_plant_import_permit_t3


def focal_officer_application(request):
    Role_Id = request.session['Role_Id']
    application_details = t_workflow_details.objects.filter(Assigned_Role_Id=Role_Id, Section='Plant',
                                                            Application_Status='P')
    return render(request, 'focal_officer_pending_list.html', {'new_import_app': application_details})


def oic_application(request):
    Field_Office_Id = request.session['field_office_id']
    Role_Id = request.session['Role_Id']
    application_details = t_workflow_details.objects.filter(Assigned_Role_Id=Role_Id, Field_Office_Id=Field_Office_Id,
                                                            Application_Status='A')
    return render(request, 'oic_pending_list.html', {'application_details': application_details})


def inspector_application(request):
    Login_Id = request.session['login_id']
    new_import_app = t_workflow_details.objects.filter(Assigned_Role_Id='5', Assigned_To=Login_Id,
                                                       Application_Status='A')
    if new_import_app.exists():
        for service_code in new_import_app:
            code = service_code.Service_Code
        service = t_service_master.objects.filter(Service_Code=code)
        for service in service:
            service_name = service.Service_Name
    else:
        service_name = None
    return render(request, 'inspector_pending_list.html',
                  {'service_name': service_name, 'application_details': new_import_app})


def apply_movement_permit(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'apply_movement_permit.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def save_details(request):
    if request.method == 'POST':
        commodity = request.POST['commodity']
        appNo = request.POST['appNo']
        qty = request.POST['qty']
        remarks = request.POST['remarks']
        t_plant_movement_permit_t2.objects.create(Application_No=appNo, Commodity=commodity,
                                                  Qty=qty,
                                                  Remarks=remarks)
        imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=appNo)
    return render(request, 'apply_movement_permit_page.html', {'import': imports_plant, 'title': appNo})


def save_movement_permit(request):
    data = dict()
    service_code = "MPP"
    last_application_no = get_application_no(request, service_code)

    Applicant_Id = request.session['email']
    permitType = request.POST.get('permitType')
    regNo = request.POST.get('regNo')
    companyName = request.POST.get('companyName')
    cid = request.POST.get('cid')
    Name = request.POST.get('Name')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location_code = request.POST.get('location_code')
    fromDzongkhag = request.POST.get('fromDzongkhag')
    toDzongkhag = request.POST.get('toDzongkhag')
    route = request.POST.get('route')
    productSource = request.POST.get('productSource')
    movementPurpose = request.POST.get('movementPurpose')
    conveyanceMeans = request.POST.get('conveyanceMeans')

    mfdUnit_regNo = request.POST.get('mfdUnit_regNo')
    appcid = request.POST.get('appcid')
    appName = request.POST.get('appName')
    phoneNumber = request.POST.get('phoneNumber')
    emailId = request.POST.get('emailId')
    location = request.POST.get('location')
    from_Dzongkhag = request.POST.get('from_Dzongkhag')
    Dzongkhag_to = request.POST.get('Dzongkhag_to')
    auth_route = request.POST.get('auth_route')
    Origin = request.POST.get('Origin')
    Purpose = request.POST.get('Purpose')
    convMeans = request.POST.get('convMeans')
    agroName = request.POST.get('agroName')
    vehicleNo = request.POST.get('vehicleNo')
    mov_date = request.POST.get('date')

    if permitType == "P":
        t_plant_movement_permit_t1.objects.create(
            Application_No=last_application_no,
            Permit_Type=permitType,
            License_No=regNo,
            Nursery_Name=companyName,
            CID=cid,
            Applicant_Name=Name,
            Contact_No=contact_number,
            Email=email,
            Dzongkhag_Code=dzongkhag,
            Gewog_Code=gewog,
            Village_Code=village,
            Location_Code=location_code,
            From_Dzongkhag_Code=fromDzongkhag,
            To_Dzongkhag_Code=toDzongkhag,
            Authorized_Route=route,
            Source_Of_Product=productSource,
            Movement_Purpose=movementPurpose,
            Conveyance_Means=conveyanceMeans,
            Name_And_Description=None,
            Vehicle_No=None,
            Movement_Date=None,
            Inspection_Date=None,
            Inspection_Leader=None,
            Inspection_Team=None,
            Application_Status='P',
            Movement_Permit_No=None,
            Remarks=None,
            Application_Date=None,
            Applicant_Id=Applicant_Id
        )
        field_id = t_location_field_office_mapping.objects.filter(pk=location_code)
    else:
        t_plant_movement_permit_t1.objects.create(
            Application_No=last_application_no,
            Permit_Type=permitType,
            License_No=mfdUnit_regNo,
            Nursery_Name=None,
            CID=appcid,
            Applicant_Name=appName,
            Contact_No=phoneNumber,
            Email=emailId,
            Dzongkhag_Code=None,
            Gewog_Code=None,
            Village_Code=None,
            Location_Code=location,
            From_Dzongkhag_Code=from_Dzongkhag,
            To_Dzongkhag_Code=Dzongkhag_to,
            Authorized_Route=auth_route,
            Source_Of_Product=Origin,
            Movement_Purpose=Purpose,
            Conveyance_Means=convMeans,
            Name_And_Description=agroName,
            Vehicle_No=vehicleNo,
            Movement_Date=mov_date,
            Inspection_Date=None,
            Inspection_Leader=None,
            Inspection_Team=None,
            Application_Status='P',
            Movement_Permit_No=None,
            Remarks=None,
            Application_Date=None,
            Applicant_Id=Applicant_Id
        )
        field_id = t_location_field_office_mapping.objects.filter(pk=location)
    for field_office in field_id:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(Application_No=last_application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=field_office_id, Section='Plant',
                                      Assigned_Role_Id='4',
                                      Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applicationNo'] = last_application_no
    return JsonResponse(data)


def get_application_no(request, service_code):
    last_application_no = t_plant_movement_permit_t1.objects.aggregate(Max('Application_No'))
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


def movement_permit_app(request):
    appNo = request.GET.get('appId')
    imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=appNo)
    return render(request, 'apply_movement_permit_page.html', {'import': imports_plant, 'title': appNo})


def load_details_page(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    return render(request, 'movement_permit_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location': location})


def update_application_details(request):
    application_id = request.POST.get('applicationNo')
    regNo = request.POST.get('regNo')
    companyName = request.POST.get('companyName')
    cid = request.POST.get('cid')
    Name = request.POST.get('Name')
    contact_number = request.POST.get('contactNumber')
    email = request.POST.get('email')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location_code = request.POST.get('location_code')
    fromDzongkhag = request.POST.get('fromDzongkhag')
    toDzongkhag = request.POST.get('toDzongkhag')
    route = request.POST.get('route')
    productSource = request.POST.get('productSource')
    movementPurpose = request.POST.get('movementPurpose')
    conveyanceMeans = request.POST.get('conveyanceMeans')

    application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    application_details.update(License_No=regNo)
    application_details.update(Nursery_Name=companyName)
    application_details.update(CID=cid)
    application_details.update(Applicant_Name=Name)
    application_details.update(Contact_No=contact_number)
    application_details.update(Email=email)
    application_details.update(Dzongkhag_Code=dzongkhag)
    application_details.update(Gewog_Code=gewog)
    application_details.update(Village_Code=village)
    application_details.update(Location_Code=location_code)
    application_details.update(From_Dzongkhag_Code=fromDzongkhag)
    application_details.update(To_Dzongkhag_Code=toDzongkhag)
    application_details.update(Authorized_Route=route)
    application_details.update(Source_Of_Product=productSource)
    application_details.update(Movement_Purpose=movementPurpose)
    application_details.update(Conveyance_Means=conveyanceMeans)

    t_workflow_details.objects.filter(Application_No=application_id)
    field_id = t_location_field_office_mapping.objects.filter(pk=location_code)
    for application in field_id:
        Field_Office = application.Field_Office_Id
    field_id.update(Field_Office_Id=Field_Office)
    field_id.update(Action_Date=date.today())
    imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=application_id)
    return render(request, 'apply_movement_permit.html', {'import': imports_plant, 'title': application_id})


def save(request):
    if request.method == 'POST':
        commodity = request.POST['commodity']
        appNo = request.POST['appNo']
        qty = request.POST['qty']
        remarks = request.POST['remarks']
        t_plant_movement_permit_t2.objects.create(Application_No=appNo, Commodity=commodity,
                                                  Qty=qty, Remarks=remarks)
        imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=appNo)
    return render(request, 'movement_page.html', {'import': imports_plant, 'title': appNo})


def forward_application(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')

    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Assigned_To=forwardTo)
    application_details.update(Action_Date=date.today())
    Field_Office_Id = request.session['field_office_id']
    Role_Id = request.session['Role_Id']
    new_movement_app = t_workflow_details.objects.filter(Assigned_To=Role_Id, Field_Office_Id=Field_Office_Id)
    return render(request, 'new_movement_permit.html', {'new_movement_app': new_movement_app})


def view_application_details(request):
    application_id = request.GET.get('application_id')
    service_code = request.GET.get('service_code')

    if service_code == 'MPP':
        application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_movement_permit_t2.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        movement_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)

        return render(request, 'app_details_inspector.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'inspector_list': user_role_list, 'movement_permit': movement_permit})

    elif service_code == 'IPP':
        application_details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
        location = t_field_office_master.objects.all()
        details_list = t_plant_import_permit_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        import_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)
        return render(request, 'import_permit/inspector_import_permit.html',
                      {'application_details': application_details,
                       'location': location, 'import': details_list, 'inspector_list': user_role_list,
                       'file': file, 'import_permit': import_permit})


def approve_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    permit_no = get_permit_no(request)
    details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=dateOfInspection)
    details.update(Movement_Permit_No=permit_no)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')

    return render(request, 'application_details.html', {'application_details': application_details})


def reject_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')

    details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=dateOfInspection)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='R')
    return render(request, 'application_details.html', {'application_details': application_details})


def add_details_ins(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_movement_permit_t3.objects.create(Application_No=application_id,
                                              Current_Observation=currentObservation,
                                              Decision_Conformity=decisionConform)
    movement_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)
    return render(request, 'add_application_details.html', {'movement_permit': movement_permit})


def get_permit_no(request):
    global Field_Code
    Field_Office_Id = request.session['Field_Office_Id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_application_no = t_plant_movement_permit_t1.objects.aggregate(Max('Movement_Permit_No'))
    lastAppNo = last_application_no['Movement_Permit_No__max']
    if not lastAppNo:
        year = timezone.now().year
        newAppNo = Field_Code + "MPP" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(lastAppNo)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newAppNo = Field_Code + "MPP" + "/" + str(year) + "/" + AppNo
    return newAppNo


def add_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments/plant/movement_permit" + str(timezone.now().year))
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def add_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'file_attachment_page.html', {'file_attach': file_attach})


def delete_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit")
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'file_attachment_page.html', {'file_attach': file_attach})


# import permit
def apply_import_permit(request):
    crop = t_plant_crop_master.objects.all()
    pesticide = t_plant_pesticide_master.objects.all()
    variety = t_plant_crop_variety_master.objects.all()
    location = t_field_office_master.objects.all()

    return render(request, 'import_permit/apply_import_permit.html',
                  {'crop': crop, 'pesticide': pesticide, 'variety': variety,
                   'location': location})


def save_import_permit(request):
    data = dict()
    service_code = "IPP"
    last_application_no = get_import_application_no(request, service_code)

    Applicant_Id = request.session['email']
    importType = request.POST.get('importType')

    regNo = request.POST.get('p_regNo')
    companyName = request.POST.get('p_businessName')
    presentAddress = request.POST.get('p_presentAddress')
    cid = request.POST.get('p_cid_number')
    Name = request.POST.get('p_Name')
    contact_number = request.POST.get('p_contactNo')
    email = request.POST.get('p_email')
    supplier = request.POST.get('p_supplier')
    conveyanceMeans = request.POST.get('p_conveyanceMeans')
    entry_place = request.POST.get('p_entry_point')
    movementPurpose = request.POST.get('p_movementPurpose')
    finalDestination = request.POST.get('p_final_Destination')
    expectedDate = request.POST.get('p_expected_arrival_date')

    a_regNo = request.POST.get('a_regNo')
    a_businessName = request.POST.get('a_businessName')
    a_presentAddress = request.POST.get('a_presentAddress')
    a_cid_number = request.POST.get('a_cid_number')
    a_Name = request.POST.get('a_Name')
    a_contactNo = request.POST.get('a_contactNo')
    a_email = request.POST.get('a_email')
    a_supplier = request.POST.get('a_supplier')
    a_conveyanceMeans = request.POST.get('a_conveyanceMeans')
    a_entry_point = request.POST.get('a_entry_point')
    a_movementPurpose = request.POST.get('a_movementPurpose')
    a_final_Destination = request.POST.get('a_final_Destination')
    a_expected_arrival_date = request.POST.get('a_expected_arrival_date')

    if importType == "P":
        t_plant_import_permit_t1.objects.create(
            Application_No=last_application_no,
            Import_Type=importType,
            License_No=regNo,
            Business_Name=companyName,
            CID=cid,
            Applicant_Name=Name,
            Present_Address=presentAddress,
            Contact_No=contact_number,
            Email=email,
            Name_And_Address_Supplier=supplier,
            Means_of_Conveyance=conveyanceMeans,
            Place_Of_Entry=entry_place,
            Purpose=movementPurpose,
            Final_Destination=finalDestination,
            Import_Inspection_Submit_Date=None,
            Proposed_Inspection_Date=None,
            Actual_Point_Of_Entry=None,
            Inspection_Request_Remarks=None,
            Import_Permit_No=None,
            Inspection_Date=None,
            Inspection_Type=None,
            Inspection_Time=None,
            Inspection_Leader=None,
            Inspection_Team=None,
            Clearance_Ref_No=None,
            Expected_Arrival_Date=expectedDate,
            FO_Remarks=None,
            Inspection_Remarks=None
        )
    else:
        t_plant_import_permit_t1.objects.create(
            Application_No=last_application_no,
            Import_Type=importType,
            License_No=a_regNo,
            Business_Name=a_businessName,
            CID=a_cid_number,
            Applicant_Name=a_Name,
            Present_Address=a_presentAddress,
            Contact_No=a_contactNo,
            Email=a_email,
            Name_And_Address_Supplier=a_supplier,
            Means_of_Conveyance=a_conveyanceMeans,
            Place_Of_Entry=a_entry_point,
            Purpose=a_movementPurpose,
            Final_Destination=a_final_Destination,
            Import_Inspection_Submit_Date=None,
            Proposed_Inspection_Date=None,
            Actual_Point_Of_Entry=None,
            Inspection_Request_Remarks=None,
            Import_Permit_No=None,
            Inspection_Date=None,
            Inspection_Type=None,
            Inspection_Time=None,
            Inspection_Leader=None,
            Inspection_Team=None,
            Clearance_Ref_No=None,
            Expected_Arrival_Date=a_expected_arrival_date,
            FO_Remarks=None,
            Inspection_Remarks=None
        )
    t_workflow_details.objects.create(Application_No=last_application_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=None, Section='Plant',
                                      Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                      Service_Code=service_code)
    data['applNo'] = last_application_no
    return JsonResponse(data)


def get_import_application_no(request, service_code):
    last_application_no = t_plant_import_permit_t1.objects.aggregate(Max('Application_No'))
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


def load_variety(request):
    crop_id = request.GET.get('crop_id')
    variety_list = t_plant_crop_variety_master.objects.filter(Crop_Id=crop_id).order_by('Crop_Variety_Name')
    return render(request, 'import_permit/crop_variety_list.html', {'variety': variety_list})


def save_import_plant(request):
    if request.method == 'POST':
        appNo = request.POST['appNo']
        Import_Category = request.POST['plant_import_category']
        crop_variety_id = request.POST['crop_variety_id']
        crop_id = request.POST['crop_id']
        unit = request.POST['unit']
        qty = request.POST['qty']
        t_plant_import_permit_t2.objects.create(Application_No=appNo, Import_Category=Import_Category,
                                                Crop_Id=crop_id, Pesticide_Id=None, Description=None,
                                                Variety_Id=crop_variety_id, Unit=unit, Quantity=qty,
                                                Quantity_Released=None, Remarks=None)
        imports_plant = t_plant_import_permit_t2.objects.filter(Application_No=appNo)
        return render(request, 'import_permit/import_page_plant.html', {'import': imports_plant, 'title': appNo})


def save_import_agro(request):
    if request.method == 'POST':
        appNo = request.POST['appNo']
        Import_Category = request.POST['agro_import_category']
        pesticide_id = request.POST['pesticide_id']
        description = request.POST['description']
        unit = request.POST['unit']
        qty = request.POST['qty']
        t_plant_import_permit_t2.objects.create(Application_No=appNo, Import_Category=Import_Category,
                                                Crop_Id=None, Pesticide_Id=pesticide_id,
                                                Description=description,
                                                Variety_Id=None, Unit=unit, Quantity=qty,
                                                Quantity_Released=None, Remarks=None)
        imports_plant = t_plant_import_permit_t2.objects.filter(Application_No=appNo)
    return render(request, 'import_permit/import_page_agro.html', {'import': imports_plant, 'title': appNo})


def fo_app_details(request):
    Application_No = request.GET.get('application_id')
    new_import_app = t_plant_import_permit_t1.objects.filter(Application_No=Application_No)
    details = t_plant_import_permit_t2.objects.filter(Application_No=Application_No)
    file = t_file_attachment.objects.filter(Application_No=Application_No)
    location = t_field_office_master.objects.all()
    return render(request, 'import_permit/fo_import_permit.html',
                  {'new_import_app': new_import_app, 'details': details, 'file': file, 'location': location})


def approve_fo_app(request):
    appNo = request.POST['appNo']
    application_details = t_workflow_details.objects.filter(Application_No=appNo)
    for application_details in application_details:
        App_id = application_details.Applicant_id
    client_id = t_user_master.objects.filter(Application_No=App_id)
    for client in client_id:
        client_login = client.Login_Id
    application_details.update(Assigned_To=client_login)
    return render(request, 'new_import_permit.html')


def call_for_inspection(request):
    login_id = request.session['login_id']
    application_details = t_workflow_details.objects.filter(Assigned_To=login_id)
    return render(request, 'import_permit/inspection_call.html', {'application_details': application_details})


def call_for_inspection_details(request):
    application_no = request.GET.get('application_id')
    location_details = t_field_office_master.objects.filter(Is_Entry_Point='Y')
    return render(request, 'import_permit/inspection_call_details.html', {'application_no': application_no,
                                                                          'location': location_details})


def print_import_details(request):
    application_no = request.GET.get('application_id')
    print_details = t_plant_import_permit_t1.objects.filter(Application_No=application_no)
    for print_import in print_details:
        finalDestination = print_import.Final_Destination
    return render(request, 'import_permit/print_import_permit.html',
                  {'Final_Destination': finalDestination})


def view_oic_details(request):
    application_id = request.GET.get('application_id')
    service_code = request.GET.get('service_code')

    if service_code == 'MPP':
        application_details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
        location = t_field_office_master.objects.all()
        details_list = t_plant_import_permit_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        inspector_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)

        return render(request, 'import_permit/oic_import_application.html',
                      {'application_details': application_details, 'details': details_list, 'location': location,
                       'file': file, 'inspector_list': inspector_list})
    elif service_code == 'IPP':
        application_id = request.GET.get('application_id')
        application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_movement_permit_t2.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)

        return render(request, 'oic_application_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'inspector_list': user_role_list})


def view_inspector_details(request):
    application_id = request.GET.get('application_id')
    application_details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    location = t_field_office_master.objects.all()
    details_list = t_plant_import_permit_t2.objects.filter(Application_No=application_id)
    file = t_file_attachment.objects.filter(Application_No=application_id)
    workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
    for application in workflow_details:
        Field_Office = application.Field_Office_Id
    user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
    import_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/inspector_import_permit.html',
                  {'application_details': application_details,
                   'location': location, 'import': details_list, 'inspector_list': user_role_list,
                   'file': file, 'import_permit': import_permit})


def add_import_details_ins(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_import_permit_t3.objects.create(Application_No=application_id,
                                            Current_Observation=currentObservation,
                                            Decision_Conformity=decisionConform)
    import_permit = t_plant_import_permit_t3.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/add_import_details.html', {'import_permit': import_permit})


def approve_import_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')
    permit_no = get_permit_no(request)
    details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=dateOfInspection)
    details.update(Movement_Permit_No=permit_no)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')

    return render(request, 'import_permit/inspector_import_permit.html', {'application_details': application_details})


def reject_import_application(request):
    application_id = request.GET.get('application_id')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')

    details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    if remarks is not None:
        details.update(Remarks=remarks)
    else:
        details.update(Remarks=None)
    details.update(Inspection_Leader=Inspection_Leader)
    details.update(Inspection_Team=Inspection_Team)
    details.update(Inspection_Date=dateOfInspection)
    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='R')
    return render(request, 'import_permit/inspector_import_permit.html', {'application_details': application_details})


def update_permit_details(request):
    appNo = request.POST.get('appNo')
    entry_point = request.POST.get('entry_point')
    date_requested = request.POST.get('date')
    remarks = request.POST.get('remarks')

    details = t_plant_import_permit_t1.objects.filter(Application_No=appNo)
    details.update(Actual_Point_Of_Entry=entry_point)
    details.update(Proposed_Inspection_Date=date_requested)
    details.update(Inspection_Request_Remarks=remarks)

    oic_details = t_user_master.objects.filter(Field_Office_Id_id=entry_point)
    for oic in oic_details:
        oic_user = oic.Login_Id
    workflow_details = t_workflow_details.objects.filter(Application_No=appNo)
    workflow_details.update(Assigned_To=oic_user)
    workflow_details.update(Assigned_Role_Id='4')
    workflow_details.update(Action_Date=date.today())
    workflow_details.update(Field_Office_Id=entry_point)

    login_id = request.session['login_id']
    application_details = t_workflow_details.objects.filter(Assigned_To=login_id)
    return render(request, 'import_permit/inspection_call.html', {'application_details': application_details})


def add_plant_import_file(request):
    data = dict()
    myFile = request.FILES['plant_document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/import_permit")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def add_agro_import_file(request):
    data = dict()
    myFile = request.FILES['agro_document']
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/import_permit")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def add_plant_attach(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'import_permit/plant_attachment_page.html', {'file_attach': file_attach})


def add_agro_attach(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'import_permit/agro_attachment_page.html', {'file_attach': file_attach})


def delete_plant_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments/plant/import_permit" + str(timezone.now().year))
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'import_permit/plant_attachment_page.html', {'file_attach': file_attach})


def delete_agro_file(request):
    File_Id = request.GET.get('file_id')
    Application_No = request.GET.get('appNo');

    file = t_file_attachment.objects.filter(pk=File_Id)
    for file in file:
        fileName = file.Attachment
        fs = FileSystemStorage("attachments/plant/import_permit" + str(timezone.now().year))
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'import_permit/agro_attachment_page.html', {'file_attach': file_attach})


def save_details_import(request):
    Application_No = request.POST.get('applicationNo');
    print(Application_No)
    details = t_workflow_details.objects.filter(Application_No=Application_No)
    details.update(Action_Date=date.today())

    crop = t_plant_crop_master.objects.all()
    pesticide = t_plant_pesticide_master.objects.all()
    variety = t_plant_crop_variety_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'import_permit/apply_import_permit.html',
                  {'crop': crop, 'pesticide': pesticide, 'variety': variety,
                   'location': location})


def fo_reject(request):
    Role_Id = request.session['Role_Id']
    appId = request.POST.get('application_id')
    remarks = request.POST.get('remarks')

    application_details = t_workflow_details.objects.filter(Application_No=appId)
    details = t_plant_import_permit_t1.objects.filter(Application_No=appId)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    for app in application_details:
        client_login_id = app.Applicant_Id
    client_id = t_user_master.objects.filter(Email_Id=client_login_id)
    for client in client_id:
        login_id = client.Login_Id
    application_details.update(Assigned_To=login_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='R')
    send_import_reject_email(remarks, details.Email)

    new_import_app = t_workflow_details.objects.filter(Assigned_Role_Id=Role_Id, Section='Plant',
                                                       Application_Status='P')
    return render(request, 'import_permit/new_import_permit_fo.html', {'new_import_app': new_import_app})


def send_import_reject_email(remarks, Email):
    subject = 'APPLICATION REJECTED'
    message = "Dear " + "Sir" + " Your Application for Import Of Plant And Plant Products Has Been Rejected Because" + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def fo_approve(request):
    new_import_permit = get_import_permit_no()
    appId = request.POST.get('application_id')
    remarks = request.POST.get('remarks')
    Role_Id = request.session['Role_Id']

    details = t_plant_import_permit_t1.objects.filter(Application_No=appId)
    for email_id in details:
        email = email_id.Email
    details.update(Import_Permit_No=new_import_permit)
    if remarks is not None:
        details.update(FO_Remarks=remarks)
    else:
        details.update(FO_Remarks=None)
    application_details = t_workflow_details.objects.filter(Application_No=appId)
    for app in application_details:
        client_login_id = app.Applicant_Id
    client_id = t_user_master.objects.filter(Email_Id=client_login_id)
    for client in client_id:
        login_id = client.Login_Id
        application_details.update(Assigned_To=login_id)
    application_details.update(Action_Date=date.today())
    application_details.update(Application_Status='A')
    send_import_approve_email(new_import_permit, email)

    new_import_app = t_workflow_details.objects.filter(Assigned_Role_Id=Role_Id, Section='Plant',
                                                       Application_Status='P')
    return render(request, 'import_permit/new_import_permit_fo.html', {'new_import_app': new_import_app})


def send_import_approve_email(new_import_permit, Email):
    subject = 'APPLICATION APPROVED'
    message = "Dear Sir Your Application for Import Of Plant And Plant Products Has Been Approved. Your " \
              "Import Permit No is:" + new_import_permit + " Please Login To BBFSS and Download The Permit. "
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def get_import_permit_no():
    last_import_permit_no = t_plant_import_permit_t1.objects.aggregate(Max('Import_Permit_No'))
    last_permit_no = last_import_permit_no['Import_Permit_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = "IPP" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_permit_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = "IPP" + "/" + str(year) + "/" + AppNo
    return newPermitNo


def assign_to_inspector(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')

    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Assigned_To=forwardTo)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_Role_Id='5')
    Field_Office_Id = request.session['field_office_id']
    Login_Id = request.session['login_id']
    application_details = t_workflow_details.objects.filter(Assigned_To=Login_Id, Field_Office_Id=Field_Office_Id)
    return render(request, 'import_permit/oic_application.html', {'application_details': application_details})


def edit_inspector_details(request, Record_Id):
    plant_import_permit = get_object_or_404(t_plant_import_permit_t2, pk=Record_Id)
    details = t_plant_import_permit_t2.objects.filter(pk=Record_Id)
    for plant in details:
        crop_id = plant.Crop_Id
    crop_master = t_plant_crop_master.objects.filter(pk=crop_id)
    for crop in crop_master:
        crop_name = crop.Crop_Common_Name
    variety = t_plant_crop_variety_master.objects.filter(Crop_Id=crop_id)
    for crop_variety in variety:
        variety_crop = crop_variety.Crop_Variety_Name
    if request.method == 'POST':
        form = ImportFormTwo(request.POST, instance=plant_import_permit)
    else:
        form = ImportFormTwo(instance=plant_import_permit)
    return save_details_form(request, form, crop_name, variety_crop, 'import_permit/edit_inspector_details.html')


def save_details_form(request, form, crop_name, variety_crop, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            import_details = t_plant_import_permit_t2.objects.all()
            data['html_form'] = render_to_string('import_permit/inspector_import_permit.html', {
                'import': import_details
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'Crop_Common_Name': crop_name, 'variety_crop': variety_crop}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def add_details_ins_import(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_import_permit_t3.objects.create(Application_No=application_id,
                                            Current_Observation=currentObservation,
                                            Decision_Conformity=decisionConform)
    import_permit = t_plant_import_permit_t3.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/add_import_details.html', {'import_permit': import_permit})


def edit_decision(request, Record_Id):
    decision = get_object_or_404(t_plant_import_permit_t3, pk=Record_Id)
    if request.method == 'POST':
        form = ImportFormThree(request.POST, instance=decision)
    else:
        form = ImportFormThree(instance=decision)
    return save_decision_form(request, form, 'import_permit/edit_decision.html')


def save_decision_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            decision = t_plant_import_permit_t3.objects.all()
            data['html_form'] = render_to_string('import_permit/add_import_details.html', {
                'import_permit': decision
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def submit_application(request):
    application_no = request.GET.get('application_no')
    Inspection_Leader = request.GET.get('Inspection_Leader')
    Inspection_Team = request.GET.get('Inspection_Team')
    remarks = request.GET.get('remarks')
    dateOfInspection = request.GET.get('dateOfInspection')

    clearnace_ref_no = clearance_ref_no(request)

    update_details = t_plant_import_permit_t1.objects.filter(Application_No=application_no)
    update_details.update(Clearance_Ref_No=clearnace_ref_no)
    update_details.update(Inspection_Leader=Inspection_Leader)
    update_details.update(Inspection_Team=Inspection_Team)
    update_details.update(Inspection_Date=dateOfInspection)
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


def clearance_ref_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_clearance_ref_no = t_plant_import_permit_t1.objects.aggregate(Max('Clearance_Ref_No'))
    last_permit_no = last_clearance_ref_no['Clearance_Ref_No__max']
    if not last_permit_no:
        year = timezone.now().year
        newPermitNo = Field_Code + "/" + "IPP" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newPermitNo = Field_Code + "/" + "IPP" + "/" + str(year) + "/" + AppNo
    return newPermitNo


def certificate_print(request):
    return render(request, 'certificate_printing.html')
