from django.db import models

# Create your models here.
from administrator.models import t_plant_crop_master, t_plant_pesticide_master, t_plant_crop_variety_master, \
    t_location_field_office_mapping


class t_plant_movement_permit_t1(models.Model):
    Application_No = models.CharField(max_length=20, primary_key=True)
    Permit_Type = models.CharField(max_length=1, default=None)
    License_No = models.CharField(max_length=100)
    Nursery_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    CID = models.BigIntegerField()
    Applicant_Name = models.CharField(max_length=250)
    Contact_No = models.IntegerField()
    Email = models.EmailField()
    Dzongkhag_Code = models.IntegerField()
    Gewog_Code = models.IntegerField()
    Village_Code = models.IntegerField()
    Location_Code = models.IntegerField()
    From_Dzongkhag_Code = models.IntegerField()
    To_Dzongkhag_Code = models.IntegerField()
    Authorized_Route = models.CharField(max_length=100)
    Source_Of_Product = models.CharField(max_length=100)
    Movement_Purpose = models.CharField(max_length=100)
    Conveyance_Means = models.CharField(max_length=20)
    Name_And_Description = models.CharField(max_length=250, default=None, blank=True, null=True)
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


class t_plant_movement_permit_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Commodity = models.CharField(max_length=100)
    Qty = models.IntegerField()
    Remarks = models.TextField()


class t_plant_movement_permit_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Current_Observation = models.TextField()
    Decision_Conformity = models.TextField()


class t_workflow_details(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Applicant_Id = models.CharField(max_length=20)
    Assigned_To = models.CharField(max_length=100, blank=True, null=True)
    Field_Office_Id = models.IntegerField()
    Section = models.CharField(max_length=20)
    Action_Date = models.DateField()
    Application_Status = models.CharField(max_length=1, default=None, blank=True, null=True)


class t_workflow_details_audit(models.Model):
    Audit_Record_Id = models.AutoField(primary_key=True)
    Workflow_Record_Id = models.IntegerField()
    Application_No = models.CharField(max_length=20)
    Applicant_Id = models.CharField(max_length=20)
    Assigned_To = models.CharField(max_length=100)
    Field_Office_Id = models.IntegerField()
    Section = models.CharField(max_length=20)
    Action_Date = models.DateField()
    Application_Status = models.CharField(max_length=1, default=None, blank=True, null=True)


class t_file_attachment(models.Model):
    File_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20, blank=True, null=True)
    Applicant_Id = models.CharField(max_length=20,blank=True, null=True)
    Role_Id = models.IntegerField(blank=True, null=True)
    Attachment = models.FileField(upload_to='media/files/%Y-%m-%d')


class t_plant_import_permit_t1(models.Model):
    Application_No = models.CharField(max_length=20, primary_key=True)
    Import_Type = models.CharField(max_length=1, default=None)
    License_No = models.CharField(max_length=100)
    Business_Name = models.CharField(max_length=100)
    CID = models.BigIntegerField()
    Applicant_Name = models.CharField(max_length=250)
    Present_Address = models.CharField(max_length=250)
    Contact_No = models.IntegerField()
    Email = models.EmailField()
    Name_And_Address_Supplier = models.TextField()
    Means_of_Conveyance = models.TextField()
    Place_Of_Entry = models.ForeignKey(t_location_field_office_mapping, on_delete=models.CASCADE)
    Purpose = models.TextField()
    Final_Destination = models.CharField(max_length=250)
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


class t_plant_import_permit_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Import_Category = models.CharField(max_length=20)
    Crop_Id = models.ForeignKey(t_plant_crop_master, on_delete=models.CASCADE)
    Pesticide_Id = models.ForeignKey(t_plant_pesticide_master, on_delete=models.CASCADE)
    Description = models.TextField()
    Variety_Id = models.ForeignKey(t_plant_crop_variety_master, on_delete=models.CASCADE)
    Unit = models.CharField(max_length=10)
    Quantity = models.IntegerField()
    Quantity_Released = models.CharField(max_length=10)
    Remarks = models.CharField(max_length=250)


class t_plant_import_permit_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Current_Observation = models.TextField()
    Decision_Conformity = models.TextField()
