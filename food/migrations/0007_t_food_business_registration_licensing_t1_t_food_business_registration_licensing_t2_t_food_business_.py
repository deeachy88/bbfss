# Generated by Django 3.1.5 on 2021-05-04 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_t_food_import_permit_inspection_t2_product_record_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_food_business_registration_licensing_t1',
            fields=[
                ('Application_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Application_Date', models.DateField()),
                ('Applicant_Id', models.CharField(blank=True, max_length=30, null=True)),
                ('Business_Name', models.CharField(blank=True, max_length=30, null=True)),
                ('CID', models.BigIntegerField(blank=True, null=True)),
                ('Name_Owner', models.CharField(blank=True, max_length=30, null=True)),
                ('Contact_No', models.IntegerField()),
                ('Email', models.CharField(blank=True, max_length=30, null=True)),
                ('Address', models.CharField(blank=True, max_length=250, null=True)),
                ('Name_Manager', models.CharField(blank=True, max_length=100, null=True)),
                ('License_Criteria', models.CharField(blank=True, max_length=100, null=True)),
                ('Product_Category', models.TextField(blank=True, null=True)),
                ('Product', models.TextField(blank=True, null=True)),
                ('Current_Status', models.CharField(blank=True, max_length=250, null=True)),
                ('Years_In_Production', models.IntegerField()),
                ('Volume_Last_Year', models.CharField(blank=True, max_length=100, null=True)),
                ('Project_Proposal', models.CharField(blank=True, max_length=5, null=True)),
                ('Water_Source', models.CharField(blank=True, max_length=100, null=True)),
                ('Site_History', models.CharField(blank=True, max_length=100, null=True)),
                ('Previous_Business', models.CharField(blank=True, max_length=250, null=True)),
                ('Process_Outsource', models.CharField(blank=True, max_length=10, null=True)),
                ('Legal_Entity', models.CharField(blank=True, max_length=100, null=True)),
                ('Large_Corporation', models.CharField(blank=True, max_length=10, null=True)),
                ('Large_Corporation_Relation', models.CharField(blank=True, max_length=100, null=True)),
                ('FBO_License_Status', models.CharField(blank=True, max_length=100, null=True)),
                ('FBO_License_No', models.CharField(blank=True, max_length=100, null=True)),
                ('Invalid_Reason', models.TextField(blank=True, null=True)),
                ('FBO_Judicial_Proceedings', models.CharField(blank=True, max_length=100, null=True)),
                ('Judicial_Proceedings_Details', models.CharField(blank=True, max_length=100, null=True)),
                ('FBO_Regulatory_Proceedings', models.CharField(blank=True, max_length=100, null=True)),
                ('Regulatory_Proceedings_Details', models.CharField(blank=True, max_length=100, null=True)),
                ('Inspection_Type', models.CharField(blank=True, max_length=100, null=True)),
                ('Desired_Inspection_Date', models.DateField(blank=True, null=True)),
                ('Remarks_Inspection', models.CharField(blank=True, max_length=250, null=True)),
                ('FB_License_No', models.CharField(blank=True, max_length=100, null=True)),
                ('FI_Inspection_Date', models.DateField(blank=True, null=True)),
                ('FI_Inspection_Leader', models.CharField(blank=True, max_length=100, null=True)),
                ('FI_Inspection_Team', models.TextField(blank=True, null=True)),
                ('FI_Recommendation', models.TextField(blank=True, null=True)),
                ('FR_Inspection_Date', models.DateField(blank=True, null=True)),
                ('FR_Inspection_Leader', models.CharField(blank=True, max_length=100, null=True)),
                ('FR_Inspection_Team', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_food_business_registration_licensing_t2',
            fields=[
                ('Record_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=30)),
                ('Process_Outsourced', models.CharField(max_length=250)),
                ('BP_Outsourced_To', models.CharField(max_length=100)),
                ('Contact_No_Address', models.TextField()),
                ('BAFRA_License_No', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='t_food_business_registration_licensing_t3',
            fields=[
                ('Record_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=30)),
                ('FH_License_No', models.CharField(max_length=30)),
                ('FH_Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='t_food_business_registration_licensing_t4',
            fields=[
                ('Record_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=30)),
                ('Meeting_Type', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=30)),
                ('Designation', models.CharField(max_length=30)),
                ('Open_Meeting_Date', models.DateField()),
                ('Closing_Meeting_Date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='t_food_business_registration_licensing_t5',
            fields=[
                ('Record_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Application_No', models.CharField(max_length=30)),
                ('Meeting_Type', models.CharField(max_length=100)),
                ('Requirement', models.TextField()),
                ('Observation', models.TextField()),
                ('FBO_Response', models.TextField()),
            ],
        ),
    ]
