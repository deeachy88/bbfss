# Generated by Django 3.1.7 on 2021-04-03 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0002_t_plant_crop_category_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_plant_crop_master',
            name='Crop_Category_Id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.t_plant_crop_category_master'),
        ),
    ]
