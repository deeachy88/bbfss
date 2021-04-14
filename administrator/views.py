import hashlib
import os
import random
import string
from datetime import date

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.template.loader import render_to_string

from administrator.forms import UserForm, LocationFieldMappingForm, FieldOfficeForm, FodderVarietyForm, PlantFodderForm, \
    PlantProductForm, PesticideForm, OrnamentalPlantForm, CropSpeciesForm, ChemicalForm, CropVarietyForm, CropForm, \
    ServiceForm, DivisionForm, SectionForm, RoleForm, CropCategoryForm
from administrator.models import t_user_master, t_security_question_master, t_role_master, t_forgot_password, \
    t_section_master, t_village_master, t_gewog_master, t_dzongkhag_master, t_location_field_office_mapping, \
    t_field_office_master, t_plant_fodder_variety_master, t_plant_fodder_master, t_plant_product_master, \
    t_plant_pesticide_master, t_plant_ornamental_master, t_plant_crop_species_master, t_plant_chemical_master, \
    t_plant_crop_variety_master, t_plant_crop_master, t_service_master, t_division_master, t_plant_crop_category_master
from bbfss import settings
from plant.models import t_payment_details


def home(request):
    return render(request, 'index.html')


def login(request):
    _message = 'Please sign in'
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = t_user_master.objects.filter(Email_Id=_username)
        if user is not None:
            for user in user:
                check_pass = check_password(_password, user.Password)
                if check_pass:
                    if user.Is_Active:
                        if not user.Last_Login_Date:
                            if str(user.Login_Type) == "C":
                                request.session['Login_Id'] = user.Login_Id
                                security = t_security_question_master.objects.all()
                            else:
                                main_role = t_role_master.objects.filter(Role_Id=user.Role_Id_id)
                                for main_role in main_role:
                                    Role_Id = main_role.Role_Id
                                request.session['Login_Id'] = user.Login_Id
                                request.session['Email_Id'] = user.Email_Id
                                request.session['Role_Id'] = Role_Id
                                security = t_security_question_master.objects.all()
                            return render(request, 'update_password.html', {'security': security})
                        else:
                            if user.Login_Type == "C":
                                client = "client"
                                request.session['email'] = user.Email_Id
                                request.session['name'] = user.Name
                                request.session['role'] = client
                                request.session['login_id'] = user.Login_Id
                                return render(request, 'common_dashboard.html')
                            else:
                                mainrole = t_role_master.objects.filter(Role_Id=user.Role_Id_id)
                                for mainroles in mainrole:
                                    admin = "Agency Admin"
                                    focal_officer = "Focal Officer"
                                    complaint_officer = "Complaint Officer"
                                    OIC = "OIC"
                                    Inspector = "Inspector"
                                    Chief = "Chief"
                                    DG = "DG"
                                    if admin == str(mainroles.Role_Name):
                                        request.session['role'] = admin
                                    elif DG == str(mainroles.Role_Name):
                                        request.session['username'] = user.Name
                                        request.session['role'] = DG
                                    elif focal_officer == str(mainroles.Role_Name):
                                        request.session['username'] = user.Name
                                        request.session['role'] = focal_officer
                                        request.session['Role_Id'] = mainroles.Role_Id
                                        request.session['section'] = user.Section_Id_id
                                    elif complaint_officer == str(mainroles.Role_Name):
                                        request.session['username'] = user.name
                                        request.session['role'] = complaint_officer
                                    elif OIC == str(mainroles.Role_Name):
                                        request.session['username'] = user.Name
                                        request.session['role'] = OIC
                                        request.session['Role_Id'] = mainroles.Role_Id
                                        request.session['field_office_id'] = user.Field_Office_Id_id
                                    elif Inspector == str(mainroles.Role_Name):
                                        request.session['username'] = user.Name
                                        request.session['role'] = Inspector
                                        request.session['field_office_id'] = user.Field_Office_Id_id
                                        request.session['login_id'] = user.Login_Id
                                    elif Chief == str(mainroles.Role_Name):
                                        request.session['username'] = user.Name
                                        request.session['role'] = Chief
                                        request.session['Division_Id'] = user.Division_Id_id
                                return render(request, 'common_dashboard.html')
                    else:
                        _message = 'Your account is not activated'
                else:
                    _message = 'Invalid login, please try again.'
        else:
            _message = 'Invalid login, please try again.'
    context = {'message': _message}
    return render(request, 'index.html', context)


def sendmail(request, name, email, password):
    subject = 'USER CREATED'
    message = "Dear " + name + " Login Id has been created for Bhutan Bio-Food Security System. Your Login Id is " \
              + email + " And Password is " + password + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def accept_mail(request, Name, Email_Id, password):
    subject = 'USER CREATED'
    message = "Dear " + Name + " Your Registration for Bhutan Bio-Food Security System Is Accepted. Your Login Id is " \
              + Email_Id + " And Password is " + password + ""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email_Id]
    send_mail(subject, message, email_from, recipient_list)


def reject_mail(request, Name, Email_Id):
    subject = 'USER CREATED'
    message = "Dear " + Name + " Your Registration for Bhutan Bio-Food Security System Is Rejected ."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email_Id]
    send_mail(subject, message, email_from, recipient_list)


