# Generated by Django 3.1.5 on 2021-03-17 08:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0020_auto_20210317_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_plant_import_permit_t1',
            name='Expected_Arrival_Date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
