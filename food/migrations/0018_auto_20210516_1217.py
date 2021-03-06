# Generated by Django 3.1.5 on 2021-05-16 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0017_auto_20210513_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='Approve_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='Clearance_Approve_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='Clearance_Validity',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='Clearance_Validity_Period',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='Conditional_Clearance_No',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='Validity',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t1',
            name='Validity_Period',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_business_registration_licensing_t1',
            name='Applicant_Id',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_export_certificate_t1',
            name='Applicant_Id',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_import_permit_inspection_t1',
            name='Applicant_Id',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_import_permit_t1',
            name='Applicant_Id',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_licensing_food_handler_t1',
            name='Applicant_Id',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
