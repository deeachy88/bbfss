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
    t_service_master, t_country_master
from bbfss import settings
from plant.forms import ImportFormThree, ImportFormTwo
from plant.models import t_workflow_details, t_plant_movement_permit_t2, t_plant_movement_permit_t1, \
    t_plant_movement_permit_t3, t_file_attachment, t_plant_import_permit_t1, t_plant_import_permit_t2, \
    t_plant_import_permit_t3, t_plant_export_certificate_plant_plant_products_t1, \
    t_plant_clearence_nursery_seed_grower_t1, t_plant_clearence_nursery_seed_grower_t2, t_plant_seed_certification_t1


def focal_officer_application(request):
    Role_Id = request.session['Role_Id']
    application_details = t_workflow_details.objects.filter(Assigned_Role_Id=Role_Id, Section='Plant',
                                                            Application_Status='P')
    return render(request, 'focal_officer_pending_list.html', {'new_import_app': application_details})


def oic_application(request):
    Field_Office_Id = request.session['field_office_id']
    Role_Id = request.session['Role_Id']
    application_details = t_workflow_details.objects.filter(Assigned_Role_Id=Role_Id, Field_Office_Id=Field_Office_Id,
                                                            Application_Status='P')
    for service in application_details:
        service_code = service.Service_Code
    service_details = t_service_master.objects.filter(Service_Code=service_code)
    for service_details in service_details:
        service_name = service_details.Service_Name
    return render(request, 'oic_pending_list.html',
                  {'service_name': service_name, 'application_details': application_details})


def inspector_application(request):
    Login_Id = request.session['login_id']
    details = t_workflow_details.objects.filter(Assigned_Role_Id='5', Assigned_To=Login_Id)
    for service in details:
        service_code = service.Service_Code
    if service_code == "IPP":
        new_import_app = t_workflow_details.objects.filter(Assigned_Role_Id='5', Assigned_To=Login_Id,
                                                           Application_Status='A')
    else:
        new_import_app = t_workflow_details.objects.filter(Assigned_Role_Id='5', Assigned_To=Login_Id,
                                                           Application_Status='P')
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

    return render(request, 'movement_permit/apply_movement_permit.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def save_details(request):
    appNo = request.POST.get('applicationNo')
    workflow_details = t_workflow_details.objects.filter(Application_No=appNo)
    workflow_details.update(Action_Date=date.today())
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'movement_permit/apply_movement_permit.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


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
    return render(request, 'movement_permit/location_list.html', {'location_list': location_list})


def movement_permit_app(request):
    appNo = request.GET.get('appId')
    imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=appNo)
    return render(request, 'movement_permit/apply_movement_permit_page.html', {'import': imports_plant, 'title': appNo})


def load_details_page(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    return render(request, 'movement_permit/movement_permit_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location': location})


def agro_details_page(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
    return render(request, 'movement_permit/movement_permit_agro_details.html',
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
    return render(request, 'movement_permit/apply_movement_permit.html',
                  {'import': imports_plant, 'title': application_id})


def save(request):
    if request.method == 'POST':
        commodity = request.POST['commodity']
        appNo = request.POST['appNo']
        qty = request.POST['qty']
        remarks = request.POST['remarks']
        t_plant_movement_permit_t2.objects.create(Application_No=appNo, Commodity=commodity,
                                                  Qty=qty, Remarks=remarks)
        imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=appNo)
    return render(request, 'movement_permit/movement_page.html', {'import': imports_plant, 'title': appNo})


def forward_application(request):
    application_id = request.POST.get('application_id')
    forwardTo = request.POST.get('forwardTo')

    application_details = t_workflow_details.objects.filter(Application_No=application_id)
    application_details.update(Assigned_To=forwardTo)
    application_details.update(Action_Date=date.today())
    application_details.update(Assigned_Role_Id='5')
    Field_Office_Id = request.session['field_office_id']
    Role_Id = request.session['Role_Id']
    application_Lists = t_workflow_details.objects.filter(Assigned_To=Role_Id, Field_Office_Id=Field_Office_Id)
    return render(request, 'oic_pending_list.html', {'application_details': application_Lists})


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
    elif service_code == 'EPP':
        application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(
            Application_No=application_id)
        location = t_location_field_office_mapping.objects.all()
        dzongkhag = t_dzongkhag_master.objects.all()
        file = t_file_attachment.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        return render(request, 'export_permit/inspector_export_permit.html',
                      {'application_details': application_details,
                       'location': location, 'inspector_list': user_role_list,
                       'file': file, 'dzongkhag': dzongkhag})
    elif service_code == 'RNS':
        application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        movement_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)

        return render(request, 'nursery_registration/inspector_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'inspector_list': user_role_list, 'file': file, 'movement_permit': movement_permit})

    elif service_code == 'RSC':
        application_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='5', Field_Office_Id_id=Field_Office)
        movement_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)

        return render(request, 'seed_cerification/inspector_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'inspector_list': user_role_list, 'file': file, 'movement_permit': movement_permit})


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

    return render(request, 'movement_permit/application_details.html', {'application_details': application_details})


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
    return render(request, 'movement_permit/application_details.html', {'application_details': application_details})


def add_details_ins(request):
    application_id = request.GET.get('application_id')
    currentObservation = request.GET.get('currentObservation')
    decisionConform = request.GET.get('decisionConform')
    t_plant_movement_permit_t3.objects.create(Application_No=application_id,
                                              Current_Observation=currentObservation,
                                              Decision_Conformity=decisionConform)
    movement_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)
    return render(request, 'movement_permit/add_application_details.html', {'movement_permit': movement_permit})


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
    fs = FileSystemStorage("attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit")
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        file_url = "attachments" + "/" + str(timezone.now().year) + "/plant/movement_permit" + "/" + myFile.name
        data['form_is_valid'] = True
        data['file_url'] = file_url
    return JsonResponse(data)