def user(request):
    if request.method == 'POST':
        name = request.POST['name']
        eid = request.POST['Employee_Id']
        gender = request.POST['gender']
        email = request.POST['email']
        contact_number = request.POST['mobile']
        role = request.POST['role']
        division = request.POST['division']
        section = request.POST['section']
        field = request.POST['field']

        password = get_random_password_string(8)
        password_value = make_password(password)
        form = UserForm(request.POST)
        if form.is_valid():
            if role == "2":
                t_user_master.objects.create(Login_Type="I", Client_Type=None, Name=name, Employee_Id=eid,
                                             Gender=gender,
                                             Mobile_Number=contact_number, Email_Id=email, Password=password_value,
                                             Password_Salt=None, CID=None, Agency=None, License_No=None,
                                             Address=None, Is_Active="Y", Logical_Delete="N",
                                             Last_Login_Date=None, Created_By=None, Created_On=None,
                                             Updated_By=None, Updated_On=None, Dzongkhag_Code_id=None,
                                             Gewog_Code_id=None, Section_Id_id=section, Village_Code_id=None,
                                             Accept_Reject=None, Division_Id_id=division, Field_Office_Id_id=None,
                                             Role_Id_id=role)
                user_details = t_user_master.objects.filter(Email_Id__iexact=email)
            elif role == "6":
                t_user_master.objects.create(Login_Type="I", Client_Type=None, Name=name, Employee_Id=eid,
                                             Gender=gender,
                                             Mobile_Number=contact_number, Email_Id=email, Password=password_value,
                                             Password_Salt=None, CID=None, Agency=None, License_No=None,
                                             Address=None, Is_Active="Y", Logical_Delete="N",
                                             Last_Login_Date=None, Created_By=None, Created_On=None,
                                             Updated_By=None, Updated_On=None, Dzongkhag_Code_id=None,
                                             Gewog_Code_id=None, Section_Id_id=None, Village_Code_id=None,
                                             Accept_Reject=None, Division_Id_id=division, Field_Office_Id_id=None,
                                             Role_Id_id=role)
                user_details = t_user_master.objects.filter(Email_Id__iexact=email)
            elif role == "4":
                t_user_master.objects.create(Login_Type="I", Client_Type=None, Name=name, Employee_Id=eid,
                                             Gender=gender,
                                             Mobile_Number=contact_number, Email_Id=email, Password=password_value,
                                             Password_Salt=None, CID=None, Agency=None, License_No=None,
                                             Address=None, Is_Active="Y", Logical_Delete="N",
                                             Last_Login_Date=None, Created_By=None, Created_On=None,
                                             Updated_By=None, Updated_On=None, Dzongkhag_Code_id=None,
                                             Gewog_Code_id=None, Section_Id_id=None, Village_Code_id=None,
                                             Accept_Reject=None, Division_Id_id=None, Field_Office_Id_id=field,
                                             Role_Id_id=role)
                user_details = t_user_master.objects.filter(Email_Id__iexact=email)
            elif role == "5":
                t_user_master.objects.create(Login_Type="I", Client_Type=None, Name=name, Employee_Id=eid,
                                             Gender=gender,
                                             Mobile_Number=contact_number, Email_Id=email, Password=password_value,
                                             Password_Salt=None, CID=None, Agency=None, License_No=None,
                                             Address=None, Is_Active="Y", Logical_Delete="N",
                                             Last_Login_Date=None, Created_By=None, Created_On=None,
                                             Updated_By=None, Updated_On=None, Dzongkhag_Code_id=None,
                                             Gewog_Code_id=None, Section_Id_id=None, Village_Code_id=None,
                                             Accept_Reject=None, Division_Id_id=None, Field_Office_Id_id=field,
                                             Role_Id_id=role)
                user_details = t_user_master.objects.filter(Email_Id__iexact=email)
            else:
                t_user_master.objects.create(Login_Type="I", Client_Type=None, Name=name, Employee_Id=eid,
                                             Gender=gender,
                                             Mobile_Number=contact_number, Email_Id=email, Password=password_value,
                                             Password_Salt=None, CID=None, Agency=None, License_No=None,
                                             Address=None, Is_Active="Y", Logical_Delete="N",
                                             Last_Login_Date=None, Created_By=None, Created_On=None,
                                             Updated_By=None, Updated_On=None, Dzongkhag_Code_id=None,
                                             Gewog_Code_id=None, Section_Id_id=None, Village_Code_id=None,
                                             Accept_Reject=None, Division_Id_id=None, Field_Office_Id_id=None,
                                             Role_Id_id=role)
                user_details = t_user_master.objects.filter(Email_Id__iexact=email)
        details = t_user_master.objects.filter(Login_Type="I")
        sendmail(request, name, email, password)
        return render(request, 'user.html', {'form': form, 'details': details})
    else:
        details = t_user_master.objects.filter(Login_Type="I")
        form = UserForm()
        roles = t_role_master.objects.all()
        section = t_section_master.objects.all()
        division = t_division_master.objects.all()
        field_office = t_field_office_master.objects.all()
        return render(request, 'user.html', {'form': form, 'details': details, 'role': roles, 'section': section,
                                             'division': division, 'field_office': field_office})


