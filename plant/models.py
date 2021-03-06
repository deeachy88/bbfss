from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
fs = FileSystemStorage()


class t_plant_movement_permit_t1(models.Model):
    Application_No = models.CharField(max_length=20, primary_key=True)
    Permit_Type = models.CharField(max_length=1, default=None)
    License_No = models.CharField(max_length=100)
    Nursery_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    CID = models.BigIntegerField()
    Applicant_Name = models.CharField(max_length=250)
    Contact_No = models.IntegerField()
    Email = models.EmailField()
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    From_Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    From_Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    From_Location = models.CharField(max_length=100)
    To_Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    To_Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    To_Location = models.CharField(max_length=100, default=None, blank=True, null=True)
    Authorized_Route = models.CharField(max_length=100)
    Source_Of_Product = models.CharField(max_length=100)
    Movement_Purpose = models.CharField(max_length=100)
    Conveyance_Means = models.CharField(max_length=20)
    Qty = models.IntegerField(default=None, blank=True, null=True)
    Unit = models.CharField(max_length=20, default=None, blank=True, null=True)
    Vehicle_No = models.CharField(max_length=100, default=None, blank=True, null=True)
    Movement_Date = models.DateField(blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, default=None, blank=True, null=True)
    Inspection_Team = models.CharField(max_length=100, default=None, blank=True, null=True)
    Application_Status = models.CharField(max_length=1, default=None, blank=True, null=True)
    Movement_Permit_No = models.CharField(max_length=250, default=None, blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100)
    Approved_Date = models.DateField(default=None, blank=True, null=True)
    Validity_Period = models.CharField(default=None, max_length=10, blank=True, null=True)
    Validity = models.DateField(default=None, blank=True, null=True)


class t_plant_movement_permit_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Commodity = models.CharField(max_length=100)
    Qty = models.IntegerField()
    Unit = models.CharField(default=None, max_length=10, blank=True, null=True)
    Remarks = models.TextField()


class t_plant_movement_permit_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Current_Observation = models.TextField()
    Decision_Conformity = models.TextField()


class t_workflow_details(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Service_Code = models.CharField(max_length=20, default=None, blank=True, null=True)
    Applicant_Id = models.CharField(max_length=20)
    Assigned_To = models.CharField(max_length=100, default=None, blank=True, null=True)
    Field_Office_Id = models.IntegerField(blank=True, null=True)
    Section = models.CharField(max_length=20, default=None, blank=True, null=True)
    Assigned_Role_Id = models.IntegerField(blank=True, null=True)
    Action_Date = models.DateField(blank=True, null=True)
    Application_Status = models.CharField(max_length=3, default=None, blank=True, null=True)


class t_workflow_details_audit(models.Model):
    Audit_Record_Id = models.AutoField(primary_key=True)
    Workflow_Record_Id = models.IntegerField()
    Application_No = models.CharField(max_length=20)
    Service_Name = models.CharField(max_length=20, default=None, blank=True, null=True)
    Applicant_Id = models.CharField(max_length=20)
    Assigned_To = models.CharField(max_length=100, default=None, blank=True, null=True)
    Field_Office_Id = models.IntegerField(blank=True, null=True)
    Section = models.CharField(max_length=20, default=None, blank=True, null=True)
    Assigned_Role_Id = models.CharField(max_length=20, blank=True, null=True)
    Action_Date = models.DateField(blank=True, null=True)
    Application_Status = models.CharField(max_length=3, default=None, blank=True, null=True)


class t_file_attachment(models.Model):
    File_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=100, blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100, blank=True, null=True)
    Role_Id = models.IntegerField(blank=True, null=True)
    File_Path = models.CharField(max_length=250)
    Attachment = models.FileField(storage=fs)


