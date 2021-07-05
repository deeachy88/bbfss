from django.db import models


# Create your models here.
class t_role_master(models.Model):
    Role_Id = models.AutoField(primary_key=True)
    Role_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Role_Name


class t_division_master(models.Model):
    Division_Id = models.AutoField(primary_key=True)
    Division_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Division_Name


class t_unit_master(models.Model):
    Unit_Id = models.AutoField(primary_key=True)
    Unit = models.CharField(max_length=20)

    def __str__(self):
        return self.Unit


class t_section_master(models.Model):
    Section_Id = models.AutoField(primary_key=True)
    Section_Name = models.CharField(max_length=100)
    Division_Id = models.ForeignKey(t_division_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Section_Name


class t_service_master(models.Model):
    Service_Id = models.AutoField(primary_key=True)
    Service_Name = models.CharField(max_length=100)
    Service_Code = models.CharField(max_length=100)

    def __str__(self):
        return self.Service_Name


class t_dzongkhag_master(models.Model):
    Dzongkhag_Code = models.AutoField(primary_key=True)
    Dzongkhag_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Dzongkhag_Name


class t_gewog_master(models.Model):
    Gewog_Code = models.AutoField(primary_key=True)
    Gewog_Name = models.CharField(max_length=100)
    Dzongkhag_Code = models.ForeignKey(t_dzongkhag_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Gewog_Name


class t_village_master(models.Model):
    Village_Code = models.AutoField(primary_key=True)
    Village_Name = models.CharField(max_length=100)
    Gewog_Code = models.ForeignKey(t_gewog_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Gewog_Code


class t_country_master(models.Model):
    Country_Code = models.AutoField(primary_key=True)
    Country_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Country_Name


class t_plant_crop_category_master(models.Model):
    Crop_Category_Id = models.AutoField(primary_key=True)
    Crop_Category_Name = models.CharField(max_length=100)
    Crop_Category_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Crop_Category_Name


class t_plant_crop_master(models.Model):
    Crop_Id = models.AutoField(primary_key=True)
    Crop_Common_Name = models.CharField(max_length=100)
    Crop_Scientific_Name = models.CharField(max_length=100)
    Crop_Category_Id = models.ForeignKey(t_plant_crop_category_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Crop_Common_Name


class t_plant_crop_variety_master(models.Model):
    Crop_Variety_Id = models.AutoField(primary_key=True)
    Crop_Variety_Name = models.CharField(max_length=100)
    Crop_Id = models.ForeignKey(t_plant_crop_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Crop_Common_Name


class t_plant_chemical_master(models.Model):
    Chemical_Id = models.AutoField(primary_key=True)
    Chemical_Type = models.TextField()
    Chemical_Name = models.CharField(max_length=100)
    Description = models.TextField()

    def __str__(self):
        return self.Chemical_Name


class t_plant_crop_species_master(models.Model):
    Crop_Species_Id = models.AutoField(primary_key=True)
    Species_Common_Name = models.CharField(max_length=100)
    Species_Scientific_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Species_Common_Name


class t_plant_ornamental_master(models.Model):
    Ornamental_Plant_Id = models.AutoField(primary_key=True)
    Ornamental_Common_Name = models.CharField(max_length=100)
    Ornamental_Scientific_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Ornamental_Common_Name


class t_plant_pesticide_master(models.Model):
    Pesticide_Id = models.AutoField(primary_key=True)
    Pesticide_Name = models.CharField(max_length=100)
    Description = models.TextField()

    def __str__(self):
        return self.Pesticide_Name


class t_plant_product_master(models.Model):
    Plant_Product_Id = models.AutoField(primary_key=True)
    Plant_Product_Name = models.CharField(max_length=100)
    Product_Scientific_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Plant_Product_Name


class t_plant_fodder_master(models.Model):
    Fodder_Id = models.AutoField(primary_key=True)
    Fodder_Common_Name = models.CharField(max_length=100)
    Fodder_Scientific_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Fodder_Common_Name


class t_plant_fodder_variety_master(models.Model):
    Fodder_Variety_Id = models.AutoField(primary_key=True)
    Fodder_Variety_Name = models.CharField(max_length=100)
    Fodder_Id = models.ForeignKey(t_plant_fodder_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Fodder_Variety_Name


class t_field_office_master(models.Model):
    Y = 'Y'
    N = 'N'
    ENTRY_POINT = [
        (Y, 'Y'),
        (N, 'N'),
    ]

    Field_Office_Id = models.AutoField(primary_key=True)
    Field_Office_Code = models.CharField(max_length=3, default=None)
    Field_Office = models.CharField(max_length=100)
    Is_Entry_Point = models.CharField(max_length=1, choices=ENTRY_POINT, default=None, blank=True, null=True)
    Dzongkhag_Code = models.ForeignKey(t_dzongkhag_master, on_delete=models.CASCADE, null=True, blank=True)
    Remarks = models.CharField(max_length=250)

    def __str__(self):
        return self.Field_Office


class t_location_field_office_mapping(models.Model):
    Location_Code = models.AutoField(primary_key=True)
    Location_Name = models.CharField(max_length=100)
    Dzongkhag_Code = models.ForeignKey(t_dzongkhag_master, on_delete=models.CASCADE, null=True, blank=True)
    Field_Office_Id = models.ForeignKey(t_field_office_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Location_Name


class t_security_question_master(models.Model):
    Question_Id = models.AutoField(primary_key=True)
    Question = models.CharField(max_length=100)

    def __str__(self):
        return self.Question


class t_app_status_master(models.Model):
    Status_Id = models.AutoField(primary_key=True)
    Status_Name = models.CharField(max_length=100)
    Status_Type = models.CharField(max_length=20)
    Status_Type_Short_Desc = models.CharField(max_length=20)

    def __str__(self):
        return self.Status_Name


class t_user_type_master(models.Model):
    User_Type_Id = models.AutoField(primary_key=True)
    User_Type = models.CharField(max_length=250)

    def __str__(self):
        return self.Question


class t_user_master(models.Model):
    Male = 'M'
    Female = 'F'
    GENDER_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
    ]

    Login_Id = models.AutoField(primary_key=True)
    Login_Type = models.TextField(default=None, blank=True, null=True)
    Client_Type = models.CharField(max_length=100, default=None, blank=True, null=True)
    Name = models.CharField(max_length=200, default=None, blank=True, null=True)
    Employee_Id = models.CharField(max_length=100, default=None, blank=True, null=True)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None, blank=True, null=True)
    Section_Id = models.ForeignKey(t_section_master, on_delete=models.CASCADE, null=True, blank=True)
    Mobile_Number = models.IntegerField(default=None, blank=True, null=True)
    Email_Id = models.EmailField(default=None, blank=True, null=True)
    Password = models.TextField(default=None, blank=True, null=True)
    Password_Salt = models.CharField(max_length=250, default=None, blank=True, null=True)
    CID = models.BigIntegerField(default=None, blank=True, null=True)
    Dzongkhag_Code = models.ForeignKey(t_dzongkhag_master, on_delete=models.CASCADE, null=True, blank=True)
    Gewog_Code = models.ForeignKey(t_gewog_master, on_delete=models.CASCADE, null=True, blank=True)
    Village_Code = models.ForeignKey(t_village_master, on_delete=models.CASCADE, null=True, blank=True)
    Agency = models.CharField(max_length=50, default=None, blank=True, null=True)
    License_No = models.CharField(max_length=50, default=None, blank=True, null=True)
    Address = models.TextField(max_length=250, default=None, blank=True, null=True)
    Is_Active = models.CharField(max_length=1, default=None, blank=True, null=True)
    Logical_Delete = models.CharField(max_length=1, default=None, blank=True, null=True)
    Last_Login_Date = models.DateField(default=None, blank=True, null=True)
    Created_By = models.CharField(max_length=250, default=None, blank=True, null=True)
    Created_On = models.DateField(default=None, blank=True, null=True)
    Updated_By = models.CharField(max_length=250, default=None, blank=True, null=True)
    Updated_On = models.DateField(default=None, blank=True, null=True)
    Accept_Reject = models.CharField(max_length=1, default=None, blank=True, null=True)
    Division_Id = models.ForeignKey(t_division_master, on_delete=models.CASCADE, null=True, blank=True)
    Field_Office_Id = models.ForeignKey(t_field_office_master, on_delete=models.CASCADE, null=True, blank=True)
    Role_Id = models.ForeignKey(t_role_master, on_delete=models.CASCADE, null=True, blank=True)
    Is_Officiating = models.CharField(max_length=3, default='No', null=True, blank=True)


class t_forgot_password(models.Model):
    Forgot_Pass_Id = models.AutoField(primary_key=True)
    Login_Id = models.IntegerField()
    Security_Question_Id = models.IntegerField()
    Answer = models.CharField(max_length=250)


class t_inspection_type_master(models.Model):
    Inspection_Type_Id = models.AutoField(primary_key=True)
    Inspection_Type = models.CharField(max_length=100)


class t_livestock_category_master(models.Model):
    Category_Id = models.AutoField(primary_key=True)
    Category_Name = models.CharField(max_length=110, default=None)

    def __str__(self):
        return self.Category_Name


class t_livestock_species_master(models.Model):
    Species_Id = models.AutoField(primary_key=True)
    Species_Name = models.CharField(max_length=150)
    Category_Id = models.ForeignKey(t_livestock_category_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Species_Name


class t_livestock_species_breed_master(models.Model):
    Species_Breed_Id = models.AutoField(primary_key=True)
    Species_Breed_Name = models.CharField(max_length=150)
    Category_Id = models.ForeignKey(t_livestock_category_master, on_delete=models.CASCADE, null=True, blank=True)
    Species_Id = models.ForeignKey(t_livestock_species_master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Species_Breed_Name


class t_livestock_product_master(models.Model):
    Product_Id = models.AutoField(primary_key=True)
    Product_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Product_Name


class t_food_category_master(models.Model):
    Category_Id = models.AutoField(primary_key=True)
    Category_Name = models.CharField(max_length=100)
    HS_Code = models.CharField(max_length=100)

    def __str__(self):
        return self.Category_Name
