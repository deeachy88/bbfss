# Generated by Django 3.1.5 on 2021-09-30 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0011_auto_20210908_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_certification_gap_t1',
            name='Manager_In_Charge',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_gap_t1',
            name='Technical_In_Charge',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_gap_t5',
            name='C_Balance_Stock_Unit',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]