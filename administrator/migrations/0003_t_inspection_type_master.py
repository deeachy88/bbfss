# Generated by Django 3.1.5 on 2021-04-13 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0002_t_unit_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_inspection_type_master',
            fields=[
                ('Inspection_Type_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Inspection_Type', models.CharField(max_length=100)),
            ],
        ),
    ]