class t_plant_import_permit_t1(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Import_Type = models.CharField(max_length=1, default=None)
    Application_Type = models.CharField(max_length=10, default=None)
    Nationality_Type = models.CharField(max_length=10, default=None)
    License_No = models.CharField(max_length=100, blank=True, null=True)
    Business_Name = models.CharField(max_length=100, blank=True, null=True)
    CID = models.BigIntegerField(blank=True, null=True)
    Applicant_Name = models.CharField(max_length=250, blank=True, null=True)
    Present_Address = models.CharField(max_length=250, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Name_And_Address_Supplier = models.TextField(blank=True, null=True)
    Means_of_Conveyance = models.TextField(blank=True, null=True)
    Place_Of_Entry = models.IntegerField(blank=True, null=True)
    Purpose = models.TextField(blank=True, null=True)
    Final_Destination = models.CharField(max_length=250, blank=True, null=True)
    Import_Inspection_Submit_Date = models.DateField(blank=True, null=True)
    Proposed_Inspection_Date = models.DateField(blank=True, null=True)
    Actual_Point_Of_Entry = models.IntegerField(blank=True, null=True)
    Inspection_Request_Remarks = models.TextField(blank=True, null=True)
    Import_Permit_No = models.CharField(max_length=20, blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Type = models.CharField(max_length=250, blank=True, null=True)
    Inspection_Time = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Team = models.TextField(blank=True, null=True)
    Clearance_Ref_No = models.CharField(max_length=20, blank=True, null=True)
    Expected_Arrival_Date = models.DateField(blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)
    Inspection_Remarks = models.TextField(blank=True, null=True)
    Country_Of_Origin = models.TextField(blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100)
    Approved_Date = models.DateField(default=None, blank=True, null=True)
    Validity_Period = models.CharField(default=None, max_length=10, blank=True, null=True)
    Validity = models.DateField(default=None, blank=True, null=True)
    passport_number = models.CharField(default=None, max_length=100, blank=True, null=True)
    Nationality = models.CharField(max_length=10, default=None, blank=True, null=True)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)


class t_plant_import_permit_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Import_Category = models.CharField(max_length=20)
    Crop_Id = models.IntegerField(blank=True, null=True)
    Pesticide_Id = models.IntegerField(blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Variety_Id = models.IntegerField(blank=True, null=True)
    Unit = models.CharField(max_length=10)
    Quantity = models.IntegerField()
    Quantity_Released = models.CharField(max_length=10, blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)


class t_plant_import_permit_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Current_Observation = models.TextField()
    Decision_Conformity = models.TextField()


class t_plant_export_certificate_plant_plant_products_t1(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Applicant_Type = models.CharField(max_length=100, blank=True, null=True)
    Certificate_Type = models.CharField(max_length=1)
    License_No = models.CharField(max_length=100, blank=True, null=True)
    CID = models.BigIntegerField(blank=True, null=True)
    Exporter_Name = models.CharField(max_length=250, blank=True, null=True)
    Exporter_Address = models.TextField(blank=True, null=True)
    Permanent_Address = models.TextField(blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Dzongkhag_Code = models.IntegerField(blank=True, null=True)
    Locatipn_Code = models.IntegerField(blank=True, null=True)
    Consingee_Name_Address = models.TextField(blank=True, null=True)
    Botanical_Name = models.CharField(max_length=250, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Qty_Gross = models.CharField(max_length=100, blank=True, null=True)
    Unit_Gross = models.CharField(max_length=10, blank=True, null=True)
    Pieces_Gross = models.IntegerField(default=None, blank=True, null=True)
    Qty_Net = models.CharField(max_length=100, blank=True, null=True)
    Unit_Net = models.CharField(max_length=10, blank=True, null=True)
    Pieces_Net = models.IntegerField(blank=True, null=True)
    Importing_Country = models.CharField(max_length=100, blank=True, null=True)
    Entry_Point = models.CharField(max_length=100, blank=True, null=True)
    Packages_No = models.CharField(max_length=10, blank=True, null=True)
    Packages_Description = models.TextField(blank=True, null=True)
    Distinguishing_Marks = models.CharField(max_length=250, default=None, blank=True, null=True)
    Purpose_End_Use = models.TextField(blank=True, null=True)
    Mode_Of_Conveyance = models.CharField(max_length=100, blank=True, null=True)
    Name_Of_Conveyance = models.CharField(max_length=250, blank=True, null=True)
    Departure_Date = models.DateField(blank=True, null=True)
    Desired_Inspection_Date = models.DateField(blank=True, null=True)
    Desired_Inspection_Place = models.CharField(max_length=100, default=None, blank=True, null=True)
    Additional_Declaring = models.TextField(blank=True, null=True)
    Pre_Application_Treatment = models.CharField(max_length=100, default=None, blank=True, null=True)
    Chemical_Name_Pre = models.CharField(max_length=100, blank=True, null=True)
    Treatment_Pre = models.CharField(max_length=100, blank=True, null=True)
    Concentration_Pre = models.CharField(max_length=100, blank=True, null=True)
    Duration_Temperature_Pre = models.CharField(max_length=100, blank=True, null=True)
    Treated_By_Pre = models.TextField(blank=True, null=True)
    Treated_Supervised_By_Pre = models.TextField(blank=True, null=True)
    Additional_Information_Pre = models.TextField(blank=True, null=True)
    Other_Pre = models.TextField(blank=True, null=True)
    Other_Treatment = models.TextField(blank=True, null=True)
    Outlet_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Outlet_Contact_No = models.IntegerField(blank=True, null=True)
    Outlet_Address = models.CharField(max_length=250, blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Sample_Drawn_By = models.CharField(max_length=100, default=None, blank=True, null=True)
    Sample_Inspected_By = models.CharField(max_length=100, default=None, blank=True, null=True)
    Sample_Drawn = models.IntegerField(blank=True, null=True)
    Sample_Size = models.IntegerField(blank=True, null=True)
    Inspection_Method = models.CharField(max_length=100, default=None, blank=True, null=True)
    Inspection_Method_Other = models.CharField(max_length=100, default=None, blank=True, null=True)
    Pest_Detected = models.CharField(max_length=3, default=None, blank=True, null=True)
    Pest_Insect = models.TextField(blank=True, null=True)
    Pest_Mite = models.TextField(blank=True, null=True)
    Pest_Fungi = models.TextField(blank=True, null=True)
    Pest_Bacteria = models.TextField(blank=True, null=True)
    Pest_Virus = models.TextField(blank=True, null=True)
    Pest_Nematode = models.TextField(blank=True, null=True)
    Pest_Weed = models.TextField(blank=True, null=True)
    Pest_Scientific_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Infestation_Level = models.CharField(max_length=100, default=None, blank=True, null=True)
    Pest_Status = models.CharField(max_length=10, default=None, blank=True, null=True)
    Pest_Risk_Category = models.CharField(max_length=100, default=None, blank=True, null=True)
    Pest_QR_Detected = models.CharField(max_length=5, default=None, blank=True, null=True)
    Pest_QR_Comment = models.TextField(blank=True, null=True)
    Treatment_Possible = models.CharField(max_length=5, default=None, blank=True, null=True)
    Treatment_Comment = models.TextField(blank=True, null=True)
    Laboratory_Analysis_Required = models.CharField(max_length=5, default=None, blank=True, null=True)
    Laboratory_Analysis_Comment = models.CharField(max_length=100, default=None, blank=True, null=True)
    Phytosanitary_Measures = models.CharField(max_length=5, default=None, blank=True, null=True)
    Phytosanitary_Measures_Comment = models.CharField(max_length=100, default=None, blank=True, null=True)
    Treatment_Chemical = models.CharField(max_length=10, default=None, blank=True, null=True)
    Treatment_Chemical_Name = models.CharField(max_length=10, default=None, blank=True, null=True)
    Treatment_Chemical_Fumigation = models.CharField(max_length=100, default=None, blank=True, null=True)
    Treatment_Chemical_Spray = models.CharField(max_length=10, default=None, blank=True, null=True)
    Treatment_Chemical_Seed = models.CharField(max_length=10, default=None, blank=True, null=True)
    Treatment_Chemical_Other = models.CharField(max_length=10, default=None, blank=True, null=True)
    Treatment_Chemical_Other_Specific = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Chemical_Concentration = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Chemical_Duration = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Chemical_Treated_By = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Chemical_Additional_Info = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Irradiation = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Hot_Water = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Dry_Heat = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Vapour_Heat = models.CharField(max_length=250, default=None, blank=True, null=True)
    Treatment_Cold_Treatment = models.CharField(max_length=250, default=None, blank=True, null=True)
    Feasibility_Status = models.CharField(max_length=5, default=None, blank=True, null=True)
    Inspection_Remarks = models.TextField(blank=True, null=True)
    Export_Permit = models.CharField(max_length=20, default=None, blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100)
    Approved_Date = models.DateField(default=None, blank=True, null=True)
    Validity_Period = models.CharField(default=None, max_length=10, blank=True, null=True)
    Validity = models.DateField(default=None, blank=True, null=True)


class t_plant_clearence_nursery_seed_grower_t1(models.Model):
    Application_No = models.CharField(max_length=100, primary_key=True)
    Nursery_Category = models.CharField(max_length=20, default=None, blank=True, null=True)
    License_No = models.CharField(max_length=100, default=None, blank=True, null=True)
    Company_Name = models.CharField(max_length=250, default=None, blank=True, null=True)
    Company_Address = models.CharField(max_length=250, default=None, blank=True, null=True)
    CID = models.BigIntegerField()
    Owner_Name = models.CharField(max_length=250, default=None, blank=True, null=True)
    contactNo = models.BigIntegerField()
    email = models.EmailField(default=None, blank=True, null=True)
    Unit_Area = models.DecimalField(decimal_places=2, max_digits=10, default=None, blank=True, null=True)
    Area = models.DecimalField(decimal_places=2, max_digits=10, default=None, blank=True, null=True)
    dzongkhag = models.CharField(max_length=10, blank=True, null=True)
    gewog = models.CharField(max_length=10, blank=True, null=True)
    village = models.CharField(max_length=10, blank=True, null=True)
    location_code = models.CharField(max_length=10, blank=True, null=True)
    Nursery_Type = models.CharField(max_length=10, blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Team = models.TextField(blank=True, null=True)
    Facilities_Land = models.TextField(blank=True, null=True)
    Facilities_Nursery_House = models.TextField(blank=True, null=True)
    Facilities_Irrigation = models.TextField(blank=True, null=True)
    Facilities_Tools = models.TextField(blank=True, null=True)
    Facilities_Store = models.TextField(blank=True, null=True)
    Manpower = models.CharField(max_length=20, blank=True, null=True)
    Seed_Type = models.CharField(max_length=100, blank=True, null=True)
    Technical_Clearance = models.CharField(max_length=100, blank=True, null=True)
    Recommendation = models.CharField(max_length=100, blank=True, null=True)
    Resubmit_Remarks = models.TextField(blank=True, null=True)
    Resubmit_Date = models.DateField(blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    Desired_Inspection_Date = models.DateField(blank=True, null=True)
    Clearance_Number = models.CharField(max_length=20, default=None, blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100)
    Approved_Date = models.DateField(default=None, blank=True, null=True)
    Validity_Period = models.CharField(default=None, max_length=10, blank=True, null=True)
    Validity = models.DateField(default=None, blank=True, null=True)


class t_plant_clearence_nursery_seed_grower_t2(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Crop_Category = models.CharField(max_length=30, blank=True, null=True)
    Crop = models.CharField(max_length=30, blank=True, null=True)
    Crop_Scientific_Name = models.CharField(max_length=100, blank=True, null=True)
    Variety = models.CharField(max_length=100, blank=True, null=True)
    Source = models.CharField(max_length=100, blank=True, null=True)
    Qty = models.IntegerField(blank=True, null=True)
    Remarks = models.CharField(max_length=100, blank=True, null=True)


class t_plant_seed_certification_t1(models.Model):
    Application_No = models.CharField(max_length=100, primary_key=True)
    Nursery_Category = models.CharField(max_length=20, default=None, blank=True, null=True)
    License_No = models.CharField(max_length=20, default=None, blank=True, null=True)
    Company_Name = models.CharField(max_length=250, default=None, blank=True, null=True)
    Company_Address = models.CharField(max_length=250, default=None, blank=True, null=True)
    CID = models.BigIntegerField(default=None, blank=True, null=True)
    Owner_Name = models.CharField(max_length=250, default=None, blank=True, null=True)
    Contact_No = models.BigIntegerField(default=None, blank=True, null=True)
    Email = models.EmailField(default=None, blank=True, null=True)
    Dzongkhag_Code = models.CharField(max_length=10, blank=True, null=True)
    Gewog_Code = models.CharField(max_length=10, blank=True, null=True)
    Village_Code = models.CharField(max_length=10, blank=True, null=True)
    Inspection_Date = models.DateField(default=None, null=True, blank=True)
    Inspection_Leader = models.CharField(max_length=250, default=None, blank=True, null=True)
    Inspection_Team = models.TextField(default=None, blank=True, null=True)
    Seed_Certificate = models.CharField(max_length=100, default=None, blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100)
    Approved_Date = models.DateField(default=None, blank=True, null=True)
    Validity_Period = models.CharField(default=None, max_length=10, blank=True, null=True)
    Validity = models.DateField(default=None, blank=True, null=True)


class t_plant_seed_certification_t2(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Crop = models.CharField(max_length=40, blank=True, null=True)
    Variety = models.CharField(max_length=40, blank=True, null=True)
    Seed_Source = models.CharField(max_length=250, default=None, blank=True, null=True)
    Quantity = models.IntegerField(default=None, blank=True, null=True)
    Unit = models.CharField(max_length=20, default=None, blank=True, null=True)
    Purpose = models.CharField(max_length=20, default=None, blank=True, null=True)
    Qty_Certified = models.IntegerField(default=None, blank=True, null=True)
    Value_Certified = models.CharField(max_length=30, blank=True, null=True)
    Qty_Rejected = models.IntegerField(default=None, blank=True, null=True)
    Unit_Rejected = models.CharField(max_length=30, blank=True, null=True)
    Value_Rejected = models.CharField(max_length=30, blank=True, null=True)
    Remarks = models.CharField(max_length=30, blank=True, null=True)


class t_plant_seed_certification_t3(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Observation = models.TextField(blank=True, null=True)
    Action = models.TextField(blank=True, null=True)


class t_payment_details(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Application_Date = models.DateField()
    Applicant_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Permit_No = models.CharField(max_length=100)
    Service_Id = models.CharField(max_length=5)
    Validity = models.DateField()
    Payment_Type = models.CharField(max_length=30, default=None, blank=True, null=True)
    Instrument_No = models.CharField(max_length=50, default=None, blank=True, null=True)
    Amount = models.IntegerField(default=None, blank=True, null=True)
    Receipt_No = models.CharField(max_length=30, default=None, blank=True, null=True)
    Receipt_Date = models.DateField(default=None, blank=True, null=True)
    Updated_By = models.CharField(max_length=100, default=None, blank=True, null=True)
    Updated_On = models.DateField(default=None, blank=True, null=True)
