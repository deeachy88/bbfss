# Generated by Django 3.1.5 on 2021-09-15 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0008_auto_20210914_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_plant_import_permit_inspection_t1',
            name='Nationality_Type',
            field=models.CharField(default=None, max_length=20),
        ),
    ]