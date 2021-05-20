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
    Acknowledge = models.CharField(blank=True, null=True, max_length=1)
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


