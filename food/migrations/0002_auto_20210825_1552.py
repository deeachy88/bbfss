# Generated by Django 3.1.5 on 2021-08-25 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t5',
            name='NC',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='t_food_business_registration_licensing_t5',
            name='NC_Category',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_business_registration_licensing_t1',
            name='FI_Inspection_Team',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_business_registration_licensing_t1',
            name='FR_Inspection_Team',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_export_certificate_t1',
            name='Export_Permit_No',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_import_permit_inspection_t1',
            name='Clearance_Ref_No',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_import_permit_inspection_t1',
            name='Import_Permit_No',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_import_permit_inspection_t2',
            name='Application_No',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='t_food_import_permit_inspection_t3',
            name='Application_No',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='t_food_import_permit_t1',
            name='Import_Permit_No',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='t_food_import_permit_t2',
            name='Application_No',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='t_food_licensing_food_handler_t1',
            name='FH_License_No',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