def add_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']
        file_url = request.POST.get('file_url')

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         File_Path=file_url, Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'movement_permit/file_attachment_page.html', {'file_attach': file_attach})


def save_movement_file(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments/plant/movement_permit" + str(timezone.now().year))
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def movement_agro_file_name(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)

        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'movement_permit/file_attachment_page.html', {'file_attach': file_attach})


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
    return render(request, 'movement_permit/ile_attachment_page.html', {'file_attach': file_attach})


# import permit
def apply_import_permit(request):
    crop = t_plant_crop_master.objects.all()
    pesticide = t_plant_pesticide_master.objects.all()
    variety = t_plant_crop_variety_master.objects.all()
    location = t_field_office_master.objects.filter(Is_Entry_Point="Y")

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
        inspector_list = t_user_master.objects.filter(Role_Id='4', Field_Office_Id_id=Field_Office)

        return render(request, 'movement_permit/oic_import_application.html',
                      {'application_details': application_details, 'details': details_list, 'location': location,
                       'file': file, 'inspector_list': inspector_list})

    elif service_code == 'IPP':
        application_id = request.GET.get('application_id')
        application_details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_import_permit_t2.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='4', Field_Office_Id_id=Field_Office)

        return render(request, 'import_permit/oic_import_application.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'file': file, 'inspector_list': user_role_list})

    elif service_code == 'EPP':
        application_id = request.GET.get('application_id')
        application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
            Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        location = t_field_office_master.objects.all()
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='4', Field_Office_Id_id=Field_Office)
        file = t_file_attachment.objects.filter(Application_No=application_id)

        return render(request, 'export_permit/oic_application_details.html',
                      {'application_details': application_details, 'file': file, 'dzongkhag': dzongkhag,
                       'location': location,
                       'inspector_list': user_role_list})
    elif service_code == 'RNS':
        application_id = request.GET.get('application_id')
        application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='4', Field_Office_Id_id=Field_Office)

        return render(request, 'nursery_registration/oic_application_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'file': file, 'inspector_list': user_role_list})
    elif service_code == 'RSC':
        application_id = request.GET.get('application_id')
        application_details = t_plant_clearence_nursery_seed_grower_t1.objects.filter(Application_No=application_id)
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        location = t_location_field_office_mapping.objects.all()
        details_list = t_plant_clearence_nursery_seed_grower_t2.objects.filter(Application_No=application_id)
        workflow_details = t_workflow_details.objects.filter(Application_No=application_id)
        file = t_file_attachment.objects.filter(Application_No=application_id)
        for application in workflow_details:
            Field_Office = application.Field_Office_Id
        user_role_list = t_user_master.objects.filter(Role_Id='4', Field_Office_Id_id=Field_Office)

        return render(request, 'seed_cerification/oic_application_details.html',
                      {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                       'village': village, 'location': location, 'details_list': details_list,
                       'file': file, 'inspector_list': user_role_list})


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


def load_import_details(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    application_id = request.GET.get('application_id')
    application_details = t_plant_import_permit_t1.objects.filter(Application_No=application_id)
    return render(request, 'import_permit/import_permit_details.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village,
                   'location': location})


# Export Permit
def apply_export_permit(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()
    country = t_country_master.objects.all()
    entry_point = t_field_office_master.objects.filter(Is_Entry_Point='Y')

    return render(request, 'export_permit/apply_permit.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location, 'entry_point': entry_point, 'country': country})


def submit_export(request):
    data = dict()
    serviceCode = "EPP"
    lastExportApplication = get_export_application_no(serviceCode)
    Applicant_Type = request.POST.get('ApplicantType')
    Certificate_Type = request.POST.get('certificateType')
    License_No = request.POST.get('p_License_No')
    CID = request.POST.get('p_cid')
    Exporter_Name = request.POST.get('p_Exporter_Name')
    Exporter_Address = request.POST.get('p_Exporter_Address')
    Contact_No = request.POST.get('p_Contact_No')
    Email = request.POST.get('p_Email')
    Dzongkhag_Code = request.POST.get('p_Dzongkhag_Code')
    Locatipn_Code = request.POST.get('p_Location_Code')
    Consingee_Name_Address = request.POST.get('p_Name_Address')
    Botanical_Name = request.POST.get('p_Botanical_Name')
    Description = request.POST.get('p_Description')
    Qty_Gross = request.POST.get('p_Qty_Gross')
    Unit_Gross = request.POST.get('p_Unit_Gross')
    Qty_Net = request.POST.get('p_Qty_Net')
    Unit_Net = request.POST.get('p_Unit_Net')
    Importing_Country = request.POST.get('p_Country_Code')
    Entry_Point = request.POST.get('p_Entry_Point')
    Packages_No = request.POST.get('p_Package_number')
    Packages_Description = request.POST.get('p_Package_description')
    Distinguishing_Marks = request.POST.get('p_Distinguish_Marks')
    Purpose_End_Use = request.POST.get('p_purpose')
    Mode_Of_Conveyance = request.POST.get('p_conveyanceMeans')
    Name_Of_Conveyance = request.POST.get('p_Conveyance_Name')
    Desired_Inspection_Date = request.POST.get('date_for_Inspection')
    Desired_Inspection_Place = request.POST.get('requested_place')
    Additional_Declaring = request.POST.get('p_additional_declaration')
    Pre_Application_Treatment = request.POST.get('treatmentType')
    Chemical_Name_Pre = request.POST.get('p_chemcial_name')
    Treatment_Pre = request.POST.get('p_treatment')
    Concentration_Pre = request.POST.get('p_Concentration')
    Duration_Temperature_Pre = request.POST.get('p_Duration_Temperature')
    Treated_By_Pre = request.POST.get('p_treated_by')
    Treated_Supervised_By_Pre = request.POST.get('p_treatment_supervised')
    Additional_Information_Pre = request.POST.get('p_additional_Info')
    Other_Pre = request.POST.get('p_others_treatment')
    Other_Treatment = request.POST.get('p_others')

    C_CID = request.POST.get('c_cid')
    C_Exporter_Name = request.POST.get('c_Exporter_Name')
    C_Contact_No = request.POST.get('c_Contact_No')
    C_Email = request.POST.get('c_Email')
    C_Dzongkhag_Code = request.POST.get('c_Dzongkhag_Code')
    C_Locatipn_Code = request.POST.get('c_Location_Code')
    c_current_address = request.POST.get('c_current_address')
    c_permanent_address = request.POST.get('c_permanent_address')
    c_License_No = request.POST.get('c_License_No')
    gross_weight_gms = request.POST.get('gross_weight_gms')
    gross_weight_pieces = request.POST.get('gross_weight_pieces')
    net_weight_gms = request.POST.get('net_weight_gms')
    net_weight_pieces = request.POST.get('net_weight_pieces')
    c_package = request.POST.get('c_package')
    c_country = request.POST.get('c_country')
    c_Name_Address = request.POST.get('c_Name_Address')
    c_conveyanceMeans = request.POST.get('c_conveyanceMeans')
    retail_gross_weight_gms = request.POST.get('c_conveyanceMeans')
    retail_gross_weight_pieces = request.POST.get('c_conveyanceMeans')
    retail_net_weight_gms = request.POST.get('c_conveyanceMeans')
    retail_net_weight_pieces = request.POST.get('c_conveyanceMeans')
    c_retail_package = request.POST.get('c_retail_package')
    c_outlet_name = request.POST.get('c_outlet_name')
    c_phoneNumber = request.POST.get('c_phoneNumber')
    c_address = request.POST.get('c_address')

    if Certificate_Type == 'P':
        t_plant_export_certificate_plant_plant_products_t1.objects.create(
            Application_No=lastExportApplication,
            Applicant_Type=None,
            Certificate_Type=Certificate_Type,
            License_No=License_No,
            CID=CID,
            Exporter_Name=Exporter_Name,
            Exporter_Address=Exporter_Address,
            Permanent_Address=None,
            Contact_No=Contact_No,
            Email=Email,
            Dzongkhag_Code=Dzongkhag_Code,
            Locatipn_Code=Locatipn_Code,
            Consingee_Name_Address=Consingee_Name_Address,
            Botanical_Name=Botanical_Name,
            Description=Description,
            Qty_Gross=Qty_Gross,
            Unit_Gross=Unit_Gross,
            Pieces_Gross=None,
            Qty_Net=Qty_Net,
            Unit_Net=Unit_Net,
            Pieces_Net=None,
            Importing_Country=Importing_Country,
            Entry_Point=Entry_Point,
            Packages_No=Packages_No,
            Packages_Description=Packages_Description,
            Distinguishing_Marks=Distinguishing_Marks,
            Purpose_End_Use=Purpose_End_Use,
            Mode_Of_Conveyance=Mode_Of_Conveyance,
            Name_Of_Conveyance=Name_Of_Conveyance,
            Departure_Date=None,
            Desired_Inspection_Date=None,
            Desired_Inspection_Place=None,
            Additional_Declaring=Additional_Declaring,
            Outlet_name=None,
            Outlet_Contact_No=None,
            Outlet_Address=None,
            Inspection_Date=None,
            Sample_Drawn_By=None,
            Sample_Inspected_By=None,
            Sample_Drawn=None,
            Sample_Size=None,
            Inspection_Method=None,
            Inspection_Method_Other=None,
            Pest_Detected=None,
            Pest_Insect=None,
            Pest_Mite=None,
            Pest_Fungi=None,
            Pest_Bacteria=None,
            Pest_Virus=None,
            Pest_Nematode=None,
            Pest_Weed=None,
            Pest_Scientific_Name=None,
            Infestation_Level=None,
            Pest_Status=None,
            Pest_Risk_Category=None,
            Pest_QR_Detected=None,
            Pest_QR_Comment=None,
            Treatment_Possible=None,
            Treatment_Comment=None,
            Phytosanitary_Measures=None,
            Phytosanitary_Measures_Comment=None,
            Treatment_Chemical_Name=None,
            Treatment_Chemical_Fumigation=None,
            Treatment_Chemical_Spray=None,
            Treatment_Chemical_Seed=None,
            Treatment_Chemical_Other=None,
            Treatment_Chemical_Other_Specific=None,
            Treatment_Chemical_Concentration=None,
            Treatment_Chemical_Duration=None,
            Treatment_Chemical_Treated_By=None,
            Treatment_Chemical_Additional_Info=None,
            Treatment_Irradiation=None,
            Treatment_Hot_Water=None,
            Treatment_Dry_Heat=None,
            Treatment_Vapour_Heat=None,
            Treatment_Cold_Treatment=None,
            Feasibility_Status=None,
            Export_Permit=None,
            Additional_Information_Pre=Additional_Information_Pre,
            Chemical_Name_Pre=Chemical_Name_Pre,
            Concentration_Pre=Concentration_Pre,
            Duration_Temperature_Pre=Duration_Temperature_Pre,
            Pre_Application_Treatment=Pre_Application_Treatment,
            Treated_By_Pre=Treated_By_Pre,
            Treated_Supervised_By_Pre=Treated_Supervised_By_Pre,
            Treatment_Pre=Treatment_Pre,
            Other_Pre=Other_Pre,
            Other_Treatment=Other_Treatment
        )
    else:
        if Applicant_Type == 'bothRadio':
            t_plant_export_certificate_plant_plant_products_t1.objects.create(
                Application_No=lastExportApplication,
                Applicant_Type=Applicant_Type,
                Certificate_Type=Certificate_Type,
                License_No=None,
                CID=C_CID,
                Exporter_Name=C_Exporter_Name,
                Exporter_Address=c_current_address,
                Permanent_Address=c_permanent_address,
                Contact_No=C_Contact_No,
                Email=C_Email,
                Dzongkhag_Code=C_Dzongkhag_Code,
                Locatipn_Code=C_Locatipn_Code,
                Consingee_Name_Address=None,
                Botanical_Name=None,
                Description=None,
                Qty_Gross=None,
                Unit_Gross=None,
                Pieces_Gross=None,
                Qty_Net=None,
                Unit_Net=None,
                Pieces_Net=None,
                Importing_Country=None,
                Entry_Point=None,
                Packages_No=None,
                Packages_Description=None,
                Distinguishing_Marks=None,
                Purpose_End_Use=None,
                Mode_Of_Conveyance=None,
                Name_Of_Conveyance=None,
                Departure_Date=None,
                Desired_Inspection_Date=Desired_Inspection_Date,
                Desired_Inspection_Place=Desired_Inspection_Place,
                Additional_Declaring=None,
                Outlet_name=None,
                Outlet_Contact_No=None,
                Outlet_Address=None,
                Inspection_Date=None,
                Sample_Drawn_By=None,
                Sample_Inspected_By=None,
                Sample_Drawn=None,
                Sample_Size=None,
                Inspection_Method=None,
                Inspection_Method_Other=None,
                Pest_Detected=None,
                Pest_Insect=None,
                Pest_Mite=None,
                Pest_Fungi=None,
                Pest_Bacteria=None,
                Pest_Virus=None,
                Pest_Nematode=None,
                Pest_Weed=None,
                Pest_Scientific_Name=None,
                Infestation_Level=None,
                Pest_Status=None,
                Pest_Risk_Category=None,
                Pest_QR_Detected=None,
                Pest_QR_Comment=None,
                Treatment_Possible=None,
                Treatment_Comment=None,
                Phytosanitary_Measures=None,
                Phytosanitary_Measures_Comment=None,
                Treatment_Chemical_Name=None,
                Treatment_Chemical_Fumigation=None,
                Treatment_Chemical_Spray=None,
                Treatment_Chemical_Seed=None,
                Treatment_Chemical_Other=None,
                Treatment_Chemical_Other_Specific=None,
                Treatment_Chemical_Concentration=None,
                Treatment_Chemical_Duration=None,
                Treatment_Chemical_Treated_By=None,
                Treatment_Chemical_Additional_Info=None,
                Treatment_Irradiation=None,
                Treatment_Hot_Water=None,
                Treatment_Dry_Heat=None,
                Treatment_Vapour_Heat=None,
                Treatment_Cold_Treatment=None,
                Feasibility_Status=None,
                Export_Permit=None,
                Additional_Information_Pre=None,
                Chemical_Name_Pre=None,
                Concentration_Pre=None,
                Duration_Temperature_Pre=None,
                Pre_Application_Treatment=None,
                Treated_By_Pre=None,
                Treated_Supervised_By_Pre=None,
                Treatment_Pre=None,
                Other_Pre=None,
                Other_Treatment=None
            )
        elif Applicant_Type == 'directRadio':
            t_plant_export_certificate_plant_plant_products_t1.objects.create(
                Application_No=lastExportApplication,
                Applicant_Type=Applicant_Type,
                Certificate_Type=Certificate_Type,
                License_No=c_License_No,
                CID=C_CID,
                Exporter_Name=C_Exporter_Name,
                Exporter_Address=c_current_address,
                Permanent_Address=c_permanent_address,
                Contact_No=C_Contact_No,
                Email=C_Email,
                Dzongkhag_Code=C_Dzongkhag_Code,
                Locatipn_Code=C_Locatipn_Code,
                Consingee_Name_Address=c_Name_Address,
                Botanical_Name=None,
                Description=None,
                Qty_Gross=gross_weight_gms,
                Unit_Gross="Gm(s)",
                Pieces_Gross=gross_weight_pieces,
                Qty_Net=net_weight_gms,
                Unit_Net="Gm(s)",
                Pieces_Net=net_weight_pieces,
                Importing_Country=c_country,
                Entry_Point=None,
                Packages_No=c_package,
                Packages_Description=None,
                Distinguishing_Marks=None,
                Purpose_End_Use=None,
                Mode_Of_Conveyance=c_conveyanceMeans,
                Name_Of_Conveyance=None,
                Departure_Date=None,
                Desired_Inspection_Date=None,
                Desired_Inspection_Place=None,
                Additional_Declaring=None,
                Outlet_name=None,
                Outlet_Contact_No=None,
                Outlet_Address=None,
                Inspection_Date=None,
                Sample_Drawn_By=None,
                Sample_Inspected_By=None,
                Sample_Drawn=None,
                Sample_Size=None,
                Inspection_Method=None,
                Inspection_Method_Other=None,
                Pest_Detected=None,
                Pest_Insect=None,
                Pest_Mite=None,
                Pest_Fungi=None,
                Pest_Bacteria=None,
                Pest_Virus=None,
                Pest_Nematode=None,
                Pest_Weed=None,
                Pest_Scientific_Name=None,
                Infestation_Level=None,
                Pest_Status=None,
                Pest_Risk_Category=None,
                Pest_QR_Detected=None,
                Pest_QR_Comment=None,
                Treatment_Possible=None,
                Treatment_Comment=None,
                Phytosanitary_Measures=None,
                Phytosanitary_Measures_Comment=None,
                Treatment_Chemical_Name=None,
                Treatment_Chemical_Fumigation=None,
                Treatment_Chemical_Spray=None,
                Treatment_Chemical_Seed=None,
                Treatment_Chemical_Other=None,
                Treatment_Chemical_Other_Specific=None,
                Treatment_Chemical_Concentration=None,
                Treatment_Chemical_Duration=None,
                Treatment_Chemical_Treated_By=None,
                Treatment_Chemical_Additional_Info=None,
                Treatment_Irradiation=None,
                Treatment_Hot_Water=None,
                Treatment_Dry_Heat=None,
                Treatment_Vapour_Heat=None,
                Treatment_Cold_Treatment=None,
                Feasibility_Status=None,
                Export_Permit=None,
                Additional_Information_Pre=None,
                Chemical_Name_Pre=None,
                Concentration_Pre=None,
                Duration_Temperature_Pre=None,
                Pre_Application_Treatment=None,
                Treated_By_Pre=None,
                Treated_Supervised_By_Pre=None,
                Treatment_Pre=None,
                Other_Pre=None,
                Other_Treatment=None
            )
        else:
            t_plant_export_certificate_plant_plant_products_t1.objects.create(
                Application_No=lastExportApplication,
                Applicant_Type=Applicant_Type,
                Certificate_Type=Certificate_Type,
                License_No=None,
                CID=C_CID,
                Exporter_Name=C_Exporter_Name,
                Exporter_Address=c_current_address,
                Permanent_Address=c_permanent_address,
                Contact_No=C_Contact_No,
                Email=C_Email,
                Dzongkhag_Code=C_Dzongkhag_Code,
                Locatipn_Code=C_Locatipn_Code,
                Consingee_Name_Address=None,
                Botanical_Name=None,
                Description=None,
                Qty_Gross=retail_gross_weight_gms,
                Unit_Gross="Gm(s)",
                Pieces_Gross=retail_gross_weight_pieces,
                Qty_Net=retail_net_weight_gms,
                Unit_Net="Gm(s)",
                Pieces_Net=retail_net_weight_pieces,
                Importing_Country=None,
                Entry_Point=None,
                Packages_No=c_retail_package,
                Packages_Description=None,
                Distinguishing_Marks=None,
                Purpose_End_Use=None,
                Mode_Of_Conveyance=None,
                Name_Of_Conveyance=None,
                Departure_Date=None,
                Desired_Inspection_Date=None,
                Desired_Inspection_Place=None,
                Additional_Declaring=None,
                Outlet_name=c_outlet_name,
                Outlet_Contact_No=c_phoneNumber,
                Outlet_Address=c_address,
                Inspection_Date=None,
                Sample_Drawn_By=None,
                Sample_Inspected_By=None,
                Sample_Drawn=None,
                Sample_Size=None,
                Inspection_Method=None,
                Inspection_Method_Other=None,
                Pest_Detected=None,
                Pest_Insect=None,
                Pest_Mite=None,
                Pest_Fungi=None,
                Pest_Bacteria=None,
                Pest_Virus=None,
                Pest_Nematode=None,
                Pest_Weed=None,
                Pest_Scientific_Name=None,
                Infestation_Level=None,
                Pest_Status=None,
                Pest_Risk_Category=None,
                Pest_QR_Detected=None,
                Pest_QR_Comment=None,
                Treatment_Possible=None,
                Treatment_Comment=None,
                Phytosanitary_Measures=None,
                Phytosanitary_Measures_Comment=None,
                Treatment_Chemical_Name=None,
                Treatment_Chemical_Fumigation=None,
                Treatment_Chemical_Spray=None,
                Treatment_Chemical_Seed=None,
                Treatment_Chemical_Other=None,
                Treatment_Chemical_Other_Specific=None,
                Treatment_Chemical_Concentration=None,
                Treatment_Chemical_Duration=None,
                Treatment_Chemical_Treated_By=None,
                Treatment_Chemical_Additional_Info=None,
                Treatment_Irradiation=None,
                Treatment_Hot_Water=None,
                Treatment_Dry_Heat=None,
                Treatment_Vapour_Heat=None,
                Treatment_Cold_Treatment=None,
                Feasibility_Status=None,
                Export_Permit=None,
                Additional_Information_Pre=None,
                Chemical_Name_Pre=None,
                Concentration_Pre=None,
                Duration_Temperature_Pre=None,
                Pre_Application_Treatment=None,
                Treated_By_Pre=None,
                Treated_Supervised_By_Pre=None,
                Treatment_Pre=None,
                Other_Pre=None,
                Other_Treatment=None
            )
        if Certificate_Type == 'P':
            field_id = t_location_field_office_mapping.objects.filter(pk=Locatipn_Code)
            for field_office in field_id:
                field_office_id = field_office.Field_Office_Id_id
        else:
            field_id = t_location_field_office_mapping.objects.filter(pk=C_Locatipn_Code)
            for field_office in field_id:
                field_office_id = field_office.Field_Office_Id_id
        t_workflow_details.objects.create(Application_No=lastExportApplication, Applicant_Id=request.session['email'],
                                          Assigned_To=None, Field_Office_Id=field_office_id, Section='Plant',
                                          Assigned_Role_Id='2', Action_Date=None, Application_Status='P',
                                          Service_Code=serviceCode)
        data['applicationNo'] = lastExportApplication
    return JsonResponse(data)


def get_export_application_no(serviceCode):
    last_export_application_no = t_plant_export_certificate_plant_plant_products_t1.objects.aggregate(
        Max('Application_No'))
    last_application_no = last_export_application_no['Application_No__max']
    if not last_application_no:
        year = timezone.now().year
        newApplicationNo = serviceCode + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_application_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newApplicationNo = serviceCode + "/" + str(year) + "/" + AppNo
    return newApplicationNo


def add_file_phyto(request):
    data = dict()
    myFile = request.FILES['phyto_document']
    fs = FileSystemStorage("attachments/plant/export_permit" + str(timezone.now().year))
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def add_file_name_phyto(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)
        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'export_permit/phyto_file_attachment_page.html', {'file_attach': file_attach})


def add_file_cordyceps(request):
    data = dict()
    myFile = request.FILES['cordyceps_document']
    fs = FileSystemStorage("attachments/plant/export_permit" + str(timezone.now().year))
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def add_file_name_cordyceps(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)
        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'export_permit/cordyceps_file_attachment_page.html', {'file_attach': file_attach})


def get_export_permit_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_export_permit = t_plant_export_certificate_plant_plant_products_t1.objects.aggregate(Max('Export_Permit'))
    last_export_permit_no = last_export_permit['Export_Permit__max']
    if not last_export_permit_no:
        year = timezone.now().year
        new_export_permit = Field_Code + "/" + "EPP" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_export_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        new_export_permit = Field_Code + "/" + "EPP" + "/" + str(year) + "/" + AppNo
    return new_export_permit


def export_complete(request):
    Login_Id = request.session['login_id']
    export_permit = get_export_permit_no(request)
    Application_No = request.POST.get('appNo')
    Inspection_Date = request.POST.get('date')
    no_of_sample_drawn = request.POST.get('no_of_sample_drawn')
    total_sample_size = request.POST.get('total_sample_size')
    sample_drawn_by = request.POST.get('sample_drawn_by')
    inspection_method = request.POST.getlist('inspection_method')
    pest_detected = request.POST.get('pest_detected')
    pest_category = request.POST.get('pest_category')

    infestation_level = request.POST.get('infestation_level')
    live_dead = request.POST.get('live_dead')
    risk_category = request.POST.get('risk_category')
    remarks = request.POST.get('remarks')
    inspection_method_other = request.POST.get('inspection_method_other')
    Pest_QR_Detected = request.POST.get('Pest_QR_Detected')
    Pest_QR_Detected_Comments = request.POST.get('Pest_QR_Detected_Comments')
    treatment_possible = request.POST.get('treatment_possible')
    Treatment_Comment = request.POST.get('Treatment_Comment')
    Pest_Scientific_Name = request.POST.get('Scientific_Name')
    Laboratory_Analysis_Required = request.POST.get('Laboratory_Analysis_Required')
    Laboratory_Analysis_Comment = request.POST.get('analysis_Comment')
    Phytosanitary_Measures = request.POST.get('analysis_Comment')
    Phytosanitary_Measures_Comment = request.POST.get('analysis_Comment')
    additional_Info = request.POST.get('additional_Info')
    treated_by = request.POST.get('treated_by')
    Duration_Temperature = request.POST.get('Duration_Temperature')
    Concentration = request.POST.get('Concentration')
    treatment = request.POST.get('treatment')
    chemcial_name = request.POST.get('chemcial_name')
    others_treatment = request.POST.get('others_treatment')
    treatmentType = request.POST.get('treatmentType')

    application_details = t_plant_export_certificate_plant_plant_products_t1.objects.filter(
        Application_No=Application_No)
    application_details.update(Inspection_Date=Inspection_Date,
                               Sample_Drawn_By=sample_drawn_by,
                               Sample_Inspected_By=None,
                               Sample_Drawn=no_of_sample_drawn,
                               Sample_Size=total_sample_size,
                               Inspection_Method=inspection_method,
                               Inspection_Method_Other=inspection_method_other,
                               Pest_Detected=pest_detected,
                               Pest_Scientific_Name=Pest_Scientific_Name,
                               Infestation_Level=infestation_level,
                               Pest_Status=live_dead,
                               Pest_Risk_Category=risk_category,
                               Pest_QR_Detected=Pest_QR_Detected,
                               Pest_QR_Comment=Pest_QR_Detected_Comments,
                               Treatment_Possible=treatment_possible,
                               Treatment_Comment=Treatment_Comment,
                               Laboratory_Analysis_Required=Laboratory_Analysis_Required,
                               Laboratory_Analysis_Comment=Laboratory_Analysis_Comment,
                               Phytosanitary_Measures=Phytosanitary_Measures,
                               Phytosanitary_Measures_Comment=Phytosanitary_Measures_Comment,
                               Inspection_Remarks=remarks,
                               Export_Permit=export_permit,
                               )
    if pest_category == "Insect":
        application_details.update(Pest_Insect=pest_category)
    elif pest_category == "Mite":
        application_details.update(Pest_Mite=pest_category)
    elif pest_category == "Fungi":
        application_details.update(Pest_Fungi=pest_category)
    elif pest_category == "Bacteria":
        application_details.update(Pest_Bacteria=pest_category)
    elif pest_category == "Virus":
        application_details.update(Pest_Virus=pest_category)
    elif pest_category == "Nematode":
        application_details.update(Pest_Nematode=pest_category)
    elif pest_category == "Weed":
        application_details.update(Pest_Weed=pest_category)

    if treatmentType == "Chemical":
        application_details.update(Treatment_Chemical=treatmentType)
        application_details.update(Treatment_Chemical_Name=chemcial_name)
        if treatment == "Fumigation":
            application_details.update(Treatment_Chemical_Fumigation=treatment)
        elif treatment == "Spray":
            application_details.update(Treatment_Chemical_Fumigation=treatment)
        elif treatment == "Seed treatment ":
            application_details.update(Treatment_Chemical_Fumigation=treatment)
        elif treatment == "others":
            application_details.update(Treatment_Chemical_Fumigation=treatment)
            application_details.update(Treatment_Chemical_Other_Specific=others_treatment)
        application_details.update(Treatment_Chemical_Concentration=Concentration)
        application_details.update(Treatment_Chemical_Duration=Duration_Temperature)
        application_details.update(Treatment_Chemical_Treated_By=treated_by)
        application_details.update(Treatment_Chemical_Additional_Info=additional_Info)
    elif treatmentType == "Irradiation":
        application_details.update(Treatment_Irradiation=treatmentType)
    elif treatmentType == "Hot Water":
        application_details.update(Treatment_Hot_Water=treatmentType)
    elif treatmentType == "Dry Heat":
        application_details.update(Treatment_Dry_Heat=treatmentType)
    elif treatmentType == "Vapour Heat":
        application_details.update(Treatment_Vapour_Heat=treatmentType)
    elif treatmentType == "Cold Treatment":
        application_details.update(Treatment_Cold_Treatment=treatmentType)

    work_details = t_workflow_details.objects.filter(Application_No=Application_No)
    work_details.update(Action_Date=date.today())
    work_details.update(Application_Status='A')
    application_list = t_workflow_details.objects.filter(Assigned_Role_Id='5', Assigned_To=Login_Id,
                                                         Application_Status='P')
    if application_list.exists():
        for service_code in application_list:
            code = service_code.Service_Code
        service = t_service_master.objects.filter(Service_Code=code)
        for service in service:
            service_name = service.Service_Name
    else:
        service_name = None
    return render(request, 'inspector_pending_list.html',
                  {'service_name': service_name, 'application_details': application_list})


# Registration Of Nursery/Seed Growers
def registration_application(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'nursery_registration/apply_nursery_registration.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def save_nursery_reg(request):
    data = dict()
    service_code = "RNS"
    nursery_reg_app_no(service_code)
    print(nursery_reg_app_no)
    Nursery_Category = request.POST.get('Nursery_Category')
    License_No = request.POST.get('Nursery_Category')
    Company_Name = request.POST.get('License_No')
    Company_Address = request.POST.get('Company_Address')
    CID = request.POST.get('CID')
    Owner_Name = request.POST.get('Owner_Name')
    contactNo = request.POST.get('contactNo')
    email = request.POST.get('email')
    Unit_Area = request.POST.get('Unit_Area')
    Area = request.POST.get('Area')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')
    location_code = request.POST.get('location_code')
    Nursery_Type = request.POST.get('Nursery_Type')

    t_plant_clearence_nursery_seed_grower_t1.objects.create(
        Application_No=nursery_reg_app_no,
        Nursery_Category=Nursery_Category,
        License_No=License_No,
        Company_Name=Company_Name,
        Company_Address=Company_Address,
        CID=CID,
        Owner_Name=Owner_Name,
        contactNo=contactNo,
        email=email,
        Unit_Area=Unit_Area,
        Area=Area,
        dzongkhag=dzongkhag,
        gewog=gewog,
        village=village,
        location_code=location_code,
        Nursery_Type=Nursery_Type,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Facilities_Land=None,
        Facilities_Nursery_House=None,
        Facilities_Irrigation=None,
        Facilities_Tools=None,
        Facilities_Store=None,
        Manpower_Labour=None,
        Manpower_Skilled=None,
        Seed_Type=None,
        Technical_Clearance=None,
        Recommendation=None,
        Resubmit_Remarks=None,
        Resubmit_Date=None,
        Clearance_Number=None
    )
    field_id = t_location_field_office_mapping.objects.filter(pk=location_code)
    for field_office in field_id:
        field_office_id = field_office.Field_Office_Id_id
    t_workflow_details.objects.create(Application_No=nursery_reg_app_no, Applicant_Id=request.session['email'],
                                      Assigned_To=None, Field_Office_Id=field_office_id, Section='Plant',
                                      Assigned_Role_Id='4',
                                      Action_Date=None, Application_Status='P',
                                      Service_Code=serviceCode)
    data['applicationNo'] = nursery_reg_app_no
    return JsonResponse(data)


def nursery_reg_app_no(serviceCode):
    last_export_application_no = t_plant_clearence_nursery_seed_grower_t1.objects.aggregate(
        Max('Application_No'))
    last_application_no = last_export_application_no['Application_No__max']
    if not last_application_no:
        year = timezone.now().year
        newApplicationNo = serviceCode + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_application_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newApplicationNo = serviceCode + "/" + str(year) + "/" + AppNo
    return newApplicationNo


def add_file_reg(request):
    data = dict()
    myFile = request.FILES['document']
    fs = FileSystemStorage("attachments/plant/nursery_registration" + str(timezone.now().year))
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def add_file_name_reg(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)
        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'nursery_registration/file_attachment_page.html', {'file_attach': file_attach})


def get_nursery_clearnace_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_export_permit = t_plant_clearence_nursery_seed_grower_t1.objects.aggregate(Max('Clearance_Number'))
    last_export_permit_no = last_export_permit['Clearance_Number__max']
    if not last_export_permit_no:
        year = timezone.now().year
        new_clearnace_no = Field_Code + "/" + "RNS" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_export_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        new_clearnace_no = Field_Code + "/" + "RNS" + "/" + str(year) + "/" + AppNo
    return new_clearnace_no


# Seed Certification
def seed_certificate_application(request):
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    location = t_location_field_office_mapping.objects.all()

    return render(request, 'seed_certification/apply_seed_certification.html',
                  {'dzongkhag': dzongkhag, 'gewog': gewog, 'village': village,
                   'location': location})


def save_seed_cert(request):
    data = dict()
    serviceCode = "RSC"
    certifcate_app_no(serviceCode)
    Nursery_Category = request.POST.get('Nursery_Category')
    License_No = request.POST.get('Nursery_Category')
    Company_Name = request.POST.get('License_No')
    Company_Address = request.POST.get('Company_Address')
    CID = request.POST.get('CID')
    Owner_Name = request.POST.get('Owner_Name')
    contactNo = request.POST.get('contactNo')
    email = request.POST.get('email')
    Unit_Area = request.POST.get('Unit_Area')
    Area = request.POST.get('Area')
    dzongkhag = request.POST.get('dzongkhag')
    gewog = request.POST.get('gewog')
    village = request.POST.get('village')

    t_plant_seed_certification_t1.objects.create(
        Application_No=certifcate_app_no,
        Nursery_Category=Nursery_Category,
        License_No=License_No,
        Company_Name=Company_Name,
        Company_Address=Company_Address,
        CID=CID,
        Owner_Name=Owner_Name,
        contactNo=contactNo,
        email=email,
        Unit_Area=Unit_Area,
        Area=Area,
        dzongkhag=dzongkhag,
        gewog=gewog,
        village=village,
        Inspection_Date=None,
        Inspection_Leader=None,
        Inspection_Team=None,
        Recommendation=None,
        Seed_Certificate=None,
        Certificate_Date=None
    )


def certifcate_app_no(serviceCode):
    last_export_application_no = t_plant_export_certificate_plant_plant_products_t1.objects.aggregate(
        Max('Application_No'))
    last_application_no = last_export_application_no['Application_No__max']
    if not last_application_no:
        year = timezone.now().year
        newApplicationNo = serviceCode + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_application_no)[9:13]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        newApplicationNo = serviceCode + "/" + str(year) + "/" + AppNo
    return newApplicationNo


