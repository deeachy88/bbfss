from django.db import models


# Create your models here.

class t_common_complaint_t1(models.Model):
    Application_No = models.CharField(max_length=20, primary_key=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(blank=True, null=True, max_length=100)
    CID = models.BigIntegerField()
    Name = models.CharField(blank=True, null=True, max_length=100)
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    Contact_No = models.IntegerField()
    Email = models.EmailField()
    Address = models.CharField(blank=True, null=True, max_length=250)
    Complaint_Type = models.CharField(blank=True, null=True, max_length=100)
    Complaint_Description = models.TextField(blank=True, null=True)
    Acknowledge = models.CharField(default='N', blank=True, null=True, max_length=1)
    Assign_To = models.CharField(blank=True, null=True, max_length=100)
    Assign_Date = models.DateField(blank=True, null=True)
    Assign_Remarks = models.TextField(blank=True, null=True)
    Investigation_Date = models.DateField(blank=True, null=True)
    Investigation_By = models.TextField(blank=True, null=True)
    Investigation_Report = models.TextField(blank=True, null=True)
    Report_Submit_Date = models.DateField(blank=True, null=True)
    Closure_Date = models.DateField(blank=True, null=True)
    Closure_Remarks = models.TextField(blank=True, null=True)
    Application_Status = models.CharField(blank=True, null=True, max_length=50)
    Acknowledge_Remarks = models.TextField(default=None, null=True)
    Acknowledge_Date = models.DateField(default=None, null=True)

# Establishment Inspection
class t_inspection_monitoring_t1(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Reference_No = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Type = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Report_Date = models.DateField(default=None, blank=True, null=True)
    FBO_Name = models.CharField(max_length=100, blank=True, null=True)
    License_No = models.CharField(max_length=100, blank=True, null=True)
    Address = models.CharField(max_length=250, blank=True, null=True)
    Email = models.CharField(max_length=100, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Dzongkhag_Code = models.CharField(max_length=10, blank=True, null=True)
    Gewog_Code = models.CharField(max_length=10, blank=True, null=True)
    Village_Code = models.CharField(max_length=10, blank=True, null=True)
    CID = models.BigIntegerField(default=None, blank=True, null=True)
    Name_Of_Owner = models.CharField(max_length=100, default=None, blank=True, null=True)
    Service_Code = models.CharField(max_length=5, default=None, blank=True, null=True)
    Observation = models.TextField(default=None, blank=True, null=True)
    Created_By = models.IntegerField(blank=True, null=True)
    Created_Date = models.DateField(blank=True, null=True)


class t_inspection_monitoring_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Reference_No = models.CharField(max_length=100, blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspector_Name = models.CharField(max_length=100, blank=True, null=True)
    Observation = models.CharField(max_length=30, blank=True, null=True)
    Correction_Proposed = models.TextField(blank=True, null=True)
    Date_Line_Correction = models.DateField(blank=True, null=True)
    Correction_Taken = models.TextField(blank=True, null=True)
    Fine_Imposed = models.IntegerField(blank=True, null=True)
    Revenue_Receipt = models.CharField(max_length=100, blank=True, null=True)
    Receipt_Date = models.DateField(blank=True, null=True)


class t_inspection_monitoring_t3(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Reference_No = models.CharField(max_length=30, blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Inspector_Name = models.CharField(max_length=100, blank=True, null=True)
    Items_Seized = models.CharField(max_length=250, blank=True, null=True)
    Qty_Seized = models.IntegerField(blank=True, null=True)
    Unit = models.CharField(max_length=50, blank=True, null=True)
    Reason = models.TextField(blank=True, null=True)
    Fine_Imposed = models.IntegerField(blank=True, null=True)
    Revenue_Receipt = models.CharField(max_length=100, blank=True, null=True)
    Receipt_Date = models.DateField(blank=True, null=True)
    Detention_Destruction_No = models.IntegerField(blank=True, null=True)


class t_inspection_monitoring_t4(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Reference_No = models.CharField(max_length=100, blank=True, null=True)
    Collection_Date = models.DateField(blank=True, null=True)
    Submission_Date = models.DateField(blank=True, null=True)
    HS_Code_Imp = models.CharField(max_length=30, blank=True, null=True)
    HS_Code_Local = models.CharField(max_length=30, blank=True, null=True)
    Sample_Type = models.CharField(max_length=100, blank=True, null=True)
    Qty = models.IntegerField(blank=True, null=True)
    Batch_No = models.CharField(max_length=100, blank=True, null=True)
    Batch_Date = models.DateField(blank=True, null=True)
    Test_Requested = models.CharField(max_length=200, blank=True, null=True)
    Test_Report = models.CharField(max_length=200, blank=True, null=True)
    Collection_Type = models.CharField(max_length=200, blank=True, null=True)


# Commodity Inspection
class t_commodity_inspection_t1(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Reference_No = models.CharField(max_length=100, blank=True, null=True)
    FBO_Name = models.CharField(max_length=100, blank=True, null=True)
    Registration_No = models.CharField(max_length=100, blank=True, null=True)
    Dzongkhag_Code = models.CharField(max_length=10, blank=True, null=True)
    Gewog_Code = models.CharField(max_length=10, blank=True, null=True)
    Village_Code = models.CharField(max_length=10, blank=True, null=True)
    Address = models.TextField(blank=True, null=True)
    Email = models.CharField(max_length=100, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Inspection_Date = models.DateField(default=None, blank=True, null=True)
    Inspection_Team = models.TextField(blank=True, null=True)
    Team_Leader = models.IntegerField(blank=True, null=True)
    Commodity = models.TextField(default=None, blank=True, null=True)
    Purpose = models.TextField(default=None, blank=True, null=True)
    Observation = models.TextField(default=None, blank=True, null=True)
    Created_By = models.IntegerField(blank=True, null=True)
    Created_Date = models.DateField(blank=True, null=True)

class t_commodity_inspection_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Reference_No = models.CharField(max_length=100, blank=True, null=True)
    Commodity = models.CharField(max_length=250, blank=True, null=True)
    Commodity_Requirement = models.CharField(max_length=250, blank=True, null=True)
    Qty_Inspected = models.IntegerField(blank=True, null=True)
    Unit = models.CharField(max_length=10, blank=True, null=True)
    Qty_Cleared = models.IntegerField(blank=True, null=True)
    Qty_Rejected = models.IntegerField(blank=True, null=True)
    Reason_For_Rejection = models.CharField(max_length=250, blank=True, null=True)

