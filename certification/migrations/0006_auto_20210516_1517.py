# Generated by Django 3.1.5 on 2021-05-16 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0005_auto_20210516_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='t_certification_food_t1',
            name='Factory_Inspection_Conformity',
        ),
        migrations.RemoveField(
            model_name='t_certification_food_t1',
            name='Factory_Inspection_Date',
        ),
        migrations.RemoveField(
            model_name='t_certification_food_t1',
            name='Factory_Inspection_Remarks',
        ),
        migrations.RemoveField(
            model_name='t_certification_food_t1',
            name='Feasibility_Inspection_Conformity',
        ),
        migrations.RemoveField(
            model_name='t_certification_food_t1',
            name='Feasibility_Inspection_Date',
        ),
        migrations.RemoveField(
            model_name='t_certification_food_t1',
            name='Feasibility_Inspection_Remarks',
        ),
        migrations.RemoveField(
            model_name='t_certification_food_t5',
            name='Inspection_Type',
        ),
        migrations.RemoveField(
            model_name='t_certification_gap_t1',
            name='Factory_Inspection_Conformity',
        ),
        migrations.RemoveField(
            model_name='t_certification_gap_t1',
            name='Factory_Inspection_Date',
        ),
        migrations.RemoveField(
            model_name='t_certification_gap_t1',
            name='Factory_Inspection_Remarks',
        ),
        migrations.RemoveField(
            model_name='t_certification_gap_t1',
            name='Feasibility_Inspection_Conformity',
        ),
        migrations.RemoveField(
            model_name='t_certification_gap_t1',
            name='Feasibility_Inspection_Date',
        ),
        migrations.RemoveField(
            model_name='t_certification_gap_t1',
            name='Feasibility_Inspection_Remarks',
        ),
        migrations.RemoveField(
            model_name='t_certification_gap_t8',
            name='Inspection_Type',
        ),
        migrations.RemoveField(
            model_name='t_certification_organic_t1',
            name='Factory_Inspection_Conformity',
        ),
        migrations.RemoveField(
            model_name='t_certification_organic_t1',
            name='Factory_Inspection_Date',
        ),
        migrations.RemoveField(
            model_name='t_certification_organic_t1',
            name='Factory_Inspection_Remarks',
        ),
        migrations.RemoveField(
            model_name='t_certification_organic_t1',
            name='Feasibility_Inspection_Conformity',
        ),
        migrations.RemoveField(
            model_name='t_certification_organic_t1',
            name='Feasibility_Inspection_Date',
        ),
        migrations.RemoveField(
            model_name='t_certification_organic_t1',
            name='Feasibility_Inspection_Remarks',
        ),
        migrations.RemoveField(
            model_name='t_certification_organic_t11',
            name='Inspection_Type',
        ),
        migrations.AddField(
            model_name='t_certification_food_t1',
            name='Audit_Type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_gap_t1',
            name='Audit_Type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='t_certification_organic_t1',
            name='Audit_Type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_food_t5',
            name='Non_Conformity',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_food_t5',
            name='Non_Conformity_Category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_food_t5',
            name='Non_Conformity_Closure',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='t_certification_food_t5',
            name='Non_Conformity_Description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
