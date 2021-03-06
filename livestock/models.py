from django.db import models


# Create your models here.

class t_livestock_clearance_meat_shop_t1(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Date = models.DateField(default=None, blank=True, null=True)
    Applicant_Id = models.CharField(max_length=30, default=None, blank=True, null=True)
    Meat_Shop_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    CID = models.BigIntegerField(blank=True, null=True)
    Name_Owner = models.CharField(max_length=30, blank=True, null=True)
    Representative = models.CharField(max_length=20, blank=True, null=True)
    License_Criteria = models.CharField(max_length=100, blank=True, null=True)
    Contact_No = models.IntegerField()
    Email = models.CharField(max_length=30, blank=True, null=True)
    Address = models.CharField(max_length=250, blank=True, null=True)
    Inspection_Type = models.CharField(max_length=100, blank=True, null=True)
    Desired_FI_Inspection_Date = models.DateField(blank=True, null=True)
    Desired_FR_Inspection_Date = models.DateField(blank=True, null=True)
    FB_License_No = models.CharField(max_length=100, blank=True, null=True)
    FI_Inspection_Date = models.DateField(blank=True, null=True)
    FI_Inspection_Leader = models.CharField(max_length=100, blank=True, null=True)
    FI_Response = models.TextField(blank=True, null=True)
    FI_Recommendation = models.TextField(blank=True, null=True)
    FR_Inspection_Date = models.DateField(blank=True, null=True)
    FR_Inspection_Leader = models.CharField(max_length=100, blank=True, null=True)
    FR_Response = models.TextField(blank=True, null=True)
    FR_Recommendation = models.TextField(blank=True, null=True)
    Field_Office_Id = models.IntegerField(default=None, blank=True, null=True)
    Conditional_Clearance_No = models.CharField(max_length=100, blank=True, null=True)
    Clearance_Approve_Date = models.DateField(blank=True, null=True)
    Clearance_Validity_Period = models.IntegerField(blank=True, null=True)
    Clearance_Validity = models.DateField(blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    FR_Inspection_Team = models.CharField(max_length=200, default=None, blank=True, null=True)
    FI_Inspection_Team = models.CharField(max_length=200, default=None, blank=True, null=True)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)


class t_livestock_clearance_meat_shop_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Meat_Item = models.CharField(max_length=100)


class t_livestock_clearance_meat_shop_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    FH_License_No = models.CharField(max_length=30)
    FH_Name = models.CharField(max_length=100)


class t_livestock_clearance_meat_shop_t4(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Meeting_Type = models.CharField(max_length=100)
    Name = models.CharField(max_length=30)
    Designation = models.CharField(max_length=30)
    Open_Meeting_Date = models.DateField()
    Closing_Meeting_Date = models.DateField()


class t_livestock_clearance_meat_shop_t5(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Inspection_Type = models.CharField(max_length=100)
    Requirement = models.TextField()
    Observation = models.TextField()
    Clause_No = models.CharField(max_length=100, default=None, blank=True, null=True)
    Concern = models.CharField(max_length=10, default=None, blank=True, null=True)
    Date = models.DateField(default=None, blank=True, null=True)
    FBO_Response = models.TextField()


class t_livestock_clearance_meat_shop_t6(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Meeting_Type = models.CharField(max_length=100)
    Name = models.CharField(max_length=30)
    Designation = models.CharField(max_length=30)


class t_livestock_import_permit_product_t1(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Type = models.CharField(max_length=50, default=None, blank=True, null=True)
    Import_Type = models.CharField(max_length=50, default=None)
    License_No = models.CharField(max_length=100, blank=True, null=True)
    Business_Name = models.CharField(max_length=100, blank=True, null=True)
    Nationality = models.CharField(max_length=50, blank=True, null=True)
    Country = models.CharField(max_length=100, blank=True, null=True)
    CID = models.BigIntegerField(blank=True, null=True)
    Applicant_Name = models.CharField(max_length=250, blank=True, null=True)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    Present_Address = models.CharField(max_length=250, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Origin_Source_Products = models.TextField(blank=True, null=True)
    Name_And_Address_Supplier = models.TextField(blank=True, null=True)
    Means_of_Conveyance = models.TextField(blank=True, null=True)
    Place_Of_Entry = models.IntegerField(blank=True, null=True)
    Final_Destination = models.CharField(max_length=250, blank=True, null=True)
    Expected_Arrival_Date = models.DateField(blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    Import_Permit_No = models.CharField(max_length=20, blank=True, null=True)


class t_livestock_import_permit_product_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Particulars = models.CharField(max_length=100, default=None, blank=True, null=True)
    Company_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Quantity = models.IntegerField(blank=True, null=True)
    Unit = models.CharField(max_length=10)
    Quantity_Balance = models.IntegerField(blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)


class t_livestock_import_permit_product_inspection_t1(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Date = models.DateField(blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Import_Permit_No = models.CharField(max_length=20, blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    Application_Type = models.CharField(max_length=50, default=None, blank=True, null=True)
    Import_Type = models.CharField(max_length=50, default=None)
    License_No = models.CharField(max_length=100, blank=True, null=True)
    Business_Name = models.CharField(max_length=100, blank=True, null=True)
    Nationality = models.CharField(max_length=50, blank=True, null=True)
    Country = models.CharField(max_length=100, blank=True, null=True)
    CID = models.BigIntegerField(blank=True, null=True)
    Applicant_Name = models.CharField(max_length=250, blank=True, null=True)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    Present_Address = models.CharField(max_length=250, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Origin_Source_Products = models.TextField(blank=True, null=True)
    Name_And_Address_Supplier = models.TextField(blank=True, null=True)
    Means_of_Conveyance = models.TextField(blank=True, null=True)
    Place_Of_Entry = models.IntegerField(blank=True, null=True)
    Final_Destination = models.CharField(max_length=250, blank=True, null=True)
    Expected_Arrival_Date = models.DateField(blank=True, null=True)
    Proposed_Inspection_Date = models.DateField(blank=True, null=True)
    Actual_Point_Of_Entry = models.IntegerField(blank=True, null=True)
    Inspection_Request_Remarks = models.TextField(blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Type = models.CharField(max_length=250, blank=True, null=True)
    Inspection_Time = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Team = models.TextField(blank=True, null=True)
    Clearance_Ref_No = models.CharField(max_length=20, blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)
    Inspection_Remarks = models.TextField(blank=True, null=True)


class t_livestock_import_permit_product_inspection_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Particulars = models.CharField(max_length=100, default=None, blank=True, null=True)
    Company_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Quantity = models.IntegerField(blank=True, null=True)
    Unit = models.CharField(max_length=10)
    Quantity_Released = models.IntegerField(blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    Quantity_Balance = models.IntegerField(blank=True, null=True)
    Product_Record_Id = models.IntegerField(blank=True, null=True)


class t_livestock_import_permit_product_inspection_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Current_Observation = models.TextField(blank=True, null=True)
    Decision_Conformity = models.TextField(blank=True, null=True)


class t_livestock_import_permit_animal_t1(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Type = models.CharField(max_length=50, default=None, blank=True, null=True)
    Import_Type = models.CharField(max_length=50, default=None)
    License_No = models.CharField(max_length=100, blank=True, null=True)
    Business_Name = models.CharField(max_length=100, blank=True, null=True)
    Nationality = models.CharField(max_length=50, blank=True, null=True)
    Country = models.CharField(max_length=100, blank=True, null=True)
    CID = models.BigIntegerField(blank=True, null=True)
    Applicant_Name = models.CharField(max_length=250, blank=True, null=True)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    Present_Address = models.CharField(max_length=250, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Origin_Source_Products = models.TextField(blank=True, null=True)
    Name_And_Address_Supplier = models.TextField(blank=True, null=True)
    Purpose = models.TextField(blank=True, null=True)
    Means_of_Conveyance = models.TextField(blank=True, null=True)
    Place_Of_Entry = models.IntegerField(blank=True, null=True)
    Final_Destination = models.CharField(max_length=250, blank=True, null=True)
    Expected_Arrival_Date = models.DateField(blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    Quarantine_Facilities = models.CharField(max_length=100, default=None, blank=True, null=True)
    Import_Permit_No = models.CharField(max_length=20, blank=True, null=True)


class t_livestock_import_permit_animal_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Species = models.IntegerField(blank=True, null=True)
    Breed = models.IntegerField(blank=True, null=True)
    Age = models.IntegerField(blank=True, null=True)
    Sex = models.CharField(max_length=10, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Quantity = models.IntegerField(blank=True, null=True)
    Quantity_Balance = models.IntegerField(blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)


class t_livestock_import_permit_animal_inspection_t1(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Date = models.DateField(blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Import_Permit_No = models.CharField(max_length=20, blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    Application_Type = models.CharField(max_length=50, default=None, blank=True, null=True)
    Import_Type = models.CharField(max_length=50, default=None)
    License_No = models.CharField(max_length=100, blank=True, null=True)
    Business_Name = models.CharField(max_length=100, blank=True, null=True)
    Nationality = models.CharField(max_length=50, blank=True, null=True)
    Country = models.CharField(max_length=100, blank=True, null=True)
    CID = models.BigIntegerField(blank=True, null=True)
    Applicant_Name = models.CharField(max_length=250, blank=True, null=True)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    Present_Address = models.CharField(max_length=250, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Origin_Source_Products = models.TextField(blank=True, null=True)
    Name_And_Address_Supplier = models.TextField(blank=True, null=True)
    Purpose = models.TextField(blank=True, null=True)
    Means_of_Conveyance = models.TextField(blank=True, null=True)
    Place_Of_Entry = models.IntegerField(blank=True, null=True)
    Final_Destination = models.CharField(max_length=250, blank=True, null=True)
    Expected_Arrival_Date = models.DateField(blank=True, null=True)
    Proposed_Inspection_Date = models.DateField(blank=True, null=True)
    Actual_Point_Of_Entry = models.IntegerField(blank=True, null=True)
    Inspection_Request_Remarks = models.TextField(blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Type = models.CharField(max_length=250, blank=True, null=True)
    Inspection_Time = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Team = models.TextField(blank=True, null=True)
    Clearance_Ref_No = models.CharField(max_length=20, blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)
    Inspection_Remarks = models.TextField(blank=True, null=True)
    Quarantine_Facilities = models.CharField(max_length=100, default=None, blank=True, null=True)


class t_livestock_import_permit_animal_inspection_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Species = models.CharField(max_length=100, blank=True, null=True)
    Breed = models.CharField(max_length=100, blank=True, null=True)
    Age = models.IntegerField(blank=True, null=True)
    Sex = models.CharField(max_length=10, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Quantity = models.IntegerField(blank=True, null=True)
    Quantity_Released = models.IntegerField(blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    Quantity_Balance = models.IntegerField(blank=True, null=True)
    Product_Record_Id = models.IntegerField(blank=True, null=True)


class t_livestock_import_permit_animal_inspection_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Current_Observation = models.TextField(blank=True, null=True)
    Decision_Conformity = models.TextField(blank=True, null=True)


class t_livestock_export_certificate_t1(models.Model):
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Date = models.DateField(blank=True, null=True)
    Application_Type = models.CharField(max_length=50, default=None, blank=True, null=True)
    Exporter_Type = models.CharField(max_length=50, default=None)
    Nationality = models.CharField(max_length=50, blank=True, null=True)
    Country = models.CharField(max_length=100, blank=True, null=True)
    CID = models.BigIntegerField(blank=True, null=True)
    Applicant_Name = models.CharField(max_length=250, blank=True, null=True)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    License_No = models.CharField(max_length=100, blank=True, null=True)
    Business_Name = models.CharField(max_length=100, blank=True, null=True)
    Present_Address = models.CharField(max_length=250, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Origin_Source_Products = models.TextField(blank=True, null=True)
    Importer_Name_Address = models.TextField(blank=True, null=True)
    Purpose = models.TextField(blank=True, null=True)
    Place_of_Exit = models.IntegerField(blank=True, null=True)
    Final_Destination = models.CharField(max_length=250, blank=True, null=True)
    Export_Expected_Date = models.DateField(blank=True, null=True)
    Proposed_Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Type = models.CharField(max_length=250, blank=True, null=True)
    Inspection_Time = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Team = models.TextField(blank=True, null=True)
    Inspection_Remarks = models.TextField(blank=True, null=True)
    Export_Permit_No = models.CharField(max_length=20, blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100, null=True, default=None)


class t_livestock_export_certificate_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Species = models.CharField(max_length=100, blank=True, null=True)
    Breed = models.CharField(max_length=100, blank=True, null=True)
    Age = models.IntegerField(blank=True, null=True)
    Sex = models.CharField(max_length=10, blank=True, null=True)
    Particulars = models.IntegerField(blank=True, null=True)
    Company_Name = models.IntegerField(blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Quantity = models.IntegerField(blank=True, null=True)
    Quantity_Released = models.IntegerField(blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    No_Of_Animal = models.CharField(max_length=10, default=None, blank=True, null=True)
    Unit = models.CharField(max_length=100, blank=True, null=True)


class t_livestock_export_certificate_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Current_Observation = models.TextField(blank=True, null=True)
    Decision_Conformity = models.TextField(blank=True, null=True)


class t_livestock_movement_permit_t1(models.Model):
    Application_No = models.CharField(max_length=20, primary_key=True)
    Permit_Type = models.CharField(max_length=3, default=None)
    Application_Type = models.CharField(max_length=20, default=None, blank=True, null=True)
    CID = models.BigIntegerField()
    Applicant_Name = models.CharField(max_length=250)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    Contact_No = models.IntegerField()
    Email = models.EmailField()
    License_No = models.CharField(max_length=100)
    Business_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    From_Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    From_Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    From_Location = models.CharField(max_length=100)
    To_Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    To_Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    To_Location = models.CharField(max_length=100, default=None, blank=True, null=True)
    Authorized_Route = models.CharField(max_length=100)
    Movement_Purpose = models.CharField(max_length=100)
    Conveyance_Means = models.CharField(max_length=20)
    Vehicle_No = models.CharField(max_length=100, default=None, blank=True, null=True)
    Movement_Date = models.DateField(blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, default=None, blank=True, null=True)
    Inspection_Team = models.CharField(max_length=100, default=None, blank=True, null=True)
    Application_Status = models.CharField(max_length=1, default=None, blank=True, null=True)
    Movement_Permit_No = models.CharField(max_length=250, default=None, blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100, default=None, blank=True, null=True)
    Approved_Date = models.DateField(default=None, blank=True, null=True)
    Validity_Period = models.CharField(default=None, max_length=10, blank=True, null=True)
    Validity = models.DateField(default=None, blank=True, null=True)


class t_livestock_movement_permit_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Common_Name = models.CharField(max_length=100, blank=True, null=True)
    Scientific_Name = models.CharField(max_length=100, blank=True, null=True)
    Age = models.IntegerField(blank=True, null=True)
    Particulars = models.CharField(max_length=100, blank=True, null=True)
    Company_Name = models.CharField(max_length=100, blank=True, null=True)
    Description = models.TextField(blank=True, null=True)
    Quantity = models.IntegerField(blank=True, null=True)
    Unit = models.CharField(max_length=100, blank=True, null=True)
    Quantity_Released = models.IntegerField(blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    No_Of_Animal = models.IntegerField(blank=True, null=True)


class t_livestock_movement_permit_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Current_Observation = models.TextField()
    Decision_Conformity = models.TextField()


class t_livestock_ante_post_mortem_t1(models.Model):
    Application_No = models.CharField(max_length=20, primary_key=True)
    Inspection_Type = models.CharField(max_length=1, default=None)
    CID = models.BigIntegerField()
    Applicant_Name = models.CharField(max_length=250)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    Address = models.TextField(default=None, blank=True, null=True)
    Contact_No = models.IntegerField()
    Email = models.EmailField()
    Location_Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Location_Code = models.IntegerField(default=None, blank=True, null=True)
    Exact_Location = models.TextField(default=None, blank=True, null=True)
    Inspection_Date_Requested = models.DateField(blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, default=None, blank=True, null=True)
    Inspection_Team = models.CharField(max_length=100, default=None, blank=True, null=True)
    Application_Status = models.CharField(max_length=1, default=None, blank=True, null=True)
    Clearance_No = models.CharField(max_length=250, default=None, blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=100, default=None, blank=True, null=True)
    Approved_Date = models.DateField(default=None, blank=True, null=True)
    Validity_Period = models.CharField(default=None, max_length=10, blank=True, null=True)
    Validity = models.DateField(default=None, blank=True, null=True)
    Respiration_Abnormalities = models.CharField(max_length=100, default=None, blank=True, null=True)
    Behaviour_Abnormalities = models.TextField(default=None, blank=True, null=True)
    Structure_Abnormalities = models.TextField(default=None, blank=True, null=True)
    Abnormal_Gait = models.CharField(max_length=10, default=None, blank=True, null=True)
    Abnormal_Posture = models.CharField(max_length=10, default=None, blank=True, null=True)
    Discharge_Abnormalities = models.TextField(default=None, blank=True, null=True)
    Abnormal_Colour = models.CharField(max_length=10, default=None, blank=True, null=True)
    Abnormal_Odour = models.CharField(max_length=10, default=None, blank=True, null=True)
    No_Without_Restrictions = models.CharField(max_length=10, default=None, blank=True, null=True)
    No_Close_Supervision = models.CharField(max_length=10, default=None, blank=True, null=True)
    No_Withheld = models.CharField(max_length=10, default=None, blank=True, null=True)
    No_Emergency = models.CharField(max_length=10, default=None, blank=True, null=True)
    No_Unfit = models.CharField(max_length=10, default=None, blank=True, null=True)


class t_livestock_ante_post_mortem_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Species = models.CharField(max_length=100, default=None, blank=True, null=True)
    Nos = models.IntegerField(default=None, blank=True, null=True)
    Quantity = models.IntegerField(blank=True, null=True)
    Remarks = models.TextField(blank=True, null=True)
