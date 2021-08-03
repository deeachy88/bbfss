# Generated by Django 3.1.7 on 2021-07-26 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livestock', '0007_auto_20210724_0708'),
    ]

    operations = [

        migrations.AlterField(
            model_name='t_livestock_clearance_meat_shop_t1',
            name='Meat_Shop_Name',
            field=models.CharField(blank=True, default=None, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='t_livestock_clearance_meat_shop_t1',
            name='Name_Owner',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='t_livestock_clearance_meat_shop_t1',
            name='Representative',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='t_livestock_clearance_meat_shop_t3',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True)),
                ('Application_No', models.CharField(max_length=30)),
                ('FH_License_No', models.CharField(max_length=30)),
                ('FH_Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='t_livestock_clearance_meat_shop_t4',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True)),
                ('Application_No', models.CharField(max_length=30)),
                ('Meeting_Type', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=30)),
                ('Designation', models.CharField(max_length=30)),
                ('Open_Meeting_Date', models.DateField()),
                ('Closing_Meeting_Date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='t_livestock_clearance_meat_shop_t5',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True)),
                ('Application_No', models.CharField(max_length=30)),
                ('Inspection_Type', models.CharField(max_length=100)),
                ('Requirement', models.TextField()),
                ('Observation', models.TextField()),
                ('Clause_No', models.CharField(max_length=100, default=None, blank=True, null=True)),
                ('Concern', models.CharField(max_length=10, default=None, blank=True, null=True)),
                ('Date', models.DateField(default=None, blank=True, null=True)),
                ('FBO_Response', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='t_livestock_clearance_meat_shop_t6',
            fields=[
                ('Record_Id', models.AutoField(primary_key=True)),
                ('Application_No', models.CharField(max_length=30)),
                ('Meeting_Type', models.CharField(max_length=100)),
                ('Name', models.CharField(max_length=30)),
                ('Designation', models.CharField(max_length=30)),
            ],
        ),
    ]
