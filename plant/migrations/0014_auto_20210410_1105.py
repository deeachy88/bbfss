# Generated by Django 3.1.5 on 2021-04-10 05:05

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0013_t_plant_movement_permit_t2_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_file_attachment',
            name='Attachment',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=''),
        ),
    ]
