from datetime import date, datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from administrator.models import t_dzongkhag_master, t_gewog_master, t_village_master, t_service_master, t_user_master, \
    t_location_field_office_mapping, t_field_office_master, t_unit_master
from bbfss import settings

from common_service.models import t_common_complaint_t1, t_inspection_monitoring_t1, t_inspection_monitoring_t2, \
    t_inspection_monitoring_t3, t_inspection_monitoring_t4, t_commodity_inspection_t1, t_commodity_inspection_t2

from plant.models import t_workflow_details, t_file_attachment
from plant.views import inspector_application


def certificate_reportForm(request):
    field_office = t_field_office_master.objects.all()
    return render(request, 'certificate_report_form.html', {'field_office': field_office})


def permit_reportFrom(request):  # list of investigation report submitted to the Complaint Officer
    field_office = t_field_office_master.objects.all()
    return render(request, 'permit_report_form.html', {'field_office': field_office})


def view_certificateList(request):
    Application_No = request.GET.get('application_id')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    complaint_file = t_file_attachment.objects.filter(Application_No=Application_No, Role_Id='8')
    investigation_file = t_file_attachment.objects.filter(Application_No=Application_No, Role_Id='5')
    for userId in details:
        user_id = userId.Assign_To
        user_details = t_user_master.objects.filter(Login_Id=user_id)

    return render(request, 'complaint_handling/complaint_officer_complaint_close.html',
                  {'complaint_details': details, 'user_details': user_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village, 'complaint_file': complaint_file, 'investigation_file': investigation_file})


def view_permitList(request):
    Application_No = request.GET.get('application_id')
    dzongkhag = t_dzongkhag_master.objects.all()
    gewog = t_gewog_master.objects.all()
    village = t_village_master.objects.all()
    details = t_common_complaint_t1.objects.filter(Application_No=Application_No)
    file = t_file_attachment.objects.filter(Application_No=Application_No)
    for userId in details:
        user_id = userId.Assign_To
        user_details = t_user_master.objects.filter(Login_Id=user_id)

    return render(request, 'complaint_handling/complaint_officer_complaint_close_details.html',
                  {'complaint_details': details, 'user_details': user_details, 'dzongkhag': dzongkhag, 'gewog': gewog,
                   'village': village, 'file': file})
