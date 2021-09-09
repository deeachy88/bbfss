from django.db import models


# Create your models here.


class t_certification_gap_t1(models.Model):  # GAP main table
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Date = models.DateField(blank=True, null=True)
    Application_Type = models.CharField(max_length=50, default=None)
    CID = models.BigIntegerField(blank=True, null=True)
    Applicant_Name = models.CharField(max_length=250, blank=True, null=True)
    Dzongkhag_Code = models.CharField(max_length=100, default=None, blank=True, null=True)
    Gewog_Code = models.CharField(max_length=100, default=None, blank=True, null=True)
    Village_Code = models.CharField(max_length=100, default=None, blank=True, null=True)
    Present_Address = models.CharField(max_length=250, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Farmer_Group_No = models.CharField(max_length=100, blank=True, null=True)
    Farmer_Group_Name = models.CharField(max_length=200, blank=True, null=True)
    Pack_House = models.CharField(max_length=1, blank=True, null=True)
    Crop_Production = models.CharField(max_length=1, blank=True, null=True)
    Proposed_Standard = models.TextField(blank=True, null=True)
    Terms_Bafra_Certification = models.CharField(max_length=10, blank=True, null=True)
    Terms_Change_Willingness = models.CharField(max_length=10, blank=True, null=True)
    Terms_Abide = models.CharField(max_length=10, blank=True, null=True)
    Terms_Agreement = models.CharField(max_length=10, blank=True, null=True)
    Acknowledge = models.CharField(max_length=1, blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)
    Audit_Team_Leader = models.IntegerField(blank=True, null=True)
    Audit_Team_Acceptance = models.CharField(max_length=1, default='R', blank=True, null=True)
    Audit_Team_Acceptance_Remarks = models.TextField(blank=True, null=True)
    Audit_Plan_Date = models.DateField(blank=True, null=True)
    Audit_Plan_Criteria = models.TextField(blank=True, null=True)
    Audit_Plan_Type = models.CharField(max_length=200, blank=True, null=True)
    Audit_Plan_Scope = models.TextField(blank=True, null=True)
    Audit_Plan_Acceptance = models.CharField(default="R", max_length=1, blank=True, null=True)
    Audit_Plan_Acceptance_Remarks = models.TextField(blank=True, null=True)
    Audit_Date = models.DateField(blank=True, null=True)
    Audit_Findings_Site_History_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Water_Source_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Product_Quality_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Harvesting_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Equipment_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Manufacturing_Production_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Sampling_Testing_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Packing_Marking_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Storage_Transport_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Traceability_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Worker_Health_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Group_Requirement_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Others_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Site_History_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Water_Source_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Product_Quality_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Harvesting_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Equipment_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Manufacturing_Production_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Sampling_Testing_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Packing_Marking_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Storage_Transport_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Traceability_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Worker_Health_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Group_Requirement_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Others_Observations = models.TextField(blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Certificate_No = models.CharField(max_length=100, blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    Farm_Location = models.CharField(max_length=250, default=None, blank=True, null=True)
    Farm_Name = models.CharField(max_length=250, blank=True, null=True)
    Applicant_Id = models.CharField(max_length=50, blank=True, null=True)
    Audit_Type = models.CharField(max_length=200, blank=True, null=True)
    Terms_Standards = models.CharField(max_length=100, blank=True, null=True)
    Others_Standards = models.CharField(max_length=110, blank=True, null=True)
    License_Number = models.CharField(max_length=110, blank=True, null=True)
    Technical_In_Charge = models.CharField(max_length=200, blank=True, null=True)
    Manager_In_Charge = models.CharField(max_length=200, blank=True, null=True)
    Corrective_Action_Taken_Auditee = models.TextField(blank=True, null=True)
    Corrective_Action_Date = models.DateField(blank=True, null=True)
    Certificate_Type = models.CharField(max_length=10, blank=True, null=True)


class t_certification_gap_t2(models.Model):  # GAP certification farmer group
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    CID = models.CharField(max_length=100, default=None, blank=True, null=True)
    Name = models.CharField(max_length=100, default=None, blank=True, null=True)


class t_certification_gap_t3(models.Model):  # GAP Certification audit team
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Login_Id = models.CharField(max_length=100, default=None, blank=True, null=True)
    Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Role = models.CharField(max_length=100, default=None, blank=True, null=True)


class t_certification_gap_t4(models.Model):  # GAP Certification crop production
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Crop_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Area_Cultivated = models.IntegerField(blank=True, null=True)
    Unit = models.CharField(max_length=50)
    P_From_Date = models.DateField(blank=True, null=True)
    P_To_Date = models.DateField(blank=True, null=True)
    P_Yield = models.IntegerField(blank=True, null=True)
    P_Yield_Unit = models.CharField(max_length=50)
    P_Harvest_Month = models.CharField(max_length=50)
    P_Sold = models.IntegerField(blank=True, null=True)
    P_Balance_Stock = models.IntegerField(blank=True, null=True)
    C_From_Date = models.DateField(blank=True, null=True)
    C_To_Date = models.DateField(blank=True, null=True)
    C_Estimated_Yield = models.IntegerField(blank=True, null=True)
    C_Yield_Unit = models.CharField(max_length=50)
    C_Harvest_Month = models.CharField(max_length=50)


class t_certification_gap_t5(models.Model):  # GAP Certification pack house
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Pack_House_Name = models.CharField(max_length=200, blank=True, null=True)
    Pack_House_Address = models.TextField(blank=True, null=True)
    P_From_Date = models.DateField(blank=True, null=True)
    P_To_Date = models.DateField(blank=True, null=True)
    P_Production = models.IntegerField(blank=True, null=True)
    P_Production_Unit = models.CharField(max_length=50)
    P_Sold = models.IntegerField(blank=True, null=True)
    P_Balance_Stock = models.IntegerField(blank=True, null=True)
    C_From_Date = models.DateField(blank=True, null=True)
    C_To_Date = models.DateField(blank=True, null=True)
    C_Production = models.IntegerField(blank=True, null=True)
    C_Sold = models.IntegerField(blank=True, null=True)
    C_Balance_Stock = models.IntegerField(blank=True, null=True)
    C_Balance_Stock_Unit = models.IntegerField(blank=True, null=True)


class t_certification_gap_t6(models.Model):  # GAP Certification Audit Plan
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Audit_Plan_Date = models.DateField(blank=True, null=True)
    Audit_Plan_Time = models.TimeField(blank=True, null=True)
    Area_Function_Department = models.TextField(blank=True, null=True)
    Company_Contact = models.TextField(blank=True, null=True)


class t_certification_gap_t7(models.Model):  # Audit Finding/Report (Farm inputs/raw materials and packaging materials)
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Audit_Findings_Farm_Inputs = models.CharField(max_length=200, blank=True, null=True)
    Audit_Findings_Farm_Supplier = models.CharField(max_length=200, blank=True, null=True)
    Audit_Findings_Farm_Invoice = models.CharField(max_length=200, blank=True, null=True)


class t_certification_gap_t8(models.Model):  # GAP Observation.
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Clause_Number = models.CharField(max_length=200, blank=True, null=True)
    Non_Conformity = models.CharField(max_length=10, blank=True, null=True)
    Non_Conformity_Category = models.CharField(max_length=10, blank=True, null=True)
    Non_Conformity_Description = models.CharField(max_length=10, blank=True, null=True)
    Corrective_Action_Proposed_Auditee = models.TextField(blank=True, null=True)
    Corrective_Action_Verified_Auditor = models.TextField(blank=True, null=True)
    Non_Conformity_Closure = models.CharField(max_length=1, blank=True, null=True)


# Organic Certification
class t_certification_organic_t1(models.Model):  # Organic Certification main table
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Date = models.DateField(blank=True, null=True)
    Application_Type = models.CharField(max_length=50, default=None)
    CID = models.BigIntegerField(blank=True, null=True)
    Applicant_Name = models.CharField(max_length=250, blank=True, null=True)
    Dzongkhag_Code = models.CharField(max_length=100, default=None, blank=True, null=True)
    Gewog_Code = models.CharField(max_length=100, default=None, blank=True, null=True)
    Village_Code = models.CharField(max_length=100, default=None, blank=True, null=True)
    Present_Address = models.CharField(max_length=250, blank=True, null=True)
    Contact_No = models.IntegerField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Farmer_Group_No = models.CharField(max_length=100, blank=True, null=True)
    Farmer_Group_Name = models.CharField(max_length=200, blank=True, null=True)
    Crop_Production = models.CharField(max_length=1, blank=True, null=True)
    Wild_Collection = models.CharField(max_length=1, blank=True, null=True)
    Animal_Husbandry = models.CharField(max_length=1, blank=True, null=True)
    Aquaculture = models.CharField(max_length=1, blank=True, null=True)
    Apiculture = models.CharField(max_length=1, blank=True, null=True)
    Processing_Unit = models.CharField(max_length=1, blank=True, null=True)
    Proposed_Standard = models.TextField(blank=True, null=True)
    Terms_Bafra_Certification = models.CharField(max_length=10, blank=True, null=True)
    Terms_Change_Willingness = models.CharField(max_length=10, blank=True, null=True)
    Terms_Abide = models.CharField(max_length=10, blank=True, null=True)
    Terms_Agreement = models.CharField(max_length=10, blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)
    Acknowledge = models.CharField(max_length=1, blank=True, null=True)
    Audit_Team_Leader = models.IntegerField(blank=True, null=True)
    Audit_Team_Acceptance = models.CharField(max_length=1, default='N', blank=True, null=True)
    Audit_Team_Acceptance_Remarks = models.TextField(blank=True, null=True)
    Audit_Plan_Date = models.DateField(blank=True, null=True)
    Audit_Plan_Criteria = models.TextField(blank=True, null=True)
    Audit_Plan_Type = models.CharField(max_length=200, blank=True, null=True)
    Audit_Plan_Scope = models.TextField(blank=True, null=True)
    Audit_Plan_Acceptance = models.CharField(default="R", max_length=10, blank=True, null=True)
    Audit_Plan_Acceptance_Remarks = models.TextField(blank=True, null=True)
    Audit_Date = models.DateField(blank=True, null=True)
    Audit_Findings_Site_History_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Water_Source_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Product_Quality_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Harvesting_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Equipment_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Manufacturing_Production_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Sampling_Testing_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Packing_Marking_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Storage_Transport_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Traceability_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Worker_Health_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Group_Requirement_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Others_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Site_History_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Water_Source_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Product_Quality_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Harvesting_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Equipment_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Manufacturing_Production_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Sampling_Testing_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Packing_Marking_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Storage_Transport_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Traceability_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Worker_Health_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Group_Requirement_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Others_Observations = models.TextField(blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Certificate_No = models.CharField(max_length=100, blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    Farm_Location = models.CharField(max_length=250, default=None, blank=True, null=True)
    Farm_Name = models.CharField(max_length=250, blank=True, null=True)
    Applicant_Id = models.CharField(max_length=50, blank=True, null=True)
    Audit_Type = models.CharField(max_length=200, blank=True, null=True)
    Terms_Standards = models.CharField(max_length=100, blank=True, null=True)
    Others_Standards = models.CharField(max_length=100, blank=True, null=True)
    Corrective_Action_Taken_Auditee = models.TextField(blank=True, null=True)
    Corrective_Action_Date = models.DateField(blank=True, null=True)
    Certificate_Type = models.CharField(max_length=10, blank=True, null=True)
    License_Number = models.CharField(max_length=100, blank=True, null=True)
    Technical_In_Charge = models.CharField(max_length=100, blank=True, null=True)
    Manager_In_Charge = models.CharField(max_length=100, blank=True, null=True)


class t_certification_organic_t2(models.Model):  # Organic Certification farmer group
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    CID = models.CharField(max_length=100, default=None, blank=True, null=True)
    Name = models.CharField(max_length=100, default=None, blank=True, null=True)


class t_certification_organic_t3(models.Model):  # Organic Certification audit team
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Login_Id = models.CharField(max_length=100, default=None, blank=True, null=True)
    Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Role = models.CharField(max_length=100, default=None, blank=True, null=True)


class t_certification_organic_t4(models.Model):  # Organic Certification crop production
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Crop_Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Area_Cultivated = models.IntegerField(blank=True, null=True)
    Unit = models.CharField(max_length=50)
    P_From_Date = models.DateField(blank=True, null=True)
    P_To_Date = models.DateField(blank=True, null=True)
    P_Yield = models.IntegerField(blank=True, null=True)
    P_Yield_Unit = models.CharField(max_length=50)
    P_Harvest_Month = models.CharField(max_length=50)
    P_Sold = models.IntegerField(blank=True, null=True)
    P_Balance_Stock = models.IntegerField(blank=True, null=True)
    C_From_Date = models.DateField(blank=True, null=True)
    C_To_Date = models.DateField(blank=True, null=True)
    C_Estimated_Yield = models.IntegerField(blank=True, null=True)
    C_Yield_Unit = models.CharField(max_length=50)
    C_Harvest_Month = models.CharField(max_length=50)


class t_certification_organic_t5(models.Model):  # Organic Certification processing unit
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Production_House_Name = models.CharField(max_length=200, blank=True, null=True)
    Production_House_Address = models.TextField(blank=True, null=True)
    Processing_Type = models.CharField(max_length=200, blank=True, null=True)
    P_From_Date = models.DateField(blank=True, null=True)
    P_To_Date = models.DateField(blank=True, null=True)
    P_Production = models.IntegerField(blank=True, null=True)
    P_Production_Unit = models.CharField(max_length=50)
    P_Sold = models.IntegerField(blank=True, null=True)
    P_Balance_Stock = models.IntegerField(blank=True, null=True)
    C_From_Date = models.DateField(blank=True, null=True)
    C_To_Date = models.DateField(blank=True, null=True)
    C_Production = models.IntegerField(blank=True, null=True)
    C_Production_Unit = models.CharField(max_length=50)
    C_Sold = models.IntegerField(blank=True, null=True)
    C_Balance_Stock = models.IntegerField(blank=True, null=True)


class t_certification_organic_t6(models.Model):  # Organic Certification Wild Collection
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Common_Name = models.CharField(max_length=200, default=None, blank=True, null=True)
    Botanical_Name = models.CharField(max_length=200, default=None, blank=True, null=True)
    Plant_Part = models.CharField(max_length=200, default=None, blank=True, null=True)
    Estimated_Harvest = models.IntegerField(default=None, blank=True, null=True)
    Harvest_Unit = models.CharField(max_length=50, default=None, blank=True, null=True)
    Harvest_Season = models.CharField(max_length=200, default=None, blank=True, null=True)
    Harvest_Acreage = models.IntegerField(default=None, blank=True, null=True)
    Acreage_Unit = models.CharField(max_length=50, default=None, blank=True, null=True)


class t_certification_organic_t7(models.Model):  # Organic Certification Animal Husbandry/Livestock
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Livestock_Type = models.CharField(max_length=100, default=None, blank=True, null=True)
    Male_no = models.IntegerField(default=None, blank=True, null=True)
    Female_no = models.IntegerField(default=None, blank=True, null=True)
    Estimated_Production = models.IntegerField(default=None, blank=True, null=True)
    Production_Unit = models.CharField(max_length=50, default=None, blank=True, null=True)
    Production_Sold = models.CharField(max_length=200, default=None, blank=True, null=True)


class t_certification_organic_t8(models.Model):  # Organic Certification Aquaculture
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Aquaculture_Type = models.CharField(max_length=20)
    Estimated_Yield = models.CharField(max_length=200, default=None, blank=True, null=True)
    Estimated_Yield_Unit = models.CharField(max_length=50, default=None, blank=True, null=True)
    Harvest_Month = models.CharField(max_length=50, default=None, blank=True, null=True)
    Sold = models.IntegerField(default=None, blank=True, null=True)
    Sold_Unit = models.CharField(max_length=50, default=None, blank=True, null=True)
    Balance_Stock = models.IntegerField(blank=True, null=True)
    Balance_Stock_Unit = models.CharField(max_length=20, default=None, blank=True, null=True)


class t_certification_organic_t9(models.Model):  # Organic Certification Api_culture
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Common_Name = models.CharField(max_length=200, default=None, blank=True, null=True)
    Botanical_Name = models.CharField(max_length=200, default=None, blank=True, null=True)
    Estimated_Harvest = models.IntegerField(default=None, blank=True, null=True)
    Harvest_Unit = models.CharField(max_length=50, default=None, blank=True, null=True)
    Harvest_Acreage = models.IntegerField(default=None, blank=True, null=True)
    Acreage_Unit = models.CharField(max_length=50, default=None, blank=True, null=True)


class t_certification_organic_t10(models.Model):  # Organic Certification Audit Finding/Report Related to T1)
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Audit_Findings_Farm_Inputs = models.CharField(max_length=200, blank=True, null=True)
    Audit_Findings_Farm_Supplier = models.CharField(max_length=200, blank=True, null=True)
    Audit_Findings_Farm_Invoice = models.CharField(max_length=200, blank=True, null=True)


class t_certification_organic_t11(models.Model):  # Organic Certification Observation.
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Clause_Number = models.CharField(max_length=200, blank=True, null=True)
    Non_Conformity = models.CharField(max_length=10, blank=True, null=True)
    Non_Conformity_Category = models.CharField(max_length=10, blank=True, null=True)
    Non_Conformity_Description = models.CharField(max_length=100, blank=True, null=True)
    Corrective_Action_Proposed_Auditee = models.TextField(blank=True, null=True)
    Corrective_Action_Verified_Auditor = models.TextField(blank=True, null=True)
    Non_Conformity_Closure = models.CharField(max_length=1, blank=True, null=True)


# Food Product Certificate
class t_certification_food_t1(models.Model):  # Food Product main table
    Application_No = models.CharField(max_length=30, primary_key=True)
    Application_Date = models.DateField(blank=True, null=True)
    Firm_Name = models.CharField(max_length=250, blank=True, null=True)
    Firm_Address = models.TextField(blank=True, null=True)
    Firm_Contact_No = models.IntegerField(blank=True, null=True)
    Firm_Email = models.EmailField(blank=True, null=True)
    Factory_Name = models.CharField(max_length=250, blank=True, null=True)
    Factory_Address = models.TextField(blank=True, null=True)
    Factory_Contact_No = models.IntegerField(default=None, blank=True, null=True)
    Factory_Email = models.EmailField(blank=True, null=True)
    Product_Description = models.TextField(blank=True, null=True)
    Product_Trade_Mark = models.TextField(blank=True, null=True)
    P_From_Date = models.DateField(blank=True, null=True)
    P_To_Date = models.DateField(blank=True, null=True)
    P_Production = models.IntegerField(blank=True, null=True)
    P_Production_Unit = models.CharField(max_length=50, blank=True, null=True)
    P_Production_Value = models.IntegerField(blank=True, null=True)
    P_Export_From_Date = models.DateField(blank=True, null=True)
    P_Export_To_Date = models.DateField(blank=True, null=True)
    P_Export = models.CharField(max_length=20, default=None, blank=True, null=True)
    P_Export_Unit = models.CharField(max_length=50, blank=True, null=True)
    P_Export_Value = models.CharField(max_length=50, blank=True, null=True)
    C_From_Date = models.DateField(blank=True, null=True)
    C_To_Date = models.DateField(blank=True, null=True)
    C_Production = models.IntegerField(blank=True, null=True)
    C_Production_Unit = models.CharField(max_length=50, blank=True, null=True)
    C_Production_Value = models.IntegerField(blank=True, null=True)
    C_Export_From_Date = models.DateField(blank=True, null=True)
    C_Export_To_Date = models.DateField(blank=True, null=True)
    C_Export = models.CharField(max_length=20, default=None, blank=True, null=True)
    C_Export_Unit = models.CharField(max_length=50, blank=True, null=True)
    C_Export_Value = models.CharField(max_length=50, blank=True, null=True)
    Proposed_Standard = models.TextField(blank=True, null=True)
    Terms_Bafra_Certification = models.CharField(max_length=10, blank=True, null=True)
    Terms_Change_Willingness = models.CharField(max_length=10, blank=True, null=True)
    Terms_Abide = models.CharField(max_length=10, blank=True, null=True)
    Terms_Agreement = models.CharField(max_length=10, blank=True, null=True)
    Acknowledge = models.CharField(max_length=1, blank=True, null=True)
    FO_Remarks = models.TextField(blank=True, null=True)
    Audit_Team_Leader = models.IntegerField(blank=True, null=True)
    Audit_Team_Acceptance = models.CharField(max_length=1, default='R', blank=True, null=True)
    Audit_Team_Acceptance_Remarks = models.TextField(blank=True, null=True)
    Audit_Plan_Date = models.DateField(blank=True, null=True)
    Audit_Plan_Criteria = models.TextField(blank=True, null=True)
    Audit_Plan_Type = models.CharField(max_length=200, blank=True, null=True)
    Audit_Plan_Scope = models.TextField(blank=True, null=True)
    Audit_Plan_Acceptance = models.CharField(default="R", max_length=1, blank=True, null=True)
    Audit_Plan_Acceptance_Remarks = models.TextField(blank=True, null=True)
    Audit_Date = models.DateField(blank=True, null=True)
    Audit_Findings_Site_History_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Water_Source_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Product_Quality_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Harvesting_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Equipment_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Manufacturing_Production_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Sampling_Testing_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Packing_Marking_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Storage_Transport_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Traceability_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Worker_Health_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Group_Requirement_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Others_OE = models.TextField(blank=True, null=True)
    Audit_Findings_Site_History_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Water_Source_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Product_Quality_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Harvesting_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Equipment_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Manufacturing_Production_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Sampling_Testing_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Packing_Marking_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Storage_Transport_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Traceability_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Worker_Health_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Group_Requirement_Observations = models.TextField(blank=True, null=True)
    Audit_Findings_Others_Observations = models.TextField(blank=True, null=True)
    Approve_Date = models.DateField(blank=True, null=True)
    Certificate_No = models.CharField(max_length=100, blank=True, null=True)
    Validity_Period = models.IntegerField(blank=True, null=True)
    Validity = models.DateField(blank=True, null=True)
    Applicant_Id = models.CharField(max_length=50, blank=True, null=True)
    Audit_Type = models.CharField(max_length=200, blank=True, null=True)
    Terms_Standards = models.CharField(max_length=100, blank=True, null=True)
    Others_Standards = models.CharField(max_length=100, blank=True, null=True)
    Corrective_Action_Taken_Auditee = models.TextField(blank=True, null=True)
    Corrective_Action_Date = models.DateField(blank=True, null=True)
    Certificate_Type = models.CharField(max_length=10, blank=True, null=True)
    License_Number = models.CharField(max_length=100, blank=True, null=True)
    Technical_In_Charge = models.CharField(max_length=100, blank=True, null=True)
    Manager_In_Charge = models.CharField(max_length=100, blank=True, null=True)


class t_certification_food_t2(models.Model):  # Food Product farmer group
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    CID = models.CharField(max_length=100, default=None, blank=True, null=True)
    Name = models.CharField(max_length=100, default=None, blank=True, null=True)


class t_certification_food_t3(models.Model):  # Food Product audit team
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Login_Id = models.CharField(max_length=100, default=None, blank=True, null=True)
    Name = models.CharField(max_length=100, default=None, blank=True, null=True)
    Role = models.CharField(max_length=100, default=None, blank=True, null=True)


class t_certification_food_t4(models.Model):  # Food Product Audit Finding/Report (Farm inputs/raw materials)
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Audit_Findings_Farm_Inputs = models.CharField(max_length=200, blank=True, null=True)
    Audit_Findings_Farm_Supplier = models.CharField(max_length=200, blank=True, null=True)
    Audit_Findings_Farm_Invoice = models.CharField(max_length=200, blank=True, null=True)


class t_certification_food_t5(models.Model):  # Food Product Observation.
    Record_Id = models.AutoField(primary_key=True)
    Application_No = models.CharField(max_length=30)
    Clause_Number = models.CharField(max_length=200, blank=True, null=True)
    Non_Conformity = models.CharField(max_length=3, blank=True, null=True)
    Non_Conformity_Category = models.CharField(max_length=50, blank=True, null=True)
    Non_Conformity_Description = models.TextField(blank=True, null=True)
    Corrective_Action_Proposed_Auditee = models.TextField(blank=True, null=True)
    Corrective_Action_Verified_Auditor = models.TextField(blank=True, null=True)
    Non_Conformity_Closure = models.CharField(max_length=3, blank=True, null=True)
