from datetime import date, datetime, timedelta

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from administrator.models import t_village_master, t_gewog_master, t_dzongkhag_master, t_country_master, \
    t_field_office_master, t_location_field_office_mapping, t_unit_master, t_service_master
from bbfss import settings
from food.models import t_food_export_certificate_t1, t_food_licensinf_food_handler_t1
from livestock.views import update_payment
from plant.models import t_workflow_details, t_file_attachment
from plant.views import inspector_application


def food_business_registration_licensing(request):
    return render(request, 'registration_licensing/registration_application.html')


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
                                      " Been Accepted. You Are Requested To Attend The Following Training"  \
                                      " Training Batch No: " + batchNo + " Training From" + from_training_Date + \
                                      " To " + to_training_Date + "." + remarks + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def result_update_list(request):
    result_details = t_food_licensinf_food_handler_t1.objects.filter(Training_Batch_No__isnull=False)
    return render(request, 'food_handler/food_handler_result_list.html',
                  {'application_details': result_details})


def result_update(request):
    app = request.POST.getlist('checkedVals')
    strings = app[0].split("#")
    for tempArr in strings:
        checkboxArr = tempArr.split("~")
        email = checkboxArr[0]
        app_no = checkboxArr[1]
        att = checkboxArr[2]
        print(email)
        print(app_no)
        print(att)