def add_file_certificate(request):
    data = dict()
    myFile = request.FILES['cordyceps_document']
    fs = FileSystemStorage("attachments/plant/export_permit" + str(timezone.now().year))
    if fs.exists(myFile.name):
        data['form_is_valid'] = False
    else:
        fs.save(myFile.name, myFile)
        data['form_is_valid'] = True
    return JsonResponse(data)


def add_file_name_certificate(request):
    if request.method == 'POST':
        Application_No = request.POST.get('appNo')
        fileName = request.POST.get('filename')
        Applicant_Id = request.session['email']

        t_file_attachment.objects.create(Application_No=Application_No, Applicant_Id=Applicant_Id,
                                         Role_Id=None,
                                         Attachment=fileName)
        file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'export_permit/cordyceps_file_attachment_page.html', {'file_attach': file_attach})


def get_seed_cerficate_no(request):
    global Field_Code
    Field_Office_Id = request.session['field_office_id']
    code = t_field_office_master.objects.filter(pk=Field_Office_Id)
    for code in code:
        Field_Code = code.Field_Office_Code

    last_export_permit = t_plant_seed_certification_t1.objects.aggregate(Max('Seed_Certificate'))
    last_export_permit_no = last_export_permit['Seed_Certificate__max']
    if not last_export_permit_no:
        year = timezone.now().year
        new_cerficate_no = Field_Code + "/" + "RSC" + "/" + str(year) + "/" + "0001"
    else:
        substring = str(last_export_permit_no)[13:17]
        substring = int(substring) + 1
        AppNo = str(substring).zfill(4)
        year = timezone.now().year
        new_cerficate_no = Field_Code + "/" + "RSC" + "/" + str(year) + "/" + AppNo
    return new_cerficate_no


