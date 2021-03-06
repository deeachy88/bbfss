# Generated by Django 3.1.5 on 2021-04-14 04:04

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='t_file_attachment',
            fields=[
                ('File_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(blank=True, max_length=20, null=True)),
                ('Applicant_Id', models.CharField(blank=True, max_length=20, null=True)),
                ('Role_Id', models.IntegerField(blank=True, null=True)),
                ('File_Path', models.CharField(max_length=250)),
                ('Attachment', models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='t_payment_details',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=30)),
                ('Application_Date', models.DateField()),
                ('Applicant_Name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Permit_No', models.CharField(max_length=100)),
                ('Service_Id', models.CharField(max_length=5)),
                ('Validity', models.DateField()),
                ('Payment_Type', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('Instrument_No', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('Amount', models.IntegerField(blank=True, default=None, null=True)),
                ('Receipt_No', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('Receipt_Date', models.DateField(blank=True, default=None, null=True)),
                ('Updated_By', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Updated_On', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_clearence_nursery_seed_grower_t1',
            fields=[
                ('Application_No', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('Nursery_Category', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('License_No', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Company_Name', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Company_Address', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('CID', models.BigIntegerField()),
                ('Owner_Name', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('contactNo', models.BigIntegerField()),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('Unit_Area', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True)),
                ('Area', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True)),
                ('dzongkhag', models.CharField(blank=True, max_length=10, null=True)),
                ('gewog', models.CharField(blank=True, max_length=10, null=True)),
                ('village', models.CharField(blank=True, max_length=10, null=True)),
                ('location_code', models.CharField(blank=True, max_length=10, null=True)),
                ('Nursery_Type', models.CharField(blank=True, max_length=10, null=True)),
                ('Inspection_Date', models.DateField(blank=True, null=True)),
                ('Inspection_Leader', models.CharField(blank=True, max_length=100, null=True)),
                ('Inspection_Team', models.TextField(blank=True, null=True)),
                ('Facilities_Land', models.TextField(blank=True, null=True)),
                ('Facilities_Nursery_House', models.TextField(blank=True, null=True)),
                ('Facilities_Irrigation', models.TextField(blank=True, null=True)),
                ('Facilities_Tools', models.TextField(blank=True, null=True)),
                ('Facilities_Store', models.TextField(blank=True, null=True)),
                ('Manpower', models.CharField(blank=True, max_length=20, null=True)),
                ('Seed_Type', models.CharField(blank=True, max_length=100, null=True)),
                ('Technical_Clearance', models.CharField(blank=True, max_length=100, null=True)),
                ('Recommendation', models.CharField(blank=True, max_length=100, null=True)),
                ('Resubmit_Remarks', models.TextField(blank=True, null=True)),
                ('Resubmit_Date', models.DateField(blank=True, null=True)),
                ('Remarks', models.TextField(blank=True, null=True)),
                ('Desired_Inspection_Date', models.DateField(blank=True, null=True)),
                ('Clearance_Number', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Application_Date', models.DateField(blank=True, null=True)),
                ('Applicant_Id', models.CharField(max_length=100)),
                ('Approved_Date', models.DateField(blank=True, default=None, null=True)),
                ('Validity_Period', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Validity', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_clearence_nursery_seed_grower_t2',
            fields=[
                ('Application_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Crop_Category', models.CharField(blank=True, max_length=30, null=True)),
                ('Crop', models.CharField(blank=True, max_length=30, null=True)),
                ('Crop_Scientific_Name', models.CharField(blank=True, max_length=100, null=True)),
                ('Variety', models.CharField(blank=True, max_length=100, null=True)),
                ('Source', models.CharField(blank=True, max_length=100, null=True)),
                ('Qty', models.IntegerField(blank=True, null=True)),
                ('Remarks', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_export_certificate_plant_plant_products_t1',
            fields=[
                ('Application_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Applicant_Type', models.CharField(blank=True, max_length=100, null=True)),
                ('Certificate_Type', models.CharField(max_length=1)),
                ('License_No', models.CharField(blank=True, max_length=100, null=True)),
                ('CID', models.BigIntegerField(blank=True, null=True)),
                ('Exporter_Name', models.CharField(blank=True, max_length=250, null=True)),
                ('Exporter_Address', models.TextField(blank=True, null=True)),
                ('Permanent_Address', models.TextField(blank=True, null=True)),
                ('Contact_No', models.IntegerField(blank=True, null=True)),
                ('Email', models.EmailField(blank=True, max_length=254, null=True)),
                ('Dzongkhag_Code', models.IntegerField(blank=True, null=True)),
                ('Locatipn_Code', models.IntegerField(blank=True, null=True)),
                ('Consingee_Name_Address', models.TextField(blank=True, null=True)),
                ('Botanical_Name', models.CharField(blank=True, max_length=250, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('Qty_Gross', models.CharField(blank=True, max_length=100, null=True)),
                ('Unit_Gross', models.CharField(blank=True, max_length=10, null=True)),
                ('Pieces_Gross', models.IntegerField(blank=True, default=None, null=True)),
                ('Qty_Net', models.CharField(blank=True, max_length=100, null=True)),
                ('Unit_Net', models.CharField(blank=True, max_length=10, null=True)),
                ('Pieces_Net', models.IntegerField(blank=True, null=True)),
                ('Importing_Country', models.CharField(blank=True, max_length=100, null=True)),
                ('Entry_Point', models.CharField(blank=True, max_length=100, null=True)),
                ('Packages_No', models.CharField(blank=True, max_length=10, null=True)),
                ('Packages_Description', models.TextField(blank=True, null=True)),
                ('Distinguishing_Marks', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Purpose_End_Use', models.TextField(blank=True, null=True)),
                ('Mode_Of_Conveyance', models.CharField(blank=True, max_length=100, null=True)),
                ('Name_Of_Conveyance', models.CharField(blank=True, max_length=250, null=True)),
                ('Departure_Date', models.DateField(blank=True, null=True)),
                ('Desired_Inspection_Date', models.DateField(blank=True, null=True)),
                ('Desired_Inspection_Place', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Additional_Declaring', models.TextField(blank=True, null=True)),
                ('Pre_Application_Treatment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Chemical_Name_Pre', models.CharField(blank=True, max_length=100, null=True)),
                ('Treatment_Pre', models.CharField(blank=True, max_length=100, null=True)),
                ('Concentration_Pre', models.CharField(blank=True, max_length=100, null=True)),
                ('Duration_Temperature_Pre', models.CharField(blank=True, max_length=100, null=True)),
                ('Treated_By_Pre', models.TextField(blank=True, null=True)),
                ('Treated_Supervised_By_Pre', models.TextField(blank=True, null=True)),
                ('Additional_Information_Pre', models.TextField(blank=True, null=True)),
                ('Other_Pre', models.TextField(blank=True, null=True)),
                ('Other_Treatment', models.TextField(blank=True, null=True)),
                ('Outlet_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Outlet_Contact_No', models.IntegerField(blank=True, null=True)),
                ('Outlet_Address', models.CharField(blank=True, max_length=250, null=True)),
                ('Inspection_Date', models.DateField(blank=True, null=True)),
                ('Sample_Drawn_By', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Sample_Inspected_By', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Sample_Drawn', models.IntegerField(blank=True, null=True)),
                ('Sample_Size', models.IntegerField(blank=True, null=True)),
                ('Inspection_Method', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Inspection_Method_Other', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Pest_Detected', models.CharField(blank=True, default=None, max_length=3, null=True)),
                ('Pest_Insect', models.TextField(blank=True, null=True)),
                ('Pest_Mite', models.TextField(blank=True, null=True)),
                ('Pest_Fungi', models.TextField(blank=True, null=True)),
                ('Pest_Bacteria', models.TextField(blank=True, null=True)),
                ('Pest_Virus', models.TextField(blank=True, null=True)),
                ('Pest_Nematode', models.TextField(blank=True, null=True)),
                ('Pest_Weed', models.TextField(blank=True, null=True)),
                ('Pest_Scientific_Name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Infestation_Level', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Pest_Status', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Pest_Risk_Category', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Pest_QR_Detected', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('Pest_QR_Comment', models.TextField(blank=True, null=True)),
                ('Treatment_Possible', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('Treatment_Comment', models.TextField(blank=True, null=True)),
                ('Laboratory_Analysis_Required', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('Laboratory_Analysis_Comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Phytosanitary_Measures', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('Phytosanitary_Measures_Comment', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Treatment_Chemical', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Treatment_Chemical_Name', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Treatment_Chemical_Fumigation', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Treatment_Chemical_Spray', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Treatment_Chemical_Seed', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Treatment_Chemical_Other', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Treatment_Chemical_Other_Specific', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Chemical_Concentration', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Chemical_Duration', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Chemical_Treated_By', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Chemical_Additional_Info', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Irradiation', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Hot_Water', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Dry_Heat', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Vapour_Heat', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Treatment_Cold_Treatment', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Feasibility_Status', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('Inspection_Remarks', models.TextField(blank=True, null=True)),
                ('Export_Permit', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Application_Date', models.DateField(blank=True, null=True)),
                ('Applicant_Id', models.CharField(max_length=100)),
                ('Approved_Date', models.DateField(blank=True, default=None, null=True)),
                ('Validity_Period', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Validity', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_import_permit_t1',
            fields=[
                ('Application_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Import_Type', models.CharField(default=None, max_length=1)),
                ('License_No', models.CharField(blank=True, max_length=100, null=True)),
                ('Business_Name', models.CharField(blank=True, max_length=100, null=True)),
                ('CID', models.BigIntegerField(blank=True, null=True)),
                ('Applicant_Name', models.CharField(blank=True, max_length=250, null=True)),
                ('Present_Address', models.CharField(blank=True, max_length=250, null=True)),
                ('Contact_No', models.IntegerField(blank=True, null=True)),
                ('Email', models.EmailField(blank=True, max_length=254, null=True)),
                ('Name_And_Address_Supplier', models.TextField(blank=True, null=True)),
                ('Means_of_Conveyance', models.TextField(blank=True, null=True)),
                ('Place_Of_Entry', models.IntegerField(blank=True, null=True)),
                ('Purpose', models.TextField(blank=True, null=True)),
                ('Final_Destination', models.CharField(blank=True, max_length=250, null=True)),
                ('Import_Inspection_Submit_Date', models.DateField(blank=True, null=True)),
                ('Proposed_Inspection_Date', models.DateField(blank=True, null=True)),
                ('Actual_Point_Of_Entry', models.IntegerField(blank=True, null=True)),
                ('Inspection_Request_Remarks', models.TextField(blank=True, null=True)),
                ('Import_Permit_No', models.CharField(blank=True, max_length=20, null=True)),
                ('Inspection_Date', models.DateField(blank=True, null=True)),
                ('Inspection_Type', models.CharField(blank=True, max_length=250, null=True)),
                ('Inspection_Time', models.CharField(blank=True, max_length=100, null=True)),
                ('Inspection_Leader', models.CharField(blank=True, max_length=100, null=True)),
                ('Inspection_Team', models.TextField(blank=True, null=True)),
                ('Clearance_Ref_No', models.CharField(blank=True, max_length=20, null=True)),
                ('Expected_Arrival_Date', models.DateField(blank=True, null=True)),
                ('FO_Remarks', models.TextField(blank=True, null=True)),
                ('Inspection_Remarks', models.TextField(blank=True, null=True)),
                ('Country_Of_Origin', models.TextField(blank=True, null=True)),
                ('Application_Date', models.DateField(blank=True, null=True)),
                ('Applicant_Id', models.CharField(max_length=100)),
                ('Approved_Date', models.DateField(blank=True, default=None, null=True)),
                ('Validity_Period', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Validity', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_import_permit_t2',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=20)),
                ('Import_Category', models.CharField(max_length=20)),
                ('Crop_Id', models.IntegerField(blank=True, null=True)),
                ('Pesticide_Id', models.IntegerField(blank=True, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('Variety_Id', models.IntegerField(blank=True, null=True)),
                ('Unit', models.CharField(max_length=10)),
                ('Quantity', models.IntegerField()),
                ('Quantity_Released', models.CharField(blank=True, max_length=10, null=True)),
                ('Remarks', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_import_permit_t3',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=20)),
                ('Current_Observation', models.TextField()),
                ('Decision_Conformity', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_movement_permit_t1',
            fields=[
                ('Application_No', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Permit_Type', models.CharField(default=None, max_length=1)),
                ('License_No', models.CharField(max_length=100)),
                ('Nursery_Name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('CID', models.BigIntegerField()),
                ('Applicant_Name', models.CharField(max_length=250)),
                ('Contact_No', models.IntegerField()),
                ('Email', models.EmailField(max_length=254)),
                ('Dzongkhag_Code', models.IntegerField(blank=True, default=None, null=True)),
                ('Gewog_Code', models.IntegerField(blank=True, default=None, null=True)),
                ('Village_Code', models.IntegerField(blank=True, default=None, null=True)),
                ('From_Dzongkhag_Code', models.IntegerField(blank=True, default=None, null=True)),
                ('From_Gewog_Code', models.IntegerField(blank=True, default=None, null=True)),
                ('From_Location', models.CharField(max_length=100)),
                ('To_Dzongkhag_Code', models.IntegerField(blank=True, default=None, null=True)),
                ('To_Gewog_Code', models.IntegerField(blank=True, default=None, null=True)),
                ('To_Location', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Authorized_Route', models.CharField(max_length=100)),
                ('Source_Of_Product', models.CharField(max_length=100)),
                ('Movement_Purpose', models.CharField(max_length=100)),
                ('Conveyance_Means', models.CharField(max_length=20)),
                ('Qty', models.IntegerField(blank=True, default=None, null=True)),
                ('Unit', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Vehicle_No', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Movement_Date', models.DateField(blank=True, null=True)),
                ('Inspection_Date', models.DateField(blank=True, null=True)),
                ('Inspection_Leader', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Inspection_Team', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Application_Status', models.CharField(blank=True, default=None, max_length=1, null=True)),
                ('Movement_Permit_No', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Remarks', models.TextField(blank=True, null=True)),
                ('Application_Date', models.DateField(blank=True, null=True)),
                ('Applicant_Id', models.CharField(max_length=100)),
                ('Approved_Date', models.DateField(blank=True, default=None, null=True)),
                ('Validity_Period', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Validity', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_movement_permit_t2',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=20)),
                ('Commodity', models.CharField(max_length=100)),
                ('Qty', models.IntegerField()),
                ('Unit', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Remarks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_movement_permit_t3',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=20)),
                ('Current_Observation', models.TextField()),
                ('Decision_Conformity', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_seed_certification_t1',
            fields=[
                ('Application_No', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('Nursery_Category', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('License_No', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Company_Name', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Company_Address', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('CID', models.BigIntegerField(blank=True, default=None, null=True)),
                ('Owner_Name', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Contact_No', models.BigIntegerField(blank=True, default=None, null=True)),
                ('Email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('Dzongkhag_Code', models.CharField(blank=True, max_length=10, null=True)),
                ('Gewog_Code', models.CharField(blank=True, max_length=10, null=True)),
                ('Village_Code', models.CharField(blank=True, max_length=10, null=True)),
                ('Inspection_Date', models.DateField(blank=True, default=None, null=True)),
                ('Inspection_Leader', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Inspection_Team', models.TextField(blank=True, default=None, null=True)),
                ('Seed_Certificate', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Application_Date', models.DateField(blank=True, null=True)),
                ('Applicant_Id', models.CharField(max_length=100)),
                ('Approved_Date', models.DateField(blank=True, default=None, null=True)),
                ('Validity_Period', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('Validity', models.DateField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_seed_certification_t2',
            fields=[
                ('Application_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Crop', models.CharField(blank=True, max_length=40, null=True)),
                ('Variety', models.CharField(blank=True, max_length=40, null=True)),
                ('Seed_Source', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('Quantity', models.IntegerField(blank=True, default=None, null=True)),
                ('Unit', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Purpose', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Qty_Certified', models.IntegerField(blank=True, default=None, null=True)),
                ('Value_Certified', models.CharField(blank=True, max_length=30, null=True)),
                ('Qty_Rejected', models.IntegerField(blank=True, default=None, null=True)),
                ('Unit_Rejected', models.CharField(blank=True, max_length=30, null=True)),
                ('Value_Rejected', models.CharField(blank=True, max_length=30, null=True)),
                ('Remarks', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_plant_seed_certification_t3',
            fields=[
                ('Application_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Observation', models.TextField(blank=True, null=True)),
                ('Action', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_workflow_details',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=20)),
                ('Service_Code', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Applicant_Id', models.CharField(max_length=20)),
                ('Assigned_To', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Field_Office_Id', models.IntegerField(blank=True, null=True)),
                ('Section', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Assigned_Role_Id', models.IntegerField(blank=True, null=True)),
                ('Action_Date', models.DateField(blank=True, null=True)),
                ('Application_Status', models.CharField(blank=True, default=None, max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_workflow_details_audit',
            fields=[
                ('Audit_Record_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Workflow_Record_Id', models.IntegerField()),
                ('Application_No', models.CharField(max_length=20)),
                ('Service_Name', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Applicant_Id', models.CharField(max_length=20)),
                ('Assigned_To', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Field_Office_Id', models.IntegerField(blank=True, null=True)),
                ('Section', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('Assigned_Role_Id', models.CharField(blank=True, max_length=20, null=True)),
                ('Action_Date', models.DateField(blank=True, null=True)),
                ('Application_Status', models.CharField(blank=True, default=None, max_length=3, null=True)),
            ],
        ),
    ]
