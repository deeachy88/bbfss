# Generated by Django 3.1.5 on 2021-04-07 18:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0008_auto_20210407_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_plant_seed_certification_t1',
            name='Applicant_Id',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='t_plant_seed_certification_t1',
            name='Application_Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
