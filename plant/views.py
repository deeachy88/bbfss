import os
from datetime import date

from django.core.files.storage import FileSystemStorage
from django.db.models import Max
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_location_field_office_mapping, \
    t_user_master, t_field_office_master
from plant.models import t_plant_movement_permit_t2, t_plant_movement_permit_t1, t_workflow_details, \
    t_plant_movement_permit_t3, t_file_attachment


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
                                                  Qty=qty,
                                                  Remarks=remarks)
        imports_plant = t_plant_movement_permit_t2.objects.filter(Application_No=appNo)
    return render(request, 'movement_page.html', {'import': imports_plant, 'title': appNo})


def save_movement_permit(request):
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
                                      Assigned_To=None, Field_Office_Id=field_office_id, Section="Plant",
                                      Action_Date=date.today(), Application_Status='P')
    return render(request,'apply_movement_permit.html', {'applicationNo': last_application_no})


def oic_app(request):
    Field_Office_Id = request.session['field_office_id']
    Role_Id = request.session['Role_Id']
    new_movement_app = t_workflow_details.objects.filter(Assigned_To=Role_Id, Field_Office_Id=Field_Office_Id)
    return render(request, 'new_movement_permit.html', {'new_movement_app': new_movement_app})


def ins_app(request):
    Login_Id = request.session['login_id']
    new_movement_app = t_workflow_details.objects.filter(Assigned_To=Login_Id)
    return render(request, 'inspector_movement_permit.html', {'new_movement_app': new_movement_app})


def view_app_details(request):
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


def view_app_details_ins(request):
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
    movement_permit = t_plant_movement_permit_t3.objects.filter(Application_No=application_id)

    return render(request, 'app_details_inspector.html',
                  {'application_details': application_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village, 'location': location, 'details_list': details_list,
                   'inspector_list': user_role_list, 'movement_permit': movement_permit})


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
    fs = FileSystemStorage("attachments/plant/" + str(timezone.now().year))
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
        fs = FileSystemStorage("attachments/plant/" + str(timezone.now().year))
        fs.delete(str(fileName))
    file.delete()

    file_attach = t_file_attachment.objects.filter(Application_No=Application_No)
    return render(request, 'file_attachment_page.html', {'file_attach': file_attach})
