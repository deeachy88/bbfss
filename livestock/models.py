from django.db import models


# Create your models here.

class t_livestock_clearence_meat_shop_t1(models.Model):
    Application_No = models.CharField(max_length=20, primary_key=True)
    Application_Date = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(blank=True, null=True, max_length=100)
    Scope = models.CharField(max_length=20, default=None)
    Purpose = models.CharField(max_length=100, default=None)
    Name_Meat_Shop = models.CharField(max_length=100, default=None, blank=True, null=True)
    Ownership_Type = models.CharField(max_length=100, default=None)
    CID = models.BigIntegerField()
    Name_Owner = models.CharField(blank=True, null=True, max_length=100)
    Contact_No = models.IntegerField()
    Email = models.EmailField()
    Dzongkhag_Code = models.IntegerField(default=None, blank=True, null=True)
    Gewog_Code = models.IntegerField(default=None, blank=True, null=True)
    Village_Code = models.IntegerField(default=None, blank=True, null=True)
    Establish_Type = models.CharField(blank=True, null=True, max_length=200)
    Establishment_Size = models.CharField(blank=True, null=True, max_length=200)
    Meat_Type = models.CharField(blank=True, null=True, max_length=200)
    Clearance_Type = models.CharField(blank=True, null=True, max_length=10)
    Any_Proceedings = models.CharField(blank=True, null=True, max_length=10)
    Reason_Suspension = models.TextField(blank=True, null=True)
    Desired_Inspection_Date = models.DateField(blank=True, null=True)
    Resubmit_Date = models.DateField(blank=True, null=True)
    Desired_Reinspection_Date = models.DateField(blank=True, null=True)
    Remarks_Reinspection = models.TextField(blank=True, null=True)
    Inspection_Date = models.DateField(blank=True, null=True)
    Remarks_Inspection = models.TextField(blank=True, null=True)
    Inspection_Leader = models.CharField(max_length=100, default=None, blank=True, null=True)
    Inspection_Team = models.CharField(max_length=100, default=None, blank=True, null=True)
    Application_Status = models.CharField(max_length=3, default=None, blank=True, null=True)
    Meat_Shop_Clearance_No = models.CharField(max_length=100, default=None, blank=True, null=True)
    Approved_Date = models.DateField(default=None, blank=True, null=True)
    Validity_Period = models.CharField(default=None, max_length=10, blank=True, null=True)
    Validity = models.DateField(default=None, blank=True, null=True)
    Identification_No = models.CharField(max_length=100, default=None, blank=True, null=True)
    Revision_No = models.CharField(max_length=100, default=None, blank=True, null=True)
    Inspection_Type = models.CharField(max_length=20, default=None, blank=True, null=True)


class t_livestock_clearence_meat_shop_t2(models.Model):
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=20)
    Observation = models.TextField(blank=True, null=True)
    Action = models.TextField(blank=True, null=True)
