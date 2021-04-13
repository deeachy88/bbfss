# Generated by Django 3.1.5 on 2021-04-07 12:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0007_auto_20210407_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_plant_clearence_nursery_seed_grower_t1',
            name='Applicant_Id',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='t_plant_clearence_nursery_seed_grower_t1',
            name='Application_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_plant_export_certificate_plant_plant_products_t1',
            name='Applicant_Id',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='t_plant_export_certificate_plant_plant_products_t1',
            name='Application_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_plant_import_permit_t1',
            name='Applicant_Id',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='t_plant_import_permit_t1',
            name='Application_Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