def edit(request, Login_Id):
    details = get_object_or_404(t_user_master, id=Login_Id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=details)
    else:
        form = UserForm(instance=details)
    return save_user_form(request, form, Login_Id, 'edit_users.html')


def save_user_form(request, form, id, template_name):
    data = dict()
    if request.method == 'POST':
        data['form_is_valid'] = True
        username = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        role = request.POST.get('role_id')
        t_user_master.objects.filter(id=id).update(name=username, email=email, contact_number=contact_number,
                                                   address=address,
                                                   role_id_id=role)
        books = t_user_master.objects.all()
        data['html_user_list'] = render_to_string('user.html', {
            'books': books
        })
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def logout(request):
    request.session.flush()
    return redirect('/')


def role_manage(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            roles = t_role_master.objects.all().order_by('Role_Id')
            return render(request, 'role.html', {'form': form, 'role': roles})
    else:
        roles = t_role_master.objects.all().order_by('Role_Id')
        form = RoleForm()
        return render(request, 'role.html', {'form': form, 'role': roles})


def edit_role(request, Role_Id):
    roles = get_object_or_404(t_role_master, pk=Role_Id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=roles)
    else:
        form = RoleForm(instance=roles)
    return save_role_form(request, form, 'edit_role.html')


def save_role_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            roles = t_role_master.objects.all().order_by('Role_Id')
            data['html_book_list'] = render_to_string('role.html', {
                'roles': roles
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def section_manage(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            section = t_section_master.objects.all()
            return render(request, 'section.html', {'form': form, 'section': section})
    else:
        section = t_section_master.objects.all()
        form = SectionForm()
        return render(request, 'section.html', {'form': form, 'section': section})


def edit_section(request, Section_Id):
    section = get_object_or_404(t_section_master, pk=Section_Id)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
    else:
        form = SectionForm(instance=section)
    return save_section_form(request, form, 'edit_section.html')


def save_section_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            section = t_section_master.objects.all()
            data['html_section_list'] = render_to_string('section.html', {
                'section': section
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def division_manage(request):
    if request.method == 'POST':
        form = DivisionForm(request.POST)
        if form.is_valid():
            form.save()
            division = t_division_master.objects.all()
            return render(request, 'division.html', {'form': form, 'division': division})
    else:
        division = t_division_master.objects.all()
        form = DivisionForm()
        return render(request, 'division.html', {'form': form, 'division': division})


def edit_division(request, Division_Id):
    division = get_object_or_404(t_division_master, pk=Division_Id)
    if request.method == 'POST':
        form = DivisionForm(request.POST, instance=division)
    else:
        form = DivisionForm(instance=division)
    return save_division_form(request, form, 'edit_division.html')


def save_division_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            division = t_division_master.objects.all()
            data['html_division_list'] = render_to_string('division.html', {
                'division': division
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def crop_category_manage(request):
    if request.method == 'POST':
        form = CropCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            crop_category = t_plant_crop_category_master.objects.all()
            return render(request, 'plant_crop_category.html', {'form': form, 'crop_category': crop_category})
    else:
        crop_category = t_plant_crop_category_master.objects.all()
        form = CropCategoryForm()
        return render(request, 'plant_crop_category.html', {'form': form, 'crop_category': crop_category})


def edit_crop_category(request, Crop_Category_Id):
    crop_category = get_object_or_404(t_plant_crop_category_master, pk=Crop_Category_Id)
    if request.method == 'POST':
        form = CropCategoryForm(request.POST, instance=crop_category)
    else:
        form = CropCategoryForm(instance=crop_category)
    return save_crop_category_form(request, form, 'edit_crop_category.html')


def save_crop_category_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            crop_category = t_plant_crop_category_master.objects.all()
            return render(request, 'plant_crop_category.html', {'form': form, 'crop_category': crop_category
                                                                })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def delete_crop_category(request, Crop_Category_Id):
    print("test check delete")
    crop_category = get_object_or_404(t_plant_crop_category_master, pk=Crop_Category_Id)
    data = dict()
    if request.method == 'POST':
        crop_category.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        crop_category = t_plant_crop_category_master.objects.all()
        data['html_form'] = render_to_string('plant_crop_category.html', {'crop_category': crop_category})
    else:
        context = {'crop_category': crop_category}
        data['html_form'] = render_to_string('crop_category_delete.html', context, request=request)
    return JsonResponse(data)


def service_manage(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            service = t_service_master.objects.all()
            return render(request, 'service.html', {'form': form, 'service': service})
    else:
        service = t_service_master.objects.all()
        form = ServiceForm()
        return render(request, 'service.html', {'form': form, 'service': service})


def edit_service(request, Service_Id):
    service = get_object_or_404(t_service_master, pk=Service_Id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
    else:
        form = ServiceForm(instance=service)
    return save_service_form(request, form, 'edit_service.html')


def save_service_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            division = t_service_master.objects.all()
            data['html_book_list'] = render_to_string('service.html', {
                'service': t_service_master
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)


def crop_manage(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            form.save()
            crop = t_plant_crop_master.objects.all()
            form = CropForm()
            return render(request, 'crop.html', {'form': form, 'crop': crop})
    else:
        crop = t_plant_crop_master.objects.all()
        form = CropForm()
        return render(request, 'crop.html', {'form': form, 'crop': crop})


def edit_crop(request, Crop_Id):
    crop = get_object_or_404(t_plant_crop_master, pk=Crop_Id)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
    else:
        form = CropForm(instance=crop)
    return save_crop_form(request, form, 'edit_crop.html')


def save_crop_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            crop = t_plant_crop_master.objects.all()
            data['html_book_list'] = render_to_string('crop.html', {
                'crop': crop
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def crop_variety_manage(request):
    if request.method == 'POST':
        form = CropVarietyForm(request.POST)
        if form.is_valid():
            form.save()
            form = CropVarietyForm()
            variety = t_plant_crop_variety_master.objects.all()
            return render(request, 'crop_variety.html', {'form': form, 'variety': variety})
    else:
        variety = t_plant_crop_variety_master.objects.all()
        form = CropVarietyForm()
        return render(request, 'crop_variety.html', {'form': form, 'variety': variety})


def edit_crop_variety(request, Crop_Variety_Id):
    variety = get_object_or_404(t_plant_crop_variety_master, pk=Crop_Variety_Id)
    if request.method == 'POST':
        form = CropVarietyForm(request.POST, instance=variety)
    else:
        form = CropVarietyForm(instance=variety)
    return save_crop_variety_form(request, form, 'edit_crop_variety.html')


def save_crop_variety_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            variety = t_plant_crop_variety_master.objects.all()
            data['html_book_list'] = render_to_string('crop_variety.html', {
                'variety': variety
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def chemical_manage(request):
    if request.method == 'POST':
        form = ChemicalForm(request.POST)
        if form.is_valid():
            form.save()
            form = ChemicalForm()
            chemical = t_plant_chemical_master.objects.all()
            return render(request, 'chemical.html', {'form': form, 'chemical': chemical})
    else:
        chemical = t_plant_chemical_master.objects.all()
        form = ChemicalForm()
        return render(request, 'chemical.html', {'form': form, 'chemical': chemical})


def edit_chemical(request, Chemical_Id):
    variety = get_object_or_404(t_plant_chemical_master, pk=Chemical_Id)
    if request.method == 'POST':
        form = ChemicalForm(request.POST, instance=variety)
    else:
        form = ChemicalForm(instance=variety)
    return save_chemical_form(request, form, 'edit_chemical.html')


def save_chemical_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            chemical = t_plant_chemical_master.objects.all()
            data['html_book_list'] = render_to_string('chemical.html', {
                'chemical': chemical
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def crop_species_manage(request):
    if request.method == 'POST':
        form = CropSpeciesForm(request.POST)
        if form.is_valid():
            form.save()
            form = CropSpeciesForm()
            species = t_plant_crop_species_master.objects.all()
            return render(request, 'crop_species.html', {'form': form, 'species': species})
    else:
        species = t_plant_crop_species_master.objects.all()
        form = CropSpeciesForm()
        return render(request, 'crop_species.html', {'form': form, 'species': species})


def edit_crop_species(request, Crop_Species_Id):
    species = get_object_or_404(t_plant_crop_species_master, pk=Crop_Species_Id)
    if request.method == 'POST':
        form = CropSpeciesForm(request.POST, instance=species)
    else:
        form = CropSpeciesForm(instance=species)
    return save_crop_species_form(request, form, 'edit_crop_species.html')


def save_crop_species_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            species = t_plant_crop_species_master.objects.all()
            data['html_book_list'] = render_to_string('crop_species.html', {
                'species': species
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def ornamental_plant_manage(request):
    if request.method == 'POST':
        form = OrnamentalPlantForm(request.POST)
        if form.is_valid():
            form.save()
            form = OrnamentalPlantForm()
            ornamental = t_plant_ornamental_master.objects.all()
            return render(request, 'plant_ornamental.html', {'form': form, 'ornamental': ornamental})
    else:
        ornamental = t_plant_ornamental_master.objects.all()
        form = OrnamentalPlantForm()
        return render(request, 'plant_ornamental.html', {'form': form, 'ornamental': ornamental})


def edit_ornamental_plant(request, Ornamental_Plant_Id):
    ornamental = get_object_or_404(t_plant_ornamental_master, pk=Ornamental_Plant_Id)
    if request.method == 'POST':
        form = OrnamentalPlantForm(request.POST, instance=ornamental)
    else:
        form = OrnamentalPlantForm(instance=ornamental)
    return save_ornamental_plant_form(request, form, 'edit_ornamental_plant.html')


def save_ornamental_plant_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            ornamental = t_plant_ornamental_master.objects.all()
            data['html_book_list'] = render_to_string('plant_ornamental.html', {
                'ornamental': ornamental
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def pesticide_manage(request):
    if request.method == 'POST':
        form = PesticideForm(request.POST)
        if form.is_valid():
            form.save()
            pesticide = t_plant_pesticide_master.objects.all()
            return render(request, 'pesticide.html', {'form': form, 'pesticide': pesticide})
    else:
        pesticide = t_plant_pesticide_master.objects.all()
        form = PesticideForm()
        return render(request, 'pesticide.html', {'form': form, 'pesticide': pesticide})


def edit_pesticide(request, Pesticide_Id):
    pesticide = get_object_or_404(t_plant_pesticide_master, pk=Pesticide_Id)
    if request.method == 'POST':
        form = PesticideForm(request.POST, instance=pesticide)
    else:
        form = PesticideForm(instance=pesticide)
    return save_pesticide_form(request, form, 'edit_pesticide.html')


def save_pesticide_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            pesticide = t_plant_pesticide_master.objects.all()
            data['html_book_list'] = render_to_string('pesticide.html', {
                'pesticide': pesticide
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def plant_product_manage(request):
    if request.method == 'POST':
        form = PlantProductForm(request.POST)
        if form.is_valid():
            form.save()
            plant_product = t_plant_product_master.objects.all()
            return render(request, 'plant_product.html', {'form': form, 'plant_product': plant_product})
    else:
        plant_product = t_plant_product_master.objects.all()
        form = PlantProductForm()
        return render(request, 'plant_product.html', {'form': form, 'plant_product': plant_product})


def edit_plant_product(request, Plant_Product_Id):
    plant_product = get_object_or_404(t_plant_product_master, pk=Plant_Product_Id)
    if request.method == 'POST':
        form = PlantProductForm(request.POST, instance=plant_product)
    else:
        form = PlantProductForm(instance=plant_product)
    return save_plant_product_form(request, form, 'edit_plant_product.html')


def save_plant_product_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            product = t_plant_product_master.objects.all()
            data['html_book_list'] = render_to_string('plant_product.html', {
                'plant_product': product
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def plant_fodder_manage(request):
    if request.method == 'POST':
        form = PlantFodderForm(request.POST)
        if form.is_valid():
            form.save()
            plant_fodder = t_plant_fodder_master.objects.all()
            return render(request, 'plant_fodder.html', {'form': form, 'plant_fodder': plant_fodder})
    else:
        plant_fodder = t_plant_fodder_master.objects.all()
        form = PlantFodderForm()
        return render(request, 'plant_fodder.html', {'form': form, 'plant_fodder': plant_fodder})


def edit_plant_fodder(request, Fodder_Id):
    plant_fodder = get_object_or_404(t_plant_fodder_master, pk=Fodder_Id)
    if request.method == 'POST':
        form = PlantFodderForm(request.POST, instance=plant_fodder)
    else:
        form = PlantFodderForm(instance=plant_fodder)
    return save_plant_fodder_form(request, form, 'edit_plant_fodder.html')


def save_plant_fodder_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            plant_fodder = t_plant_fodder_master.objects.all()
            data['html_book_list'] = render_to_string('plant_fodder.html', {
                'plant_fodder': plant_fodder
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def plant_fodder_variety_manage(request):
    if request.method == 'POST':
        form = FodderVarietyForm(request.POST)
        if form.is_valid():
            form.save()
            fodder_variety = t_plant_fodder_variety_master.objects.all()
            return render(request, 'fodder_variety.html', {'form': form, 'fodder_variety': fodder_variety})
    else:
        fodder_variety = t_plant_fodder_variety_master.objects.all()
        form = FodderVarietyForm()
        return render(request, 'fodder_variety.html', {'form': form, 'fodder_variety': fodder_variety})


def edit_fodder_variety(request, Fodder_Variety_Id):
    fodder_variety = get_object_or_404(t_plant_fodder_variety_master, pk=Fodder_Variety_Id)
    if request.method == 'POST':
        form = FodderVarietyForm(request.POST, instance=fodder_variety)
    else:
        form = FodderVarietyForm(instance=fodder_variety)
    return save_fodder_variety_form(request, form, 'edit_fodder_variety.html')


def save_fodder_variety_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            fodder_variety = t_plant_fodder_variety_master.objects.all()
            data['html_book_list'] = render_to_string('fodder_variety.html', {
                'fodder_variety': fodder_variety
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def field_office_page_manage(request):
    if request.method == 'POST':
        form = FieldOfficeForm(request.POST)
        if form.is_valid():
            form.save()
            field_office = t_field_office_master.objects.all()
            return render(request, 'field_office.html', {'form': form, 'field_office': field_office})
    else:
        field_office = t_field_office_master.objects.all()
        form = FieldOfficeForm()
        return render(request, 'field_office.html', {'form': form, 'field_office': field_office})


def edit_field_office(request, Field_Office_Id):
    field_office = get_object_or_404(t_field_office_master, pk=Field_Office_Id)
    if request.method == 'POST':
        form = FieldOfficeForm(request.POST, instance=field_office)
    else:
        form = FieldOfficeForm(instance=field_office)
    return save_field_office_form(request, form, 'edit_field_office.html')


def save_field_office_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            field_office = t_field_office_master.objects.all()
            data['html_book_list'] = render_to_string('field_office.html', {
                'fodder_office': field_office
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def location_field_manage(request):
    if request.method == 'POST':
        form = LocationFieldMappingForm(request.POST)
        if form.is_valid():
            form.save()
            location_mapping = t_location_field_office_mapping.objects.all()
            form = LocationFieldMappingForm()
            return render(request, 'location_mapping.html', {'form': form, 'location_mapping': location_mapping})
    else:
        location_mapping = t_location_field_office_mapping.objects.all()
        form = LocationFieldMappingForm()
        return render(request, 'location_mapping.html', {'form': form, 'location_mapping': location_mapping})


def edit_location_field(request, Location_Code):
    location_mapping = get_object_or_404(t_location_field_office_mapping, pk=Location_Code)
    if request.method == 'POST':
        form = LocationFieldMappingForm(request.POST, instance=location_mapping)
    else:
        form = LocationFieldMappingForm(instance=location_mapping)
    return save_location_field_form(request, form, 'edit_location_mapping.html')


def save_location_field_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            location_mapping = t_location_field_office_mapping.objects.all()
            data['html_book_list'] = render_to_string('location_mapping.html', {
                'location_mapping': location_mapping
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def delete_role(request, Role_Id):
    roles = get_object_or_404(t_role_master, pk=Role_Id)
    data = dict()
    if request.method == 'POST':
        roles.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        role = t_role_master.objects.all()
        data['html_form'] = render_to_string('role.html', {'role': role})
    else:
        context = {'role': roles}
        data['html_form'] = render_to_string('role_delete.html', context, request=request)
    return JsonResponse(data)


def delete_division(request, Division_Id):
    division = get_object_or_404(t_division_master, pk=Division_Id)
    data = dict()
    if request.method == 'POST':
        division.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        division = t_division_master.objects.all()
        data['html_form'] = render_to_string('division.html', {'division': division})
    else:
        context = {'division': division}
        data['html_form'] = render_to_string('division_delete.html', context, request=request)
    return JsonResponse(data)


def delete_section(request, Section_Id):
    section = get_object_or_404(t_section_master, pk=Section_Id)
    data = dict()
    if request.method == 'POST':
        section.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        section = t_section_master.objects.all()
        data['html_form'] = render_to_string('section.html', {'section': section})
    else:
        context = {'section': section}
        data['html_form'] = render_to_string('section_delete.html', context, request=request)
    return JsonResponse(data)


def delete_service(request, Service_Id):
    service = get_object_or_404(t_service_master, pk=Service_Id)
    data = dict()
    if request.method == 'POST':
        service.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        service = t_service_master.objects.all()
        data['html_form'] = render_to_string('service.html', {'service': service})
    else:
        context = {'service': service}
        data['html_form'] = render_to_string('service_delete.html', context, request=request)
    return JsonResponse(data)


def delete_crop(request, Crop_Id):
    crop = get_object_or_404(t_plant_crop_master, pk=Crop_Id)
    data = dict()
    if request.method == 'POST':
        crop.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        crops = t_plant_crop_master.objects.all()
        data['html_crop_list'] = render_to_string('crop.html', {'crop': crops})
    else:
        context = {'crop': crop}
        data['html_form'] = render_to_string('crop_delete.html', context, request=request)
    return JsonResponse(data)


def delete_crop_variety(request, Crop_Variety_Id):
    variety = get_object_or_404(t_plant_crop_variety_master, pk=Crop_Variety_Id)
    data = dict()
    if request.method == 'POST':
        variety.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        crop_variety = t_plant_crop_variety_master.objects.all()
        data['html_form'] = render_to_string('crop_variety.html', {'variety': crop_variety})
    else:
        context = {'variety': variety}
        data['html_form'] = render_to_string('crop_variety_delete.html', context, request=request)
    return JsonResponse(data)


def delete_chemical(request, Chemical_Id):
    chemical = get_object_or_404(t_plant_chemical_master, pk=Chemical_Id)
    data = dict()
    if request.method == 'POST':
        chemical.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        chemical = t_plant_chemical_master.objects.all()
        data['html_form'] = render_to_string('chemical.html', {'chemical': chemical})
    else:
        context = {'chemical': chemical}
        data['html_form'] = render_to_string('chemical_delete.html', context, request=request)
    return JsonResponse(data)


def delete_plant_species(request, Crop_Species_Id):
    species = get_object_or_404(t_plant_crop_species_master, pk=Crop_Species_Id)
    data = dict()
    if request.method == 'POST':
        species.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        species = t_plant_crop_species_master.objects.all()
        data['html_form'] = render_to_string('chemical.html', {'species': species})
    else:
        context = {'species': species}
        data['html_form'] = render_to_string('plant_species_delete.html', context, request=request)
    return JsonResponse(data)


def delete_ornamental(request, Ornamental_Plant_Id):
    ornamental = get_object_or_404(t_plant_ornamental_master, pk=Ornamental_Plant_Id)
    data = dict()
    if request.method == 'POST':
        ornamental.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        ornamental = t_plant_ornamental_master.objects.all()
        data['html_form'] = render_to_string('plant_ornamental.html', {'ornamental': ornamental})
    else:
        context = {'ornamental': ornamental}
        data['html_form'] = render_to_string('plant_ornamental_delete.html', context, request=request)
    return JsonResponse(data)


def delete_pesticide(request, Pesticide_Id):
    pesticide = get_object_or_404(t_plant_pesticide_master, pk=Pesticide_Id)
    data = dict()
    if request.method == 'POST':
        pesticide.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        pesticide = t_plant_pesticide_master.objects.all()
        data['html_form'] = render_to_string('pesticide.html', {'pesticide': pesticide})
    else:
        context = {'pesticide': pesticide}
        data['html_form'] = render_to_string('pesticide_delete.html', context, request=request)
    return JsonResponse(data)


def delete_product(request, Plant_Product_Id):
    plant_product = get_object_or_404(t_plant_product_master, pk=Plant_Product_Id)
    data = dict()
    if request.method == 'POST':
        plant_product.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        plant_products = t_plant_product_master.objects.all()
        data['html_form'] = render_to_string('plant_product.html', {'plant_product': plant_products})
    else:
        context = {'plant_product': plant_product}
        data['html_form'] = render_to_string('plant_product_delete.html', context, request=request)
    return JsonResponse(data)


def delete_plant_fodder(request, Fodder_Id):
    plant_fodder = get_object_or_404(t_plant_fodder_master, pk=Fodder_Id)
    data = dict()
    if request.method == 'POST':
        plant_fodder.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        plant_fodder = t_plant_fodder_master.objects.all()
        data['html_form'] = render_to_string('plant_fodder.html', {'plant_fodder': plant_fodder})
    else:
        context = {'plant_fodder': plant_fodder}
        data['html_form'] = render_to_string('plant_fodder_delete.html', context, request=request)
    return JsonResponse(data)


def delete_fodder_variety(request, Fodder_Variety_Id):
    fodder_variety = get_object_or_404(t_plant_fodder_variety_master, pk=Fodder_Variety_Id)
    data = dict()
    if request.method == 'POST':
        fodder_variety.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        fodder_variety = t_plant_fodder_variety_master.objects.all()
        data['html_form'] = render_to_string('fodder_variety.html', {'fodder_variety': fodder_variety})
    else:
        context = {'fodder_variety': fodder_variety}
        data['html_form'] = render_to_string('fodder_variety_delete.html', context, request=request)
    return JsonResponse(data)


def delete_field_office(request, Field_Office_Id):
    field_office = get_object_or_404(t_field_office_master, pk=Field_Office_Id)
    data = dict()
    if request.method == 'POST':
        field_office.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        field_office = t_field_office_master.objects.all()
        data['html_form'] = render_to_string('field_office.html', {'field_office': field_office})
    else:
        context = {'field_office': field_office}
        data['html_form'] = render_to_string('field_office_delete.html', context, request=request)
    return JsonResponse(data)


def delete_location_mapping(request, Location_Code):
    location_mapping = get_object_or_404(t_location_field_office_mapping, pk=Location_Code)
    data = dict()
    if request.method == 'POST':
        location_mapping.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        location_mapping = t_location_field_office_mapping.objects.all()
        data['html_form'] = render_to_string('location_mapping.html', {'location_mapping': location_mapping})
    else:
        context = {'location_mapping': location_mapping}
        data['html_form'] = render_to_string('location_mapping_delete.html', context, request=request)
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        client = request.POST['client']
        cid = request.POST['cid']
        name = request.POST['name']
        gender = request.POST['gender']
        email = request.POST['email']
        contact_number = request.POST['contactnumber']
        address = request.POST['address']

        contactPerson = request.POST['contactPerson']
        emailId = request.POST['emailId']
        mobile_number = request.POST['mobile_number']
        org_agency = request.POST['org_agency']
        org_license = request.POST['org_license']
        dzongkhag = request.POST['dzongkhag']
        gewog = request.POST['gewog']
        village = request.POST['village']
        org_address = request.POST['org_address']
        if client == "I":
            t_user_master.objects.create(Login_Type="C", Client_Type="I", Name=name, Employee_Id=None, Gender=gender,
                                         Mobile_Number=contact_number, Email_Id=email, Password=None,
                                         Password_Salt=None, CID=cid, Agency=None, License_No=None,
                                         Address=address, Is_Active="N", Logical_Delete="N",
                                         Last_Login_Date=None, Created_By=None, Created_On=None,
                                         Updated_By=None, Updated_On=None, Dzongkhag_Code_id=None,
                                         Gewog_Code_id=None, Section_Id_id=None, Village_Code_id=None,
                                         Accept_Reject=None, Division_Id_id=None, Field_Office_Id_id=None)
        else:
            t_user_master.objects.create(Login_Type="C", Client_Type="O", Name=contactPerson, Employee_Id=None,
                                         Gender=gender, Mobile_Number=mobile_number, Email_Id=emailId, Password=None,
                                         Password_Salt=None, CID=None, Agency=org_agency, License_No=org_license,
                                         Address=org_address, Is_Active="N", Logical_Delete="N",
                                         Last_Login_Date=None, Created_By=None, Created_On=None,
                                         Updated_By=None, Updated_On=None, Dzongkhag_Code_id=dzongkhag,
                                         Gewog_Code_id=gewog, Section_Id_id=None, Village_Code_id=village,
                                         Accept_Reject=None, Division_Id_id=None, Field_Office_Id_id=None)
        return render(request, 'client_register.html')
    else:
        dzongkhag = t_dzongkhag_master.objects.all()
        gewog = t_gewog_master.objects.all()
        village = t_village_master.objects.all()
        return render(request, 'client_register.html', {'dzongkhag': dzongkhag,
                                                        'gewog': gewog, 'village': village})


def new_registration(request):
    reg_clients = t_user_master.objects.filter(Login_Type="C")
    clients = reg_clients.filter(Accept_Reject=None)
    return render(request, 'registered_clients.html', {'reg_clients': clients})


def registered_clients(request):
    reg_clients = t_user_master.objects.filter(Login_Type="C")
    clients = reg_clients.filter(Accept_Reject='A')
    return render(request, 'client_details.html', {'reg_clients': clients})


def accept_registration(request, Email_Id, Name):
    password = get_random_password_string(8)
    password_value = make_password(password)
    reg_clients = t_user_master.objects.filter(Email_Id=Email_Id)
    reg_clients.update(Accept_Reject="A")
    reg_clients.update(Is_Active="Y")
    reg_clients.update(Password=password_value)
    accept_mail(request, Name, Email_Id, password)
    clients = reg_clients.filter(Accept_Reject=None)
    return render(request, 'registered_clients.html', {'reg_clients': clients})


def reject_registration(request, Login_Id, Email_Id, Name):
    reg_clients = t_user_master.objects.filter(Email_Id=Email_Id)
    reg_clients.update(Accept_Reject="R")
    clients = reg_clients.filter(Accept_Reject=None)
    reject_mail(request, Name, Email_Id)
    return render(request, 'registered_clients.html', {'reg_clients': clients})


def get_random_password_string(length):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for i in range(length))
    return password


def reset_password(request, Login_Id, Email_Id, Name):
    salt = os.urandom(32)
    password = get_random_password_string(8)
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    reg_users = t_user_master.objects.filter(Email_Id=Email_Id)
    reg_users.update(Last_Login_Date=None)
    reg_users.update(Password=key)
    reg_users.update(Password_Salt=salt)
    details = t_user_master.objects.filter(Login_Type="I")
    return render(request, 'user.html', {'details': details})


def deactivate_user(request, Login_Id, Email_Id, Name):
    reg_users = t_user_master.objects.filter(Email_Id=Email_Id)
    reg_users.update(Is_Active='N')
    details = t_user_master.objects.filter(Login_Type="I")
    return render(request, 'user.html', {'details': details})


def reset_client_password(request, Login_Id, Email_Id, Name):
    salt = os.urandom(32)
    password = get_random_password_string(8)
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    reg_users = t_user_master.objects.filter(Email_Id=Email_Id)
    reg_users.update(Last_Login_Date=None)
    reg_users.update(Password=key)
    reg_users.update(Password_Salt=salt)
    details = t_user_master.objects.filter(Login_Type="C")
    return render(request, 'registered_clients.html', {'details': details})


def deactivate_client(request, Login_Id, Email_Id, Name):
    reg_users = t_user_master.objects.filter(Email_Id=Email_Id)
    reg_users.update(Is_Active='N')
    details = t_user_master.objects.filter(Login_Type="I")
    return render(request, 'registered_clients.html', {'details': details})


def load_gewog(request):
    dzongkhag_id = request.GET.get('dzongkhag_id')
    gewog_list = t_gewog_master.objects.filter(Dzongkhag_Code_id=dzongkhag_id).order_by('Gewog_Name')
    return render(request, 'gewog_list.html', {'gewog_list': gewog_list})


def load_village(request):
    gewog_id = request.GET.get('gewog_id')
    village_list = t_village_master.objects.filter(Gewog_Code_id=gewog_id).order_by('Village_Name')
    return render(request, 'village_list.html', {'village_list': village_list})


def load_section(request):
    division_id = request.GET.get('division_id')
    section_list = t_section_master.objects.filter(Division_Id_id=division_id).order_by('Section_Name')
    return render(request, 'section_list.html', {'section_list': section_list})


def password_update(request):
    if request.method == 'POST':
        Login_Id = request.POST['Login_Id']
        confirm_password = request.POST['password']
        security_question = request.POST['security_question']
        Answer = request.POST['Answer']
        today = date.today()

        password = make_password(confirm_password)
        reg_users = t_user_master.objects.filter(pk=Login_Id)
        reg_users.update(Password=password)
        reg_users.update(Last_Login_Date=today)
        t_forgot_password.objects.create(Login_Id=Login_Id, Security_Question_Id=security_question, Answer=Answer)
    return render(request, 'common_dashboard.html')


def payment_list(request):
    application_details = t_payment_details.objects.filter(Receipt_No__isnull=True)
    service_details = t_service_master.objects.all()
    return render(request, 'payment_details_list.html', {'application_details': application_details,
                                                         'service_details': service_details})


def update_payment_details(request):
    Application_No = request.POST['application_no']
    Payment_Type = request.POST['Payment_Type']
    Instrument_No = request.POST['Instrument_No']
    Amount = request.POST['Amount']
    Receipt_No = request.POST['Receipt_No']
    Receipt_Date = request.POST['Receipt_Date']
    application_details = t_payment_details.objects.filter(Application_No=Application_No)
    application_details.update(Payment_Type=Payment_Type, Instrument_No=Instrument_No, Amount=Amount,
                               Receipt_No=Receipt_No, Receipt_Date=Receipt_Date,
                               Updated_By=request.session['email'], Updated_On=date.today())
    return redirect(payment_list)