# certificates
def certificate_print(request):
    return render(request, 'certificate_printing.html')


def get_certificate_details(request):
    application_No = request.POST.get('application_id')
    service_code = request.POST.get('service_code')
    if service_code == 'MPP':
        application_details = t_workflow_details.objects.filter(Application_No=application_No, Application_Status='A')
        if application_details.exists():
            details = t_plant_movement_permit_t1.objects.filter(Application_No=application_No, Permit_Type='P')
            if details.exists():
                certificate_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_No)
                return render(request, 'certificate_printing.html', {'certificate_details': certificate_details})
            else:
                certificate_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_No,
                                                                                Permit_Type='A')
                return render(request, 'certificate_printing.html', {'certificate_details': certificate_details})
        else:
            details = t_plant_movement_permit_t1.objects.filter(Movement_Permit_No=application_No)
            if details.exists():
                certificate_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_No)
                return render(request, 'certificate_printing.html', {'certificate_details': certificate_details})
            else:
                certificate_details = t_plant_movement_permit_t1.objects.filter(Application_No=application_No,
                                                                                Permit_Type='A')
                return render(request, 'certificate_printing.html', {'certificate_details': certificate_details})
    elif service_code == 'IPP':
        application_details = t_workflow_details.objects.filter(Application_No=application_No, Application_Status='A')
        if application_details.exists():
            details = t_plant_import_permit_t1.objects.filter(Application_No=application_No, Permit_Type='P')
            if details.exists():
                certificate_details = t_plant_import_permit_t1.objects.filter(Application_No=application_No)
                return render(request, 'certificate_printing.html', {'certificate_details': certificate_details})
            else:
                certificate_details = t_plant_import_permit_t1.objects.filter(Application_No=application_No,
                                                                              Permit_Type='A')
                return render(request, 'certificate_printing.html', {'certificate_details': certificate_details})
        else:
            details = t_plant_import_permit_t1.objects.filter(Movement_Permit_No=application_No)
            if details.exists():
                certificate_details = t_plant_import_permit_t1.objects.filter(Application_No=application_No)
                return render(request, 'certificate_printing.html', {'certificate_details': certificate_details})
            else:
                certificate_details = t_plant_import_permit_t1.objects.filter(Application_No=application_No,
                                                                              Permit_Type='A')
                return render(request, 'certificate_printing.html', {'certificate_details': certificate_details})
